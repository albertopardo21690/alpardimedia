#!/usr/bin/env python3
"""Sincroniza el audio de un video con la imagen de otro.

Alinea la pista de audio de una fuente ("audio") contra la de un video de
referencia ("video") y remezcla el video de referencia con el audio alineado.

La alineacion es por anclajes: se buscan coincidencias cada pocos segundos y
se agrupan en tramos lineales, de modo que el resultado tolera tanto la deriva
de velocidad (capturas PAL/NTSC, VHS) como los cortes e inserciones. Los
tramos de la fuente de audio que no casan con nada del video de referencia se
consideran insertos (cortes publicitarios) y quedan fuera del montaje.

Uso tipico:

    python3 syncvid.py --video URL_O_FICHERO --audio URL_O_FICHERO -o salida.mp4

Requiere ffmpeg, ffprobe y numpy. yt-dlp solo si se pasan URLs.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field, asdict

import numpy as np

# --- Parametros del analisis -------------------------------------------------

SR = 16000                  # frecuencia de muestreo del analisis
HOP = 160                   # 10 ms por trama
NFFT = 512
FPS = SR / HOP              # 100 tramas por segundo
NBANDS = 24
FMIN, FMAX = 40.0, 7600.0

W_FLUX, W_LOUD = 0.65, 0.35  # peso de cada descriptor en la correlacion


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def require_tools(need_ytdlp: bool) -> None:
    missing = [t for t in ("ffmpeg", "ffprobe") if shutil.which(t) is None]
    if need_ytdlp and shutil.which("yt-dlp") is None:
        missing.append("yt-dlp")
    if missing:
        sys.exit("Faltan herramientas en el PATH: " + ", ".join(missing))


def probe_duration(path: str) -> float:
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", path,
    ]).stdout.decode().strip()
    return float(out)


# --- Descriptores ------------------------------------------------------------

def _band_matrix() -> np.ndarray:
    """Matriz (NBANDS x bins) que agrupa el espectro en bandas log-espaciadas."""
    bins = NFFT // 2 + 1
    freqs = np.linspace(0.0, SR / 2.0, bins)
    edges = np.geomspace(FMIN, FMAX, NBANDS + 1)
    m = np.zeros((NBANDS, bins), dtype=np.float32)
    for b in range(NBANDS):
        sel = (freqs >= edges[b]) & (freqs < edges[b + 1])
        if not sel.any():
            sel = np.array([np.argmin(np.abs(freqs - edges[b]))])
        m[b, sel] = 1.0 / np.count_nonzero(sel)
    return m


def envelopes(path: str, duration: float) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve (flujo espectral, sonoridad) muestreados a FPS tramas/segundo.

    El audio se decodifica en streaming: nunca se guarda el PCM completo en
    memoria, solo las envolventes, que son ~400 KB por hora de material.
    """
    mat = _band_matrix()
    window = np.hanning(NFFT).astype(np.float32)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1",
         "-ar", str(SR), "-f", "f32le", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    carry = np.zeros(0, dtype=np.float32)
    bands_chunks: list[np.ndarray] = []
    read_size = SR * 4 * 60  # 60 s por lectura
    try:
        while True:
            raw = proc.stdout.read(read_size)
            if not raw:
                break
            carry = np.concatenate([carry, np.frombuffer(raw, dtype=np.float32)])
            if carry.size < NFFT:
                continue
            nframes = (carry.size - NFFT) // HOP + 1
            frames = np.lib.stride_tricks.as_strided(
                carry, shape=(nframes, NFFT),
                strides=(carry.strides[0] * HOP, carry.strides[0]),
            )
            spec = np.abs(np.fft.rfft(frames * window, axis=1)).astype(np.float32)
            bands_chunks.append(spec @ mat.T)
            carry = carry[nframes * HOP:].copy()
    finally:
        proc.stdout.close()
        proc.wait()
    if proc.returncode not in (0, None):
        raise RuntimeError(f"ffmpeg fallo al decodificar {path}: "
                           f"{proc.stderr.read().decode()[:400]}")
    if not bands_chunks:
        raise RuntimeError(f"No se obtuvo audio de {path}")

    bands = np.log1p(np.concatenate(bands_chunks, axis=0) * 100.0)
    diff = np.diff(bands, axis=0, prepend=bands[:1])
    flux = np.maximum(diff, 0.0).sum(axis=1).astype(np.float32)
    loud = bands.mean(axis=1).astype(np.float32)
    return _normalize(flux), _normalize(loud)


def _moving_mean(x: np.ndarray, win: int) -> np.ndarray:
    win = max(1, min(win, x.size))
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    half = win // 2
    lo = np.clip(np.arange(x.size) - half, 0, x.size)
    hi = np.clip(np.arange(x.size) - half + win, 0, x.size)
    return ((c[hi] - c[lo]) / np.maximum(hi - lo, 1)).astype(np.float32)


def _normalize(x: np.ndarray) -> np.ndarray:
    """Quita la tendencia lenta y normaliza, para no depender del nivel."""
    x = x - _moving_mean(x, int(5 * FPS))
    scale = float(np.sqrt(np.mean(x.astype(np.float64) ** 2))) or 1.0
    return (x / scale).astype(np.float32)


# --- Correlacion normalizada -------------------------------------------------

def _prefix(x: np.ndarray) -> np.ndarray:
    return np.concatenate([[0.0], np.cumsum(x.astype(np.float64))])


def _next_pow2(n: int) -> int:
    return 1 << (n - 1).bit_length()


class Reference:
    """Envolventes del video de referencia con sumas acumuladas precalculadas."""

    def __init__(self, flux: np.ndarray, loud: np.ndarray):
        self.sig = (flux, loud)
        self.cum = [(_prefix(s), _prefix(s * s)) for s in self.sig]
        self.n = flux.size

    def _local_std(self, k: int, lo: int, hi: int, w: int) -> np.ndarray:
        c1, c2 = self.cum[k]
        idx = np.arange(lo, hi - w + 1)
        s1 = c1[idx + w] - c1[idx]
        s2 = c2[idx + w] - c2[idx]
        var = np.maximum(s2 / w - (s1 / w) ** 2, 1e-12)
        return np.sqrt(var)

    def ncc(self, queries: tuple[np.ndarray, ...], lo: int, hi: int) -> np.ndarray:
        """Correlacion normalizada combinada para desplazamientos en [lo, hi)."""
        w = queries[0].size
        lo = max(0, lo)
        hi = min(self.n, hi + w)
        if hi - lo < w + 1:
            return np.zeros(0, dtype=np.float32)
        total = np.zeros(hi - lo - w + 1, dtype=np.float64)
        for k, (sig, q, weight) in enumerate(
                zip(self.sig, queries, (W_FLUX, W_LOUD))):
            qz = q - q.mean()
            qstd = float(np.sqrt(np.mean(qz.astype(np.float64) ** 2)))
            if qstd < 1e-9:
                continue
            seg = sig[lo:hi]
            n = _next_pow2(seg.size + w)
            corr = np.fft.irfft(
                np.fft.rfft(seg, n) * np.conj(np.fft.rfft(qz, n)), n
            )[:total.size]
            total += weight * (corr / w) / (self._local_std(k, lo, hi, w) * qstd)
        return total


@dataclass
class Anchor:
    t2: float
    t1: float
    score: float
    margin: float


def _best_match(ref: Reference, queries, lo: int, hi: int,
                excl: int) -> tuple[int, float, float] | None:
    ncc = ref.ncc(queries, lo, hi)
    if ncc.size == 0:
        return None
    i = int(np.argmax(ncc))
    peak = float(ncc[i])
    masked = ncc.copy()
    masked[max(0, i - excl):i + excl + 1] = -np.inf
    runner = float(np.max(masked)) if np.isfinite(masked).any() else -1.0
    return max(0, lo) + i, peak, peak - runner


def find_anchors(ref: Reference, src: tuple[np.ndarray, np.ndarray],
                 dur2: float, win_s: float, near_s: float, wide_s: float,
                 min_score: float, min_margin: float) -> list[Anchor]:
    """Busca coincidencias cada win_s segundos, encadenando la prediccion."""
    w = int(win_s * FPS)
    excl = int(0.5 * FPS)
    near, wide = int(near_s * FPS), int(wide_s * FPS)
    anchors: list[Anchor] = []
    predicted: int | None = None
    total = max(1, int((dur2 - win_s) * FPS) // w)
    for n, start in enumerate(range(0, max(1, src[0].size - w), w)):
        queries = (src[0][start:start + w], src[1][start:start + w])
        if queries[0].size < w:
            break
        tries = []
        if predicted is not None:
            tries.append((predicted - near, predicted + near))
            tries.append((predicted - wide, predicted + wide))
        tries.append((0, ref.n))
        hit = None
        for lo, hi in tries:
            got = _best_match(ref, queries, lo, hi, excl)
            if got and got[1] >= min_score and got[2] >= min_margin:
                hit = got
                break
        if hit is None:
            predicted = None  # tramo sin correspondencia: reengancha global
            continue
        pos, score, margin = hit
        anchors.append(Anchor(start / FPS, pos / FPS, score, margin))
        predicted = pos + w
        if n % 25 == 0:
            log(f"  anclajes {len(anchors)}/{n + 1} (~{total} ventanas)")
    return anchors


# --- Tramos lineales ---------------------------------------------------------

@dataclass
class Segment:
    t2_start: float
    t2_end: float
    rate: float           # segundos de referencia por segundo de fuente
    intercept: float      # t1 = rate * t2 + intercept
    anchors: int = 0
    score: float = 0.0

    def map(self, t2: float) -> float:
        return self.rate * t2 + self.intercept

    @property
    def t1_start(self) -> float:
        return self.map(self.t2_start)

    @property
    def t1_end(self) -> float:
        return self.map(self.t2_end)


def _fit(anchors: list[Anchor]) -> tuple[float, float]:
    x = np.array([a.t2 for a in anchors])
    y = np.array([a.t1 for a in anchors])
    if x.size < 2 or np.ptp(x) < 1e-6:
        return 1.0, float(np.mean(y - x))
    for _ in range(3):
        rate, intercept = np.polyfit(x, y, 1)
        resid = np.abs(y - (rate * x + intercept))
        mad = float(np.median(resid)) or 1e-6
        keep = resid <= max(4.0 * mad, 0.05)
        if keep.all() or keep.sum() < 2:
            break
        x, y = x[keep], y[keep]
    return float(rate), float(intercept)


def segment_anchors(anchors: list[Anchor], win_s: float, jump_s: float,
                    min_anchors: int) -> list[Segment]:
    """Parte los anclajes donde el desfase salta: cada salto es un corte."""
    if not anchors:
        return []
    runs: list[list[Anchor]] = [[anchors[0]]]
    for prev, cur in zip(anchors, anchors[1:]):
        gap2 = cur.t2 - prev.t2
        drift_allow = 0.02 * gap2  # tolera hasta un 2% de deriva local
        jumped = abs((cur.t1 - cur.t2) - (prev.t1 - prev.t2)) > jump_s + drift_allow
        runs.append([cur]) if jumped else runs[-1].append(cur)

    segments: list[Segment] = []
    for run in runs:
        if len(run) < min_anchors:
            continue
        rate, intercept = _fit(run)
        if not (0.85 <= rate <= 1.15):
            rate, intercept = 1.0, float(np.mean([a.t1 - a.t2 for a in run]))
        segments.append(Segment(
            t2_start=run[0].t2, t2_end=run[-1].t2 + win_s,
            rate=rate, intercept=intercept, anchors=len(run),
            score=float(np.mean([a.score for a in run])),
        ))
    return segments


def _corr_at(ref: Reference, src: tuple[np.ndarray, np.ndarray],
             i2: int, w: int, seg: Segment) -> float:
    """Correlacion en el desplazamiento exacto que predice el tramo.

    Sin libertad de busqueda no hay pico espurio que valga: dentro del
    contenido comun sale alta y en un inserto cae a cero.
    """
    if i2 < 0 or i2 + w > src[0].size:
        return -1.0
    i1 = int(round(seg.map(i2 / FPS) * FPS))
    if i1 < 0 or i1 + w > ref.n:
        return -1.0
    total = 0.0
    for sig, q, weight in zip(ref.sig, (src[0][i2:i2 + w], src[1][i2:i2 + w]),
                              (W_FLUX, W_LOUD)):
        a = sig[i1:i1 + w].astype(np.float64)
        b = q.astype(np.float64)
        a -= a.mean()
        b -= b.mean()
        na, nb = np.sqrt(a @ a), np.sqrt(b @ b)
        if na < 1e-9 or nb < 1e-9:
            continue
        total += weight * float(a @ b) / (na * nb)
    return total


def _scan(ref: Reference, src, seg: Segment, w: int, step: int,
          threshold: float, start: int, limit: int, direction: int,
          patience: int) -> int:
    """Avanza el borde mientras el contenido siga casando.

    Tolera hasta `patience` sondas fallidas seguidas: un silencio o un
    pasaje flojo no debe cortar un tramo por la mitad. Devuelve la ultima
    posicion que caso de verdad, asi que un inserto largo si lo detiene.
    """
    i = best = start
    fails = 0
    while True:
        i += direction * step
        if i < 0 or i + w > limit:
            break
        if _corr_at(ref, src, i, w, seg) >= threshold:
            best, fails = i, 0
        else:
            fails += 1
            if fails >= patience:
                break
    return best


def _seek_inside(ref: Reference, src, seg: Segment, w: int, step: int,
                 threshold: float, start: int, stop: int, limit: int,
                 direction: int) -> int | None:
    """Entra hacia el interior del tramo hasta pisar contenido de verdad.

    Exige dos sondas consecutivas buenas para no dar por bueno un pico
    suelto dentro de un anuncio.
    """
    i = start
    while (0 <= i and i + w <= limit
           and (i - stop) * direction <= 0):
        if (_corr_at(ref, src, i, w, seg) >= threshold
                and _corr_at(ref, src, i + direction * step, w, seg) >= threshold):
            return i
        i += direction * step
    return None


def refine_edges(ref: Reference, src: tuple[np.ndarray, np.ndarray],
                 segments: list[Segment], threshold: float,
                 patience_s: float = 4.0,
                 passes: tuple[tuple[float, float], ...] =
                 ((4.0, 0.5), (1.5, 0.25))) -> None:
    """Ajusta los bordes de cada tramo con correlacion al desfase exacto.

    Dos pasadas: una ancha para situar el borde y otra corta para cerrarlo.
    """
    limit = src[0].size
    for seg in segments:
        for probe_s, step_s in passes:
            w = max(2, int(probe_s * FPS))
            step = max(1, int(step_s * FPS))
            patience = max(2, int(patience_s / step_s))
            lo, hi = int(seg.t2_start * FPS), int(seg.t2_end * FPS)

            tail = _seek_inside(ref, src, seg, w, step, threshold,
                                min(hi, limit) - w, lo, limit, -1)
            head = _seek_inside(ref, src, seg, w, step, threshold,
                                max(0, lo), hi - w, limit, +1)
            if tail is None or head is None:
                break

            end = _scan(ref, src, seg, w, step, threshold, tail, limit,
                        +1, patience) + w
            begin = _scan(ref, src, seg, w, step, threshold, head, limit,
                          -1, patience)
            if end - begin < w:
                break
            seg.t2_start, seg.t2_end = max(0, begin) / FPS, min(limit, end) / FPS


# --- Plan de montaje ---------------------------------------------------------

@dataclass
class Plan:
    pieces: list[dict] = field(default_factory=list)
    ads: list[dict] = field(default_factory=list)     # insertos de la fuente
    holes: list[dict] = field(default_factory=list)   # referencia sin audio


def build_plan(segments: list[Segment], dur1: float, dur2: float,
               min_gap: float) -> Plan:
    plan = Plan()
    ordered = sorted(segments, key=lambda s: s.t1_start)
    pos = 0.0
    for seg in ordered:
        t1s, t1e = seg.t1_start, seg.t1_end
        t2s, t2e = seg.t2_start, seg.t2_end
        if t1e <= pos + 1e-3 or t1s >= dur1:
            continue
        if t1s < pos:  # solape: recorta el principio
            t2s += (pos - t1s) / seg.rate
            t1s = pos
        if t1e > dur1:  # se sale del final de la referencia
            t2e -= (t1e - dur1) / seg.rate
            t1e = dur1
        if t1e - t1s < 0.05 or t2e - t2s < 0.05:
            continue
        if t1s > pos + 0.05:
            plan.holes.append({"start": round(pos, 3), "end": round(t1s, 3)})
            plan.pieces.append({"kind": "silence", "out": round(t1s - pos, 3)})
        plan.pieces.append({
            "kind": "audio", "src_start": round(t2s, 3), "src_end": round(t2e, 3),
            "out_start": round(t1s, 3), "out": round(t1e - t1s, 3),
        })
        pos = t1e
    if pos < dur1 - 0.05:
        plan.holes.append({"start": round(pos, 3), "end": round(dur1, 3)})
        plan.pieces.append({"kind": "silence", "out": round(dur1 - pos, 3)})

    covered = sorted((s.t2_start, s.t2_end) for s in segments)
    cursor = 0.0
    for a, b in covered + [(dur2, dur2)]:
        if a - cursor >= min_gap:
            plan.ads.append({"start": round(cursor, 3), "end": round(a, 3),
                             "duration": round(a - cursor, 3)})
        cursor = max(cursor, b)
    return plan


# --- Render ------------------------------------------------------------------

def parse_time(text: str) -> float:
    parts = text.strip().split(":")
    if not all(parts):
        raise ValueError(f"tiempo invalido: {text!r}")
    total = 0.0
    for part in parts:
        total = total * 60.0 + float(part)
    return total


def parse_ranges(text: str) -> list[tuple[float, float]]:
    out = []
    for chunk in filter(None, (c.strip() for c in text.split(","))):
        if "-" not in chunk:
            raise ValueError(f"rango invalido: {chunk!r} (usa inicio-fin)")
        a, b = chunk.rsplit("-", 1)
        start, end = parse_time(a), parse_time(b)
        if end <= start:
            raise ValueError(f"rango invalido: {chunk!r}")
        out.append((start, end))
    return sorted(out)


def sponsorblock_ranges(video_id: str) -> list[tuple[float, float]]:
    import urllib.error
    import urllib.request
    cats = "&".join(f"category={c}" for c in
                    ("sponsor", "selfpromo", "interaction", "intro", "outro"))
    url = f"https://sponsor.ajay.app/api/skipSegments?videoID={video_id}&{cats}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            log("  SponsorBlock: sin segmentos para este video")
            return []
        raise
    return sorted((float(s["segment"][0]), float(s["segment"][1])) for s in data)


def atempo_chain(factor: float) -> list[str]:
    """atempo solo admite 0.5..100 por instancia; encadena si hace falta."""
    steps = []
    while factor > 100.0:
        steps.append(100.0)
        factor /= 100.0
    while factor < 0.5:
        steps.append(0.5)
        factor /= 0.5
    steps.append(factor)
    return [f"atempo={s:.9f}" for s in steps]


def render_audio(src: str, plan: Plan, mutes: list[tuple[float, float]],
                 workdir: str, rate: int = 48000) -> str:
    workdir = os.path.abspath(workdir)
    parts_dir = os.path.join(workdir, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    listing = os.path.join(workdir, "parts.txt")
    paths = []
    for i, piece in enumerate(plan.pieces):
        path = os.path.join(parts_dir, f"{i:05d}.wav")
        if piece["kind"] == "silence":
            run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                 f"anullsrc=r={rate}:cl=stereo", "-t", f"{piece['out']:.6f}",
                 "-c:a", "pcm_s16le", path])
        else:
            t2s, t2e = piece["src_start"], piece["src_end"]
            span = t2e - t2s
            chain = []
            for m_start, m_end in mutes:
                lo, hi = max(m_start, t2s), min(m_end, t2e)
                if hi > lo:
                    chain.append("volume=enable='between(t,{:.3f},{:.3f})'"
                                 ":volume=0".format(lo - t2s, hi - t2s))
            chain += atempo_chain(span / piece["out"])
            chain.append(f"aresample={rate}:first_pts=0")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t2s:.6f}", "-i", src,
                 "-t", f"{span:.6f}", "-vn", "-af", ",".join(chain),
                 "-ac", "2", "-ar", str(rate), "-c:a", "pcm_s16le", path])
        paths.append(path)
        if i % 20 == 0:
            log(f"  render {i + 1}/{len(plan.pieces)}")
    with open(listing, "w") as fh:
        for path in paths:
            fh.write(f"file {shlex.quote(path)}\n")
    merged = os.path.join(workdir, "aligned.wav")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", listing, "-c:a", "pcm_s16le", "-ac", "2", "-ar", str(rate), merged])
    return merged


def mux(video: str, audio: str, output: str, bitrate: str,
        keep_original: bool, lang: str) -> None:
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio,
           "-map", "0:v:0", "-map", "1:a:0"]
    if keep_original:
        cmd += ["-map", "0:a:0?"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", bitrate,
            "-metadata:s:a:0", f"language={lang}"]
    cmd += ["-shortest", "-movflags", "+faststart", output]
    run(cmd)


# --- Entrada -----------------------------------------------------------------

def youtube_id(url: str) -> str | None:
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("youtu.be"):
        return parsed.path.lstrip("/") or None
    if "youtube" in parsed.netloc:
        return urllib.parse.parse_qs(parsed.query).get("v", [None])[0]
    return None


def fetch(source: str, workdir: str, tag: str, fmt: str,
          cookie_args: list[str]) -> str:
    if os.path.exists(source):
        return os.path.abspath(source)
    log(f"Descargando {tag}: {source}")
    template = os.path.join(workdir, f"{tag}.%(ext)s")
    run(["yt-dlp", "--no-playlist", "-f", fmt, "-o", template,
         *cookie_args, source])
    found = [os.path.join(workdir, f) for f in sorted(os.listdir(workdir))
             if f.startswith(f"{tag}.")]
    if not found:
        sys.exit(f"yt-dlp no dejo ningun fichero para {tag}")
    return found[0]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Sincroniza el audio de un video con la imagen de otro.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("--video", required=True,
                   help="video de referencia (imagen final): fichero o URL")
    p.add_argument("--audio", required=True,
                   help="fuente del audio: fichero o URL")
    p.add_argument("-o", "--output", default="salida.mp4")
    p.add_argument("--work", help="directorio de trabajo (por defecto temporal)")
    p.add_argument("--keep", action="store_true",
                   help="conserva el directorio de trabajo")
    p.add_argument("--report", help="escribe el informe de alineacion en JSON")
    p.add_argument("--analyze-only", action="store_true",
                   help="solo analiza y escribe el informe, no renderiza")

    g = p.add_argument_group("descarga")
    g.add_argument("--video-format", default="bestvideo*+bestaudio/best")
    g.add_argument("--audio-format", default="bestaudio/best")
    g.add_argument("--cookies-from-browser",
                   help="p. ej. chrome, firefox, edge, safari")
    g.add_argument("--cookies", help="fichero cookies.txt")

    g = p.add_argument_group("anuncios")
    g.add_argument("--mute", default="",
                   help="rangos a silenciar en la fuente de audio, "
                        "p. ej. '1:20-2:05,1:10:00-1:12:30'")
    g.add_argument("--sponsorblock", action="store_true",
                   help="anade los segmentos de SponsorBlock a --mute")
    g.add_argument("--min-gap", type=float, default=8.0,
                   help="hueco minimo en la fuente para considerarlo inserto")
    g.add_argument("--keep-ads", action="store_true",
                   help="no descarta los insertos detectados (solo informa)")

    g = p.add_argument_group("alineacion")
    g.add_argument("--window", type=float, default=20.0,
                   help="ventana de analisis en segundos")
    g.add_argument("--edge-ratio", type=float, default=0.55,
                   help="exigencia del afinado de bordes, como fraccion de la "
                        "correlacion tipica de los anclajes")
    g.add_argument("--near", type=float, default=30.0,
                   help="busqueda local alrededor de la prediccion")
    g.add_argument("--wide", type=float, default=600.0,
                   help="busqueda ampliada si falla la local")
    g.add_argument("--jump", type=float, default=0.75,
                   help="salto de desfase que separa dos tramos")
    g.add_argument("--min-score", type=float, default=0.20,
                   help="correlacion minima para aceptar un anclaje")
    g.add_argument("--min-margin", type=float, default=0.05,
                   help="ventaja minima del pico sobre el segundo candidato")
    g.add_argument("--min-anchors", type=int, default=3,
                   help="anclajes minimos para validar un tramo")

    g = p.add_argument_group("salida")
    g.add_argument("--bitrate", default="256k")
    g.add_argument("--lang", default="spa")
    g.add_argument("--keep-original-audio", action="store_true",
                   help="conserva el audio del video de referencia como 2a pista")

    args = p.parse_args(argv)

    need_ytdlp = not (os.path.exists(args.video) and os.path.exists(args.audio))
    require_tools(need_ytdlp)

    workdir = os.path.abspath(args.work or tempfile.mkdtemp(prefix="syncvid-"))
    os.makedirs(workdir, exist_ok=True)
    log(f"Directorio de trabajo: {workdir}")

    cookie_args: list[str] = []
    if args.cookies_from_browser:
        cookie_args += ["--cookies-from-browser", args.cookies_from_browser]
    if args.cookies:
        cookie_args += ["--cookies", args.cookies]

    try:
        video = fetch(args.video, workdir, "video", args.video_format, cookie_args)
        source = fetch(args.audio, workdir, "audio", args.audio_format, cookie_args)

        dur1, dur2 = probe_duration(video), probe_duration(source)
        log(f"Referencia: {dur1:.1f}s  |  Fuente de audio: {dur2:.1f}s")

        log("Analizando el video de referencia...")
        ref = Reference(*envelopes(video, dur1))
        log("Analizando la fuente de audio...")
        src = envelopes(source, dur2)

        log("Buscando anclajes...")
        anchors = find_anchors(ref, src, dur2, args.window, args.near,
                               args.wide, args.min_score, args.min_margin)
        log(f"Anclajes validos: {len(anchors)}")
        if not anchors:
            sys.exit("No se encontro ninguna coincidencia entre las dos pistas.")

        segments = segment_anchors(anchors, args.window, args.jump,
                                   args.min_anchors)
        if not segments:
            sys.exit("Se hallaron anclajes sueltos pero ningun tramo estable.")
        floor = args.edge_ratio * float(np.median([a.score for a in anchors]))
        log(f"Tramos: {len(segments)} — afinando bordes (umbral {floor:.2f})...")
        refine_edges(ref, src, segments, floor)
        segments.sort(key=lambda s: s.t2_start)

        plan = build_plan(segments, dur1, dur2, args.min_gap)

        mutes = parse_ranges(args.mute) if args.mute else []
        if args.sponsorblock:
            vid = youtube_id(args.audio)
            if vid:
                mutes += sponsorblock_ranges(vid)
            else:
                log("  SponsorBlock omitido: la fuente no es una URL de YouTube")
        if args.keep_ads:
            log("--keep-ads: los insertos detectados no se descartan")
        else:
            mutes += [(a["start"], a["end"]) for a in plan.ads]
        mutes.sort()

        for seg in segments:
            drift = (seg.rate - 1.0) * 1e6
            log(f"  tramo fuente {seg.t2_start:9.2f}-{seg.t2_end:9.2f}s"
                f" -> ref {seg.t1_start:9.2f}-{seg.t1_end:9.2f}s"
                f"  desfase {seg.t1_start - seg.t2_start:+8.3f}s"
                f"  deriva {drift:+.0f} ppm  ({seg.anchors} anclajes,"
                f" r={seg.score:.2f})")
        for ad in plan.ads:
            log(f"  inserto detectado en la fuente: {ad['start']:.1f}-"
                f"{ad['end']:.1f}s ({ad['duration']:.1f}s)")
        for hole in plan.holes:
            log(f"  sin audio disponible: {hole['start']:.1f}-{hole['end']:.1f}s")

        report = {
            "video": video, "audio": source,
            "duration_video": dur1, "duration_audio": dur2,
            "anchors": len(anchors),
            "segments": [asdict(s) for s in segments],
            "ads": plan.ads, "holes": plan.holes,
            "muted": [{"start": a, "end": b} for a, b in mutes],
        }
        if args.report:
            with open(args.report, "w") as fh:
                json.dump(report, fh, indent=2, ensure_ascii=False)
            log(f"Informe: {args.report}")
        if args.analyze_only:
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0

        log("Renderizando el audio alineado...")
        aligned = render_audio(source, plan, mutes, workdir)
        log("Multiplexando...")
        mux(video, aligned, args.output, args.bitrate,
            args.keep_original_audio, args.lang)
        log(f"Listo: {args.output}")
        return 0
    finally:
        if not args.keep and not args.work:
            shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
