#!/usr/bin/env python3
"""Pack the voxel tree artwork as a small, GPU-ready RGBA5551 texture."""

import argparse
from pathlib import Path
import struct

from PIL import Image

# Twice as wide as tall: the drawn assets fill the left half, as they always
# did, and the right half holds trees taken from the game's own tilesets at
# build time (ISLAND). voxel_tree.c writes u in units of the left half.
WIDTH, DIM = 128, 64
SOURCES = (("tree_crown.png", (32, 36), (0, 0)),
           ("tree_trunk.png", (32, 32), (32, 0)),
           ("tree_small_crown.png", (16, 32), (32, 32)),
           ("tree_small_trunk.png", (16, 16), (48, 32)),
           ("grass_tuft.png", (16, 10), (0, 44)),
           ("grass_long_tuft.png", (16, 16), (16, 44)),
           ("grass_ash_tuft.png", (16, 10), (48, 50)),
           ("flowers.png", (16, 10), (0, 54)))


def texel_offset(x, y):
    """8x8 Morton tiles, matching CtrVideo_Texel (top row is v=1)."""
    morton = sum(((x >> bit) & 1) << (2 * bit) |
                 ((y >> bit) & 1) << (2 * bit + 1) for bit in range(3))
    return ((y // 8) * (WIDTH // 8) + x // 8) * 64 + morton


# Dewford's trees, and the wood round Route 106: a tree of the island's
# tileset is two cells, its crown's top in the cell north of its trunk. Its
# drawing is the upper layer of 239 (the top) over that of 23A (the rest of
# the crown, the trunk, its shadow on the sand); the lower layer is the sand.
# The crown and trunk stand as a card (16x32 at 64,0) and the cell keeps the
# sand with the shadow (16x16 at 80,0).
ISLAND = ("gTileset_General", "gTileset_Dewford", 0x239, 0x23A)
ISLAND_SHADOW = {(0xbd, 0xac, 0x52), (0x9c, 0x8b, 0x31)}
FLOWER_SHADOW = {(0x18, 0xa4, 0x6a)}


def island_tree(tree):
    """(card, ground) as RGBA images, from the tilesets of the built tree."""
    import os
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    here = os.getcwd()
    os.chdir(tree)
    try:
        import dump_region_art as art
        primary, secondary, top, foot = ISLAND
        ts = art.Tilesets(primary, secondary)
        meta = art.read_u16(os.path.join(art.tileset_dir(secondary), "metatiles.bin"))
    finally:
        os.chdir(here)

    def layer(metatile, which):
        entries = meta[(metatile - 512) * 8:(metatile - 512) * 8 + 8]
        img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        px = img.load()
        for quad in range(4):
            entry = entries[which * 4 + quad]
            data = ts.subtile(entry & 0x3FF, (entry >> 12) & 0xF)
            for y in range(8):
                for x in range(8):
                    sx = 7 - x if entry & 0x400 else x
                    sy = 7 - y if entry & 0x800 else y
                    rgb, index = data[sy * 8 + sx]
                    if index:
                        px[(quad & 1) * 8 + x, (quad >> 1) * 8 + y] = tuple(rgb) + (255,)
        return img

    card = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    card.paste(layer(top, 1), (0, 0))
    lower = layer(foot, 1)
    ground = layer(foot, 0)
    for y in range(16):
        for x in range(16):
            r, g, b, a = lower.getpixel((x, y))
            if not a:
                continue
            if (r, g, b) in ISLAND_SHADOW:
                ground.putpixel((x, y), (r, g, b, 255))
            else:
                card.putpixel((x, 16 + y), (r, g, b, 255))
                if y >= 7:
                    ground.putpixel((x, y), (r, g, b, 255))   # the trunk's foot
    # The General tileset's flowers (metatile 004): its upper layer is the
    # cluster, over plain grass. Stood up as a card it is the drawing's own
    # flowers; a card of other art in their place did not read as them. The
    # layer is opaque: round the cluster it repeats the grass under it, and
    # its shadow on that grass. Neither stands up - a card that carried them
    # was a square of lawn in front of the flowers behind it.
    general = art.read_u16(os.path.join(tree, art.tileset_dir(primary), "metatiles.bin"))
    lawn = set(FLOWER_SHADOW)
    for entry in general[4 * 8:4 * 8 + 4]:
        lawn |= {tuple(rgb) for (rgb, index) in ts.subtile(entry & 0x3FF, (entry >> 12) & 0xF) if index}
    entries = general[4 * 8 + 4:4 * 8 + 8]
    flowers = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    fpx = flowers.load()
    for quad, entry in enumerate(entries):
        data = ts.subtile(entry & 0x3FF, (entry >> 12) & 0xF)
        for y in range(8):
            for x in range(8):
                sx = 7 - x if entry & 0x400 else x
                sy = 7 - y if entry & 0x800 else y
                rgb, index = data[sy * 8 + sx]
                if index and tuple(rgb) not in lawn:
                    fpx[(quad & 1) * 8 + x, (quad >> 1) * 8 + y] = tuple(rgb) + (255,)
    return card, ground, flowers


def pack(assets, tree):
    pixels = bytearray(WIDTH * DIM * 2)
    images = []
    for name, size, origin in SOURCES:
        with Image.open(assets / name) as source:
            if source.size != size:
                raise ValueError(f"{name}: expected {size}, got {source.size}")
            images.append((source.convert("RGBA"), size, origin))
    card, ground, flowers = island_tree(tree)
    images += [(card, card.size, (64, 0)), (ground, ground.size, (80, 0)),
               (flowers, flowers.size, (96, 0))]
    for image, size, (ox, oy) in images:
        for y in range(size[1]):
            for x in range(size[0]):
                r, g, b, a = image.getpixel((x, y))
                value = ((r >> 3) << 11 | (g >> 3) << 6 |
                         (b >> 3) << 1 | int(a >= 128))
                struct.pack_into("<H", pixels, 2 * texel_offset(ox + x, oy + y), value)
    return pixels


def main():
    port = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=port / "assets/voxel/trees")
    parser.add_argument("--output", type=Path, default=port / "romfs/voxel/trees.rgba5551")
    parser.add_argument("--tree", type=Path, default=port.parent,
                        help="the built source tree, for the tilesets' own trees")
    args = parser.parse_args()
    pixels = pack(args.assets, args.tree)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pixels)
    print(f"voxel trees: {WIDTH}x{DIM}, {len(pixels)} bytes -> {args.output}")


if __name__ == "__main__":
    main()
