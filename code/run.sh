#!/usr/bin/env bash
# Pick one of the built example executables and run it.
# Extra args are forwarded, e.g.: ./run.sh --export
set -e

cd "$(dirname "$0")"

if [ ! -d build ]; then
    echo "No build/ directory yet — configuring and building first..."
    cmake -B build
    cmake --build build -j"$(nproc)"
fi

mapfile -t executables < <(
    find build -mindepth 2 -maxdepth 2 -type f -executable ! -path "*/CMakeFiles/*" -printf "%f\n" | sort -u
)

if [ ${#executables[@]} -eq 0 ]; then
    echo "No executables found in build/. Try: cmake --build build" >&2
    exit 1
fi

echo "Which example?"
PS3="> "
select choice in "${executables[@]}"; do
    [ -n "$choice" ] && break
    echo "Not a valid choice."
done

dir="build/$choice"
echo "Running $choice from $dir (--project_path .)"
cd "$dir"
./"$choice" --project_path . "$@"
