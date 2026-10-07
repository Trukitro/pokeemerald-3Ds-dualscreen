#!/bin/bash
# Build another checkout (a worktree of upstream with the test harness, a pull
# request branch) in a tree of its own, from clean, and leave its 3DSX in
# build/other/<name>.3dsx for devtools/autotest.py --rom.
#   bash devtools/build_other.sh /mnt/c/.../worktree name
SRC=$1
NAME=${2:-other}
REPO=$(cd "$(dirname "$0")/.." && pwd)
TREE=$HOME/emerald3ds_pr
cd "$SRC" || exit 1
python3 tools/bootstrap.py --dir "$TREE" > "$HOME/other_boot.log" 2>&1 || { tail -3 "$HOME/other_boot.log"; exit 1; }
cd "$TREE"
[ -x tools/gbagfx/gbagfx ] || make tools -j"$(nproc)" > "$HOME/other_tools.log" 2>&1
make generated -j"$(nproc)" > "$HOME/other_gen.log" 2>&1
cd 3ds_port
# nothing of the checkout before: its objects are newer than this one's sources
rm -rf build romfs/voxel romfs/shaders/voxel.shbin emerald3ds.3dsx emerald3ds.elf
make -j"$(nproc)" PYTHON=python3 > "$HOME/other_build.log" 2>&1
echo "BUILD EXIT=$?"
grep -E '(error:|\*\*\* )' "$HOME/other_build.log" | cut -c1-200 | head -5
mkdir -p "$REPO/build/other" && cp emerald3ds.3dsx "$REPO/build/other/$NAME.3dsx" && ls -la --time-style=+%H:%M "$REPO/build/other/$NAME.3dsx"
