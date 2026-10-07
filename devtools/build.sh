#!/bin/bash
# Refresh the WSL build tree from this checkout, build the 3DSX, run the voxel
# host tests, and copy the 3DSX to build/sd/3ds/emerald3ds/ (git-ignored).
#   wsl -d Ubuntu-24.04 -- bash devtools/build.sh
REPO=$(cd "$(dirname "$0")/.." && pwd)
TREE=${EMERALD3DS_TREE:-$HOME/emerald3ds}
LOG=$HOME/emerald3ds-build.log
cd "$REPO" && python3 tools/bootstrap.py --dir "$TREE" 2>&1 | tail -1
cd "$TREE/3ds_port" || exit 1
make -j"$(nproc)" PYTHON=python3 > "$LOG" 2>&1
echo "BUILD EXIT=$?"
grep -n -E '(error:|\*\*\* )' "$LOG" | cut -c1-260 | head -8
make -k verify PYTHON=python3 > "$HOME/verify.log" 2>&1
echo "host tests passed: $(grep -c '^PASS' "$HOME/verify.log"); failed: $(grep -E '^make: \*\*\*' "$HOME/verify.log" | grep -v 'not remade' | sed 's/.*\[//; s/\].*//' | tr '\n' ' ')"
mkdir -p "$REPO/build/sd/3ds/emerald3ds" && cp emerald3ds.3dsx "$REPO/build/sd/3ds/emerald3ds/"
ls -la --time-style=+%H:%M emerald3ds.3dsx
