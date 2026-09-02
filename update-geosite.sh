#!/bin/bash
# update-geosite.sh — перегенерирует geosite.dat из списков Shadowrocket
# Использование: ./update-geosite.sh [--check]
#
# Переменные окружения (опционально):
#   SR_SRC_DIR       — путь к спискам Shadowrocket (по умолчанию: ../ShadowRocketSimpleConfig/lists)
#   DLC_DIR          — путь к domain-list-community (по умолчанию: ./domain-list-community)
#   OUTPUT_DIR       — куда сохранить geosite.dat (по умолчанию: ./output)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="${SR_SRC_DIR:-$REPO_DIR/../ShadowRocketSimpleConfig/lists}"
DLC_DIR="${DLC_DIR:-$REPO_DIR/domain-list-community}"
OUTPUT_DIR="${OUTPUT_DIR:-$REPO_DIR/output}"
DATA_DIR="$REPO_DIR/data"

echo "=== srscdat — geosite.dat generator ==="
echo "  Source lists: $SRC_DIR"
echo "  DLC tool:     $DLC_DIR"
echo "  Output:       $OUTPUT_DIR"
echo ""

# Проверяем зависимities
if [ ! -d "$DLC_DIR" ]; then
    echo "=== Cloning domain-list-community ==="
    git clone https://github.com/v2fly/domain-list-community.git "$DLC_DIR"
fi

if [ ! -d "$SRC_DIR" ]; then
    echo "[ERROR] Source lists not found: $SRC_DIR"
    echo "Set SR_SRC_DIR or clone ShadowRocketSimpleConfig alongside srscdat."
    exit 1
fi

# Конвертируем
echo "=== Конвертация списков ==="
python3 "$REPO_DIR/src/convert.py" "$SRC_DIR" "$DATA_DIR"

echo ""
echo "=== Генерация geosite.dat ==="
mkdir -p "$OUTPUT_DIR"
cd "$DLC_DIR"
go run ./ --datapath="$DATA_DIR" --outputname=geosite.dat --outputdir="$OUTPUT_DIR/"

echo ""
echo "=== Готово ==="
ls -lh "$OUTPUT_DIR/geosite.dat"

if [[ "${1:-}" == "--check" ]]; then
    echo ""
    python3 "$REPO_DIR/src/check.py" "$OUTPUT_DIR/geosite.dat"
fi
