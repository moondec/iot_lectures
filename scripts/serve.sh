#!/usr/bin/env bash
# Lokalny serwer podglądu zbudowanych prezentacji.
#
#   scripts/serve.sh            # port 8090, nasłuch na pętli zwrotnej
#   scripts/serve.sh 8095       # inny port
#   scripts/serve.sh 8090 all   # nasłuch na wszystkich interfejsach (sieć lokalna)
#
# Uwaga: port 8088 jest zajęty przez inną usługę — nie używamy go.
set -euo pipefail

PORT="${1:-8090}"
BIND_MODE="${2:-loopback}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS="$ROOT/docs"

if [ "$PORT" = "8088" ]; then
  echo "Port 8088 jest zarezerwowany dla innej usługi. Wybierz inny." >&2
  exit 2
fi

if [ ! -f "$DOCS/index.html" ]; then
  echo "Brak $DOCS/index.html — najpierw zbuduj projekt:" >&2
  echo "  export PATH=\"/opt/data/tools/quarto/quarto-1.10.18/bin:\$PATH\"" >&2
  echo "  export QUARTO_CHROMIUM=\"\$AGENT_BROWSER_EXECUTABLE_PATH\"" >&2
  echo "  quarto render" >&2
  exit 1
fi

if [ "$BIND_MODE" = "all" ]; then
  BIND="0.0.0.0"
else
  BIND="127.0.0.1"
fi

echo "Serwuję $DOCS na http://$BIND:$PORT/"
echo "  strona indeksowa : http://$BIND:$PORT/index.html"
echo "  wykład 1         : http://$BIND:$PORT/slides/01-architektura-i-wymagania.html"
echo "Zatrzymanie: Ctrl+C"
exec python3 -m http.server "$PORT" --bind "$BIND" --directory "$DOCS"
