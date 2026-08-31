#!/usr/bin/env bash
# Ceremonia de inauguración de Barcelona 92:
# imagen del canal oficial + audio original en español.
#
#   vídeo   IzGCXdX6gig  "Barcelona 1992 Opening Ceremony - Full Length"  3h18m51s
#   audio   eUMPQu4nQWk  "Inauguración de las Olimpiadas de Barcelona 92" 3h04m56s
#
# YouTube pide sesión iniciada para servir los streams, así que hay que
# ejecutarlo desde un equipo con el navegador logueado. Cambia "chrome" por
# firefox, edge o safari según cuál uses.

set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAVEGADOR="${NAVEGADOR:-chrome}"
TRABAJO="${TRABAJO:-$PWD/barcelona92-trabajo}"
SALIDA="${SALIDA:-$PWD/barcelona92-audio-espanol.mp4}"

VIDEO="https://youtu.be/IzGCXdX6gig"
AUDIO="https://youtu.be/eUMPQu4nQWk"

comun=(
  --video "$VIDEO"
  --audio "$AUDIO"
  --cookies-from-browser "$NAVEGADOR"
  --work "$TRABAJO" --keep
  --report "$TRABAJO/informe.json"
)

# Paso 1: analizar y revisar los cortes detectados antes de renderizar nada.
if [[ "${1:-}" == "--analizar" ]]; then
  python3 "$AQUI/syncvid.py" "${comun[@]}" --analyze-only
  echo
  echo "Revisa los tramos y los 'ads' de $TRABAJO/informe.json."
  echo "Si falta algún corte, añádelo con --mute y vuelve a lanzar sin --analizar."
  exit 0
fi

# Paso 2: montar. MUTE_EXTRA admite rangos en tiempos del vídeo 2,
# p. ej. MUTE_EXTRA="1:12:30-1:15:10,2:40:00-2:43:20"
python3 "$AQUI/syncvid.py" "${comun[@]}" \
  --mute "${MUTE_EXTRA:-}" \
  --keep-original-audio \
  --lang spa \
  -o "$SALIDA"

echo "Listo: $SALIDA"
