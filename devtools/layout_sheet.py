#!/usr/bin/env python3
"""A layout's drawing with its cells numbered, for measuring a room by eye.

    python devtools/layout_sheet.py LAYOUT_ID... [--scale N] [--out file.png]

(Windows or WSL: it reads the pictures devtools/workbench_prepare.py wrote
to build/workbench/layouts.) A yellow line every cell, the cell's column and
row along the top and the left, and a red tint on the cells the game blocks.
"""
import argparse
import json
import os

from PIL import Image, ImageDraw

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(REPO, "build", "workbench", "layouts")


def sheet(lid, k):
    img = Image.open(os.path.join(SRC, lid + ".png")).convert("RGB")
    data = json.load(open(os.path.join(SRC, lid + ".json")))
    w, h = data["w"], data["h"]
    img = img.resize((img.width * k, img.height * k), 0)
    tint = Image.new("RGB", img.size, (235, 60, 60))
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    for i, b in enumerate(data["blocks"]):
        if b & 0xC00:
            x, y = (i % w) * 16 * k, (i // w) * 16 * k
            md.rectangle((x, y, x + 16 * k - 1, y + 16 * k - 1), fill=46)
    img = Image.composite(tint, img, mask)
    out = Image.new("RGB", (img.width + 22, img.height + 30), (40, 0, 40))
    out.paste(img, (22, 30))
    d = ImageDraw.Draw(out)
    d.text((2, 1), "%s %dx%d" % (lid, w, h), fill=(255, 255, 0))
    for x in range(w + 1):
        d.line((22 + x * 16 * k, 30, 22 + x * 16 * k, out.height), fill=(255, 255, 0, 90))
        if x < w:
            d.text((24 + x * 16 * k, 16), str(x), fill=(255, 255, 255))
    for y in range(h + 1):
        d.line((22, 30 + y * 16 * k, out.width, 30 + y * 16 * k), fill=(255, 255, 0))
        if y < h:
            d.text((2, 32 + y * 16 * k), str(y), fill=(255, 255, 255))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("layouts", nargs="+")
    ap.add_argument("--scale", type=int, default=3)
    ap.add_argument("--out", default=os.path.join(REPO, "build", "previews", "layout_sheet.png"))
    args = ap.parse_args()
    ims = [sheet(l, args.scale) for l in args.layouts]
    out = Image.new("RGB", (max(i.width for i in ims), sum(i.height for i in ims)), (0, 0, 0))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out.save(args.out)
    print(args.out, out.size)


if __name__ == "__main__":
    main()
