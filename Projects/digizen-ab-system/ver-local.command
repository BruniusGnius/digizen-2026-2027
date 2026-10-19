#!/bin/bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
URL='http://127.0.0.1:8765/'

for program in node python3 curl; do
  if ! command -v "$program" >/dev/null 2>&1; then
    echo "Falta $program en tu Mac. Instálalo antes de abrir la vista local."
    exit 1
  fi
done

echo 'Preparando rutas /a/ y /b/ y comprobando recursos...'
python3 "$HERE/stage.py"
python3 "$HERE/audit-assets.py"
node "$HERE/tests/router.test.mjs"

if [[ "${1:-}" == '--check' ]]; then
  echo 'Revisión local terminada. No se abrió ningún servidor.'
  exit 0
fi

if curl -fsS --max-time 1 "$URL" >/dev/null 2>&1; then
  echo "El puerto 8765 ya está ocupado. Si es la vista DIGIZEN, ábrela en $URL; si no, ciérrala y vuelve a ejecutar este archivo."
  exit 1
fi

echo "Abriendo $URL"
echo 'A: http://127.0.0.1:8765/?variant=A'
echo 'B: http://127.0.0.1:8765/?variant=B'
echo 'Detén el servidor con Control+C en esta ventana.'
python3 -u "$HERE/simulate.py" &
SERVER_PID=$!
cleanup() { kill "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM

READY=0
for _ in {1..30}; do
  if curl -fsS --max-time 1 "$URL" >/dev/null 2>&1; then READY=1; break; fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then break; fi
  sleep 0.2
done
if [[ "$READY" != 1 ]]; then
  echo 'No se pudo iniciar el servidor local en el puerto 8765.'
  wait "$SERVER_PID" || true
  exit 1
fi
if command -v open >/dev/null 2>&1; then open "$URL"; fi
wait "$SERVER_PID"
