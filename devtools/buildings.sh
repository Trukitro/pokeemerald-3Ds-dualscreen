#!/bin/bash
# Run the voxel building generator on this checkout's specs and say what failed.
#   bash devtools/buildings.sh                 the whole proof (about 25 s)
#   bash devtools/buildings.sh preview NAME... a 3D picture of each spec's room,
#                                              written to build/previews/
# The generator proves every model against its drawing, pixel for pixel; the
# preview is the only way to see a room before it is on a console.
REPO=$(cd "$(dirname "$0")/.." && pwd)
TREE=${EMERALD3DS_TREE:-$HOME/emerald3ds}
cp "$REPO"/3ds_port/scripts/*.py "$TREE/3ds_port/scripts/"
cd "$TREE/3ds_port" || exit 1
if [ "$1" = preview ]; then
    shift
    mkdir -p "$REPO/build/previews"
    for n in "$@"; do
        L=$(python3 -c "import sys; sys.path.insert(0,'scripts'); import voxel_building_specs as v; print([s['interior']['layout'] for s in v.SPECS if s.get('name')=='$n'][0])")
        rm -rf "/tmp/prev_$n"
        timeout 300 python3 scripts/gen_voxel_buildings.py --only "$n" --town "$L" --preview "/tmp/prev_$n" --output /tmp/prev.bin > /dev/null 2>&1
        for f in /tmp/prev_$n/layout_*_overview.png /tmp/prev_$n/layout_*_yaw30.png; do
            [ -f "$f" ] && cp "$f" "$REPO/build/previews/${n}_$(basename "$f" | sed 's/.*_//')" && echo "build/previews/${n}_$(basename "$f" | sed 's/.*_//')"
        done
    done
    exit 0
fi
python3 scripts/gen_voxel_buildings.py --output /tmp/buildings.bin > /tmp/buildings.log 2>&1
echo "EXIT=$?"
grep 'pixel(s) differ' /tmp/buildings.log | grep -v ' 0 pixel' | cut -c1-150
grep -B2 'does not reproduce\|claims no pixel\|exceeds\|does not fit' /tmp/buildings.log | cut -c1-170 | tail -6
grep 'exact:' /tmp/buildings.log | grep -v 'wrong=0 missing=0 extra=0' | cut -c1-150 | head
grep '^voxel buildings: [0-9]* models' /tmp/buildings.log | cut -c1-150
