#!/usr/bin/env python3
"""What is still flat in an area's voxel view, asked of the running game.

    python devtools/voxel_audit.py MapName... [--no-rooms] [--out DIR] [--wait FRAMES]

For each map named - and, unless --no-rooms, every map its doors lead to -
the game is run in the emulator (devtools/autotest.py's harness) and asked
what every cell is in the voxel view: a model, a tree, relief, a sign, water,
open ground, or BLOCKED AND FLAT - a cell the game does not let the player
walk through and on which nothing stands. Those are the walls, furniture,
buildings and trees still lying on the ground as their drawing.

It is the game's own answer, not a judgement of a picture: a building's
drawing lying flat and a model of it look much alike in a capture, and were
taken for each other once.

Written to DIR (build/audit):
    <Map>.txt   the grid and the flat cells, as the game wrote them
    <Map>.png   the grid as a picture (red: blocked and flat) beside the capture
and the area's section of devtools/VOXEL_BACKLOG.md is rewritten with what is
left, grouped into objects (touching cells), each with its place and tiles.

Not every red cell is a fault: a counter's row a clerk stands behind, an
invisible wall, the edge of a room past its walls. The list is where to look.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import autotest  # noqa: E402

REPO = autotest.REPO
MAPS = autotest.MAPS
BACKLOG = os.path.join(REPO, "devtools", "VOXEL_BACKLOG.md")
COLOURS = {".": (214, 204, 160), "M": (90, 140, 220), "T": (60, 150, 70), "R": (150, 110, 80),
           "S": (240, 200, 60), "W": (120, 180, 240), "F": (170, 120, 200), "V": (20, 20, 20),
           "#": (230, 40, 40)}
LEGEND = [("#", "blocked and flat"), ("M", "model"), ("T", "tree"), ("R", "relief"),
          ("S", "sign"), ("F", "furniture"), ("W", "water"), (".", "open ground")]


def map_name(const):
    """MAP_DEWFORD_TOWN_HALL -> the folder of data/maps whose id it is."""
    for name in os.listdir(MAPS):
        path = os.path.join(MAPS, name, "map.json")
        if os.path.exists(path) and json.load(open(path)).get("id") == const:
            return name
    return None


def rooms_of(name):
    data = json.load(open(os.path.join(MAPS, name, "map.json")))
    out = []
    for w in data.get("warp_events") or []:
        room = map_name(w["dest_map"])
        if room and room != name and room not in out:
            out.append(room)
    return out


def run(names, wait):
    exe = autotest.azahar()
    card = os.path.join(os.path.dirname(exe), "user", "sdmc", "3ds", "emerald3ds")
    os.makedirs(card, exist_ok=True)
    rom = os.path.join(card, "emerald3ds.3dsx")
    shutil.copy2(os.path.join(REPO, "build", "sd", "3ds", "emerald3ds", "emerald3ds.3dsx"), rom)
    shots = os.path.join(card, "shots")
    shutil.rmtree(shots, ignore_errors=True)
    os.makedirs(shots, exist_ok=True)
    done = os.path.join(card, "autotest.done")
    if os.path.exists(done):
        os.remove(done)
    ids = autotest.map_ids()
    lines = ["voxel 1"]
    for name in names:
        tag, (g, n), x, y = autotest.place(name, ids)
        lines += ["warp %d %d %d %d" % (g, n, x, y), "wait %d" % wait, "audit %s" % name,
                  "shot %s" % name]
    lines.append("quit")
    with open(os.path.join(card, "autotest.txt"), "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    proc = subprocess.Popen([exe, rom])
    start, limit = time.time(), 90 + 20 * len(names)
    while time.time() - start < limit and not os.path.exists(done) and proc.poll() is None:
        time.sleep(1)
    if proc.poll() is None:
        proc.terminate()
    os.remove(os.path.join(card, "autotest.txt"))
    return shots


def objects(flat):
    """Touching flat cells as one object: [(x0, y0, x1, y1, cells, tiles)]."""
    left, out = dict(flat), []
    while left:
        start = next(iter(left))
        stack, cells = [start], {start: left.pop(start)}
        while stack:
            x, y = stack.pop()
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q in left:
                    cells[q] = left.pop(q)
                    stack.append(q)
        xs, ys = [c[0] for c in cells], [c[1] for c in cells]
        out.append((min(xs), min(ys), max(xs), max(ys), len(cells), sorted(set(cells.values()))))
    return sorted(out, key=lambda o: (o[1], o[0]))


def read(path):
    rows, flat = [], {}
    with open(path) as f:
        head = f.readline().split()
        height = int(head[5])
        for _ in range(height):
            rows.append(f.readline().rstrip("\n"))
        for line in f:
            x, y, tile = line.split()
            flat[(int(x), int(y))] = tile
    return rows, flat, head[7] == "1"


def picture(rows, capture, path):
    from PIL import Image, ImageDraw
    cell = max(6, min(16, 320 // max(len(rows), len(rows[0]))))
    w, h = len(rows[0]) * cell, len(rows) * cell
    shot = Image.open(capture).convert("RGB").crop((0, 0, 400, 240)) if os.path.exists(capture) else None
    sheet = Image.new("RGB", (w + 120 + (410 if shot else 0), max(h, 240, 16 * len(LEGEND) + 8)), (40, 40, 40))
    dr = ImageDraw.Draw(sheet)
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            dr.rectangle((x * cell, y * cell, x * cell + cell - 2, y * cell + cell - 2),
                         fill=COLOURS.get(c, (255, 0, 255)))
    for i, (c, text) in enumerate(LEGEND):
        dr.rectangle((w + 8, 6 + i * 16, w + 18, 16 + i * 16), fill=COLOURS[c])
        dr.text((w + 24, 5 + i * 16), text, fill=(230, 230, 230))
    if shot:
        sheet.paste(shot, (w + 120, 0))
    sheet.save(path)


def backlog(area, report):
    """Rewrite the area's audited section, keeping everything else."""
    begin, end = "<!-- audit:%s -->" % area, "<!-- /audit:%s -->" % area
    body = [begin, "### %s - audit of %s" % (area, time.strftime("%Y-%m-%d")), ""]
    total = 0
    for name, objs, indoor in report:
        if objs is None:
            body.append("- [ ] **%s**: no audit written (the map did not load?)" % name)
            continue
        if not objs:
            body.append("- [x] **%s**: nothing blocked lies flat" % name)
            continue
        cells = sum(o[4] for o in objs)
        total += cells
        body.append("- [ ] **%s**: %d flat cell(s) in %d object(s) - `build/audit/%s.png`" %
                    (name, cells, len(objs), name))
        for x0, y0, x1, y1, n, tiles in objs:
            where = "(%d, %d)" % (x0, y0) if n == 1 else "(%d, %d)-(%d, %d)" % (x0, y0, x1, y1)
            body.append("  - [ ] %s, %d cell(s), tiles %s" % (where, n, " ".join(tiles)))
    body += ["", "%d blocked cell(s) still flat in this area." % total, end]
    text = open(BACKLOG, encoding="utf-8").read() if os.path.exists(BACKLOG) else ""
    block = "\n".join(body)
    if begin in text:
        text = re.sub(re.escape(begin) + ".*?" + re.escape(end), lambda m: block, text, flags=re.S)
    else:
        text = text.rstrip("\n") + "\n\n" + block + "\n"
    with open(BACKLOG, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("maps", nargs="+")
    ap.add_argument("--no-rooms", action="store_true")
    ap.add_argument("--out", default=os.path.join(REPO, "build", "audit"))
    ap.add_argument("--wait", type=int, default=150)
    args = ap.parse_args()

    for area in args.maps:
        names = [area] + ([] if args.no_rooms else rooms_of(area))
        shots = run(names, args.wait)
        os.makedirs(args.out, exist_ok=True)
        report = []
        for name in names:
            src = os.path.join(shots, name + "_audit.txt")
            if not os.path.exists(src):
                report.append((name, None, False))
                print("%-40s no audit" % name)
                continue
            shutil.copy2(src, os.path.join(args.out, name + ".txt"))
            rows, flat, indoor = read(src)
            objs = objects(flat)
            picture(rows, os.path.join(shots, name + "_top.bmp"), os.path.join(args.out, name + ".png"))
            report.append((name, objs, indoor))
            print("%-40s %3d flat cell(s) in %d object(s)" % (name, len(flat), len(objs)))
        total = backlog(area, report)
        print("%s: %d blocked cell(s) still flat; devtools/VOXEL_BACKLOG.md updated" % (area, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
