#!/usr/bin/env bash
# Instalacja Quarto w katalogu użytkownika, bez zmian w systemie.
#
#   scripts/install-quarto.sh                 # wersja przypięta poniżej
#   QUARTO_VERSION=1.10.18 scripts/install-quarto.sh
#   QUARTO_DIR=~/narzedzia/quarto scripts/install-quarto.sh
#
# Skrypt pobiera oficjalne archiwum z GitHuba, WERYFIKUJE SUMĘ KONTROLNĄ
# wobec pliku checksums publikowanego przez wydawcę i rozpakowuje archiwum.
set -euo pipefail

# Wersja przypięta — ta sama, na której zbudowano i przetestowano prezentacje.
VERSION="${QUARTO_VERSION:-1.10.18}"
DEST="${QUARTO_DIR:-/opt/data/tools/quarto}"

ARCH="$(uname -m)"
case "$ARCH" in
  x86_64)  PKG_ARCH="linux-amd64" ;;
  aarch64|arm64) PKG_ARCH="linux-arm64" ;;
  *) echo "Nieobsługiwana architektura: $ARCH" >&2; exit 2 ;;
esac

TARBALL="quarto-${VERSION}-${PKG_ARCH}.tar.gz"
BASE="https://github.com/quarto-dev/quarto-cli/releases/download/v${VERSION}"

mkdir -p "$DEST"
cd "$DEST"

echo "[1/4] Pobieranie sum kontrolnych"
curl -fsSL -o "quarto-${VERSION}-checksums.txt" "${BASE}/quarto-${VERSION}-checksums.txt"

echo "[2/4] Pobieranie archiwum ${TARBALL}"
curl -fsSL -o "$TARBALL" "${BASE}/${TARBALL}"

echo "[3/4] Weryfikacja sumy SHA-256"
EXPECTED="$(grep "  ${TARBALL}\$" "quarto-${VERSION}-checksums.txt" | awk '{print $1}')"
ACTUAL="$(sha256sum "$TARBALL" | awk '{print $1}')"
if [ -z "$EXPECTED" ]; then
  echo "Nie znaleziono wpisu dla ${TARBALL} w pliku checksums." >&2
  exit 3
fi
if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "NIEZGODNA SUMA KONTROLNA" >&2
  echo "  oczekiwano: $EXPECTED" >&2
  echo "  otrzymano : $ACTUAL" >&2
  exit 4
fi
echo "      OK: $ACTUAL"

echo "[4/4] Rozpakowanie"
tar -xzf "$TARBALL"

BIN="${DEST}/quarto-${VERSION}/bin"
echo
echo "Zainstalowano Quarto ${VERSION} w ${DEST}/quarto-${VERSION}"
echo
echo "Dodaj do PATH:"
echo "  export PATH=\"${BIN}:\$PATH\""
echo
echo "Budowanie wymaga przeglądarki (mermaid-format: svg). Jeżeli Quarto jej nie znajdzie,"
echo "wskaż istniejącą binarkę Chromium/Chrome:"
echo "  export QUARTO_CHROMIUM=\"/ścieżka/do/chrome-headless-shell\""
echo "albo zainstaluj ją narzędziem Quarto:"
echo "  \"${BIN}/quarto\" install chromium"
echo
"${BIN}/quarto" --version
