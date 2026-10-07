#!/usr/bin/env python3
"""A layout's drawing as the game composes it, for measuring and for looking.

    python3 devtools/layout_view.py LAYOUT_ID out.png [--crop x0 y0 x1 y1] [--scale N]
                                    [--ruler] [--grid]

Reads the bootstrapped tree ($EMERALD3DS_TREE, default ~/emerald3ds). With
--ruler the picture carries pixel coordinates along its edges, which is what a
piece of voxel_building_specs.py is measured in; with --grid it prints each
cell's metatile id and whether it is blocked ('#').
"""
import argparse
import collections
import json
import os
import struct
import sys

TREE = os.environ.get("EMERALD3DS_TREE", os.path.expanduser("~/emerald3ds"))
sys.path.insert(0, os.path.join(TREE, "3ds_port", "scripts"))
from PIL import Image, ImageDraw  # noqa: E402
import dump_region_art as d       # noqa: E402


def load(layout_id):
    layouts = json.load(open(os.path.join(TREE, "data/layouts/layouts.json")))["layouts"]
    lay = next(l for l in layouts if l and l["id"] == layout_id)
    raw = open(os.path.join(TREE, lay["blockdata_filepath"]), "rb").read()
    return lay, [v for (v,) in struct.iter_unpack("<H", raw)]


def render(lay, blocks):
    ts = d.Tilesets(lay["primary_tileset"], lay["secondary_tileset"])
    metas = [d.read_u16(os.path.join(d.tileset_dir(lay[k]), "metatiles.bin"))
             for k in ("primary_tileset", "secondary_tileset")]
    w, h = lay["width"], lay["height"]
    img = Image.new("RGBA", (w * 16, h * 16))
    for i, v in enumerate(blocks):
        m = v & 0x3FF
        src, k = (metas[0], m) if m < 512 else (metas[1], m - 512)
        if k * 8 + 8 <= len(src):
            img.paste(d.metatile_image(src[k * 8:k * 8 + 8], ts), ((i % w) * 16, (i // w) * 16))
    return img


def with_ruler(img, x0, y0, scale):
    margin = 28
    out = Image.new("RGB", (img.width + margin, img.height + margin), (20, 20, 20))
    out.paste(img, (margin, margin))
    dr = ImageDraw.Draw(out)
    for x in range(x0, x0 + img.width // scale + 1, 4):
        X = margin + (x - x0) * scale
        major = x % 16 == 0
        dr.line((X, margin - (8 if x % 8 == 0 else 4), X, out.height if major else margin),
                fill=(255, 255, 0) if major else (160, 160, 160))
        if x % 8 == 0:
            dr.text((X + 1, 2), str(x), fill=(255, 255, 255))
    for y in range(y0, y0 + img.height // scale + 1, 4):
        Y = margin + (y - y0) * scale
        major = y % 16 == 0
        dr.line((margin - (8 if y % 8 == 0 else 4), Y, out.width if major else margin, Y),
                fill=(255, 255, 0) if major else (160, 160, 160))
        if y % 8 == 0:
            dr.text((1, Y + 1), str(y), fill=(255, 255, 255))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("layout")
    ap.add_argument("out")
    ap.add_argument("--crop", type=int, nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--ruler", action="store_true")
    ap.add_argument("--grid", action="store_true")
    args = ap.parse_args()

    lay, blocks = load(args.layout)
    w, h = lay["width"], lay["height"]
    print("%s %dx%d cells (%dx%d px) %s + %s" % (args.layout, w, h, w * 16, h * 16,
                                                 lay["primary_tileset"], lay["secondary_tileset"]))
    if args.grid:
        for y in range(h):
            print("%3d " % y + " ".join("%03X%s" % (blocks[y * w + x] & 0x3FF,
                                                    "#" if (blocks[y * w + x] >> 10) & 3 else ".")
                                         for x in range(w)))
        print(collections.Counter(b & 0x3FF for b in blocks).most_common(12))
    img = render(lay, blocks)
    x0, y0, x1, y1 = args.crop or (0, 0, w * 16, h * 16)
    img = img.crop((x0, y0, x1, y1)).resize(((x1 - x0) * args.scale, (y1 - y0) * args.scale), Image.NEAREST)
    (with_ruler(img, x0, y0, args.scale) if args.ruler else img).save(args.out)


if __name__ == "__main__":
    main()
