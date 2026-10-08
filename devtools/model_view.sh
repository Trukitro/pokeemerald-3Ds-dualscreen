#!/bin/bash
# Look at a model before it goes to a console or the emulator.
#   bash devtools/model_view.sh SPEC_NAME [LAYOUT_ID]
# (in WSL.) Builds that one model, proves it against its drawing, and lays
# its pictures side by side in build/previews/SPEC_NAME_sheet.png: the proof
# (drawing | model as the GBA camera sees it | difference), the game's
# camera, and the same from the left, the right and above - where a model
# that is only its drawing lifted up shows what it is. Prints what
# model_lint says of it: background carried into it, faces textured from
# past its drawing, a dithered shadow's dots.
REPO=$(cd "$(dirname "$0")/.." && pwd)
TREE=${EMERALD3DS_TREE:-$HOME/emerald3ds}
cp "$REPO"/3ds_port/scripts/*.py "$TREE/3ds_port/scripts/"
cd "$TREE/3ds_port" || exit 1
N=$1
L=${2:-$(python3 -c "import sys; sys.path.insert(0,'scripts'); import voxel_building_specs as v; s=[s for s in v.SPECS if s.get('name')=='$N'][0]; print(s.get('layout') or s['interior']['layout'])")}
rm -rf "/tmp/mv_$N"
timeout 300 python3 scripts/gen_voxel_buildings.py --only "$N" --town "$L" --preview "/tmp/mv_$N" --output /tmp/mv.bin > "/tmp/mv_$N.log" 2>&1
grep -E "^lint |exact:|differ|Traceback|Error" "/tmp/mv_$N.log" | cut -c1-160
mkdir -p "$REPO/build/previews"
python3 - "$N" "/tmp/mv_$N" "$REPO/build/previews/${N}_sheet.png" <<'PY'
import glob, json, os, sys
from PIL import Image
name, src, out = sys.argv[1:4]
kinds = [(k, f) for k in ("ortho", "game", "yaw35", "yaw-50", "left", "right", "high")
         for f in sorted(glob.glob(os.path.join(src, "*_%s.png" % k)))[:1]]
if not kinds:
    sys.exit("no pictures: see /tmp/mv_%s.log" % name)
ims = [Image.open(f).convert("RGB") for (_, f) in kinds]
ims[0] = ims[0].resize((ims[0].width * 2, ims[0].height * 2), 0)
cols = 2
cw = max(i.width for i in ims[1:]) if len(ims) > 1 else ims[0].width
ch = max(i.height for i in ims[1:]) if len(ims) > 1 else 0
rows = (len(ims) - 1 + cols - 1) // cols
sheet = Image.new("RGB", (max(ims[0].width, cw * cols), ims[0].height + rows * ch), (30, 30, 36))
sheet.paste(ims[0], (0, 0))
# where each picture lies in the sheet, for the workbench to open one alone
where = [[kinds[0][0], 0, 0, ims[0].width, ims[0].height]]
for k, im in enumerate(ims[1:]):
    at = ((k % cols) * cw, ims[0].height + (k // cols) * ch)
    sheet.paste(im, at)
    where.append([kinds[k + 1][0], at[0], at[1], im.width, im.height])
sheet.save(out)
json.dump(where, open(out[:-4] + ".json", "w"))
print(out)
PY
