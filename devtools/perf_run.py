#!/usr/bin/env python3
"""The same stand-still benchmark on the console for two builds, and its result.

    python devtools/perf_run.py card [--out DIR] [--places P...] [--frames N]
    python devtools/perf_run.py report PERF_TXT

`card` lays out a folder to copy onto the SD card's root: both builds, the
harness's script (3ds_port/src/3ds_autotest.c) and nothing else. Each build,
started from the Homebrew Launcher, walks the script by itself - a new game,
a warp to each place, a few seconds for the world to build, then FRAMES
frames measured - adds its lines to 3ds/emerald3ds/perf.txt and exits.
`report` reads that file back: fps and frame work per place, build by build.

The script plays a new game in memory and never saves, so the card's save
is not written; it leaves the VOXEL 3D option on. Standing still measures what a place
costs every frame - the animated ground, water, trees, the fog - not the
chunks built while walking; that is what port.log is for (perf_log.py).
"""
import argparse
import os
import shutil
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from autotest import REPO, map_ids, place

PLACES = ["LittlerootTown", "Route101:10,10", "OldaleTown", "Route102:25,10", "PetalburgCity",
          "Route104:20,60", "PetalburgWoods:15,8", "RustboroCity", "DewfordTown", "Route110:20,50",
          "SlateportCity", "Route117:30,10", "Route119:20,60", "FortreeCity", "Route120:12,62",
          "LilycoveCity", "SootopolisCity", "GraniteCave_1F:20,12"]
# the 2D view of a few of them: what the console does without the voxel world
FLAT = ["LittlerootTown", "PetalburgWoods:15,8", "Route119:20,60"]
BUILDS = {"fork": os.path.join(REPO, "build", "sd", "3ds", "emerald3ds", "emerald3ds.3dsx"),
          "upstream": os.path.join(REPO, "build", "other", "upstream-perf.3dsx")}


def card(args):
    ids = map_ids()
    lines = []
    for voxel, places in ((0, FLAT if args.places == PLACES else []), (1, args.places)):
        lines.append("voxel %d" % voxel)
        for spec in places:
            tag, (g, n), x, y = place(spec, ids)
            lines += ["warp %d %d %d %d" % (g, n, x, y), "wait %d" % args.settle,
                      "perf %s %d" % (tag, args.frames)]
    lines.append("quit")
    folder = os.path.join(args.out, "3ds", "emerald3ds")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "autotest.txt"), "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    for name, built in BUILDS.items():
        if not os.path.exists(built):
            sys.exit("not built: %s" % built)
        shutil.copy2(built, os.path.join(folder, "perf-%s.3dsx" % name))
    seconds = (len(lines) - 3) // 3 * (args.settle + args.frames) / 60
    print("%s: %d places, about %.0f min a build at 60 fps (longer on a console that is not)"
          % (args.out, (len(lines) - 3) // 3, seconds / 60 + 1))


def report(args):
    rows = defaultdict(dict)
    order = []
    for line in open(args.perf, encoding="utf-8", errors="replace"):
        parts = line.split()
        if len(parts) < 4:
            continue
        build, name = parts[0], parts[1]
        values = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
        key = (name, values.get("voxel", "?"))
        if key not in rows:
            order.append(key)
        rows[key][build] = {k: float(v) for k, v in values.items()}    # a later run replaces an earlier
    builds = sorted({b for r in rows.values() for b in r}, key=lambda b: b != "upstream")
    head = "%-26s %-5s" % ("place", "view") + "".join("%26s" % b for b in builds)
    print(head)
    print("%-32s" % "" + "".join("%26s" % "fps  work  cpu  gpu  late" for _ in builds))
    for key in order:
        cells = ""
        for b in builds:
            v = rows[key].get(b)
            cells += "%26s" % ("%5.1f %5.1f %4.1f %4.1f %4d" % (v["fps"], v["work"], v["cpu"], v["gpu"], v["late"])
                               if v else "-")
        if len(builds) == 2 and all(b in rows[key] for b in builds):
            a, c = (rows[key][b] for b in builds)
            cells += "   %+5.1f fps %+5.1f ms" % (c["fps"] - a["fps"], c["work"] - a["work"])
        print("%-26s %-5s" % (key[0], "voxel" if key[1] == "1" else "2D") + cells)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("card")
    c.add_argument("--out", default=os.path.join(REPO, "build", "perf_card"))
    c.add_argument("--places", nargs="+", default=PLACES)
    c.add_argument("--frames", type=int, default=600)
    c.add_argument("--settle", type=int, default=360, help="frames before measuring, for the world to build")
    c.set_defaults(run=card)
    r = sub.add_parser("report")
    r.add_argument("perf")
    r.set_defaults(run=report)
    args = ap.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
