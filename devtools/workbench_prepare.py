#!/usr/bin/env python3
"""Every map's drawing and grid, for devtools/workbench.py.

    python3 devtools/workbench_prepare.py          (in WSL: it reads the built tree)

Writes build/workbench/layouts/<LAYOUT_ID>.png and .json (size, tilesets, the
metatile and collision of every cell) and build/workbench/index.json (every
layout, with the maps that use it). Run it once, and again after the game's
maps change.
"""
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout_view as lv  # noqa: E402


def main():
    out = os.path.join(REPO, "build", "workbench", "layouts")
    os.makedirs(out, exist_ok=True)
    os.chdir(lv.TREE)
    layouts = json.load(open("data/layouts/layouts.json"))["layouts"]
    maps = {}
    root = "data/maps"
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name, "map.json")
        if os.path.exists(path):
            maps.setdefault(json.load(open(path)).get("layout"), []).append(name)
    index = []
    for lay in layouts:
        if not lay or not lay.get("blockdata_filepath") or not os.path.exists(lay["blockdata_filepath"]):
            continue
        try:
            entry, blocks = lv.load(lay["id"])
            img = lv.render(entry, blocks)
        except Exception as error:      # a layout with no tileset of its own
            print("skipped %s: %s" % (lay["id"], error))
            continue
        img.convert("RGB").save(os.path.join(out, lay["id"] + ".png"))
        json.dump({"id": lay["id"], "w": lay["width"], "h": lay["height"],
                   "primary": lay["primary_tileset"], "secondary": lay["secondary_tileset"],
                   "blocks": blocks}, open(os.path.join(out, lay["id"] + ".json"), "w"))
        index.append({"id": lay["id"], "w": lay["width"], "h": lay["height"],
                      "maps": maps.get(lay["id"], [])})
    json.dump(index, open(os.path.join(REPO, "build", "workbench", "index.json"), "w"))
    print("%d layouts -> build/workbench" % len(index))


if __name__ == "__main__":
    main()
