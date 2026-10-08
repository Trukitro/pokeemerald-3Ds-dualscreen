#!/usr/bin/env python3
"""The pixel box of a thing in a room's drawing, from a point on it.

    python devtools/measure_thing.py LAYOUT_ID FLOOR_CELL[,FLOOR_CELL...] X,Y [X,Y ...]

FLOOR_CELL is "cx:cy", a cell that is nothing but floor: its colours are the
floor's. From each point X,Y (pixels of the drawing) the thing is followed
through every touching pixel that is not one of those colours, and its box
is printed as a piece's rectangle (x0, y0, x1, y1). Reads the pictures of
devtools/workbench_prepare.py.
"""
import os
import sys

from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main():
    lid, cells, points = sys.argv[1], sys.argv[2], sys.argv[3:]
    im = Image.open(os.path.join(REPO, "build", "workbench", "layouts", lid + ".png")).convert("RGB")
    px, (W, H) = im.load(), im.size
    floor = set()
    for c in cells.split(","):
        cx, cy = (int(v) for v in c.split(":"))
        floor |= {px[cx * 16 + i, cy * 16 + j] for i in range(16) for j in range(16)}
    print("floor:", " ".join(sorted("%02x%02x%02x" % c for c in floor)))
    for p in points:
        x, y = (int(v) for v in p.split(","))
        if px[x, y] in floor:
            print("%s: floor there" % p)
            continue
        todo, seen = [(x, y)], {(x, y)}
        while todo:
            a, b = todo.pop()
            for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                if 0 <= q[0] < W and 0 <= q[1] < H and q not in seen and px[q] not in floor:
                    seen.add(q)
                    todo.append(q)
        xs, ys = [q[0] for q in seen], [q[1] for q in seen]
        print("%s: (%d, %d, %d, %d)  %dx%d, %d px" % (p, min(xs), min(ys), max(xs) + 1, max(ys) + 1,
                                                    max(xs) + 1 - min(xs), max(ys) + 1 - min(ys), len(seen)))


if __name__ == "__main__":
    main()
