#!/usr/bin/env bash
# Build every demo and record it to docs/static/<name>.mp4 with slope's --record.
#
#   ./render.sh                         # slope from the public repo (needs --record on main)
#   ./render.sh -DSLOPE_SOURCE_DIR=/path/to/slope   # an unreleased local build
#   FORCE=1 ./render.sh                 # re-record every demo, ignoring the cache
#
# A demo is re-recorded only when its inputs change: any file under demos/<src>/,
# the built executable (so a slope or CMake change counts), or the record args.
# Extra args are forwarded to cmake configure.
set -euo pipefail
cd "$(dirname "$0")"

DEMOS_DIR="$(pwd)"
BUILD="${BUILD:-build}"
STATIC="$DEMOS_DIR/../docs/static"
CACHE="$BUILD/.render-cache"
RES="${RES:-1920x1080}"
FPS="${FPS:-30}"

cmake -S . -B "$BUILD" "$@"
cmake --build "$BUILD" -j"$(nproc)"
mkdir -p "$CACHE"

# a digest of everything a render depends on
fingerprint() {   # <src> <exe> <dwell>
    {
        find "$DEMOS_DIR/$1" -type f ! -name '*.mp4' -exec sha1sum {} + | sort
        sha1sum "$BUILD/$1/$2"
        echo "$RES $FPS $3"
    } | sha1sum | cut -d' ' -f1
}

# <executable> <source subdir> <output basename> <dwell seconds>
# dwell is per demo: how long each settled slide is held, clocks still running.
render() {
    local exe="$1" src="$2" out="$3" dwell="$4"
    local fp cf; fp="$(fingerprint "$src" "$exe" "$dwell")"; cf="$CACHE/$out"

    if [ "${FORCE:-}" != 1 ] && [ -f "$STATIC/$out.mp4" ] \
       && [ -f "$cf" ] && [ "$(cat "$cf")" = "$fp" ]; then
        echo ">> $out unchanged, skipping"
        return
    fi

    echo ">> $out"
    "$BUILD/$src/$exe" --project_path "$DEMOS_DIR/$src" \
        --record --resolution "$RES" --fps "$FPS" --record_dwell "$dwell"
    mv "$DEMOS_DIR/$src/$out.mp4" "$STATIC/$out.mp4"
    # recompute: the run may have written default views/*.glsl into the source dir
    fingerprint "$src" "$exe" "$dwell" > "$cf"
    echo ">> wrote docs/static/$out.mp4"
}

render code_demo  code   code   0.8
render board_demo plots  board  2.0
