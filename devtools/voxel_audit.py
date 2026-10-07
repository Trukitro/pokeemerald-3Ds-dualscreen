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
ACCEPT = os.path.join(REPO, "devtools", "voxel_audit_accept.json")
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
    """Every map the area's doors lead to, and theirs in turn while they are
    the area's own (DewfordTown_PokemonCenter_2F from its 1F): a stair's far
    end in another town is that town's."""
    out, todo = [], [name]
    while todo:
        here = todo.pop(0)
        data = json.load(open(os.path.join(MAPS, here, "map.json")))
        for w in data.get("warp_events") or []:
            room = map_name(w["dest_map"])
            if room and room != name and room not in out and room.startswith(name + "_"):
                out.append(room)
                todo.append(room)
    return out


def run(names, wait, shot=True):
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
        lines += ["warp %d %d %d %d" % (g, n, x, y), "wait %d" % wait, "audit %s" % name]
        if shot:
            lines.append("shot %s" % name)
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


def accepted(name, flat):
    """Split the flat cells: (those still to do, {why: count} of those left
    flat on purpose - devtools/voxel_audit_accept.json)."""
    rules = json.load(open(ACCEPT, encoding="utf-8")).get(name, []) if os.path.exists(ACCEPT) else []
    todo, left = {}, {}
    for (x, y), tile in flat.items():
        why = next((r[4] for r in rules if r[0] <= x <= r[2] and r[1] <= y <= r[3]), None)
        if why is None:
            todo[(x, y)] = tile
        else:
            left[why] = left.get(why, 0) + 1
    return todo, left


def painted(name, indoor):
    """What the room still has painted on its floor, from the building
    generator's own composition of it (build/audit/flat, written by
    devtools/build.sh and buildings.sh): [(x0, y0, x1, y1, pixels)] in the
    drawing's pixels, less what voxel_audit_accept.json leaves under
    "<Map>#px"; None when the room has no model at all. This sees what the
    blocked-cell check cannot: a step's face, a low table, a rug - anything
    drawn on cells the player can walk on."""
    if not indoor:
        return []
    layout = json.load(open(os.path.join(MAPS, name, "map.json")))["layout"]
    path = os.path.join(REPO, "build", "audit", "flat", layout.lower() + "_flat.json")
    if not os.path.exists(path):
        return None
    rules = json.load(open(ACCEPT, encoding="utf-8")).get(name + "#px", []) if os.path.exists(ACCEPT) else []
    out = []
    for x0, y0, x1, y1, n in json.load(open(path))["objects"]:
        if not any(r[0] <= x0 and r[1] <= y0 and x1 <= r[2] and y1 <= r[3] for r in rules):
            out.append((x0, y0, x1, y1, n))
    return out


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


def paint_lines(paint):
    if paint is None:
        return ["  - [ ] the room has no model: everything in it is painted on its floor"]
    return ["  - [ ] painted on the floor: pixels (%d, %d)-(%d, %d), %d px" % o for o in paint[:12]]


def backlog(area, report):
    """Rewrite the area's audited section, keeping everything else."""
    begin, end = "<!-- audit:%s -->" % area, "<!-- /audit:%s -->" % area
    body = [begin, "### %s - audit of %s" % (area, time.strftime("%Y-%m-%d")), ""]
    total = 0
    for name, objs, left, paint in report:
        if objs is None:
            body.append("- [ ] **%s**: no audit written (the map did not load?)" % name)
            continue
        if not objs:
            body.append("- [x] **%s**: nothing blocked lies flat%s" %
                        (name, " that is not left so on purpose" if left else ""))
            for why, n in left.items():
                body.append("  - left flat, %d cell(s): %s" % (n, why))
            body += paint_lines(paint)
            continue
        cells = sum(o[4] for o in objs)
        total += cells
        body.append("- [ ] **%s**: %d flat cell(s) in %d object(s) - `build/audit/%s.png`" %
                    (name, cells, len(objs), name))
        for x0, y0, x1, y1, n, tiles in objs:
            where = "(%d, %d)" % (x0, y0) if n == 1 else "(%d, %d)-(%d, %d)" % (x0, y0, x1, y1)
            body.append("  - [ ] %s, %d cell(s), tiles %s" % (where, n, " ".join(tiles)))
        for why, n in left.items():
            body.append("  - left flat, %d cell(s): %s" % (n, why))
        body += paint_lines(paint)
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


def sweep(out, wait):
    """Every map of the game, a batch of them an emulator run, without
    captures: the audits alone, and a table of the areas (a map's name up to
    its first underscore: Route104 with Mr. Briney's house, GraniteCave's
    floors) in devtools/VOXEL_BACKLOG.md, the most to do first."""
    names = sorted(n for n in os.listdir(MAPS) if os.path.exists(os.path.join(MAPS, n, "map.json")))
    os.makedirs(out, exist_ok=True)
    for i in range(0, len(names), 150):
        batch = names[i:i + 150]
        shots = run(batch, wait, shot=False)
        for name in batch:
            src = os.path.join(shots, name + "_audit.txt")
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(out, name + ".txt"))
        print("maps %d-%d of %d audited" % (i + 1, i + len(batch), len(names)), flush=True)
    areas = {}
    for name in names:
        a = areas.setdefault(name.split("_")[0], dict(maps=0, cells=0, objects=0, bare=0, paint=0, none=0))
        a["maps"] += 1
        path = os.path.join(out, name + ".txt")
        if not os.path.exists(path):
            a["none"] += 1
            continue
        rows, flat, indoor = read(path)
        flat, left = accepted(name, flat)
        a["cells"] += len(flat)
        a["objects"] += len(objects(flat))
        paint = painted(name, indoor)
        if paint is None:
            a["bare"] += 1
        else:
            a["paint"] += len(paint)
    begin, end = "<!-- audit:summary -->", "<!-- /audit:summary -->"
    body = [begin, "## The whole game - audit of %s" % time.strftime("%Y-%m-%d"), "",
            "`python devtools/voxel_audit.py --all`. An area is a map and those named after it. "
            "*Flat cells*: blocked cells nothing stands on. *Rooms without a model*: indoor maps "
            "whose walls and furniture are all painted on the floor. *Painted*: things the "
            "modelled rooms still have drawn on their floors (rugs and shadows among them). "
            "*Not audited*: maps that did not load from a bare warp.", "",
            "| Area | Maps | Flat cells | Objects | Rooms without a model | Painted | Not audited |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    order = sorted(areas.items(), key=lambda kv: -(kv[1]["cells"] + 40 * kv[1]["bare"]))
    for area, a in order:
        body.append("| %s | %d | %d | %d | %d | %d | %d |" % (
            area, a["maps"], a["cells"], a["objects"], a["bare"], a["paint"], a["none"]))
    tot = {k: sum(a[k] for a in areas.values()) for k in ("maps", "cells", "objects", "bare", "paint", "none")}
    body += ["| **all** | %(maps)d | %(cells)d | %(objects)d | %(bare)d | %(paint)d | %(none)d |" % tot, end]
    text = open(BACKLOG, encoding="utf-8").read() if os.path.exists(BACKLOG) else ""
    block = "\n".join(body)
    if begin in text:
        text = re.sub(re.escape(begin) + ".*?" + re.escape(end), lambda m: block, text, flags=re.S)
    else:
        text = text.rstrip("\n") + "\n\n" + block + "\n"
    with open(BACKLOG, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("%(maps)d maps: %(cells)d flat cell(s) in %(objects)d object(s), %(bare)d room(s) without a model, "
          "%(none)d not audited" % tot)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("maps", nargs="*")
    ap.add_argument("--all", action="store_true", help="every map of the game: the summary table")
    ap.add_argument("--no-rooms", action="store_true")
    ap.add_argument("--out", default=os.path.join(REPO, "build", "audit"))
    ap.add_argument("--wait", type=int, default=150)
    args = ap.parse_args()

    if args.all:
        sweep(os.path.join(args.out, "all"), 40)
    for area in args.maps:
        names = [area] + ([] if args.no_rooms else rooms_of(area))
        shots = run(names, args.wait)
        os.makedirs(args.out, exist_ok=True)
        report = []
        for name in names:
            src = os.path.join(shots, name + "_audit.txt")
            if not os.path.exists(src):
                report.append((name, None, {}, []))
                print("%-40s no audit" % name)
                continue
            shutil.copy2(src, os.path.join(args.out, name + ".txt"))
            rows, flat, indoor = read(src)
            flat, left = accepted(name, flat)
            objs = objects(flat)
            picture(rows, os.path.join(shots, name + "_top.bmp"), os.path.join(args.out, name + ".png"))
            paint = painted(name, indoor)
            report.append((name, objs, left, paint))
            print("%-40s %3d flat cell(s) in %d object(s)%s; %s" % (
                name, len(flat), len(objs), ", %d left on purpose" % sum(left.values()) if left else "",
                "no room model" if paint is None else "%d thing(s) painted on the floor" % len(paint)))
        total = backlog(area, report)
        print("%s: %d blocked cell(s) still flat; devtools/VOXEL_BACKLOG.md updated" % (area, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
