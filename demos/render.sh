#!/usr/bin/env bash
# Build every demo and record it to docs/static/<name>.mp4 with slope's --record.
#
#   ./render.sh                         # slope from the public repo (needs --record on main)
#   ./render.sh -DSLOPE_SOURCE_DIR=/path/to/slope   # an unreleased local build
#
# Extra args are forwarded to cmake configure.
set -euo pipefail
cd "$(dirname "$0")"

DEMOS_DIR="$(pwd)"
BUILD="${BUILD:-build}"
STATIC="$DEMOS_DIR/../docs/static"
RES="${RES:-1920x1080}"
FPS="${FPS:-30}"
DWELL="${DWELL:-0.8}"

cmake -S . -B "$BUILD" "$@"
cmake --build "$BUILD" -j"$(nproc)"

# <executable> <source subdir> <output basename>  [extra runtime args...]
render() {
    local exe="$1" src="$2" out="$3"; shift 3
    echo ">> $out"
    "$BUILD/$src/$exe" --project_path "$DEMOS_DIR/$src" \
        --record --resolution "$RES" --fps "$FPS" --record_dwell "$DWELL" "$@"
    mv "$DEMOS_DIR/$src/$out.mp4" "$STATIC/$out.mp4"
    echo ">> wrote docs/static/$out.mp4"
}

render code_demo code code
