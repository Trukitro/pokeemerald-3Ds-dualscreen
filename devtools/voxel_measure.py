#!/usr/bin/env python3
"""Measure the things the audit found flat in a room, on the room's drawing.

    python3 devtools/voxel_measure.py MapName [--floor RRGGBB,...] [--picture out.png]

(run in WSL: it reads the bootstrapped tree, as devtools/layout_view.py does.)
For every object in build/audit/<MapName>.txt - touching blocked cells with
nothing standing on them - it finds the pixels drawn there that are not the
floor's and prints their bounding box, in the drawing's pixels, with the
colours round it: what a piece of voxel_building_specs.py is written from.
An object's drawing often reaches above its blocked cells (a table's top, a
plant's leaves), so the pixels are followed out of the cells while they stay
off the floor's colours.

The floor's colours are those of the room's most common walkable metatiles,
unless --floor gives them.
"""
import argparse
import collections
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout_view as lv  # noqa: E402


def objects(flat):
    left, out = set(flat), []
    while left:
        start = left.pop()
        stack, cells = [start], [start]
        while stack:
            x, y = stack.pop()
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q in left:
                    left.discard(q)
                    cells.append(q)
                    stack.append(q)
        out.append(sorted(cells, key=lambda c: (c[1], c[0])))
    return sorted(out, key=lambda o: (o[0][1], o[0][0]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("map")
    ap.add_argument("--floor", default=None)
    ap.add_argument("--picture", default=None)
    args = ap.parse_args()

    audit = os.path.join(REPO, "build", "audit", args.map + ".txt")
    lines = open(audit).read().split("\n")
    height = int(lines[0].split()[5])
    rows = lines[1:1 + height]
    flat = [tuple(int(v) for v in l.split()[:2]) for l in lines[1 + height:] if l.strip()]
    layout_id = json.load(open(os.path.join(lv.TREE, "data", "maps", args.map, "map.json")))["layout"]
    lay, blocks = lv.load(layout_id)
    img = lv.render(lay, blocks).convert("RGB")
    px, W, H = img.load(), img.width, img.height
    hexa = lambda c: "%02x%02x%02x" % c

    if args.floor:
        floor = set(args.floor.lower().split(","))
    else:
        # the colours of the open cells' drawing: every colour that fills at
        # least a twentieth of them
        count, total = collections.Counter(), 0
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == ".":
                    for j in range(16):
                        for i in range(16):
                            count[hexa(px[x * 16 + i, y * 16 + j])] += 1
                    total += 256
        floor = {c for c, n in count.items() if n * 20 >= total}
    print("%s  %s  %dx%d px  floor: %s" % (args.map, layout_id, W, H, " ".join(sorted(floor))))

    marks = []
    for cells in objects(flat):
        seed = {(x * 16 + i, y * 16 + j) for (x, y) in cells for j in range(16) for i in range(16)
                if hexa(px[x * 16 + i, y * 16 + j]) not in floor}
        # out of the cells, upwards and sideways, while off the floor's colours
        # and within a cell and a half of them
        x0 = min(c[0] for c in cells) * 16 - 8
        x1 = max(c[0] for c in cells) * 16 + 24
        y0 = min(c[1] for c in cells) * 16 - 24
        y1 = max(c[1] for c in cells) * 16 + 16
        todo, seen = list(seed), set(seed)
        while todo:
            x, y = todo.pop()
            for q in ((x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)):
                if (q not in seen and x0 <= q[0] < x1 and y0 <= q[1] < y1 and 0 <= q[0] < W
                        and 0 <= q[1] < H and hexa(px[q]) not in floor):
                    seen.add(q)
                    todo.append(q)
        if not seen:
            print("  cells %s: nothing drawn there but floor" % (cells,))
            continue
        bx0, bx1 = min(p[0] for p in seen), max(p[0] for p in seen) + 1
        by0, by1 = min(p[1] for p in seen), max(p[1] for p in seen) + 1
        tiles = sorted({"%03X" % (blocks[y * lay["width"] + x] & 0x3FF) for (x, y) in cells})
        print("  cells (%d, %d)-(%d, %d)  tiles %s\n      pixels (%d, %d, %d, %d)  %dx%d, %d px drawn" % (
            cells[0][0], cells[0][1], cells[-1][0], max(c[1] for c in cells), " ".join(tiles),
            bx0, by0, bx1, by1, bx1 - bx0, by1 - by0, len(seen)))
        marks.append((bx0, by0, bx1, by1))
    if args.picture:
        from PIL import ImageDraw
        big = img.resize((W * 4, H * 4), 0)
        dr = ImageDraw.Draw(big)
        for (a, b, c, d) in marks:
            dr.rectangle((a * 4, b * 4, c * 4 - 1, d * 4 - 1), outline=(255, 0, 255))
            dr.text((a * 4 + 2, b * 4 + 2), "%d,%d" % (a, b), fill=(255, 255, 0))
        big.save(args.picture)


if __name__ == "__main__":
    main()
