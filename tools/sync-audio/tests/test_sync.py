#!/usr/bin/env python3
"""Prueba de extremo a extremo de syncvid.py con material sintetico.

Fabrica dos ficheros que imitan el caso real: un video de referencia con su
propio comentario y una fuente de audio del mismo evento que empieza mas
tarde, va un pelin mas rapida (deriva tipo captura analogica), lleva un corte
publicitario insertado en medio y no cubre ni el principio ni el final.
Despues comprueba que syncvid.py reconstruye ese mapa.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(os.path.dirname(HERE), "syncvid.py")
SR = 44100

# Guion del material sintetico (segundos).
EVENT_DUR = 600.0
SRC_FROM, SRC_TO = 30.0, 560.0   # tramo del evento que cubre la fuente
CUT_AT = 300.0                   # instante del evento donde entra el anuncio
AD_DUR = 25.0
DRIFT = 1.0005                   # la fuente corre un 0,05% mas rapida

TOL = 1.5                        # tolerancia en segundos


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def write_wav(path: str, data: np.ndarray) -> None:
    peak = float(np.max(np.abs(data))) or 1.0
    pcm = (np.clip(data / peak * 0.89, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(path, "wb") as fh:
        fh.setnchannels(1)
        fh.setsampwidth(2)
        fh.setframerate(SR)
        fh.writeframes(pcm.tobytes())


def hits(rng: np.random.Generator, duration: float, count: int,
         level: float) -> np.ndarray:
    """Ruido de fondo con golpes percusivos: da envolventes con onsets claros."""
    n = int(duration * SR)
    out = rng.standard_normal(n).astype(np.float32) * 0.01 * level
    for start in rng.uniform(0.0, duration - 1.0, count):
        i = int(start * SR)
        length = int(rng.uniform(0.05, 0.6) * SR)
        decay = np.exp(-np.linspace(0.0, rng.uniform(3.0, 9.0), length))
        tone = np.sin(2 * np.pi * rng.uniform(80.0, 3000.0)
                      * np.arange(length) / SR)
        burst = (rng.standard_normal(length) * 0.5 + tone)
        out[i:i + length] += (burst * decay * rng.uniform(0.3, 1.0)
                              * level).astype(np.float32)
    return out


def build_fixtures(work: str) -> tuple[str, str]:
    rng = np.random.default_rng(20250831)
    event = hits(rng, EVENT_DUR, 900, 1.0)
    write_wav(os.path.join(work, "event.wav"), event)
    write_wav(os.path.join(work, "comm_a.wav"),
              hits(rng, EVENT_DUR, 500, 0.55))
    write_wav(os.path.join(work, "comm_b.wav"),
              hits(rng, EVENT_DUR, 500, 0.55))
    write_wav(os.path.join(work, "ad.wav"), hits(rng, AD_DUR, 60, 1.0))

    # Video de referencia: imagen sintetica + evento con el comentario A.
    run(["ffmpeg", "-v", "error", "-y",
         "-f", "lavfi", "-i", f"testsrc2=s=320x180:r=10:d={EVENT_DUR}",
         "-i", os.path.join(work, "event.wav"),
         "-i", os.path.join(work, "comm_a.wav"),
         "-filter_complex", "[1:a][2:a]amix=inputs=2:weights=1 0.7[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
         "-t", str(EVENT_DUR), os.path.join(work, "reference.mp4")])

    # Fuente: mismo evento con el comentario B, recortado y acelerado.
    run(["ffmpeg", "-v", "error", "-y",
         "-ss", str(SRC_FROM), "-t", str(SRC_TO - SRC_FROM),
         "-i", os.path.join(work, "event.wav"),
         "-t", str(SRC_TO - SRC_FROM), "-i", os.path.join(work, "comm_b.wav"),
         "-filter_complex",
         f"[0:a][1:a]amix=inputs=2:weights=1 0.7,atempo={DRIFT}[a]",
         "-map", "[a]", "-c:a", "pcm_s16le", os.path.join(work, "src_full.wav")])

    split = (CUT_AT - SRC_FROM) / DRIFT
    run(["ffmpeg", "-v", "error", "-y", "-t", str(split),
         "-i", os.path.join(work, "src_full.wav"),
         "-c:a", "pcm_s16le", os.path.join(work, "src_p1.wav")])
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(split),
         "-i", os.path.join(work, "src_full.wav"),
         "-c:a", "pcm_s16le", os.path.join(work, "src_p2.wav")])
    listing = os.path.join(work, "src_list.txt")
    with open(listing, "w") as fh:
        for name in ("src_p1.wav", "ad.wav", "src_p2.wav"):
            fh.write(f"file '{os.path.join(work, name)}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", listing, "-c:a", "aac", "-b:a", "128k",
         os.path.join(work, "source.m4a")])
    return os.path.join(work, "reference.mp4"), os.path.join(work, "source.m4a")


def check(label: str, got: float, want: float, tol: float) -> bool:
    ok = abs(got - want) <= tol
    print(f"  [{'ok ' if ok else '!! '}] {label}: {got:.3f} "
          f"(esperado {want:.3f} +-{tol})")
    return ok


def expected_ref(t_src: float) -> float:
    """Instante del evento (y por tanto de la referencia) para un instante
    de la fuente, deshaciendo el corte publicitario y la deriva."""
    split = (CUT_AT - SRC_FROM) / DRIFT
    if t_src <= split:
        return SRC_FROM + t_src * DRIFT
    return CUT_AT + (t_src - split - AD_DUR) * DRIFT


def verify_render(reference: str, output: str) -> bool:
    """Comprueba sobre el fichero final que la imagen y el audio van juntos."""
    sys.path.insert(0, os.path.dirname(HERE))
    import syncvid

    ref = syncvid.Reference(*syncvid.envelopes(reference, EVENT_DUR))
    out = syncvid.envelopes(output, EVENT_DUR)
    w = int(20 * syncvid.FPS)
    slack = int(15 * syncvid.FPS)
    ok = True
    for probe in (100.0, 200.0, 350.0, 500.0):
        i = int(probe * syncvid.FPS)
        got = syncvid._best_match(
            ref, (out[0][i:i + w], out[1][i:i + w]),
            i - slack, i + slack, int(0.5 * syncvid.FPS))
        lag = (got[0] - i) / syncvid.FPS if got else float("nan")
        ok &= check(f"desfase residual del MP4 en t={probe:.0f}s", lag, 0.0, 0.15)
    return ok


def main() -> int:
    work = sys.argv[1] if len(sys.argv) > 1 else "/tmp/syncvid-test"
    os.makedirs(work, exist_ok=True)
    print("Generando material de prueba...")
    reference, source = build_fixtures(work)

    report_path = os.path.join(work, "report.json")
    output = os.path.join(work, "out.mp4")
    print("Ejecutando syncvid.py...")
    subprocess.run([sys.executable, TOOL, "--video", reference,
                    "--audio", source, "-o", output,
                    "--report", report_path,
                    "--work", os.path.join(work, "wd")], check=True)
    report = json.load(open(report_path))

    split = (CUT_AT - SRC_FROM) / DRIFT
    src_end = split + AD_DUR + (SRC_TO - CUT_AT) / DRIFT
    segments = sorted(report["segments"], key=lambda s: s["t2_start"])

    print("\nComprobaciones")
    if len(segments) != 2:
        print(f"  [!! ] tramos: {len(segments)} (esperado 2)")
        print(json.dumps(segments, indent=2))
        return 1
    print("  [ok ] tramos detectados: 2")
    a, b = segments
    mapped = lambda s, t: s["rate"] * t + s["intercept"]

    ok = True
    print(" -- sincronia (lo que determina si imagen y audio van a la par)")
    for seg, probes in ((a, (50.0, 150.0, 250.0)), (b, (320.0, 450.0, 540.0))):
        for t in probes:
            ok &= check(f"fuente t={t:.0f}s -> referencia",
                        mapped(seg, t), expected_ref(t), 0.4)
    for name, seg in (("tramo 1", a), ("tramo 2", b)):
        ok &= check(f"{name}: deriva (ppm)", (seg["rate"] - 1) * 1e6,
                    (DRIFT - 1) * 1e6, 200.0)

    print(" -- bordes y anuncios (precision de recorte, ~2 s)")
    ok &= check("tramo 1: fin en la fuente", a["t2_end"], split, 3.0)
    ok &= check("tramo 2: inicio en la fuente", b["t2_start"], split + AD_DUR, 3.0)
    ok &= check("tramo 2: fin en la fuente", b["t2_end"], src_end, 3.0)
    ads = report["ads"]
    if len(ads) != 1:
        print(f"  [!! ] insertos detectados: {len(ads)} (esperado 1) -> {ads}")
        ok = False
    else:
        ok &= check("anuncio: inicio en la fuente", ads[0]["start"], split, 3.0)
        ok &= check("anuncio: duracion", ads[0]["duration"], AD_DUR, 5.0)
    holes = report["holes"]
    if len(holes) != 2:
        print(f"  [!! ] huecos: {len(holes)} (esperado 2) -> {holes}")
        ok = False
    else:
        ok &= check("hueco inicial: fin", holes[0]["end"], SRC_FROM, 1.0)
        ok &= check("hueco final: inicio", holes[1]["start"], SRC_TO, 3.0)

    print(" -- fichero final")
    if not os.path.exists(output):
        print("  [!! ] no se genero el fichero de salida")
        return 1
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", output],
        check=True, capture_output=True).stdout.decode().strip())
    ok &= check("duracion de la salida", dur, EVENT_DUR, 2.0)
    ok &= verify_render(reference, output)

    print("\nRESULTADO:", "TODO OK" if ok else "HAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
