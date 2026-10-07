#!/usr/bin/env python3
"""What a console run cost, from its SD log.

The port logs to sdmc:/3ds/emerald3ds/port.log when debug.txt exists beside
it (3ds_log.c): the profiler's averages every 300 frames, every frame over
15 ms of work, and every frame the display did not get in time (DROP). This
reads one log, or two side by side: the same walk on the same console with
two builds.

    python devtools/perf_log.py port.log
    python devtools/perf_log.py upstream.log fork.log
"""
import re
import sys
from collections import Counter

FRAME_MS = 1000.0 / 60
AVG = re.compile(r"PROF avg f=(\d+) cb2=(\w+) work=([\d.]+) peak=([\d.]+):(.*)")
DROP = re.compile(r"DROP frame=(\d+) gap=([\d.]+)ms \(\+(\d+) quiet\): present=([\d.]+) \((.*?)\) (.*)")
PAIR = re.compile(r"([\w+]+)=([\d.]+)")
ATLAS = re.compile(r"VOXEL atlas for (\d+):(\d+)")
SLOW_CHUNK = re.compile(r"VOXEL slow chunk .*?: ([\d.]+) ms")


def read(path):
    run = {"path": path, "avg": [], "drops": [], "slow": 0, "chunks": [], "frames": 0}
    last_map = "-"
    with open(path, encoding="utf-8", errors="replace") as log:
        for line in log:
            if m := ATLAS.search(line):
                last_map = f"{m[1]}:{m[2]}"
            elif m := AVG.search(line):
                run["avg"].append({"f": int(m[1]), "work": float(m[3]), "peak": float(m[4]),
                                   "sec": {k: float(v) for k, v in PAIR.findall(m[5])}, "map": last_map})
                run["frames"] = int(m[1])
            elif m := DROP.search(line):
                parts = {k: float(v) for k, v in PAIR.findall(m[5] + " " + m[6])}
                late = "cpu" if "(cpu late)" in line else "gpu" if "(gpu late)" in line else "other"
                # the quiet ones were dropped too, only not logged one by one
                run["drops"].append({"f": int(m[1]), "gap": float(m[2]), "quiet": int(m[3]),
                                     "present": float(m[4]), "late": late, "parts": parts})
            elif "PROF slow" in line:
                run["slow"] += 1
            elif m := SLOW_CHUNK.search(line):
                run["chunks"].append(float(m[1]))
    return run


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def summary(run):
    avg, drops = run["avg"], run["drops"]
    minutes = run["frames"] / 3600 or 1
    dropped = sum(1 + d["quiet"] for d in drops)
    out = {
        "frames": run["frames"],
        "work avg ms": mean(a["work"] for a in avg),
        "work worst window ms": max((a["work"] for a in avg), default=0.0),
        "windows over 16.7 ms %": 100.0 * sum(a["work"] > FRAME_MS for a in avg) / (len(avg) or 1),
        "frames over 15 ms /min": run["slow"] / minutes,
        "dropped frames /min": dropped / minutes,
        "  cpu late": sum(d["late"] == "cpu" for d in drops),
        "  gpu late": sum(d["late"] == "gpu" for d in drops),
        "slow voxel chunks": len(run["chunks"]),
    }
    sections = Counter()
    for a in avg:
        sections.update(a["sec"])
    for name, total in sections.most_common(6):
        out[f"sec {name} ms"] = total / len(avg)
    for name in ("voxel", "world", "chunks", "sprites", "stream", "anim", "gpu", "game", "bottom"):
        out[f"at a drop: {name} ms"] = mean(d["parts"].get(name, 0.0) for d in drops)
    return out


def timeline(run):
    print(f"\n{run['path']}: work per 300 frames (ms), # = over 16.7")
    for a in run["avg"]:
        bar = "#" if a["work"] > FRAME_MS else "."
        print(f"  f={a['f']:>7} map {a['map']:>6} work={a['work']:6.2f} peak={a['peak']:7.2f} "
              f"{bar * min(60, int(a['work'] * 2))}")


def main():
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        sys.exit(__doc__)
    runs = [read(p) for p in paths]
    tables = [summary(r) for r in runs]
    keys = list(dict.fromkeys(k for t in tables for k in t))
    print(f"{'':28}" + "".join(f"{r['path'][-18:]:>20}" for r in runs))
    for key in keys:
        print(f"{key:28}" + "".join(f"{t.get(key, 0.0):>20.2f}" for t in tables))
    if "--timeline" in sys.argv:
        for run in runs:
            timeline(run)


if __name__ == "__main__":
    main()
