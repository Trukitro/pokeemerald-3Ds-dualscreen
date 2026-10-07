#!/usr/bin/env python3
"""Run the game in Azahar on a list of places and bring the captures back.

    python devtools/autotest.py PLACE... [--out DIR] [--no-2d] [--no-3d] [--wait FRAMES] [--keep-open]

A PLACE is MapName or MapName:X,Y (the folder names of data/maps: PetalburgCity,
Route103:20,10, RustboroCity_Flat2_1F). Without coordinates the player is put
on the map's first warp, or its middle. Each place is captured in 2D and in
voxel 3D: DIR/<place>_2d.png, DIR/<place>_3d.png (top screen over bottom).

Runs on Windows with the emulator unpacked in build/tools/azahar-*/ and the
3DSX built (build/sd/3ds/emerald3ds/emerald3ds.3dsx). The emulator keeps its
own SD card in its `user` folder, so nothing of the player's is touched.
The harness is 3ds_port/src/3ds_autotest.c.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAPS = os.path.join(REPO, "build", "upstream", "data", "maps")


def azahar():
    found = sorted(glob.glob(os.path.join(REPO, "build", "tools", "azahar-*", "azahar.exe")))
    if not found:
        sys.exit("no emulator under build/tools/azahar-*/")
    return found[-1]


def map_ids():
    groups = json.load(open(os.path.join(MAPS, "map_groups.json")))
    ids = {}
    for g, name in enumerate(groups["group_order"]):
        for n, m in enumerate(groups[name]):
            ids[m] = (g, n)
    return ids


def place(spec, ids):
    name, _, at = spec.partition(":")
    if name not in ids:
        sys.exit("no map %s (folder names of data/maps)" % name)
    data = json.load(open(os.path.join(MAPS, name, "map.json")))
    layouts = json.load(open(os.path.join(REPO, "build", "upstream", "data", "layouts", "layouts.json")))["layouts"]
    lay = next(l for l in layouts if l and l["id"] == data["layout"])
    if at:
        x, y = (int(v) for v in at.split(","))
    elif data.get("warp_events"):
        w = data["warp_events"][0]
        # a door's warp is in the wall: the cell in front of it
        x, y = w["x"], min(w["y"] + 1, lay["height"] - 1)
    else:
        x, y = lay["width"] // 2, lay["height"] // 2
    tag = name if not at else "%s_%d_%d" % (name, x, y)
    return tag, ids[name], x, y


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("places", nargs="+")
    ap.add_argument("--out", default=os.path.join(REPO, "build", "shots"))
    ap.add_argument("--no-2d", action="store_true")
    ap.add_argument("--no-3d", action="store_true")
    ap.add_argument("--wait", type=int, default=240, help="frames to let the voxel world build")
    ap.add_argument("--timeout", type=int, default=0, help="seconds; 0 = by the number of places")
    ap.add_argument("--keep-open", action="store_true")
    ap.add_argument("--rom", default=None, help="another build's 3DSX (to compare with upstream's)")
    ap.add_argument("--suffix", default="", help="added to every capture's name")
    args = ap.parse_args()

    exe = azahar()
    card = os.path.join(os.path.dirname(exe), "user", "sdmc", "3ds", "emerald3ds")
    os.makedirs(card, exist_ok=True)
    built = args.rom or os.path.join(REPO, "build", "sd", "3ds", "emerald3ds", "emerald3ds.3dsx")
    rom = os.path.join(card, "emerald3ds.3dsx")
    shutil.copy2(built, rom)
    shots = os.path.join(card, "shots")
    shutil.rmtree(shots, ignore_errors=True)
    done = os.path.join(card, "autotest.done")
    if os.path.exists(done):
        os.remove(done)
    open(os.path.join(card, "debug.txt"), "a").close()

    ids = map_ids()
    lines, wanted = [], []
    for spec in args.places:
        tag, (g, n), x, y = place(spec, ids)
        modes = ([] if args.no_2d else [("2d", 0, 90)]) + ([] if args.no_3d else [("3d", 1, args.wait)])
        for mode, voxel, wait in modes:
            lines += ["voxel %d" % voxel, "warp %d %d %d %d" % (g, n, x, y), "wait %d" % wait,
                      "shot %s_%s" % (tag, mode)]
            wanted.append("%s_%s" % (tag, mode))
    lines.append("quit")
    with open(os.path.join(card, "autotest.txt"), "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    proc = subprocess.Popen([exe, rom])
    limit = args.timeout or 90 + 25 * len(wanted)
    start = time.time()
    while time.time() - start < limit and not os.path.exists(done) and proc.poll() is None:
        time.sleep(1)
    finished = os.path.exists(done)
    if not args.keep_open and proc.poll() is None:
        proc.terminate()
    os.remove(os.path.join(card, "autotest.txt"))

    from PIL import Image
    os.makedirs(args.out, exist_ok=True)
    made = 0
    for tag in wanted:
        top, bottom = (os.path.join(shots, "%s_%s.bmp" % (tag, s)) for s in ("top", "bottom"))
        if not os.path.exists(top):
            print("missing: %s" % tag)
            continue
        t = Image.open(top).convert("RGB")
        sheet = Image.new("RGB", (400, 480), (0, 0, 0))
        sheet.paste(t, (0, 0))
        if os.path.exists(bottom):
            sheet.paste(Image.open(bottom).convert("RGB"), (40, 240))
        sheet.save(os.path.join(args.out, tag + args.suffix + ".png"))
        made += 1
    print("%s in %.0f s: %d of %d captures in %s" % ("finished" if finished else "TIMED OUT",
                                                    time.time() - start, made, len(wanted), args.out))
    log = os.path.join(card, "port.log")
    if not finished and os.path.exists(log):
        print("--- last lines of port.log")
        print("".join(open(log, errors="replace").readlines()[-12:]))
    return 0 if finished else 1


if __name__ == "__main__":
    sys.exit(main())
