#!/usr/bin/env python3
"""Building models, one reading of the drawing per building type.

Each spec names where a reference copy of the building sits (layout and cell
rectangle), which metatiles are the ground around it, the parts that rebuild
it, and the art rectangles the model must reproduce pixel for pixel when it
is rendered in the GBA's projection. Row numbers are art rows of that
rectangle.

Littleroot's houses
-------------------
The two houses are the same building. The drawing, from the top:

    rows  1- 8  upper ridge cap       rows 17-24 lower ridge cap  (the "ears")
    rows  9-15  upper ridge teeth     rows 25-31 lower ridge teeth
    rows 16-35  upper roof, 5 courses rows 32-51 lower roof, 5 courses
    rows 36-37  upper fascia          rows 52-53 lower fascia
    rows 38-44  upper storey wall     rows 54-79 ground floor facade

The ears are the same ridge and the same courses as the upper roof, sixteen
rows lower: a full-width lower roof, and a narrower upper storey that comes up
through it with its own roof.

The drawing is shallower than the house. Taken literally (every band at the
depth the 45-degree projection gives it) the house would be two tiles deep,
while it stands on four rows of collision. So the model keeps the real
footprint, and the depth the drawing does not have is covered the way a roof
covers it - with more courses of the same tiles (Strip), never with stretched
ones. The facade, the pent roof in front of the upper storey, the upper wall
and the upper roof's first four courses stay exactly the drawing; only the
roofs grow, by the courses the depth needs.

Both roofs are hipped: seen from the side they are tiles too, laid along the
side eave, so no gable wall of plaster ever shows.
"""

import os
from voxel_building import (Band, Barrel, Cylinder, Drum, Frustum, HipRoof, Prism, Proj, Scaled, Strip, Tile,
                            Vault, Walls)

GRASS = 0x001

PITCH = 22.0        # degrees, front and back slopes
ROOF_COLUMNS = (12, 68)   # courses sampled away from the drawn verges


def littleroot_house(plaster_x):
    """Both houses. They share every row and every edge; only the middle of
    the facade is rearranged, so each names the 8-px column of plain plaster
    (no window, no door, no post) its walls are dressed from."""
    px0, px1 = plaster_x, plaster_x + 8
    front_z, back_z = 80, 16    # the four collision rows, 5..8
    overhang = 2

    lower = HipRoof(
        "roof_lo", 0, 82, zf=front_z + overhang, zb=back_z - overhang, y0=28,
        fascia=Strip((52, 54), wrap=ROOF_COLUMNS),
        # the seven rows drawn in front of the upper storey, then courses
        # continuing in phase (row 45 sits one above a course's first row)
        slope=Strip((45, 52), repeat=(16, 20), start=16, wrap=ROOF_COLUMNS),
        teeth=(25, 32), cap=(17, 25), pitch=PITCH, run=7,
        ridge_u=(0, 80), end_tile=Tile(0, 25, 8, 32))

    # The upper storey stands on the pent roof where its seventh row ends.
    z_wall, y_base = lower.slope_point(7)
    zf_hi = z_wall + overhang
    y0_hi = zf_hi - 38          # the upper fascia is drawn on rows 36-37
    zb_hi = (lower.zf + lower.zb) - zf_hi
    upper = HipRoof(
        "roof_hi", 8, 72, zf=zf_hi, zb=zb_hi, y0=y0_hi,
        fascia=Strip((36, 38), wrap=ROOF_COLUMNS),
        slope=Strip((32, 36), repeat=(16, 32), wrap=ROOF_COLUMNS),
        teeth=(9, 16), cap=(1, 9), pitch=PITCH, run=6,
        ridge_u=(8, 72), end_tile=Tile(12, 9, 20, 16))

    storey_back = zb_hi + overhang
    post = Tile(10, 38, 14, 45, top=y0_hi)
    storey = Prism(
        "storey", 10, 70,
        [(z_wall, 28), (z_wall, y0_hi), (storey_back, y0_hi), (storey_back, 28)],
        edges={0: Proj(38, 45), 2: Tile(20, 38, 28, 45, top=y0_hi)}, skip=(1, 3),
        caps=[Band(-64, 200, Tile(20, 38, 28, 45, top=y0_hi), z_wall,
                   front=post, back=post, z1=storey_back)])

    wall_top = 28
    corner = Tile(2, 54, 8, 80, top=26)
    base = Prism(
        "ground_floor", 2, 80,
        [(front_z, 0), (front_z, wall_top), (back_z, wall_top), (back_z, 0)],
        edges={0: Proj(54, 80), 2: Tile(px0, 54, px1, 80, top=26)}, skip=(1, 3),
        caps=[Band(0, 26, Tile(px0, 54, px1, 80, top=26), front_z,
                   front=corner, back=corner, z1=back_z),
              Band(26, wall_top + 1, Tile(px0, 54, px1, 55, top=wall_top), front_z)])
    return [base, lower, storey, upper]


# What the model must reproduce exactly: the ground floor, the pent roof in
# front of the upper storey, the upper storey, and the upper roof's fascia and
# first four courses - everything the drawing shows at its own depth.
HOUSE_EXACT = [(2, 54, 80, 80), (12, 45, 68, 54), (10, 38, 70, 45), (12, 16, 68, 38)]

def littleroot_lab():
    """Professor Birch's lab, cells 3..9 x 12..16 of Littleroot.

    The drawing, from the top (112 x 80):

        rows  1- 9  flat top of the roof, light panels, period 8 across
        rows 10-14  its front edge
        rows 15-49  olive tile courses, period 4 down and 8 across
        rows 50-52  fascia
        rows 53-79  facade: posts, two windows, the door

    and on the roof, x 16-47 rows 2-31, a ventilator: a box whose front is
    rows 25-31 and top rows 15-24, carrying a round cowl drawn as a circle
    (rows 2-24). The box stands on the slope exactly where its front row 31
    meets the courses, so its front is the drawing at 45 degrees.
    """
    front_z, back_z = 80, 16    # collision rows 13..16
    overhang = 2
    lab_columns = (8, 104)      # courses away from both verges (12 x 8)
    roof = HipRoof(
        "roof", 0, 114, zf=front_z + overhang, zb=back_z - overhang, y0=29,
        fascia=Strip((50, 53), wrap=lab_columns),
        slope=Strip((46, 50), repeat=(34, 46), wrap=lab_columns),
        teeth=(10, 15), cap=(1, 10), pitch=18.0, run=6,
        ridge_u=(0, 112), end_tile=Tile(48, 10, 57, 15),
        ridge_wrap=(48, 104))    # the drawn ridge is behind the vent at 17-47

    # Ventilator: box front bottom on the slope where art row 32 lies.
    zbox, ybox = roof.slope_point(50 - 32)
    ytop = zbox - 25
    grey = Tile(20, 25, 40, 32, top=ytop)
    box = Prism(
        "vent_box", 16, 48,
        [(zbox, ybox - 6), (zbox, ytop), (zbox - 10, ytop), (zbox - 10, ybox - 6)],
        edges={0: Proj(25, 32), 2: grey}, skip=(3,),
        caps=[Band(-64, 200, grey, zbox)])
    cowl = Cylinder("vent_cowl", 32, zbox - 10, 12, 9, ytop - 4, ytop + 4,
                    back_tile=Tile(24, 16, 40, 25))

    wall_top = 29
    post = Tile(2, 53, 8, 80, top=27)
    plaster = Tile(8, 53, 16, 80, top=27)
    base = Prism(
        "ground_floor", 2, 112,
        [(front_z, 0), (front_z, wall_top), (back_z, wall_top), (back_z, 0)],
        edges={0: Proj(53, 80), 2: plaster}, skip=(1, 3),
        caps=[Band(0, 27, plaster, front_z, front=post, back=post, z1=back_z),
              Band(27, wall_top + 1, Tile(8, 53, 16, 54, top=wall_top), front_z)])
    return [base, roof, box, cowl]


LAB_EXACT = [(2, 53, 112, 80), (8, 32, 104, 53), (48, 16, 104, 32)]

# The Center's crown, read off its drawn front arch (rows 16-23): the height
# of the arch over each column, 1 px at x 16 and 47 and 8 px from 27 to 36.
# Its back arch is drawn exactly 16 rows higher in every column, so the vault
# is 16 px deep - the one depth the drawing states outright.
CENTER_ARCH = [(16, 0), (16.5, 1), (17.5, 2), (18.5, 3), (19.5, 4), (20.5, 4),
               (21.5, 5), (22.5, 6), (23.5, 6), (24.5, 7), (26.5, 7), (27.5, 8),
               (36.5, 8), (37.5, 7), (39.5, 7), (40.5, 6), (41.5, 6), (42.5, 5),
               (43.5, 4), (44.5, 4), (45.5, 3), (46.5, 2), (47.5, 1), (48, 0)]


def center_or_mart(rib_repeat, crown=False):
    """The Pokemon Center and the Poke Mart: one building, two paint jobs.

    The drawing (64 x 64), from the top:

        rows  2- 8  the Center's raised crown (the Mart has none)
        rows  9-23  the flat top, ribbed front to back
        rows 24-37  the roof band with its emblem, drawn round
        rows 38-63  walls: fascia, glass, the door, the sign, the plinth

    The plan is an octagon: the front runs x 8-56, and 8-px chamfers turn the
    corners. The drawing says so itself - the plinth runs diagonally from
    (8, 63) to (0, 56) and the eave from (8, 38) to (0, 30), which is what a
    45-degree chamfer looks like at 45 degrees. The emblem is drawn round, so
    the band faces the camera square on: it pitches at 45 degrees, rising 7.

    Real depth: three collision rows, Z 16-64. The top grows backwards by rows
    of its own ribs, which run front to back and so repeat without a seam.
    """
    front, back = 64, 16
    plan = [(8, front), (56, front), (64, front - 8), (64, back + 8),
            (56, back), (8, back), (0, back + 8), (0, front - 8)]
    parts = [Frustum(
        "body", plan, wall_top=26,
        wall_side=Strip((38, 64), wrap=(8, 16)),
        band_rise=7,
        band_side=Strip((24, 38), wrap=(8, 16)),
        top=Strip((9, 24), repeat=rib_repeat, wrap=(8, 56)))]
    if crown:
        # on the flat top (y 33), from its front edge (z 57) back 16
        parts.append(Vault("crown", CENTER_ARCH, zf=57, zb=41, y0=33))
    return parts


# The walls, the chamfers, the band and the top as drawn; the corners above
# the chamfers are the band's sides, which the real depth moves.
CENTER_EXACT = [(8, 30, 56, 64), (0, 38, 64, 64), (12, 9, 52, 30)]
# The Center adds its crown, whole: both arches and the ribs between them.
CROWN_EXACT = CENTER_EXACT + [(16, 0, 48, 24, True)]

def oldale_house():
    """Oldale's two houses, cells 4..7 x 4..7 and 14..17 x 13..16.

    The drawing (64 x 64), from the top:

        rows  0- 9  the ridge's top, notched along its back edge
        rows 10-13  its front
        rows 14-33  five courses of tiles, period 4 down and 8 across
        rows 34-35  fascia
        rows 36-63  facade: posts, the window, the door

    One storey under a hipped roof, the same reading as Littleroot's lower
    roof. Real depth: the three collision rows, Z 16-64.
    """
    front_z, back_z = 64, 16
    overhang = 2
    columns = (8, 56)           # courses away from both verges (6 x 8)
    roof = HipRoof(
        "roof", 0, 64, zf=front_z + overhang, zb=back_z - overhang, y0=30,
        fascia=Strip((34, 36), wrap=columns),
        slope=Strip((30, 34), repeat=(14, 30), wrap=columns),
        teeth=(10, 14), cap=(0, 10), pitch=22.0, run=6,
        ridge_u=(0, 64), end_tile=Tile(8, 10, 18, 14))

    wall_top = 30
    post = Tile(2, 36, 9, 64, top=28)
    plaster = Tile(9, 36, 15, 64, top=28)
    base = Prism(
        "ground_floor", 2, 64,
        [(front_z, 0), (front_z, wall_top), (back_z, wall_top), (back_z, 0)],
        edges={0: Proj(36, 64), 2: plaster}, skip=(1, 3),
        caps=[Band(0, 28, plaster, front_z, front=post, back=post, z1=back_z),
              Band(28, wall_top + 1, Tile(9, 36, 15, 37, top=wall_top), front_z)])
    return [base, roof]


OLDALE_HOUSE_EXACT = [(2, 36, 64, 64), (8, 14, 56, 36)]


def briney_house():
    """Mr Briney's cottage on Route 104, cells 15..19 x 47..50 (80 x 64).

    The drawing, from the top:

        rows  0- 8  the ridge's top: thatch bundles, period 8 across
        rows  9-15  its front: a batten and a short course between dark lines
        rows 16-35  the thatch: period 8 down (rows 16-23 = 24-31) and across,
                    its eave course fringed at rows 32-35
        rows 36-38  fascia
        rows 39-47  the lattice under the eave (x 0-80)
        rows 48-63  the ground floor (x 1-80): posts, reed walls, the door

    One storey under a hipped roof, like Oldale's houses. Real depth: the
    three collision rows, Z 16-64. The verges (x 0-7 and 72-79) are drawn
    as edge bundles, so the courses are sampled from x 8-72.
    """
    front_z, back_z = 64, 16
    overhang = 2
    columns = (8, 72)
    roof = HipRoof(
        "roof", 0, 80, zf=front_z + overhang, zb=back_z - overhang, y0=27,
        fascia=Strip((36, 39), wrap=columns),
        slope=Strip((16, 36), repeat=(16, 24), wrap=columns),
        teeth=(9, 16), cap=(0, 9), pitch=22.0, run=6,
        ridge_u=(0, 80), end_tile=Tile(8, 9, 18, 16))

    floor_top, wall_top = 16, 27
    post = Tile(1, 48, 8, 64, top=floor_top)
    reed = Tile(8, 48, 18, 64, top=floor_top)
    lattice = Tile(8, 39, 16, 48, top=25)
    lattice_end = Tile(0, 39, 3, 48, top=25)
    ground_floor = Prism(
        "ground_floor", 1, 80,
        [(front_z, 0), (front_z, floor_top), (back_z, floor_top), (back_z, 0)],
        edges={0: Proj(48, 64), 2: reed}, skip=(1, 3),
        caps=[Band(0, floor_top, reed, front_z, front=post, back=post, z1=back_z)])
    upper = Prism(
        "lattice", 0, 80,
        [(front_z, floor_top), (front_z, wall_top), (back_z, wall_top), (back_z, floor_top)],
        edges={0: Proj(39, 48), 2: lattice}, skip=(1, 3),
        caps=[Band(floor_top, wall_top + 1, lattice, front_z, front=lattice_end,
                   back=lattice_end, z1=back_z)])
    return [ground_floor, upper, roof]


BRINEY_HOUSE_EXACT = [(1, 39, 80, 64), (0, 39, 1, 48), (8, 16, 72, 39)]


def flower_shop():
    """The Pretty Petal flower shop on Route 104, cells 3..8 x 15..18 (96 x 64).

    A flat roof of corrugated sheet, seen from above as the GBA sees every
    flat top. The drawing, from the top:

        rows  0- 3  the roof's back edge: an outline and three light rows
        rows  4-27  the sheet, every row the same (ribs period 4 across)
        rows 28-37  the roof slab's red front and the dark line under it
        rows 38-63  the facade (x 1-95): posts, the awning, windows, the door

    Real depth: the three collision rows, Z 16-64. The sheet is laid back
    to them with more of its own rows, the back edge closing it.
    """
    front, back = 64, 16
    wall = 64 - 38
    top = wall + (38 - 28)
    post = Tile(1, 38, 6, 64, top=wall)
    siding = Tile(72, 40, 80, 48, top=wall - 2)
    rim = Tile(9, 28, 17, 38, top=top)
    body = Prism(
        "ground_floor", 1, 95,
        [(front, 0), (front, wall), (back, wall), (back, 0)],
        edges={0: Proj(38, 64), 2: siding}, skip=(1, 3),
        caps=[Band(0, wall, siding, front, front=post, back=post, z1=back)])
    roof = Prism(
        "roof", 0, 96,
        [(front, wall), (front, top), (back, top), (back, wall)],
        edges={0: Proj(28, 38), 1: Strip((4, 28), repeat=(20, 28), tail=(0, 4)), 2: rim},
        skip=(3,), caps=[Band(wall, top + 1, rim, front)])
    return [body, roof]


FLOWER_SHOP_EXACT = [(0, 4, 96, 38), (1, 38, 95, 64)]

def kit_house(width):
    """The General tileset's red-roofed house, any width (in pixels).

    Built from a kit - roof caps, repeated middles, a facade of posts, windows
    and a door - so the same drawing comes 4 and 5 cells wide. The rows are
    the kit's, whatever the width (64 high):

        rows  0- 9  the ridge's top, period 8 across
        rows 10-15  its front
        rows 16-34  scale tiles: two 8-row courses and the eave's three rows
        rows 35-37  fascia
        rows 38-63  facade

    Real depth: three collision rows, Z 16-64. Courses are sampled between
    the drawn verges (x 0-2 and the last three columns), keeping the phase.
    """
    front_z, back_z = 64, 16
    overhang = 2
    columns = (8, width - 8)
    roof = HipRoof(
        "roof", 0, width, zf=front_z + overhang, zb=back_z - overhang, y0=28,
        fascia=Strip((35, 38), wrap=columns),
        slope=Strip((32, 35), repeat=(16, 32), wrap=columns),
        teeth=(10, 16), cap=(0, 10), pitch=22.0, run=6,
        ridge_u=(0, width), end_tile=Tile(8, 10, 18, 16))
    wall_top = 28
    post = Tile(2, 38, 8, 64, top=26)
    boards = Tile(9, 38, 15, 64, top=26)
    base = Prism(
        "ground_floor", 2, width - 2,
        [(front_z, 0), (front_z, wall_top), (back_z, wall_top), (back_z, 0)],
        edges={0: Proj(38, 64), 2: boards}, skip=(1, 3),
        caps=[Band(0, 26, boards, front_z, front=post, back=post, z1=back_z),
              Band(26, wall_top + 1, Tile(9, 38, 15, 39, top=wall_top), front_z)])
    return [base, roof]


def kit_house_exact(width):
    return [(2, 38, width - 2, 64), (8, 16, width - 8, 38)]

def gym():
    """The gym of Petalburg, Mauville, Mossdeep and Lavaridge (96 x 80).

        rows  1-40  a flat gravel roof, period 2 down and across
        rows 41-44  its edge: a light lip and the fascia
        rows 45-71  the facade either side of the porch
        rows 41-48  (x 40-71) the roof running on over the porch
        rows 49-53  the porch's own fascia, eight rows lower: it stands out 8
        rows 54-79  the porch: doors square on, and 8-px chamfers either side,
                    whose plinth runs diagonally from (40, 71) to (48, 79)

    Real depth: the four collision rows reach the top of the drawing, so the
    back wall stands at Z 2 and the gravel repeats back to it.
    """
    front, porch, back = 72, 80, 2
    wall_top, roof_top = 27, 31
    panel = Tile(72, 45, 88, 72, top=wall_top)      # a window bay, for sides
    corner = Tile(88, 45, 94, 72, top=wall_top)
    lip = Tile(8, 41, 16, 45, top=roof_top)
    body = Prism(
        "body", 2, 94,
        [(front, -1), (front, wall_top), (back, wall_top), (back, -1)],
        edges={0: Proj(45, 72), 2: panel}, skip=(1, 3),
        caps=[Band(-1, wall_top, panel, front, front=corner, back=corner, z1=back)])
    roof = Prism(
        "roof", 0, 96,
        [(front, wall_top), (front, roof_top), (back, roof_top), (back, wall_top)],
        edges={0: Proj(41, 45), 1: Strip((5, 41), repeat=(5, 7)), 2: lip},
        skip=(3,), caps=[Band(wall_top, roof_top + 1, lip, front)])
    porch_roof = Prism(
        "porch_roof", 40, 72,
        [(porch, wall_top), (porch, roof_top), (front, roof_top), (front, wall_top)],
        edges={0: Proj(49, 54)}, skip=(2, 3),
        caps=[Band(wall_top, roof_top + 1, lip, porch)])
    porch_walls = Walls("porch", [(40, front), (48, porch), (64, porch), (72, front)],
                        -1, wall_top)
    return [body, roof, porch_roof, porch_walls]


GYM_EXACT = [(2, 45, 40, 72), (72, 45, 94, 72), (3, 5, 93, 45), (40, 41, 72, 80)]

def flat_block(width, height, roof, cornice, facade_top, unit=None):
    """A flat-roofed block: parapeted roof, cornice, facade (any size).

    `roof` = (fixed, repeat, tail): the roof's rows as the drawing lays them
    from its front rim back, the course that repeats to the real depth, and
    the back parapet that closes it. `cornice` = (top, bottom) rows of the
    parapet's front; the facade runs from `facade_top` to the bottom. `unit`
    = (x0, x1, top, face, foot): a box on the roof whose top is drawn from
    row `top`, whose front from `face` to its foot on the roof at `foot`.

    Real depth: the collision starts one row below the drawing's top, so the
    back wall stands at Z 16 and the front at the drawing's foot.
    """
    front, back = height, 16
    wall = height - facade_top
    c0, c1 = cornice
    top = wall + (c1 - c0)
    fixed, repeat, tail = roof
    brick = Tile(8, facade_top, 16, facade_top + 16, top=wall)
    pilaster = Tile(0, facade_top, 8, facade_top + 16, top=wall)
    rim = Tile(8, c0, 16, c1, top=top)
    body = Prism(
        "body", 0, width,
        [(front, -1), (front, wall), (back, wall), (back, -1)],
        edges={0: Proj(facade_top, height), 2: brick}, skip=(1, 3),
        caps=[Band(-1, wall, brick, front, front=pilaster, back=pilaster, z1=back)])
    parts = [body]

    def slab(name, x0, x1, offset=0.0):
        return Prism(
            name, x0, x1,
            [(front, wall), (front, top), (back, top), (back, wall)],
            edges={0: Proj(c0, c1),
                   1: Strip(fixed, repeat=repeat, tail=tail,
                            repeat_offset=offset if offset else None), 2: rim},
            skip=(3,), caps=[Band(wall, top + 1, rim, front)],
            west=(x0 == 0), east=(x1 == width))

    if unit is None:
        parts.append(slab("roof", 0, width))
    else:
        ux0, ux1, t0, t1, t2 = unit
        # under and behind the unit the roof is laid from plain roof columns
        parts += [slab("roof_w", 0, ux0), slab("roof_u", ux0, ux1, offset=8 - ux0),
                  slab("roof_e", ux1, width)]
        zu = t2 + top
        side = Tile(ux0 + 8, t1, ux0 + 16, t2, top=top + (t2 - t1))
        parts.append(Prism(
            "unit", ux0, ux1,
            [(zu, top - 1), (zu, top + (t2 - t1)), (zu - (t1 - t0), top + (t2 - t1)),
             (zu - (t1 - t0), top - 1)],
            edges={0: Proj(t1, t2), 1: Proj(t0, t1), 2: side}, skip=(3,),
            caps=[Band(top - 1, top + (t2 - t1) + 1, side, zu)]))
    return parts


def stone_block(width, height, meta):
    """Rustboro's stone blocks (224..21f): the flat roof drawn rows 0-38, a
    course of 4 rows repeating, the back parapet rows 0-6; the parapet's front
    rows 39-47; the facade below, one row of windows per storey."""
    return flat_block(width, height, ((7, 39), (7, 11), (0, 7)), (39, 48), 48)


def olive_block(width, height, meta):
    """Rustboro's olive-roofed blocks (220..243): the roof drawn rows 0-39 in
    8-row courses, the cornice rows 40-47, the facade below. Most carry a
    ventilation unit on the right end of the roof (metatiles 222 223)."""
    unit = (width - 24, width - 4, 1, 16, 31) if meta.get("unit") else None
    return flat_block(width, height, ((8, 40), (8, 16), (0, 8)), (40, 48), 48, unit)


def box_building(width, foot, facade_top, top=0, side_x=0):
    """Any building as a box: the bottom of its drawing, from `facade_top`
    down to its `foot`, is its front wall, and everything above, from `top`,
    is laid back from the wall's top as its roof, row for row. A pitched roof
    drawn from above lies flat on it - a building that stands, with its roof
    as it is drawn, until it is given a shape of its own. Its sides are
    dressed with eight columns of the facade from `side_x`.

    `top` and `foot` are the rows the drawing itself begins and ends on, not
    the rectangle's: a page holds a drawing cropped to what is drawn, and a
    face laid past it shows whatever the page has beside it (the museum had
    the market's jars along its foot)."""
    return [box_part("body", 0, width, foot, facade_top, top, side_x)]


def box_part(name, x0, x1, foot, facade_top, top=0, side_x=None):
    """One box of a building over the columns [x0, x1): its front the rows
    from `facade_top` to `foot`, its lid the rows from `top` to `facade_top`
    laid back from the front's top. Boxes with different feet side by side
    are a front that steps: pillars standing out of a wall, a round drum."""
    wall = foot - facade_top
    front, back = foot, foot - (facade_top - top)
    side_x = x0 if side_x is None else side_x
    side = Tile(side_x, facade_top, side_x + 8, foot, top=wall)
    return Prism(
        name, x0, x1,
        [(front, 0), (front, wall), (back, wall), (back, 0)],
        edges={0: Proj(facade_top, foot), 1: Proj(top, facade_top), 2: side}, skip=(3,),
        caps=[Band(0, wall + 1, side, front)])


def slateport_museum():
    """The Oceanic Museum: a hall under a flat roof (its drawing's rows 9-48;
    the rows over it are the quay's kerb behind, which lies with it), a front
    wall 32 rows tall, four pillars standing eight rows out of it and as much
    taller, and the steps to its door."""
    return ([box_part("hall", 0, 96, 80, 48, 0, side_x=16)]
            + [box_part("pillar_%d" % x, x, x + 8, 88, 48, 40) for x in (8, 24, 64, 80)]
            + [box_part("steps", 32, 64, 88, 84, 80)])


def market_stall(width, lid=(1, 26), rim=(26, 29), depth=28, high=26):
    """A market stall: a canopy on two posts, open all round. `width` is its
    rectangle's, in pixels; the canopy is drawn eight columns in from each
    side, rows 1-28, and its posts under its front corners, four columns each.

    Not the drawing's own geometry: there the canopy hangs 18 rows up, lower
    than whoever sells under it stands. It is a thin slab 26 rows up, the
    canopy's rows laid back on it from its front edge, and the posts are the
    posts' own shaft repeated up to it. Nothing else: no front under the
    canopy, no sides, no back - a box's faces dressed with the drawing put a
    second pair of posts on its sides and a skirt before the sellers."""
    x0, x1, front = 8, width - 8, 48
    drop = rim[1] - rim[0]          # the canopy's front edge, hanging from it

    def post(name, x, z=None):
        z = front if z is None else z
        return Prism(name, x, x + 4, [(z, 0), (z, high), (z - 2, high), (z - 2, 0)],
                     edges={0: Tile(x, 34, x + 4, 44, top=high)}, skip=(1, 2, 3),
                     caps=None, west=False, east=False)

    lid = Prism("canopy", x0, x1,
                [(front, high - drop), (front, high), (front - depth, high), (front - depth, high - drop)],
                edges={0: Tile(x0, rim[0], x1, rim[1], top=high), 1: Strip(lid)}, skip=(2, 3),
                caps=None, west=False, east=False)
    return [lid, post("post_w", x0 + 1), post("post_e", x1 - 5),
            # and the two behind, which the drawing's camera does not show
            post("post_nw", x0 + 1, front - depth + 2), post("post_ne", x1 - 5, front - depth + 2)]


def standing_card(width=16, height=16):
    """An object a cell across as a card: its drawing stood up at the cell's
    foot, the ground round it cleared (a spec's `clear`). A jar, a bowl, a
    bunch of flowers: drawn as seen from in front, and round - a box of it
    is a block with a jar painted on its lid."""
    return [Prism("card", 0, width, [(height, 0), (height, height), (height - 1, height), (height - 1, 0)],
                  edges={0: Proj(0, height)}, skip=(1, 2, 3), caps=None, west=False, east=False)]


# the lawn's three greens, and the shadow drawn on it
GRASS_COLOURS = ("73c5a4", "a4d5c5", "41b483", "18a46a")
SLATEPORT_PAVING = ("73c5a4", "a49ca4", "c5b4de", "cdcdde", "e6e6ee")
# the market's goods that are round, and the quay's bollard: a tile, and a
# cell that draws it (the others are found by their tile)
SLATEPORT_CARDS = [(0x20B, 7, 36), (0x20C, 6, 34), (0x213, 6, 36), (0x214, 10, 54), (0x21B, 5, 36),
                   (0x21C, 5, 35), (0x223, 7, 45), (0x22B, 3, 36), (0x28D, 3, 47), (0x28E, 11, 43),
                   (0x344, 4, 38), (0x32D, 36, 39)]


def slateport_tent():
    """The Battle Tent: a drum drawn round. Its front steps back towards its
    sides, five boxes under one lid, so it is not a square box; the feet of
    the arches at its sides, drawn lower than the steps stand, are lost."""
    return [box_part("drum_%d" % k, x0, x1, foot, 48, 0, side_x=36)
            for k, (x0, x1, foot) in enumerate(((0, 8, 68), (8, 20, 75), (20, 60, 80),
                                                (60, 72, 75), (72, 80, 68)))]


def flat_block_exact(width, height, first_roof_row):
    return [(0, first_roof_row, width, height)]

def flat_part(name, x0, x1, front, back, roof, cornice, facade_top,
              brick, rim, west=True, east=True):
    """One flat-roofed volume over [x0, x1): facade from `facade_top` to its
    foot at `front`, the parapet's front `cornice` above it, and the roof laid
    back to `back` by `roof` = (fixed, repeat, tail). `brick` and `rim` are
    the art rectangles its sides are dressed with."""
    wall = front - facade_top
    c0, c1 = cornice
    top = wall + (c1 - c0)
    fixed, repeat, tail = roof
    brick_t = Tile(*brick, top=wall)
    rim_t = Tile(*rim, top=top)
    body = Prism(
        name, x0, x1,
        [(front, 0), (front, wall), (back, wall), (back, 0)],
        edges={0: Proj(facade_top, front), 2: brick_t}, skip=(1, 3),
        caps=[Band(0, wall, brick_t, front)], west=west, east=east)
    slab = Prism(
        name + "_roof", x0, x1,
        [(front, wall), (front, top), (back, top), (back, wall)],
        edges={0: Proj(c0, c1), 1: Strip(fixed, repeat=repeat, tail=tail), 2: rim_t},
        skip=(3,), caps=[Band(wall, top + 1, rim_t, front)], west=west, east=east)
    return [body, slab]


def devon():
    """Devon Corporation (160 x 144): two wings and a tower between them.

        wings  x 0-47, 112-159: roof rows 2-31 (a 2-row lattice), parapet
               front rows 32-39, three storeys rows 40-127
        tower  x 48-111: roof rows 0-39 (8-row courses) with the company's
               emblem across its front rim, a double cornice rows 40-55,
               the facade and the arched doors rows 56-143 - it stands one
               row further south than the wings

    Real depth: the collision covers the drawing's top row, so the back wall
    stands at Z 0.
    """
    wing_roof = ((8, 32), (8, 10), (2, 8))
    parts = []
    parts += flat_part("wing_w", 0, 48, 128, 0, wing_roof, (32, 40), 40,
                       brick=(8, 40, 48, 72), rim=(8, 32, 48, 40), east=False)
    parts += flat_part("wing_e", 112, 160, 128, 0, wing_roof, (32, 40), 40,
                       brick=(112, 40, 152, 72), rim=(112, 32, 152, 40), west=False)
    parts += flat_part("tower", 48, 112, 144, 0, ((9, 40), (9, 17), (0, 9)), (40, 56), 56,
                       brick=(48, 56, 56, 88), rim=(56, 40, 64, 56))
    return parts


DEVON_EXACT = [(0, 8, 160, 128), (48, 128, 112, 144)]


def fountain():
    """Rustboro's fountain (48 x 48): an octagonal basin, its white rim and
    water drawn as one flat top 9 px up, the front wall and its chamfers
    below it, a bowl standing in the water and its jet.

    Drawn at its own depth, not stretched to the collision: a basin is as
    deep as it is wide, and the drawing says so.
    """
    h = 9
    front = 46
    top = [(9, front), (39, front), (47, front - 8), (47, 20), (37, 10), (11, 10), (1, 20),
           (1, front - 8)]
    walls = Walls("basin", [(1, front - 8), (9, front), (39, front), (47, front - 8)], -1, h)
    parts = [walls, Relief_top(top, h), Cylinder("bowl", 24, 31, 8, 7, h - 1, 14,
                                                 back_tile=Tile(16, 22, 32, 29)),
             Jet("jet", 21, 27, 31, 14, 26)]
    return parts


class Relief_top:
    """A flat polygon at height `h`, projected: the basin's rim and water."""

    def __init__(self, poly, h):
        self.poly, self.h = poly, h

    def emit(self, mesh):
        h = self.h
        mesh.poly([(x, h, z, x, z - h) for (x, z) in reversed(self.poly)], 1.0, "fountain.top")
        # the sides and back the drawing never shows: the front wall's stone
        n = len(self.poly)
        for i in range(2, n - 1):
            (xa, za), (xb, zb) = self.poly[i], self.poly[(i + 1) % n]
            quad = [(xa, -1, za), (xb, -1, zb), (xb, h, zb), (xa, h, za)]
            # projected: from the front it is the drawing, gaps included
            mesh.poly([q + (q[0], q[2] - q[1]) for q in quad], 0.7, "fountain.side~proj")


class Jet:
    """The fountain's jet: a standing plane through the bowl, projected."""

    def __init__(self, name, x0, x1, z, y0, y1):
        self.name, self.x0, self.x1, self.z, self.y0, self.y1 = name, x0, x1, z, y0, y1

    def emit(self, mesh):
        z = self.z
        quad = [(self.x0, self.y0, z), (self.x1, self.y0, z), (self.x1, self.y1, z),
                (self.x0, self.y1, z)]
        mesh.poly([(x, y, zz, x, zz - y) for (x, y, zz) in quad], 1.0, self.name + "~proj")


# ── Interiors ─────────────────────────────────────────────────────────────
#
# A room is cut into pieces, front first; see gen_voxel_buildings.interior_specs.
# Shapes are in pixels of the room's drawing; `height` is the rows of a piece's
# front, standing at its drawn foot; `base` lifts it onto another piece.

WALL_COLOURS = ("f6b473", "de7b31", "ffe6b4")   # the Center's orange wall


def piece(name, shape, height, base=0, fill=None, leave=(), side=None, solid=False,
          back=None, card=False, top=None, foot=None, walls=(), cells=(), against=None,
          claim=()):
    """`back`: the Z its top runs back to, where the cartridge's collision
    says it ends (or the wall it stands against); `against`: that wall's Z,
    where a top drawn deeper than the room in front of it stops, its back
    rows standing up the wall; `top`: the stretch of the room's
    drawing that depth is laid with, when its own drawn top is too thin to
    repeat; `card`: leaves, not a box; `foot`: the row a wall with a doorway
    stands on; `walls`: the side walls it carries, ((x, z), (x, z)[, height])
    - facing left of a->b - dressed with `side`."""
    return {"name": name, "shape": shape, "height": height, "base": base,
            "fill": fill, "leave": leave, "side": side, "solid": solid,
            "back": back, "card": card, "top": top, "foot": foot, "walls": walls,
            "cells": cells, "against": against, "claim": claim}


def own_shell(pieces):
    """Marks a room's shell - its walls, its doorways' recesses, a maze's
    blocks - as its own (`alone`): the generator stands a known piece
    wherever its cells are drawn again, and a side wall, which is drawn
    nowhere, was found wherever another room had the same floor down a
    column - walls standing loose in the middle of Rustboro's flats."""
    for pc in pieces:
        if pc["name"].split("_")[0] in ("wall", "side", "stairwell", "edge", "block",
                                         "partition", "divider"):
            pc["alone"] = True
    return pieces


# the Center's floor and its shadows, and the counter's cream and trim: what
# a stool, the table or a Poke Ball on the counter leaves round it
CENTER_FLOOR = ("cdc58b", "eedea4", "ffffc5")
CENTER_COUNTER = ("ffffc5", "e6e6b4", "de9c62", "ffe6b4", "de7b31")


def facet(name, a, b, height, walls=(), side=None, cells=()):
    """A chamfered corner: a wall along its foot, from a = (x, top, foot) to
    b in the drawing's pixels, carrying the side walls that run on from it
    (edge on to the GBA camera, drawn nowhere), `height` tall."""
    (xa, ta, fa), (xb, tb, fb) = a, b
    return {"name": name, "shape": [[(xa, ta), (xb, tb), (xb, fb), (xa, fa)]],
            "height": height, "facet": (a, b), "walls": walls, "side": side,
            "cells": cells}


# a stretch of the Center's back wall, full height and one panel wide, as the
# room looks with the furniture taken out: for the faces the drawing never shows
CENTER_WALL_SIDE = (64, 0, 80, 32)


def center_walls(front):
    """The Center's walls, 32 px: the back one, standing at row 32 - in two,
    west and east of x 128, so each half counts against the chunk it stands in
    - and its corners, chamfered at 45 degrees, from which the side walls run
    on to where the floor ends at `front`. The drawing has no side walls: they
    are edge on to its camera; from the console's they close the room."""
    return [
        facet("corner_w", (0, 15, 47), (16, -1, 31), 32, walls=[((0, front), (0, 47))],
              side=CENTER_WALL_SIDE, cells=[(0, front // 16 - 1)]),
        facet("corner_e", (208, -1, 31), (224, 15, 47), 32, walls=[((224, 47), (224, front))],
              side=CENTER_WALL_SIDE, cells=[(13, front // 16 - 1)]),
        piece("wall_e", [(128, 0, 208, 32)], 32, fill=16, side=CENTER_WALL_SIDE),
        piece("wall", [(16, 0, 128, 32)], 32, fill=16, side=CENTER_WALL_SIDE),
    ]


POKEMON_CENTER_1F = [
    # the Poke Balls on the counter's two arms
    piece("ball_w", [("ellipse", 72, 45.5, 7.6, 7.6)], 12, base=10, leave=CENTER_COUNTER),
    piece("ball_e", [("ellipse", 152, 45.5, 7.6, 7.6)], 12, base=10, leave=CENTER_COUNTER),
    # the counter: a bar across the front, an arm back to the wall each end
    piece("counter", [(64, 24, 80, 64), (144, 24, 161, 64), (64, 44, 161, 64)], 10, fill=1,
          back=48),
    # behind it, standing on the floor where the nurse stands
    piece("phone", [(126, 22, 146, 45)], 16, leave=WALL_COLOURS, back=32),
    piece("healer", [(80, 14, 112, 45)], 24, leave=WALL_COLOURS, back=32),
    piece("pc", [(158, 6, 178, 42)], 26, leave=WALL_COLOURS, back=32),
    piece("bookcase", [(32, 14, 65, 42)], 18, leave=WALL_COLOURS, back=32),
    piece("plant", [(14, 10, 34, 40)], 26, leave=WALL_COLOURS, card=True),
    piece("stool_1", [(16, 47, 32, 64)], 6, leave=CENTER_FLOOR),
    piece("stool_2", [(32, 47, 48, 64)], 6, leave=CENTER_FLOOR),
    piece("stool_3", [(160, 95, 176, 111)], 6, leave=CENTER_FLOOR),
    piece("stool_4", [(160, 111, 176, 127)], 6, leave=CENTER_FLOOR),
    piece("stool_5", [(176, 127, 192, 144)], 6, leave=CENTER_FLOOR),
    piece("stool_6", [(192, 127, 208, 144)], 6, leave=CENTER_FLOOR),
    piece("table", [(176, 95, 208, 128)], 8, leave=CENTER_FLOOR),
    piece("escalator", [(0, 78, 34, 123)], 8, leave=CENTER_FLOOR),
    # the walls: the back one, its chamfered corners, the two side walls
    # whose tops are the lines down the room's edges, the front corners
] + center_walls(144)



POKEMON_CENTER_2F = [
    # the three link terminals, in front of the counter, and the glass
    # tubes that stand behind them
    piece("terminal_1", [(48, 40, 64, 73)], 24, leave=WALL_COLOURS, back=48),
    piece("terminal_2", [(128, 54, 144, 81)], 20, back=64),
    piece("terminal_3", [(192, 54, 208, 81)], 20, back=64),
    piece("gate_1", [(80, 46, 96, 57)], 8),
    piece("gate_2", [(144, 46, 160, 57)], 8),
    piece("counter", [(0, 40, 48, 63), (64, 40, 80, 63), (96, 40, 128, 63),
                      (160, 40, 192, 63), (208, 40, 218, 63)], 9, fill=1, back=48),
    # glass tubes: as deep as they are wide, the rest of their drawing height
    piece("tube_1", [(48, 6, 64, 42)], 24, leave=WALL_COLOURS),
    piece("tube_2", [(128, 6, 144, 58)], 33, leave=WALL_COLOURS),
    piece("tube_3", [(192, 6, 208, 58)], 33, leave=WALL_COLOURS),
    piece("plant_1", [(80, 128, 96, 160)], 24, card=True),
    piece("plant_2", [(96, 128, 112, 160)], 24, card=True),
    piece("plant_3", [(144, 128, 160, 160)], 24, card=True),
    piece("plant_4", [(160, 128, 176, 160)], 24, card=True),
    # the five stools along the front are the ground floor's, tile for tile,
    # and stand here as they are (gen_voxel_buildings.reuse_pieces)
    piece("escalator", [(0, 86, 34, 122)], 8, leave=CENTER_FLOOR),
] + center_walls(160)


MART_WALL = ("ffffff", "8bd5de", "d5ded5", "b4b4a4", "83b4b4")
MART_WALL_SIDE = (32, 0, 48, 32)

MART = [
    # the till on the glass counter's arm; the counter, an L from the wall
    piece("till", [(32, 22, 48, 42)], 12, base=15, leave=MART_WALL),
    # a glass case, whose drawn top is two rows: its depth is laid with the
    # glass of the arm that runs back to the wall, which shows its top whole
    piece("counter", [(32, 24, 48, 80), (0, 58, 48, 80)], 15, fill=1, back=64,
          top=(34, 56, 46, 70)),
    # the shelves along the back wall, the plant, the three standing shelves
    piece("shelves_back", [(96, 14, 160, 42)], 20, leave=MART_WALL, back=32),
    piece("plant", [(160, 30, 172, 64)], 26, leave=MART_WALL, card=True),
    # the display stands: low, their front the band at their foot, their
    # three compartments of goods their top, as long as the three cells
    # their collision blocks
    piece("shelf_1", [(96, 62, 112, 111)], 14, back=64),
    piece("shelf_2", [(112, 62, 128, 111)], 14, back=64),
    piece("shelf_3", [(160, 54, 172, 111)], 14, back=64),
    # the walls as the Center's: 7-px corners, the side walls run on from them
    facet("corner_w", (0, 6, 40), (7, -1, 33), 34, walls=[((0, 128), (0, 40))],
          side=MART_WALL_SIDE, cells=[(0, 7)]),
    facet("corner_e", (169, -1, 33), (176, 6, 40), 34, walls=[((176, 40), (176, 128))],
          side=MART_WALL_SIDE, cells=[(10, 7)]),
    piece("wall", [(7, 0, 169, 32)], 32, fill=16, side=MART_WALL_SIDE),
]


def _replace(pieces, names, new):
    """A room like another but for some pieces: `new` stands where the first
    of `names` did, and the rest of them are gone."""
    out, done = [], False
    for pc in pieces:
        if pc["name"] in names:
            if not done:
                out += new
                done = True
            continue
        out.append(pc)
    return out


# Lavaridge's Center: a door to the hot spring in the back wall, a plant
# either side of it. Its counter, Poke Balls, machines, stools, table and
# escalator are the other Centers', tile for tile, and stand here as they are
# (gen_voxel_buildings.reuse_pieces), and so is the back wall east of the
# door; the plants and the rest of the walls are its own.
LAVARIDGE_CENTER_1F = [
    piece("plant_w", [(14, 10, 34, 40)], 26, leave=WALL_COLOURS),
    piece("plant_e", [(46, 10, 66, 40)], 26, leave=WALL_COLOURS),
] + [pc for pc in center_walls(144) if pc["name"] != "wall_e"]


# The front corners the GBA leaves black: the outside of a room whose front
# wall it never draws. In the round they are floor, not a hole in it.
CENTER_1F_OPEN = [[(0, 126), (18, 144), (0, 144)], [(224, 126), (206, 144), (224, 144)]]
CENTER_2F_OPEN = [[(0, 142), (18, 160), (0, 160)], [(224, 142), (206, 160), (224, 160)]]
MART_OPEN = [[(0, 118), (10, 128), (0, 128)], [(176, 118), (166, 128), (176, 128)]]

# ── Littleroot's two houses ───────────────────────────────────────────────
#
# Brendan's and May's, each a ground floor and a bedroom, the one house the
# other way round. The ground floor's back wall steps forward a cell where the
# stairs go up, and the stairs are a doorway in it: the flight is drawn inside
# the doorway as the GBA sees it from above, so it lies on the floor of a
# recess one cell deep, with the doorway's sides and back round it. Upstairs
# the same doorway leads down, drawn on the floor behind the wall's face.
#
# Furniture against the back wall stands on the wall's own row of collision,
# so what it is drawn with in front of the wall is all the depth it has; a
# desk drawn with more top than that stands its back rows up the wall.

HOUSE_WALL = ("d5d5b4", "b4b4a4", "ffffff")          # plaster, baseboard, trim
HOUSE_FLOOR = ("b4a44a", "947329", "ac8b39", "cdc55a")   # the planks
BLUE_RUG = ("6a94c5", "8bbdf6", "838394")               # and the chairs' shadows
PINK_RUG = ("d57bac", "838394")


def house_chair(name, back, seat, leave):
    """A kitchen chair seen from the side: its back, a narrow slab, and its
    seat, as deep as one another."""
    return [piece(name + "_back", [back], 9, leave=leave, solid=True),
            piece(name + "_seat", [seat], 5, leave=leave, solid=True)]


def stairwell(name, x0, x1, front, back, opening, side, crest):
    """The sides and back of a doorway's recess, x0..x1 from the wall's face
    at `front` back to `back`; `opening` is the doorway's height. `crest` is
    the row the wall's top is drawn on: nothing of the recess may rise above
    it at 45 degrees, so the sides step down where the doorway's height
    would."""
    low = min(opening, back - crest)
    mid = crest + opening
    if mid >= front or mid <= back:
        walls = [((x0, front), (x0, back), low), ((x1, back), (x1, front), low)]
    else:
        walls = [((x0, front), (x0, mid), opening), ((x0, mid), (x0, back), low),
                 ((x1, back), (x1, mid), low), ((x1, mid), (x1, front), opening)]
    walls.append(((x0, back), (x1, back), low))
    return piece(name, [], 32, side=side, walls=walls)


def brendan_1f():
    rug = BLUE_RUG
    return (house_chair("chair_nw", (33, 96, 37, 112), (37, 100, 47, 112), rug)
            + house_chair("chair_sw", (33, 112, 37, 128), (37, 116, 47, 128), rug)
            + house_chair("chair_ne", (91, 96, 95, 112), (81, 100, 91, 112), rug)
            + house_chair("chair_se", (91, 112, 95, 128), (81, 116, 91, 128), rug) + [
        piece("table", [(50, 96, 78, 128)], 8, leave=rug, solid=True),
        # the television on its stand, a set as deep as the cell it blocks,
        # and the low white cupboard beside it
        # its sides the casing: the dark grey the set is framed with, on its stand
        piece("tv", [(64, 61, 80, 88)], 20, back=72, top=(68, 62, 78, 63),
              side=(64, 68, 66, 88)),
        piece("cabinet", [(32, 65, 63, 88)], 9, back=72),
        # the kitchen along the back wall: fridge, sink, china cabinet
        piece("fridge", [(0, 18, 16, 48)], 24, leave=HOUSE_FLOOR, back=32),
        piece("tap", [(22, 24, 29, 29)], 5, base=8, leave=HOUSE_WALL[:2]),
        piece("sink", [(16, 29, 48, 41), (17, 41, 47, 48)], 8, back=32, top=(18, 38, 46, 39)),
        piece("dresser", [(49, 19, 72, 48)], 23, back=32),
        stairwell("stairwell", 128, 144, 48, 29, 19, (128, 29, 144, 34), 16),
        # the back wall, a cell forward east of the step; the doorway is cut
        # out of it and it stands on its foot
        piece("wall_e", [(112, 32, 113, 48), (113, 16, 176, 29), (113, 29, 128, 48),
                         (144, 29, 176, 48)], 32, fill=16, foot=48,
              side=(156, 16, 172, 48), walls=[((112, 32), (112, 48))]),
        piece("wall", [(0, 0, 113, 32), (113, 0, 117, 16)], 32, fill=16, foot=32,
              side=(72, 0, 80, 32)),
        piece("side_w", [], 32, side=(72, 0, 80, 32), walls=[((0, 144), (0, 32))]),
        piece("side_e", [], 32, side=(156, 16, 172, 48), walls=[((176, 48), (176, 144))]),
    ])


def may_1f():
    rug = PINK_RUG
    # the chairs' seats are Brendan's, pixel for pixel on another rug, and
    # stand here as they are; their backs are drawn over the rug
    return [pc for pc in (house_chair("chair_nw", (81, 96, 85, 112), (85, 100, 95, 112), rug)
                          + house_chair("chair_sw", (81, 112, 85, 128), (85, 116, 95, 128), rug)
                          + house_chair("chair_ne", (139, 96, 143, 112), (129, 100, 139, 112), rug)
                          + house_chair("chair_se", (139, 112, 143, 128), (129, 116, 139, 128), rug))
            if pc["name"].endswith("_back")] + [
        piece("table", [(98, 96, 126, 128)], 8, leave=rug, solid=True),
        # the television and its cabinet, the fridge, the tap and the sink
        # are Brendan's, pixel for pixel, and stand here as they are
        # (gen_voxel_buildings.reuse_pieces)
        piece("dresser", [(105, 19, 128, 48)], 23, back=32),
        stairwell("stairwell", 32, 48, 48, 29, 19, (32, 29, 48, 34), 16),
        piece("wall_w", [(63, 32, 64, 48), (0, 16, 63, 29), (0, 29, 32, 48),
                         (48, 29, 63, 48)], 32, fill=16, foot=48,
              side=(4, 16, 20, 48), walls=[((64, 48), (64, 32))]),
        piece("wall", [(63, 0, 176, 32), (59, 0, 63, 16)], 32, fill=16, foot=32,
              side=(96, 0, 104, 32)),
        piece("side_w", [], 32, side=(4, 16, 20, 48), walls=[((0, 144), (0, 48))]),
        piece("side_e", [], 32, side=(96, 0, 104, 32), walls=[((176, 32), (176, 144))]),
    ]


def brendan_2f():
    return [
        # the desk: the computer and the stereo on it, the chair before it
        piece("chair_back", [(1, 33, 5, 48)], 9, leave=HOUSE_FLOOR, solid=True),
        piece("chair_seat", [(5, 36, 14, 48)], 5, leave=HOUSE_FLOOR, solid=True),
        piece("pc", [(1, 9, 16, 30)], 16, base=9, leave=HOUSE_WALL, back=32),
        piece("stereo", [(18, 24, 30, 31)], 6, base=9, solid=True),
        piece("desk", [(0, 20, 32, 40)], 9, leave=HOUSE_FLOOR, against=32),
        # the games console and its pad, the television
        piece("console", [(51, 24, 64, 40)], 9, leave=HOUSE_WALL + HOUSE_FLOOR, back=32),
        piece("tv", [(64, 13, 80, 40)], 20, back=32, top=(68, 14, 78, 15),
              side=(64, 20, 66, 40)),
        # the bed, its head a board at the mattress's back
        piece("bed_head", [(12, 62, 36, 70)], 7, base=7, leave=HOUSE_FLOOR),
        piece("bed", [(12, 70, 36, 93)], 7, leave=HOUSE_FLOOR, solid=True, claim=[(12, 70, 36, 72)]),
        stairwell("stairwell", 112, 128, 32, 13, 19, (113, 14, 127, 26), 0),
        piece("wall", [(0, 0, 112, 32), (112, 0, 128, 13), (128, 0, 144, 32)], 32, fill=16,
              foot=32, side=(96, 0, 104, 32)),
        piece("side_w", [], 32, side=(96, 0, 104, 32), walls=[((0, 128), (0, 32))]),
        piece("side_e", [], 32, side=(96, 0, 104, 32), walls=[((144, 32), (144, 128))]),
    ]


def may_2f():
    return [
        piece("chair_back", [(139, 33, 143, 48)], 9, leave=HOUSE_FLOOR, solid=True),
        piece("chair_seat", [(130, 36, 139, 48)], 5, leave=HOUSE_FLOOR, solid=True),
        piece("pc", [(128, 9, 143, 30)], 16, base=9, leave=HOUSE_WALL, back=32),
        piece("stereo", [(114, 24, 126, 31)], 6, base=9, solid=True),
        piece("desk", [(112, 20, 144, 40)], 9, leave=HOUSE_FLOOR, against=32),
        piece("console", [(83, 24, 98, 40)], 9, leave=HOUSE_WALL + HOUSE_FLOOR, back=32),
        # the television is Brendan's, tile for tile
        piece("bed_head", [(108, 62, 132, 70)], 7, base=7, leave=HOUSE_FLOOR),
        piece("bed", [(108, 70, 132, 93)], 7, leave=HOUSE_FLOOR, solid=True,
              claim=[(108, 70, 132, 72)]),
        stairwell("stairwell", 16, 32, 32, 13, 19, (17, 14, 31, 26), 0),
        piece("wall", [(0, 0, 16, 32), (16, 0, 32, 13), (32, 0, 144, 32)], 32, fill=16,
              foot=32, side=(40, 0, 48, 32)),
        piece("side_w", [], 32, side=(40, 0, 48, 32), walls=[((0, 128), (0, 32))]),
        piece("side_e", [], 32, side=(40, 0, 48, 32), walls=[((144, 32), (144, 128))]),
    ]


# ── The two houses most of Hoenn lives in ─────────────────────────────────
#
# LAYOUT_HOUSE1 and LAYOUT_HOUSE2 (Oldale's two houses, and nineteen more
# maps'): a glass case and a chest of drawers or a kitchen along the back
# wall, a table and its chairs in the room, potted plants. Built like
# Littleroot's: furniture against the back wall stands on the wall's row of
# collision; what the second house repeats of the first tile for tile (the
# glass case, the plant in the corner) is the first's model
# (gen_voxel_buildings.reuse_pieces).

GENERIC_WALL = ("d5d5b4", "b4b4a4", "ffffff", "629c8b")   # plaster, trim, baseboard
GENERIC_FLOOR = ("ded552", "bdb431", "8b8b8b", "9c9410")  # the planks, their shade
GENERIC_RUG = ("ffcd8b", "f6f6a4")
GENERIC_TABLE = ("fff683", "bdac52")


def potted_plant(x, y):
    """The potted plant's outline, its crown's top-left at (x, y): the
    lines between the planks are drawn in the pot's own outline colour, so
    the shape follows the crown, the stem and the pot instead of a box."""
    return [(x, y, x + 16, y + 13), (x + 2, y + 13, x + 14, y + 14),
            (x + 3, y + 14, x + 13, y + 15), (x + 5, y + 15, x + 11, y + 16),
            (x + 6, y + 16, x + 10, y + 18), (x + 4, y + 18, x + 12, y + 19),
            (x + 3, y + 19, x + 13, y + 20), (x + 2, y + 20, x + 14, y + 30),
            (x + 4, y + 30, x + 12, y + 31)]


def house1():
    rug = GENERIC_RUG
    return (house_chair("chair_n", (74, 64, 78, 80), (65, 68, 74, 80), rug)
            + house_chair("chair_s", (74, 80, 78, 96), (65, 84, 74, 96), rug) + [
        # the teapot on the table
        piece("teapot", [(49, 72, 59, 80)], 5, base=11, leave=GENERIC_TABLE),
        # what the teapot hides of the table top is the table's own pixels
        piece("table", [(34, 64, 62, 97)], 11, leave=rug, solid=True, fill=1, foot=97),
        piece("plant_se", potted_plant(144, 113), 31, leave=GENERIC_FLOOR, card=True),
        piece("plant_1", potted_plant(128, 17), 31, leave=GENERIC_WALL + GENERIC_FLOOR, card=True),
        piece("plant_2", potted_plant(144, 17), 31, leave=GENERIC_WALL + GENERIC_FLOOR, card=True),
        # the glass case and the chest of drawers against the back wall
        piece("case", [(0, 12, 32, 40)], 20, leave=GENERIC_WALL + GENERIC_FLOOR, back=32),
        piece("drawers", [(33, 11, 57, 41)], 21, leave=GENERIC_WALL + GENERIC_FLOOR, back=32),
        piece("wall", [(0, 0, 160, 32)], 32, fill=16, foot=32, side=(64, 0, 80, 32)),
        piece("side_w", [], 32, side=(64, 0, 80, 32), walls=[((0, 144), (0, 32))]),
        piece("side_e", [], 32, side=(64, 0, 80, 32), walls=[((160, 32), (160, 144))]),
    ])


def house2():
    fl = GENERIC_FLOOR
    # the east chairs' seats and the plant are the first house's, pixel for
    # pixel on another floor, and stand here as they are
    return (house_chair("chair_nw", (66, 64, 70, 80), (70, 68, 79, 80), fl)
            + house_chair("chair_sw", (66, 80, 70, 96), (70, 84, 79, 96), fl)
            + [piece("chair_ne_back", [(122, 64, 126, 80)], 9, leave=fl, solid=True),
               piece("chair_se_back", [(122, 80, 126, 96)], 9, leave=fl, solid=True)] + [
        piece("table", [(82, 64, 110, 96)], 10, leave=fl, solid=True),
        # the television on its glass-doored stand: Littleroot's set, whose
        # tile this is, on a stand a row shorter
        piece("tv", [(32, 13, 48, 39)], 19, leave=GENERIC_WALL + fl, back=32,
              top=(36, 14, 46, 15), side=(32, 20, 34, 39)),
        # the kitchen: a cupboard, the sink and hob, the fridge
        piece("tap", [(133, 16, 142, 25)], 8, base=8, leave=GENERIC_WALL[:2]),
        piece("cupboard", [(112, 17, 128, 40)], 16, leave=GENERIC_WALL + fl, back=32),
        piece("sink", [(128, 21, 160, 40)], 8, leave=GENERIC_WALL + fl, against=32),
        piece("fridge", [(160, 10, 176, 40)], 24, leave=GENERIC_WALL + fl, back=32),
        piece("wall", [(0, 0, 176, 32)], 32, fill=16, foot=32, side=(48, 0, 64, 32)),
        piece("side_w", [], 32, side=(48, 0, 64, 32), walls=[((0, 128), (0, 32))]),
        piece("side_e", [], 32, side=(48, 0, 64, 32), walls=[((176, 32), (176, 128))]),
    ])


def house_with_bed():
    """LAYOUT_HOUSE_WITH_BED (Petalburg's second house, and two more maps'):
    the two houses' room with a bed in it, two chests and a bookcase along
    the back wall, a table and two chairs."""
    fl = GENERIC_FLOOR
    # the chairs and the chest of drawers are the second house's, pixel for
    # pixel, and stand here as they are (gen_voxel_buildings.reuse_pieces)
    return [
        piece("table", [(128, 64, 158, 96)], 10, leave=fl, solid=True),
        # the bed, its head a board at the mattress's back
        piece("bed_head", [(4, 48, 28, 56)], 7, base=7, leave=fl),
        piece("bed", [(4, 56, 28, 80)], 7, leave=fl, solid=True),
        # along the back wall: the green chest, the bookcase
        piece("chest", [(16, 15, 32, 40)], 17, leave=GENERIC_WALL + fl, back=32),
        piece("bookcase", [(128, 10, 160, 40)], 22, leave=GENERIC_WALL + fl, back=32),
        piece("wall", [(0, 0, 160, 32)], 32, fill=16, foot=32, side=(64, 0, 80, 32)),
        piece("side_w", [], 32, side=(64, 0, 80, 32), walls=[((0, 128), (0, 32))]),
        piece("side_e", [], 32, side=(64, 0, 80, 32), walls=[((160, 32), (160, 128))]),
    ]


def petalburg_gym():
    """Petalburg's gym: nine rooms one under another in the black between
    them, each nine cells wide and eight deep under a back wall two cells
    tall, its doors and its plate drawn on the wall's face. Back walls only:
    the drawing has no side walls, and a pair made for every room (as the
    houses have, to close them from the console's camera) puts the layout's
    page past the console's 512x512 - four rooms' fit, and four closed rooms
    of nine would read as a fault."""
    side = (16, 208, 48, 240)       # a stretch of the second room's panelling
    floor = ("e6cd73", "cdb452", "f6e683")
    # the two statues by the door of the first room (the last of the layout):
    # an orb on a plinth, a card each
    statues = only_here([piece("statue_w", [(16, 1744, 32, 1776)], 31, leave=floor, card=True),
                         piece("statue_e", [(112, 1744, 128, 1776)], 31, leave=floor, card=True)],
                        "statue_w", "statue_e")     # Rustboro's gym has its own
    return statues + [piece("wall_%d" % room, [(0, y, 144, y + 32)], 32, fill=16, foot=y + 32, side=side)
                      for room, y in ((room, room * 13 * 16) for room in range(9))]


# ── The other houses of the general indoor tileset ────────────────────────
#
# Rooms no one has modelled piece by piece yet: a back wall two cells tall,
# blocked all across, over a rectangle of floor. Their walls stand - the back
# one, and where the floor runs to the room's edges the two sides the drawing
# has no pixel of - and their furniture stays drawn on the floor until the
# room gets pieces of its own. Each: its layout, its size in cells, its floor,
# the wall's cell the sides are dressed with (bare panelling: the pair of
# metatiles the wall repeats most), and whether it has side walls.

PLAIN_ROOMS = [
    ("LAYOUT_HOUSE3", 10, 8, 0x229, 1, True),
    ("LAYOUT_DEWFORD_TOWN_HALL", 17, 9, 0x223, 3, True),
    ("LAYOUT_HOUSE4", 10, 9, 0x229, 3, True),
    ("LAYOUT_LILYCOVE_CITY_HOUSE2", 8, 8, 0x229, 3, True),
    ("LAYOUT_VERDANTURF_TOWN_WANDAS_HOUSE", 17, 8, 0x223, 5, True),
    ("LAYOUT_PACIFIDLOG_TOWN_HOUSE1", 10, 9, 0x3A3, 4, True),
    ("LAYOUT_PACIFIDLOG_TOWN_HOUSE2", 10, 9, 0x3A3, 5, True),
    ("LAYOUT_RUSTBORO_CITY_HOUSE", 12, 9, 0x32C, 3, True),
    ("LAYOUT_RUSTBORO_CITY_HOUSE1", 13, 8, 0x32C, 4, True),
    ("LAYOUT_RUSTBORO_CITY_CUTTERS_HOUSE", 11, 9, 0x32C, 4, True),
    ("LAYOUT_FORTREE_CITY_HOUSE1", 8, 6, 0x3D9, 2, True),
    ("LAYOUT_FORTREE_CITY_HOUSE2", 8, 6, 0x3D9, 1, True),
    ("LAYOUT_ROUTE116_TUNNELERS_REST_HOUSE", 10, 9, 0x229, 3, True),
    ("LAYOUT_ROUTE110_TRICK_HOUSE_ENTRANCE", 12, 8, 0x229, 1, True),
    ("LAYOUT_FORTREE_CITY_DECORATION_SHOP", 8, 6, 0x3D9, 1, False),
    ("LAYOUT_SOOTOPOLIS_CITY_LOTAD_AND_SEEDOT_HOUSE", 8, 7, 0x3FE, 2, True),
    ("LAYOUT_SOOTOPOLIS_CITY_HOUSE1", 8, 7, 0x3FE, 1, True),
    ("LAYOUT_SOOTOPOLIS_CITY_HOUSE2", 8, 7, 0x3FE, 4, True),
    ("LAYOUT_SOOTOPOLIS_CITY_HOUSE3", 8, 7, 0x3FE, 3, True),
    ("LAYOUT_MOSSDEEP_CITY_STEVENS_HOUSE", 11, 8, 0x223, 3, True),
]


def plain_room(width, height, plain_x, sides):
    w, h = width * 16, height * 16
    side = (plain_x * 16, 0, plain_x * 16 + 16, 32)
    pieces = [piece("wall", [(0, 0, w, 32)], 32, fill=16, foot=32, side=side)]
    if sides:
        pieces += [piece("side_w", [], 32, side=side, walls=[((0, h), (0, 32))]),
                   piece("side_e", [], 32, side=side, walls=[((w, 32), (w, h))])]
    return pieces


# ── Mr. Briney's house ────────────────────────────────────────────────────
#
# A room of tatami by the dock on Route 104: a chest of drawers, a small one
# and a glass case along the back wall, three jars in the corner, a low table.

BRINEY_FLOOR = ("c5ffac", "a4cd6a", "83ac4a", "7b7b83", "6a8b31", "414a6a")
BRINEY_WALL = ("d5b483", "ffffff", "d5c54a", "947329", "ac8b39", "629c8b")


def briney_room():
    fl = BRINEY_FLOOR
    side = (48, 0, 64, 32)
    return [
        # the table, the small chest and the glass case are Dewford's houses'
        # (house3_furniture, house4_furniture), found here as they are
        piece("jar_s", [(1, 65, 14, 80)], 9, leave=fl, solid=True),
        piece("jar_w", [(1, 49, 14, 64)], 9, leave=fl, solid=True),
        piece("jar_e", [(17, 49, 30, 64)], 9, leave=fl, solid=True),
        piece("drawers", [(17, 10, 45, 45)], 22, leave=BRINEY_WALL + fl, back=32),
        piece("wall", [(0, 0, 192, 32)], 32, fill=16, foot=32, side=side),
        piece("side_w", [], 32, side=side, walls=[((0, 144), (0, 32))]),
        piece("side_e", [], 32, side=side, walls=[((192, 32), (192, 144))]),
    ]


# ── Dewford's two houses ──────────────────────────────────────────────────
#
# LAYOUT_HOUSE3 and LAYOUT_HOUSE4: Mr. Briney's tatami and his furniture in
# other places - the glass case, a stove, a bookcase and a cabinet along the
# back wall of the first; the case, two jars and the small chest in the
# second; a low table in each. They were plain rooms: walls, and everything
# else painted on the floor. Their pieces, added to the plain room's walls.

def tatami_posts(width):
    """The posts at the back wall's two ends, drawn in the wall's own colours
    down to a foot three rows into the room: they stand in front of it."""
    return [piece("post_w", [(0, 0, 8, 35), (1, 35, 7, 36)], 32, back=32),
            piece("post_e", [(width - 8, 0, width, 35), (width - 7, 35, width - 1, 36)], 32, back=32)]


def tatami_edge(y, cells=1):
    """The front of the tatami's platform, where it ends before the entrance:
    eleven rows of face across the room - a board, the dark line under it and
    the grey of the platform's side. Left on the floor it read as a wall lying
    at the door. A cell of the face a piece, so that it is found again in
    every room with a platform, whatever its width. The west cell's face is
    drawn in the wall's shadow, and the grey that runs forward from it to the
    room's front is that shadow on the entrance's floor: it lies there. Stood
    up as a block it was a box in the corner where the step should be."""
    return ([piece("platform_face_w", [(0, y, 16, y + 11)], 11)]
            + [piece("platform_face_%d" % i, [(16 + 16 * i, y, 32 + 16 * i, y + 11)], 11)
               for i in range(cells)])


def house3_furniture():
    fl, wall = BRINEY_FLOOR, BRINEY_WALL + BRINEY_FLOOR
    pieces = [
        piece("table", [(66, 51, 91, 78)], 10, leave=fl, solid=True),
        piece("case", [(16, 12, 49, 45)], 20, leave=wall, back=32),
        piece("stove", [(80, 12, 96, 45)], 20, leave=wall, back=32),
        piece("bookcase", [(96, 12, 128, 45)], 20, leave=wall, back=32),
        # its greens are the tatami's own: claimed whole, by its outline
        piece("cabinet", [(130, 16, 142, 17), (129, 17, 143, 18), (128, 18, 144, 39),
                          (129, 39, 143, 40)], 16, back=32),
    ] + tatami_posts(160) + tatami_edge(96, 9)
    return only_here(pieces, "stove", "bookcase", "cabinet", "post_w", "post_e")


def house4_furniture():
    fl, wall = BRINEY_FLOOR, BRINEY_WALL + BRINEY_FLOOR
    pieces = [
        piece("table", [(114, 67, 139, 94)], 10, leave=fl, solid=True),
        piece("jar_w", [(49, 33, 62, 48)], 9, leave=fl, solid=True),
        piece("jar_e", [(65, 33, 78, 48)], 9, leave=fl, solid=True),
        piece("chest", [(128, 16, 144, 45)], 16, leave=wall, back=32),
    ] + tatami_posts(160)
    # the jars stand against the wall here, and are Mr. Briney's elsewhere
    return only_here(pieces, "jar_w", "jar_e", "post_w", "post_e")


def only_here(pieces, *names):
    """Pieces measured on this room's floor alone: not stood wherever their
    cells are drawn again (`alone`), where another floor shows round them."""
    for pc in pieces:
        if pc["name"] in names:
            pc["alone"] = True
    return pieces


def hall_furniture():
    """Dewford's Town Hall: a wall that parts the room, running forward from
    the back wall, seen from above as the white of its top with a face at
    its end; a low wall across the east half, a desk and a small chest in
    front of it; a table in the west half."""
    fl = GENERIC_FLOOR
    pieces = [
        piece("hall_table", [(32, 64, 80, 96)], 11, leave=fl, solid=True),
        # (the small chest by the desk is the second house's cupboard, found here)
        piece("hall_desk", [(224, 104, 255, 128)], 8, leave=fl, solid=True),
        piece("divider", [(211, 75, 272, 76), (210, 76, 272, 77), (209, 77, 272, 109),
                          (210, 109, 272, 110), (211, 110, 272, 111)], 24, solid=True, fill=1),
        piece("partition", [(161, 4, 175, 111)], 28, solid=True),
    ]
    return only_here(pieces, "hall_table", "hall_desk")


PLAIN_FURNITURE = {
    "LAYOUT_DEWFORD_TOWN_HALL": hall_furniture,
    "LAYOUT_HOUSE3": house3_furniture,
    "LAYOUT_HOUSE4": house4_furniture,
}


# ── Rooms with a flight of stairs in the back wall ────────────────────────
#
# Rustboro's flats (and whatever else is built like them): the plain room's
# walls, with a doorway a cell wide in the back wall for every flight. Like
# Littleroot's: the flight is drawn inside the doorway as the GBA sees it from
# above, so it lies on the floor of a recess one cell deep, with the doorway's
# sides and back round it - a way out of the room, not a picture of stairs
# flat on the floor. Each: its layout, its size in cells, its floor, the
# wall's cell the sides are dressed with, and the doorways' columns - and, in
# Rustboro's second block of flats, where the wall that parts the room in two
# runs down from the back wall (its left edge), with the low wall the same
# three floors have along the front of the east half.

FLAT_FLOOR = ("d5d5b4", "f6f6a4", "b4b4a4", "8b8b8b", "ded552")

STAIR_ROOMS = [
    ("LAYOUT_RUSTBORO_CITY_FLAT1_1F", 14, 8, 0x32C, 5, (2,)),
    ("LAYOUT_RUSTBORO_CITY_FLAT1_2F", 14, 8, 0x32C, 5, (2,)),
    ("LAYOUT_RUSTBORO_CITY_FLAT2_1F", 14, 9, 0x32C, 1, (3,), 80),
    ("LAYOUT_RUSTBORO_CITY_FLAT2_2F", 14, 9, 0x32C, 9, (1, 3), 80),
    ("LAYOUT_RUSTBORO_CITY_FLAT2_3F", 14, 9, 0x32C, 3, (1,), 64),
    ("LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_1F", 12, 9, 0x229, 4, (2,)),
    ("LAYOUT_LILYCOVE_CITY_COVE_LILY_MOTEL_2F", 12, 9, 0x229, 4, (2,)),
    ("LAYOUT_ROUTE114_FOSSIL_MANIACS_HOUSE", 10, 8, 0x229, 2, (4,)),
    ("LAYOUT_ROUTE110_TRICK_HOUSE_END", 12, 8, 0x229, 6, (2, 10)),
    # the Devon Corporation's upper floors
    ("LAYOUT_RUSTBORO_CITY_DEVON_CORP_2F", 19, 9, 0x380, 4, (2, 14)),
    ("LAYOUT_RUSTBORO_CITY_DEVON_CORP_3F", 19, 9, 0x380, 4, (2,)),
    # Slateport's Oceanic Museum: the stairs' doorway in the back wall
    ("LAYOUT_SLATEPORT_CITY_OCEANIC_MUSEUM_1F", 20, 9, 0x201, 0, (6,)),
    ("LAYOUT_SLATEPORT_CITY_OCEANIC_MUSEUM_2F", 20, 9, 0x201, 0, (6,)),
    # Stern's shipyard
    ("LAYOUT_SLATEPORT_CITY_STERNS_SHIPYARD_1F", 21, 15, 0x202, 5, (3,)),
    ("LAYOUT_SLATEPORT_CITY_STERNS_SHIPYARD_2F", 17, 15, 0x202, 0, (3,)),
]


def stair_room(width, height, plain_x, doors, partition=None):
    w, h = width * 16, height * 16
    side = (plain_x * 16, 0, plain_x * 16 + 16, 32)
    wall, pieces, x = [], [], 0
    if partition is not None:
        # seen from above: the white of their tops, and a face at the end
        pieces += [
            piece("divider", [(128, 90, 224, 127)], 27, solid=True, leave=FLAT_FLOOR),
            piece("partition", [(partition, 0, partition + 16, 127)], 29, solid=True),
        ]
    for door in sorted(doors):
        d = door * 16
        wall += [(x, 0, d, 32), (d, 0, d + 16, 13)]
        # the doorway: 19 pixels tall under the 13 of wall over it, its
        # sides the dark of the flight's own well
        pieces.append(stairwell("stairwell_%d" % door, d, d + 16, 32, 13, 19,
                                (d + 1, 14, d + 15, 26), 0))
        x = d + 16
    wall.append((x, 0, w, 32))
    return pieces + [
        piece("wall", wall, 32, fill=16, foot=32, side=side),
        piece("side_w", [], 32, side=side, walls=[((0, h), (0, 32))]),
        piece("side_e", [], 32, side=side, walls=[((w, 32), (w, h))]),
    ]


# ── Rustboro's Pokemon school ─────────────────────────────────────────────
#
# One classroom. Its back wall is drawn from 8 rows down the first cell (the
# black over it is nothing) to its foot 36 rows down, the blackboard and the
# windows on its face; the pillars' feet and the teacher's step, drawn a few
# rows further, stay on the floor.

def school_room():
    side = (176, 8, 192, 36)
    return [
        piece("wall", [(0, 8, 192, 36)], 28, fill=16, foot=36, side=side),
        piece("side_w", [], 28, side=side, walls=[((0, 176), (0, 36))]),
        piece("side_e", [], 28, side=side, walls=[((192, 36), (192, 176))]),
    ]


# ── The Pretty Petal flower shop ──────────────────────────────────────────
#
# Route 104's shop: planters of flowers and racks of potted plants about the
# floor, a table of pots and a shelf along the back wall. The counter, the
# stools and the vases stay drawn on the floor.

SHOP_FLOOR = ("eef6ff", "d5d5e6", "b4acb4")
SHOP_WALL = ("bdbd94", "e6e68b", "ffffbd", "629c62", "9cd59c", "4a7b41")


def flower_shop_room():
    fl = SHOP_FLOOR
    side = (48, 0, 64, 32)

    def planter(name, x, y0, y1):
        return piece(name, [(x, y0, x + 16, y1)], 10, leave=fl, solid=True)

    def rack(name, x):
        # A low table of green slats on four legs, three potted plants in a
        # row down it. It was one box as tall as the plants: a crate with
        # plants painted on its lid. Now each pot stands, a card of its own
        # (the nearest first, as the drawing overlaps them), and the table's
        # front - its apron and legs, seven rows - stands at its foot; the
        # slats between stay drawn, the floor showing through them.
        slats = fl + ("9cd59c",)
        return [piece("%s_pot%d" % (name, k), [(x + 2, y0, x + 14, y1)], y1 - y0,
                      leave=slats, card=True)
                for k, (y0, y1) in ((3, (106, 120)), (2, (94, 109)), (1, (80, 97)))] + [
            piece(name, [(x, 121, x + 16, 128)], 7, leave=fl)]

    return [
        planter("planter_sw", 0, 112, 144),
        planter("planter_w", 80, 96, 128), planter("planter_c", 128, 96, 128),
        planter("planter_e1", 192, 80, 128), planter("planter_e2", 208, 80, 128),
        *rack("rack_1", 96), *rack("rack_2", 112), *rack("rack_e", 224),
        planter("planter_n1", 176, 48, 64), planter("planter_n2", 192, 48, 64),
        piece("shelf", [(112, 24, 152, 56)], 18, leave=SHOP_WALL + fl, back=42),
        piece("pots", [(162, 18, 209, 48)], 14, leave=SHOP_WALL + fl, back=32),
        # the counter down the west side: nine rows of front at its foot
        piece("counter", [(16, 47, 32, 96)], 9, leave=fl, solid=True),
        piece("wall", [(0, 0, 240, 32)], 32, fill=16, foot=32, side=side),
        piece("side_w", [], 32, side=side, walls=[((0, 144), (0, 32))]),
        piece("side_e", [], 32, side=side, walls=[((240, 32), (240, 144))]),
    ]


# ── Dewford's gym ─────────────────────────────────────────────────────────
#
# A maze cut in rock two cells tall: every blocked cell is rock, its top or
# the two rows of its face, so each column's run of blocked cells is a block
# drawn from the run's first row to its foot. Runs side by side with the same
# rows are one rectangle (cells: x0, y0, x1, y1), front first. The leader's
# alcove and the statues, blocked too, are not rock and stay flat.

DEWFORD_GYM_BLOCKS = [
    (0, 0, 1, 28), (1, 18, 2, 28), (2, 23, 3, 28), (3, 24, 4, 28), (8, 23, 12, 28),
    (13, 23, 16, 28), (16, 19, 17, 28), (17, 0, 18, 28), (3, 17, 6, 22), (6, 15, 8, 22),
    (9, 15, 10, 21), (10, 16, 11, 21), (12, 16, 13, 19), (13, 9, 14, 19), (8, 15, 9, 18),
    (14, 13, 16, 18), (3, 11, 5, 16), (1, 12, 2, 15), (5, 7, 6, 14), (6, 6, 7, 14),
    (10, 9, 12, 14), (7, 9, 9, 13), (14, 7, 16, 12), (1, 6, 2, 10), (3, 7, 5, 10),
    (16, 0, 17, 9), (13, 0, 15, 6), (7, 0, 10, 5), (12, 0, 13, 5), (11, 0, 12, 4),
    (2, 0, 3, 3), (5, 0, 6, 3), (10, 0, 11, 3), (15, 0, 16, 3),
    # found flat by the audit (devtools/voxel_audit.py): blocked rock no run
    # above had taken, and the front wall's ends either side of the door
    (7, 6, 12, 8), (2, 7, 3, 9), (2, 19, 3, 21), (13, 20, 16, 22),
    (4, 26, 5, 28), (7, 26, 8, 28), (12, 26, 13, 28),
    # (the rock behind the leader's place - x 1, 3-4 and 6, rows 0-2 - stays
    # flat: with it the layout's page is past the console's 512x512)
]
DEWFORD_GYM_GROUND = ("838362", "737352")       # the floor, and its shade
DEWFORD_GYM_FLOOR = [0x201, 0x202, 0x203, 0x205, 0x206, 0x209, 0x20A, 0x20B, 0x20D, 0x211,
                     0x212, 0x213, 0x215, 0x216, 0x218, 0x21A, 0x21B, 0x222, 0x223]


def dewford_gym():
    side = (128, 416, 144, 448)     # a stretch of the front wall's face
    # The rock the room is cut in, down its west and east edges, is a wall's
    # face each side and not a block: a block's art is its drawing three times
    # over (its hidden top and sides), and those two columns' would put the
    # layout's page past the console's 512x512.
    fl = DEWFORD_GYM_GROUND
    return only_here([
        # the two statues by the door, an orb on a plinth: a card each, kept
        # to this room (Rustboro's gym has its own, in two pieces)
        piece("statue_w", [(64, 368, 80, 400)], 31, leave=fl, card=True),
        piece("statue_e", [(112, 368, 128, 400)], 31, leave=fl, card=True),
        # the shelves either side of the leader, standing before the rock
        piece("shelf_w", [(17, 29, 32, 65)], 31, leave=fl, solid=True),
        piece("shelf_e", [(97, 29, 112, 65)], 31, leave=fl, solid=True),
    ], "statue_w", "statue_e") + [piece("block_%d" % i, [(x0 * 16, y0 * 16, x1 * 16, y1 * 16)], 32)
            for i, (x0, y0, x1, y1) in enumerate(DEWFORD_GYM_BLOCKS)
            if x0 not in (0, 17)] + [
        piece("edge_w", [], 32, side=side, walls=[((16, 448), (16, 32))]),
        piece("edge_e", [], 32, side=side, walls=[((272, 32), (272, 448))]),
    ]


# ── Professor Birch's lab ─────────────────────────────────────────────────
#
# Desks and a bookcase along the back wall, standing on its row of collision
# (so no deeper than the drawing puts them in front of it); in the room, the
# boxes, book stacks, bookcases and desks run back as far as the cells they
# block, and the machine is read column by column off its round drawing.

LAB_SHADOW = ("b4b4a4", "949494")      # the floor's shade, and its grid in it


def lab():
    sh = LAB_SHADOW
    return [
        piece("plant_s", [(48, 189, 64, 208)], 18, card=True),
        # the desk down the west side: its computer at the far end, the book
        # stacks against the wall, the chair
        # seen from behind: its back stands at the back of its seat
        piece("chair_sw_back", [(34, 160, 47, 167)], 7, base=4, leave=sh, solid=True),
        piece("chair_sw_seat", [(34, 167, 47, 176)], 4, leave=sh, solid=True),
        piece("books_sw1", [(1, 160, 16, 176)], 9, leave=sh, back=160),
        piece("books_sw2", [(1, 176, 16, 192)], 9, leave=sh, back=176),
        piece("pc_sw", [(16, 145, 32, 160)], 8, base=8, solid=True),
        piece("desk_sw", [(16, 160, 32, 192)], 8, leave=sh, back=160),
        # and its twin down the east side
        piece("plant_se", [(192, 141, 208, 161)], 18, card=True),
        piece("boxes_se", [(192, 164, 208, 192)], 20, leave=sh, back=176),
        piece("chair_se_back", [(161, 160, 165, 176)], 9, leave=sh, solid=True),
        piece("chair_se_seat", [(165, 164, 176, 176)], 5, leave=sh, solid=True),
        piece("pc_se", [(176, 145, 192, 160)], 8, base=8, solid=True),
        piece("desk_se", [(176, 160, 192, 192)], 8, leave=sh, back=160),
        # the machine, its dome, the two canisters beside it
        piece("dome", [("ellipse", 176, 103.5, 8.5, 7.5)], 5, base=10),
        piece("machine", [(160, 95, 192, 128)], 10, side=(168, 110, 184, 120)),
        piece("canisters", [(192, 109, 208, 128)], 16, leave=sh, back=112),
        # the two bookcases in the room, a box on each
        piece("box_w1", [(8, 82, 23, 96)], 6, base=21, solid=True),
        piece("box_w2", [(40, 82, 55, 96)], 6, base=21, solid=True),
        piece("bookcase_w1", [(0, 85, 32, 128)], 21, back=96),
        piece("bookcase_w2", [(32, 85, 64, 128)], 21, back=96),
        # boxes and book stacks in the north-east corner
        piece("boxes_ne1", [(144, 56, 160, 80)], 8, leave=sh),
        piece("boxes_ne2", [(160, 52, 176, 80)], 18, leave=sh, back=64),
        piece("books_ne1", [(177, 32, 193, 48)], 8, leave=sh, back=32),
        piece("books_ne2", [(193, 32, 208, 48)], 8, leave=sh, back=32),
        piece("books_ne3", [(193, 48, 208, 64)], 8, leave=sh, back=48),
        piece("chair_n_back", [(75, 48, 79, 64)], 9, leave=sh, solid=True),
        piece("chair_n_seat", [(64, 52, 75, 64)], 5, leave=sh, solid=True),
        piece("boxes_w", [(0, 41, 16, 64)], 7, leave=sh),
        # along the back wall
        piece("plant_nw", [(32, 29, 48, 48)], 18, card=True),
        piece("computer", [(49, 10, 72, 30)], 17, base=8, back=32),
        piece("desk_pc", [(48, 20, 80, 39)], 8, leave=sh, against=32),
        piece("book_red", [(117, 19, 128, 31)], 11, base=8, back=32),
        piece("book_open", [(134, 19, 147, 30)], 6, base=8, solid=True),
        piece("binder", [(147, 17, 158, 31)], 13, base=8, back=32),
        piece("desk_a", [(96, 20, 128, 39)], 8, leave=sh, against=32),
        piece("desk_b", [(128, 20, 160, 39)], 8, leave=sh, against=32),
        piece("bookcase_nw", [(0, 8, 32, 40)], 21, against=32),
        piece("wall", [(0, 0, 208, 32)], 32, fill=16, foot=32, side=(80, 0, 96, 32)),
        piece("side_w", [], 32, side=(80, 0, 96, 32), walls=[((0, 208), (0, 32))]),
        piece("side_e", [], 32, side=(80, 0, 96, 32), walls=[((208, 32), (208, 208))]),
    ]


# ── Rustboro's gym ────────────────────────────────────────────────────────
#
# A maze of low stone walls on a tiled floor: each block stands on the cells
# it blocks, its top drawn from 8 rows into the cell north of them and its
# front the last 10 rows of its own. The floor's shadows are floor. At the
# back, the gym's crenellated wall, one cell deeper at either end.

GYM_WALL_SIDE = (32, 7, 48, 32)
GYM_FLOOR = ("bdbdac",)             # the floor's shade round a statue's foot     # a stretch of the back wall without the emblem


def gym_block(name, rects):
    """A maze block: `rects` in cells (x0, y0, x1, y1), each drawn from 8 rows
    north of its cells to its foot."""
    return piece(name, [(x0 * 16, y0 * 16 - 8, x1 * 16, y1 * 16) for (x0, y0, x1, y1) in rects],
                 10, side=(56, 118, 72, 128))


def gym_statue(x):
    """A gym statue's outline, its cell's left edge at x: its pedestal's
    bottom corners are rounded off, the floor showing there."""
    return [(x, 272, x + 16, 302), (x + 1, 302, x + 15, 303), (x + 2, 303, x + 14, 304)]


def rustboro_gym():
    return [
        # the statues by the door: a ball on a pedestal. Every gym has them,
        # on its own floor: they stand in each as they are (reuse_pieces),
        # so they must not take the floor showing at their feet
        piece("statue_w_ball", [("ellipse", 40, 279, 7, 7)], 8, base=16),
        piece("statue_w", gym_statue(32), 16, back=288),
        piece("statue_e_ball", [("ellipse", 136, 279, 7, 7)], 8, base=16),
        piece("statue_e", gym_statue(128), 16, back=288),
        # the maze, front first
        gym_block("block_sw", [(2, 13, 4, 15), (2, 15, 5, 16)]),
        gym_block("block_s", [(6, 15, 8, 16)]),
        gym_block("block_w", [(4, 9, 5, 11), (2, 11, 5, 12)]),
        gym_block("block_c", [(6, 9, 8, 11)]),
        # the comb along the north and east, in three: a piece's art is its
        # whole rectangle, and one of 11 x 10 cells for this outline would
        # take a texture page of half a megabyte. Cut between columns, so no
        # column's run is split
        gym_block("block_e_arm", [(6, 12, 9, 13), (7, 13, 9, 14)]),
        gym_block("block_e", [(9, 6, 11, 16)]),
        gym_block("block_n", [(3, 6, 9, 8)]),
        gym_block("block_west", [(0, 6, 1, 16)]),
        # the back wall and its two deeper ends
        piece("wall_w", [(0, 0, 16, 48)], 25, fill=16, foot=48, side=GYM_WALL_SIDE),
        piece("wall_e", [(160, 0, 176, 48)], 25, fill=16, foot=48, side=GYM_WALL_SIDE),
        piece("wall", [(16, 0, 160, 32)], 25, fill=16, foot=32, side=GYM_WALL_SIDE),
        # the side walls in two each: one the room's length would need a
        # texture page too tall to share VRAM with the city's
        piece("side_w", [], 25, side=GYM_WALL_SIDE, walls=[((0, 176), (0, 48))]),
        piece("side_w2", [], 25, side=GYM_WALL_SIDE, walls=[((0, 320), (0, 176))]),
        piece("side_e", [], 25, side=GYM_WALL_SIDE, walls=[((176, 48), (176, 176))]),
        piece("side_e2", [], 25, side=GYM_WALL_SIDE, walls=[((176, 176), (176, 320))]),
    ]


SPECS = [
    {
        "name": "littleroot_house_w",
        "layout": "LAYOUT_LITTLEROOT_TOWN",
        "rect": (2, 4, 5, 5),
        "ground": [GRASS],
        "parts": lambda: littleroot_house(8),
        "exact": HOUSE_EXACT,
    },
    {
        "name": "littleroot_house_e",
        "layout": "LAYOUT_LITTLEROOT_TOWN",
        "rect": (13, 4, 5, 5),
        "ground": [GRASS],
        "parts": lambda: littleroot_house(64),
        "exact": HOUSE_EXACT,
    },
    {
        "name": "littleroot_lab",
        "layout": "LAYOUT_LITTLEROOT_TOWN",
        "rect": (3, 12, 7, 5),
        "ground": [GRASS],
        "parts": littleroot_lab,
        "exact": LAB_EXACT,
    },
    {
        # The canonical copy: Oldale paints its path into the top row.
        "name": "pokemon_center",
        "layout": "LAYOUT_PETALBURG_CITY",
        "rect": (19, 13, 4, 4),
        "match_rows": (1, 4),
        "ground": [GRASS],
        "parts": lambda: center_or_mart((9, 16), crown=True),
        "exact": CROWN_EXACT,
    },
    {
        # Oldale's copy has a tree's crown over its top-right corner.
        "name": "poke_mart",
        "layout": "LAYOUT_MAUVILLE_CITY",
        "rect": (22, 11, 4, 4),
        "match_rows": (1, 4),
        "ground": [GRASS],
        "parts": lambda: center_or_mart((12, 16)),
        "exact": CENTER_EXACT,
    },
    {
        "name": "oldale_house",
        "layout": "LAYOUT_OLDALE_TOWN",
        "rect": (4, 4, 4, 4),
        "ground": [GRASS],
        "parts": oldale_house,
        "exact": OLDALE_HOUSE_EXACT,
    },
    {
        "name": "briney_house",
        "layout": "LAYOUT_ROUTE104",
        "rect": (15, 47, 5, 4),
        "ground": [GRASS],
        "parts": briney_house,
        "exact": BRINEY_HOUSE_EXACT,
    },
    {
        "name": "flower_shop",
        "layout": "LAYOUT_ROUTE104",
        "rect": (3, 15, 6, 4),
        # the cobbled path round it
        "ground": [GRASS, 0x206, 0x207],
        "parts": flower_shop,
        "exact": FLOWER_SHOP_EXACT,
    },
    {
        "name": "kit_house_4",
        "layout": "LAYOUT_PETALBURG_CITY",
        "rect": (9, 16, 4, 4),
        "ground": [GRASS],
        "parts": lambda: kit_house(64),
        "exact": kit_house_exact(64),
    },
    {
        "name": "kit_house_5",
        "layout": "LAYOUT_PETALBURG_CITY",
        "rect": (5, 2, 5, 4),
        "ground": [GRASS],
        "parts": lambda: kit_house(80),
        "exact": kit_house_exact(80),
    },
    {
        # Dewford's blue-roofed houses: the same kit in another tileset's
        # colours, on sand. The reference is the one with open sand behind
        # it; the one under the trees, whose roof's back row is other tiles,
        # is found as a copy of it
        "name": "dewford_house_4",
        "layout": "LAYOUT_DEWFORD_TOWN",
        "rect": (16, 11, 4, 4),
        "ground": [0x124],
        "parts": lambda: kit_house(64),
        "exact": kit_house_exact(64),
    },
    {
        "name": "dewford_house_5",
        "layout": "LAYOUT_DEWFORD_TOWN",
        "rect": (1, 0, 5, 4),
        "ground": [0x124],
        "parts": lambda: kit_house(80),
        "exact": kit_house_exact(80),
    },
    {
        # Slateport's houses, under a purple roof: the same kit again
        "name": "slateport_house_4",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (20, 41, 4, 4),
        "ground": [GRASS],
        "parts": lambda: kit_house(64),
        "exact": kit_house_exact(64),
    },
    {
        "name": "slateport_house_6",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (24, 41, 6, 4),
        "ground": [GRASS],
        "parts": lambda: kit_house(96),
        "exact": kit_house_exact(96),
    },
    {
        # Slateport's large buildings, each a box under its own roof
        "name": "slateport_fan_club",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (25, 7, 7, 6),
        "ground": [GRASS],
        "parts": lambda: box_building(112, 96, 64),
        "exact": [(0, 0, 112, 96)],
    },
    {
        "name": "slateport_museum",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (28, 22, 6, 6),
        "ground": [GRASS],
        "parts": slateport_museum,
        "exact": [(0, 0, 96, 88, True)],
    },
    {
        "name": "slateport_harbor",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (24, 32, 8, 7),
        "ground": [GRASS],
        "parts": lambda: box_building(128, 112, 72),
        "exact": [(0, 0, 128, 112)],
    },
    {
        # the Battle Tent's dome: a drum under its roof, drawn round
        "name": "slateport_battle_tent",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (8, 8, 5, 5),
        "ground": [GRASS],
        # a dome: lifted off its drawing, round from every side
        "mound": {"rise": 0.9, "step": 4},
        "exact": [(0, 0, 80, 80)],
    },
    {
        "name": "slateport_shipyard",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (2, 22, 5, 5),
        "ground": [GRASS],
        "parts": lambda: box_building(80, 80, 52, top=8, side_x=36),
        "exact": [(0, 0, 80, 80, True)],
    },
    # The market's stalls: a canopy on four posts. The canopy is the box's
    # lid and its front the posts, the paving between them left clear, so
    # whoever stands under it is seen. They lay painted on the paving, which
    # nobody is blocked by and the audit does not see.
    {
        "name": "slateport_stall_0",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (2, 41, 5, 3),
        "ground": [0x211, 0x285, 0x210, 0x212, 0x209],
        "parts": lambda: market_stall(80),
        "exact": [],
    },
    {
        "name": "slateport_stall_1",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (2, 45, 5, 3),
        "ground": [0x211, 0x285, 0x210, 0x212, 0x209],
        "parts": lambda: market_stall(80),
        "exact": [],
    },
    {
        "name": "slateport_stall_2",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (2, 49, 5, 3),
        "ground": [0x211, 0x285, 0x210, 0x212, 0x209],
        "parts": lambda: market_stall(80),
        "exact": [],
    },
    {
        "name": "slateport_stall_3",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (10, 41, 4, 3),
        "ground": [0x211, 0x285, 0x210, 0x212, 0x209],
        "parts": lambda: market_stall(64),
        "exact": [],
    },
    {
        "name": "slateport_stall_4",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (10, 45, 4, 3),
        "ground": [0x211, 0x285, 0x210, 0x212, 0x209],
        "parts": lambda: market_stall(64),
        "exact": [],
    },
    {
        "name": "slateport_stall_5",
        "layout": "LAYOUT_SLATEPORT_CITY",
        "rect": (10, 49, 4, 3),
        "ground": [0x211, 0x285, 0x210, 0x212, 0x209],
        "parts": lambda: market_stall(64),
        "exact": [],
    },
    {
        # read column by column, as a hedge is: its outline is not a box's
        "name": "slateport_lighthouse",
        "components": {
            "primary": "gTileset_General",
            "layouts": ["LAYOUT_SLATEPORT_CITY"],
            "tiles": {0x246, 0x247, 0x24E, 0x24F, 0x256, 0x257, 0x25E, 0x25F},
            "height": 32,
        },
        "ground": [GRASS],
    },
    {
        # the fence where it runs north and south, and its corners
        "name": "slateport_posts",
        "components": {
            "primary": "gTileset_General",
            "layouts": ["LAYOUT_SLATEPORT_CITY"],
            "tiles": {0x133, 0x139, 0x13A, 0x140, 0x141, 0x142, 0x148, 0x14A},
            "height": 10, "block": 2,
        },
        "ground": [GRASS],
    },
    {
        # the quay's white kerbs and steps
        "name": "slateport_quay",
        "components": {
            "primary": "gTileset_General",
            "layouts": ["LAYOUT_SLATEPORT_CITY"],
            "tiles": {0x04E, 0x045, 0x047, 0x234, 0x23C, 0x245, 0x24D, 0x255, 0x25D, 0x2B8, 0x2B9, 0x2BA, 0x2FE, 0x2FF, 0x27E, 0x2BB},
            "height": 6, "block": 2,
        },
        "ground": [GRASS],
    },
    {
        # the market's crates, which are boxes (its jars, bowls and flowers are cards)
        "name": "slateport_market",
        "components": {
            "primary": "gTileset_General",
            "layouts": ["LAYOUT_SLATEPORT_CITY"],
            "tiles": {0x32E, 0x32F, 0x336, 0x337, 0x33E, 0x33F},
            "height": 10, "block": 1,
        },
        "ground": [GRASS],
    },
    {
        "name": "gym",
        "layout": "LAYOUT_PETALBURG_CITY",
        "rect": (12, 4, 6, 5),
        # the bottom row is porch and the town's own ground
        "match_rows": (0, 4),
        "ground": [GRASS],
        "parts": gym,
        "exact": GYM_EXACT,
    },
    {
        # Dewford's gym: the same building under an orange roof, on sand.
        "name": "gym_dewford",
        "layout": "LAYOUT_DEWFORD_TOWN",
        "rect": (5, 13, 6, 5),
        "match_rows": (0, 4),
        "ground": [0x124],
        "parts": gym,
        "exact": GYM_EXACT,
    },
    {
        # Petalburg's hedges. Not a building: a run of metatiles of any shape,
        # so each connected run becomes its own model, read column by column
        # off its drawing. The front, where a run ends to the south, is
        # drawn 11 rows tall.
        "name": "hedge",
        "components": {
            "secondary": "gTileset_Petalburg",
            "tiles": {0x23c, 0x23d, 0x23e, 0x244, 0x245, 0x246, 0x24c, 0x24d, 0x24e,
                      0x254, 0x255, 0x256, 0x264, 0x265, 0x266,
                      # the rounded ends either side of the gym (found by the audit)
                      0x23f},
            "height": 11,
        },
        "ground": [GRASS],
    },
    {
        # The General tileset's picket fence, wherever it has been looked at:
        # a run of posts and rails, ten rows tall at its foot.
        "name": "fence",
        "components": {
            "primary": "gTileset_General",
            "layouts": ["LAYOUT_ROUTE104", "LAYOUT_PETALBURG_WOODS", "LAYOUT_SLATEPORT_CITY",
                        "LAYOUT_ROUTE110"],
            "tiles": {0x149},
            "height": 10, "block": 4,
        },
        "ground": [GRASS],
    },
    {
        # The seed beds beside Petalburg's house: low boxes of earth.
        "name": "seedbed",
        "components": {
            "primary": "gTileset_General",
            "layouts": ["LAYOUT_PETALBURG_CITY"],
            "tiles": {0x007},
            "height": 4,
        },
        "ground": [GRASS],
    },
    {
        # Rustboro's stone blocks, any width and any number of storeys: every
        # one in the map is found by its corners and modelled from its own art.
        "name": "rustboro_stone",
        "kit": {"layout": "LAYOUT_RUSTBORO_CITY", "corner": 0x224, "top": {0x225},
                "end": {0x226}, "foot": 0x21c},
        "ground": [0x2BB, 0x2C3, GRASS],
        "parts": stone_block,
        "exact": lambda w, h, meta: flat_block_exact(w, h, 7),
    },
    {
        "name": "rustboro_olive",
        "kit": {"layout": "LAYOUT_RUSTBORO_CITY", "corner": 0x220, "top": {0x221, 0x222},
                "end": {0x223, 0x23F}, "foot": 0x240},
        "ground": [0x2BB, 0x2C3, GRASS],
        "parts": olive_block,
        "exact": lambda w, h, meta: flat_block_exact(w, h, 8),
    },
    {
        # The gym again: Rustboro's copy has its own roof and flanks.
        "name": "gym_rustboro",
        "layout": "LAYOUT_RUSTBORO_CITY",
        "rect": (24, 15, 6, 5),
        "ground": [0x2BB, 0x2C3, GRASS],
        "parts": gym,
        "exact": GYM_EXACT,
    },
    {
        # Rustboro's iron railings, read column by column like the hedges: a
        # railing along a row is all front, one down a column is a line on top
        # with its front where it ends. The bars keep their gaps (alpha).
        "name": "railing",
        "components": {
            "secondary": "gTileset_Rustboro",
            "tiles": {0x2A7, 0x2FC, 0x318, 0x319, 0x31A, 0x315, 0x31D, 0x320, 0x321,
                      0x32C, 0x32D, 0x2BE, 0x2BF, 0x2CD, 0x352, 0x2E9,
                      # the same railings over grass or a building's shade
                      0x2B7, 0x2C6, 0x2C7, 0x2D5, 0x2D7, 0x2DC, 0x2DE, 0x2DF,
                      0x2E6, 0x2E7, 0x2EC, 0x31B,
                      # along the city's south edge, over the tops of the
                      # trees beyond it (found by the audit)
                      0x337, 0x33E, 0x33F},
            "height": 12, "hull": 12, "bridge": 3, "block": 4,
            # drawn whole on the upper layer; the bottom one is the ground
            # with its grass edges, which the map paints under it
            "upper": True,
            # a railing down a column shows its bars on its sides: those of
            # the railing along a row
            "flank": 0x2A7,
        },
        "ground": [0x2BB, 0x2C3, GRASS],
    },
    {
        # The grey rock in the sea, found by its four tiles wherever they are
        # drawn (voxel_props.py): over the water round it, by a sandbank, by
        # a shore. A low dome, as deep as it is drawn tall below its crest.
        # The water round it stays the map's own, animated.
        "name": "sea_rock",
        "props": "sea_rock",
        "ground": [0x170],
        "rise": 1.0,
        "step": 2,
        # its foam on the water
        "ring": [(222, 230, 238)],
    },
    {
        # A boulder on the sand or the grass, a cell across (Route 106's beach,
        # Route 111's desert, the Safari Zone).
        "name": "sand_boulder",
        "props": "sand_boulder",
        "ground": [0x124],
        "rise": 1.0,
        "step": 2,
    },
    {
        # The brown stack in the sea: a peak, taller than it is deep.
        "name": "sea_stack",
        "props": "sea_stack",
        "ground": [0x170],
        "rise": 1.6,
        "step": 4,
        # its grey shadow on the water
        "ring": [(131, 131, 139)],
    },
    {
        "name": "devon_corporation",
        "layout": "LAYOUT_RUSTBORO_CITY",
        "rect": (7, 7, 10, 9),
        "ground": [0x2BB, 0x2C3, GRASS],
        "parts": devon,
        "exact": DEVON_EXACT,
    },
    {
        "name": "rustboro_fountain",
        "layout": "LAYOUT_RUSTBORO_CITY",
        "rect": (27, 38, 3, 3),
        "ground": [0x2BB, 0x2C3, GRASS],
        "parts": fountain,
        "exact": [(0, 0, 48, 48)],
    },
    {
        # Every town's Pokemon Center has this one ground floor.
        "name": "pc1f",
        "interior": {"layout": "LAYOUT_POKEMON_CENTER_1F", "ground": [0x202],
                     "pieces": POKEMON_CENTER_1F, "open": CENTER_1F_OPEN},
    },
    {
        "name": "pc2f",
        "interior": {"layout": "LAYOUT_POKEMON_CENTER_2F", "ground": [0x202],
                     "pieces": POKEMON_CENTER_2F, "open": CENTER_2F_OPEN},
    },
    {
        # Every Poke Mart but the department store has this one room.
        "name": "mart",
        "interior": {"layout": "LAYOUT_MART", "ground": [0x201], "pieces": MART,
                     "open": MART_OPEN,
                     "shade": [0x202, 0x204, 0x206, 0x208, 0x20A]},
    },
    {
        "name": "brendan_1f",
        "interior": {"layout": "LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F", "ground": [0x201],
                     "pieces": brendan_1f()},
    },
    {
        "name": "brendan_2f",
        "interior": {"layout": "LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F", "ground": [0x201],
                     "pieces": brendan_2f()},
    },
    {
        "name": "may_1f",
        "interior": {"layout": "LAYOUT_LITTLEROOT_TOWN_MAYS_HOUSE_1F", "ground": [0x201],
                     "pieces": may_1f()},
    },
    {
        "name": "may_2f",
        "interior": {"layout": "LAYOUT_LITTLEROOT_TOWN_MAYS_HOUSE_2F", "ground": [0x201],
                     "pieces": may_2f()},
    },
    {
        "name": "lab",
        "interior": {"layout": "LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", "ground": [0x202],
                     "pieces": lab()},
    },
    {
        # after the starter: the boxes by the machine give way to a table.
        # The rest of the furniture is the lab's, tile for tile, and stands
        # here as it is, its back wall too; the side walls are its own.
        "name": "lab_table",
        "interior": {"layout": "LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB_WITH_TABLE",
                     "ground": [0x202],
                     "pieces": [piece("table", [(128, 64, 176, 89)], 8, leave=LAB_SHADOW,
                                      solid=True)]
                     + [pc for pc in lab() if pc["name"] in ("side_w", "side_e")]},
    },
    {
        "name": "lavaridge_pc1f",
        "interior": {"layout": "LAYOUT_LAVARIDGE_TOWN_POKEMON_CENTER_1F", "ground": [0x202],
                     "pieces": LAVARIDGE_CENTER_1F, "open": CENTER_1F_OPEN},
    },
    {
        # Oldale's first house, and eight more maps'
        "name": "house1",
        "interior": {"layout": "LAYOUT_HOUSE1", "ground": [0x223], "pieces": house1()},
    },
    {
        # Oldale's second house, and eleven more maps'
        "name": "house2",
        "interior": {"layout": "LAYOUT_HOUSE2", "ground": [0x223], "pieces": house2()},
    },
    {
        # Petalburg's second house, and two more maps'
        "name": "house_with_bed",
        "interior": {"layout": "LAYOUT_HOUSE_WITH_BED", "ground": [0x223], "pieces": own_shell(house_with_bed())},
    },
] + [
    {
        "name": layout[len("LAYOUT_"):].lower(),
        "interior": {"layout": layout, "ground": [ground],
                     "pieces": own_shell(PLAIN_FURNITURE.get(layout, list)()
                                         + plain_room(width, height, plain_x, sides))},
    }
    for layout, width, height, ground, plain_x, sides in PLAIN_ROOMS
] + [
    {
        # Mr. Briney's house, by the dock on Route 104
        "name": "briney_room",
        "interior": {"layout": "LAYOUT_ROUTE104_MR_BRINEYS_HOUSE", "ground": [0x229],
                     "pieces": own_shell(briney_room())},
    },
] + [
    {
        "name": layout[len("LAYOUT_"):].lower(),
        "interior": {"layout": layout, "ground": [ground],
                     "pieces": own_shell(stair_room(width, height, plain_x, doors, *extra))},
    }
    for layout, width, height, ground, plain_x, doors, *extra in STAIR_ROOMS
] + [
    {
        # Rustboro's Pokemon school
        "name": "school_room",
        "interior": {"layout": "LAYOUT_RUSTBORO_CITY_POKEMON_SCHOOL", "ground": [0x201],
                     "pieces": own_shell(school_room())},
    },
    {
        # The Pretty Petal flower shop on Route 104
        "name": "flower_shop_room",
        "interior": {"layout": "LAYOUT_ROUTE104_PRETTY_PETAL_FLOWER_SHOP", "ground": [0x201],
                     "pieces": own_shell(flower_shop_room())},
    },
    {
        # Dewford's gym: Brawly's maze
        "name": "dewford_gym",
        "interior": {"layout": "LAYOUT_DEWFORD_TOWN_GYM", "ground": [0x210],
                     "shade": DEWFORD_GYM_FLOOR, "pieces": own_shell(dewford_gym())},
    },
    {
        # Petalburg's gym: Norman's rooms
        "name": "petalburg_gym",
        "interior": {"layout": "LAYOUT_PETALBURG_CITY_GYM", "ground": [0x22B, 0x201],
                     "shade": [0x209, 0x212, 0x213, 0x214, 0x22A, 0x232,
                               0x216, 0x22C],
                     "pieces": own_shell(petalburg_gym())},
    },
    {
        # Rustboro's gym: Roxanne's maze
        "name": "rustboro_gym",
        "interior": {"layout": "LAYOUT_RUSTBORO_CITY_GYM", "ground": [0x201],
                     "shade": [0x202, 0x203, 0x204, 0x216, 0x22f, 0x237],
                     "pieces": rustboro_gym()},
    },
]


# ── Furniture the audit found flat ────────────────────────────────────────
#
# Rooms whose walls stood and whose tables and desks were painted on the
# floor (devtools/voxel_audit.py), measured on the drawing
# (devtools/voxel_measure.py): each a box read off its own pixels - its top,
# and `height` rows of front at its foot - on the room's floor. They are
# put in front of the room's own pieces. One written here is found again
# wherever its cells are drawn (the same table in the next flat), unless it
# is kept to its room (`alone`: the school's desks, each with its own book).

def _box(name, rect, height, floor, alone=False, card=False):
    pc = piece(name, [rect], height, leave=floor, solid=not card, card=card)
    if alone:
        pc["alone"] = True
    return pc


_FLAT = ("8b8b8b", "b4b4a4", "d5d5b4", "ded552", "f6f6a4", "ffcd8b")
_SCHOOL = ("c5c5bd", "dedede")
_DEVON = ("bd6252", "cd837b", "deaca4")
_MUSEUM = ("006a73", "208b94", "4aa4a4", "7bbdb4", "a4d5c5")

def shipyard_1f():
    """Stern's shipyard, ground floor: the wall that parts the office from
    the workshop (its white top, a pillar's face where it ends at the door
    and again south of it), the three girders of the gantry, and the stacks
    of red beams."""
    shop = ("6a7b41", "839473", "acb494", "dedec5")
    return only_here([
        piece("partition_n", [(97, 0, 112, 146)], 32, solid=True),
        piece("partition_s", [(97, 170, 112, 240)], 32, solid=True),
        piece("girder_a", [(113, 65, 132, 112)], 40, leave=shop, solid=True),
        piece("girder_b", [(161, 145, 175, 208)], 56, leave=shop, solid=True),
        piece("girder_c", [(225, 161, 239, 208)], 40, leave=shop, solid=True),
        piece("beams_e", [(305, 49, 335, 111)], 6, leave=shop, solid=True),
        piece("beams_se", [(289, 161, 335, 223)], 6, leave=shop, solid=True),
        piece("beams_sw", [(113, 176, 170, 239)], 6, leave=shop, solid=True),
        # the Facility tileset's furniture, as in the ship's captain's office
        piece("chart_table", [(64, 97, 96, 127)], 8, leave=SHIPYARD_FLOOR, solid=True),
        piece("consoles", [(128, 12, 160, 38)], 20, leave=SHIPYARD_WALL + shop, back=32),
        piece("shelf", [(0, 32, 32, 44)], 8, leave=SHIPYARD_WALL + SHIPYARD_FLOOR, solid=True),
        piece("locker", [(161, 17, 175, 39)], 15, leave=SHIPYARD_WALL + shop, back=32),
        # the dry dock: the submarine, nose out of its bay; the bay's dome;
        # the low white cradle round them; the tank and its console; and,
        # behind them all, the dock's wall under its white top, ended by a
        # pillar
        # (rounded across their width and still their drawing - a piece's
        # `arch`, vb.Arch: the bay a housing twenty-one rows tall at its sides
        # and thirty-two in the middle, its roof level, in front of the
        # dock's wall (any lower and its back would be behind it); the
        # submarine's nose a cylinder's end as tall, its top climbing to it
        # from the bay. As boxes they were flat-topped; made by hand as a
        # vault and a drum they went through the wall and lost the drawing.)
        # The dry dock - the housing against its wall, the drum out of it,
        # the cradle, the dock's wall and pillar - is left as it is drawn,
        # flat (the user's call, 2026-10-08). It is a long machine drawn
        # foreshortened into a few rows against a wall: stood up as boxes, a
        # hood in two steps, domes, a hand-made vault and drum (through the
        # wall, larger than drawn), then arches with one part or the other
        # the taller, it never read as the machine it is, and distorted is
        # worse than flat. vb.Arch, vb.Barrel, vb.Drum and a piece's `dome`,
        # `arch` and `made` stay for things they do suit.
        piece("tank", [(145, 74, 176, 120)], 30, leave=shop, solid=True),
    ], "tank", "partition_n", "partition_s", "girder_a", "girder_b", "girder_c", "beams_e", "beams_se", "beams_sw")


SHIPYARD_FLOOR = ("62627b", "628b83", "739c8b", "8bb4ac", "9c8b94", "a4cdbd")
SHIPYARD_WALL = ("6a7b7b", "8b94a4", "a4acde")


def office_furniture(layout_id):
    """An office of the Facility tileset, read off its layout: every desk (a
    cell of 248, or 249 with its computer, and the cell east of it; its top
    is drawn eight rows up the cell above), every stool (21D) and every bin
    (205). Each is a piece of its own, so none is looked for elsewhere."""
    import voxel_building as vb
    lay = vb.LayoutArt(layout_id)
    fl, out = SHIPYARD_FLOOR, []
    for y in range(lay.h):
        for x in range(lay.w):
            m, X, Y = lay.metatile(x, y), x * 16, y * 16
            if m in (0x248, 0x249):
                out.append(piece("desk_%d_%d" % (x, y), [(X, Y - 8, X + 32, Y + 16)], 10, leave=fl, solid=True))
            elif m == 0x21D:
                out.append(piece("stool_%d_%d" % (x, y), [(X + 2, Y + 1, X + 14, Y + 15)], 3, leave=fl, solid=True))
            elif m == 0x205:
                out.append(piece("bin_%d_%d" % (x, y), [(X + 2, Y, X + 14, Y + 16)], 8, leave=fl, solid=True))
    for pc in out:
        pc["alone"] = True
    return out


def tent_counter():
    """A Battle Tent's lobby: the counter, a U open towards the door - two
    arms with a hook at their back ends and a front each side of the way
    through - eight rows tall. (The record machine by the east drape stays flat: its
    outline is no box's.)"""
    fl = ("b4acf6", "cdd5ff", "ffffff", "9c94e6", "a49cee", "c5bdff")
    box = lambda name, r: piece(name, [r], 8, leave=fl, solid=True)
    return [
        box("counter_w_arm", (33, 32, 48, 96)), box("counter_w_hook", (48, 32, 63, 48)),
        box("counter_w_front", (48, 77, 95, 96)),
        box("counter_e_arm", (160, 32, 175, 96)), box("counter_e_hook", (145, 32, 160, 48)),
        box("counter_e_front", (113, 77, 160, 96)),
        piece("recorder", [(176, 55, 200, 98)], 42, leave=fl, card=True),
    ]


def harbor_quay():
    """A harbour's hall: the railing round the basin - north, west and south
    of it, open at the steps - as a low wall, and the stools."""
    fl = ("62627b", "628b83", "739c8b", "8bb4ac", "9c8b94", "a4cdbd", "29418b", "39529c", "526ad5",
          "6a83d5")
    bay = ("6a7b41", "839473", "acb494", "dedec5")
    rail = lambda name, r: piece(name, [r], 8, leave=fl + bay, solid=True)
    return [
        rail("rail_n", (56, 63, 384, 80)),
        rail("rail_w", (48, 80, 56, 176)),
        rail("rail_sw", (56, 160, 117, 176)), rail("rail_s", (152, 160, 284, 176)),
        # the loading bay east of the hall: its railing, and the crates - a
        # stack against the quay with one more behind it, and a stack by the
        # east wall - their slatted lids over a dark front
        rail("rail_se", (320, 160, 384, 176)), rail("rail_e", (272, 176, 280, 240)),
        piece("crates_n", [(288, 160, 320, 176), (288, 176, 352, 207)], 15, leave=fl + bay, solid=True),
        piece("crates_e", [(352, 192, 384, 240)], 16, leave=fl + bay, solid=True),
    ] + office_furniture("LAYOUT_HARBOR")


EXTRA_PIECES = {
    "LAYOUT_BATTLE_TENT_LOBBY": tent_counter,
    "LAYOUT_HARBOR": harbor_quay,
    "LAYOUT_SLATEPORT_CITY_STERNS_SHIPYARD_1F": lambda: (
        shipyard_1f() + office_furniture("LAYOUT_SLATEPORT_CITY_STERNS_SHIPYARD_1F")),
    "LAYOUT_SLATEPORT_CITY_STERNS_SHIPYARD_2F": lambda: office_furniture(
        "LAYOUT_SLATEPORT_CITY_STERNS_SHIPYARD_2F"),
    # Rustboro's flats and houses: their tables
    "LAYOUT_RUSTBORO_CITY_FLAT1_1F": lambda: [_box("table_a", (16, 64, 46, 96), 10, _FLAT)],
    "LAYOUT_RUSTBORO_CITY_FLAT1_2F": lambda: [_box("stand", (140, 80, 164, 108), 12, _FLAT)],
    "LAYOUT_RUSTBORO_CITY_CUTTERS_HOUSE": lambda: [_box("table_b", (128, 65, 160, 96), 10, _FLAT)],
    "LAYOUT_RUSTBORO_CITY_HOUSE1": lambda: [_box("table_c", (48, 64, 96, 96), 10, _FLAT)],
    "LAYOUT_RUSTBORO_CITY_HOUSE": lambda: [_box("table_d", (82, 64, 110, 96), 10, _FLAT, alone=True)],
    # the school: the teacher's desk and twelve pupils'
    "LAYOUT_RUSTBORO_CITY_POKEMON_SCHOOL": lambda: (
        [_box("teachers_desk", (80, 58, 112, 79), 9, _SCHOOL, alone=True)]
        + [_box("desk_%d_%d" % (x, y), (x, y, x + 16, y + 16), 8, _SCHOOL, alone=True)
           for y in (80, 112, 144) for x in (16, 48, 128, 160)]),
    # Devon: the researchers' desks and the drawing board; the president's
    # tables and the two glass cases
    "LAYOUT_RUSTBORO_CITY_DEVON_CORP_2F": lambda: [
        _box("board", (35, 64, 64, 95), 12, _DEVON, alone=True),
        _box("bin_w", (16, 64, 34, 80), 16, _DEVON, alone=True, card=True),
        _box("bin_e", (112, 80, 128, 96), 16, _DEVON, alone=True, card=True),
        _box("desk", (160, 56, 192, 80), 10, _DEVON, alone=True)] + [
        # a desk is found again in other rooms, not in its own: each is written
        _box("desk_%d_%d" % (x, y), (x, y, x + 32, y + 24), 10, _DEVON, alone=True)
        for (x, y) in ((96, 56), (224, 56), (96, 104), (160, 104), (224, 104))],
    # Slateport's Oceanic Museum: the pillars, the glass cases, the two
    # counters shaped like a U (a box read column by column: its bar ends at
    # the bar's foot, its arms at theirs), the model tables upstairs
    "LAYOUT_SLATEPORT_CITY_OCEANIC_MUSEUM_1F": lambda: [
        _box("counter_w", (80, 94, 152, 144), 10, _MUSEUM, alone=True),
        _box("counter_e", (168, 94, 240, 144), 10, _MUSEUM, alone=True),
        _box("pillar_n", (32, 48, 48, 80), 22, _MUSEUM, alone=True),
        _box("pillar_s", (32, 96, 48, 128), 22, _MUSEUM, alone=True),
        _box("case_1", (240, 53, 256, 80), 18, _MUSEUM, alone=True),
        _box("case_2", (288, 53, 304, 80), 18, _MUSEUM, alone=True),
        _box("case_3", (288, 101, 304, 128), 18, _MUSEUM, alone=True)],
    "LAYOUT_SLATEPORT_CITY_OCEANIC_MUSEUM_2F": lambda: [
        _box("table_n", (32, 46, 96, 80), 12, _MUSEUM, alone=True),
        _box("table_s", (32, 94, 96, 128), 12, _MUSEUM, alone=True),
        _box("stand_1", (192, 56, 216, 80), 14, _MUSEUM, alone=True),
        _box("stand_2", (240, 56, 264, 80), 14, _MUSEUM, alone=True),
        _box("stand_3", (208, 105, 240, 128), 12, _MUSEUM, alone=True),
        _box("pillar_n", (288, 48, 304, 80), 22, _MUSEUM, alone=True),
        _box("pillar_s", (288, 96, 304, 128), 22, _MUSEUM, alone=True)],
    "LAYOUT_SLATEPORT_CITY_POKEMON_FAN_CLUB": lambda: [
        _box("table", (81, 98, 143, 128), 12, ("cd6a6a", "ded58b", "ee836a", "f6eeb4"), alone=True)],
    "LAYOUT_RUSTBORO_CITY_DEVON_CORP_3F": lambda: [
        _box("table", (112, 61, 192, 112), 12, _DEVON, alone=True),
        _box("side_table", (240, 61, 272, 112), 12, _DEVON, alone=True),
        _box("case_n", (16, 67, 32, 96), 20, _DEVON, alone=True),
        _box("case_s", (16, 99, 32, 128), 20, _DEVON, alone=True)],
}

# ── Devon's ground floor ──────────────────────────────────────────────────
#
# A hall under a wall two cells tall, with two alcoves set back in it: the
# reception's, with its two glass cases, and the stairs'. Three stretches of
# the front wall at Z 80, the alcoves' own back walls at Z 32 and their
# sides between, edge on to the GBA's camera and drawn nowhere. The room had
# no model at all: every wall of it lay on the floor.

def devon_1f():
    side = (80, 0, 96, 32)          # a stretch of the reception's bare wall
    seen = _DEVON + ("ac5a4a", "bd736a")
    d = 224                          # the stairs' doorway
    return [
        _box("case_w", (48, 24, 64, 47), 14, seen, alone=True),
        _box("case_e", (128, 24, 144, 47), 14, seen, alone=True),
        stairwell("stairwell_14", d, d + 16, 32, 13, 19, (d + 1, 14, d + 15, 26), 0),
        piece("wall_reception", [(48, 0, 144, 32)], 32, fill=16, foot=32, side=side,
              walls=[((48, 80), (48, 32)), ((144, 32), (144, 80))]),
        piece("wall_stairs", [(208, 0, d, 32), (d, 0, d + 16, 13), (d + 16, 0, 256, 32)], 32,
              fill=16, foot=32, side=side,
              walls=[((208, 80), (208, 32)), ((256, 32), (256, 80))]),
        piece("wall_west", [(0, 48, 48, 80)], 32, fill=16, foot=80, side=side,
              walls=[((0, 144), (0, 80))]),
        piece("wall_mid", [(144, 48, 208, 80)], 32, fill=16, foot=80, side=side),
        piece("wall_east", [(256, 48, 304, 80)], 32, fill=16, foot=80, side=side,
              walls=[((304, 80), (304, 144))]),
    ]


SPECS.append({
    "name": "devon_1f",
    "interior": {"layout": "LAYOUT_RUSTBORO_CITY_DEVON_CORP_1F", "ground": [0x380],
                 "shade": [0x381, 0x383, 0x384, 0x385, 0x386, 0x387, 0x38D],
                 "pieces": own_shell(devon_1f())},
})

# ── Slateport's rooms that had no model ───────────────────────────────────

def fan_club():
    """The Pokemon Fan Club: a wall two cells tall under a row of black, its
    foot 40 rows down, bookcases and plants drawn on it."""
    side = (96, 8, 112, 40)
    return [
        piece("wall", [(0, 8, 224, 40)], 32, fill=16, foot=40, side=side),
        piece("side_w", [], 32, side=side, walls=[((0, 176), (0, 40))]),
        piece("side_e", [], 32, side=side, walls=[((224, 40), (224, 176))]),
    ]


def battle_tent_lobby():
    """A Battle Tent's lobby: the tent's back, two cells tall, between the
    drapes drawn down its sides, which stay as they are drawn."""
    return [piece("wall", [(32, 0, 176, 32)], 32, fill=16, foot=32, side=(48, 0, 64, 32))]


def harbor():
    """A harbour's hall: its wall four cells tall along the quay, windows on
    its face, and the two sides the drawing has no pixel of."""
    side = (0, 0, 16, 64)
    return [
        piece("wall", [(0, 0, 384, 64)], 64, fill=16, foot=64, side=side),
        piece("side_w", [], 64, side=side, walls=[((0, 240), (0, 64))]),
        piece("side_e", [], 64, side=side, walls=[((384, 64), (384, 240))]),
    ]


SPECS += [
    {"name": "harbor",
     "interior": {"layout": "LAYOUT_HARBOR", "ground": [0x202],
                  "shade": [0x203, 0x204], "pieces": own_shell(harbor())}},
    {"name": "fan_club",
     "interior": {"layout": "LAYOUT_SLATEPORT_CITY_POKEMON_FAN_CLUB", "ground": [0x201],
                  "shade": [0x202, 0x204], "pieces": own_shell(fan_club())}},
    {"name": "battle_tent_lobby",
     "interior": {"layout": "LAYOUT_BATTLE_TENT_LOBBY", "ground": [0x210],
                  "shade": [0x211, 0x209, 0x208], "pieces": own_shell(battle_tent_lobby())}},
]

# The market's two orange awnings, over its gate and over the path north of
# the Battle Tent: the stall's canopy with a scalloped edge eight rows deep,
# hung high enough to walk under.
SPECS += [
    {"name": "slateport_awning_%s" % name,
     "layout": "LAYOUT_SLATEPORT_CITY",
     "rect": (x, y, 5, 3),
     "ground": ground,
     "parts": lambda: market_stall(80, lid=(1, 24), rim=(24, 32), depth=23, high=32),
     "exact": []}
    for (name, x, y, ground) in (("gate", 8, 30, [0x211, 0x285, 0x210, 0x212, 0x209]),
                                 ("north", 16, 7, [GRASS]))]

SPECS += [
    {"name": "slateport_card_%03x" % tile,
     "layout": "LAYOUT_SLATEPORT_CITY",
     "rect": (x, y, 1, 1),
     "ground": [0x211],
     "clear": SLATEPORT_PAVING,
     "card": True,
     "exact": []}
    for (tile, x, y) in SLATEPORT_CARDS]

# The round bushes at the Battle Tent's sides: a dome each, lifted off its
# own drawing as the tent is, and nothing of the lawn round it. As a low box
# it was a square of grass with a bush painted on its lid.
SPECS += [
    {"name": "slateport_bush",
     "layout": "LAYOUT_SLATEPORT_CITY",
     "rect": (7, 10, 1, 1),
     "ground": [GRASS],
     "clear": GRASS_COLOURS,
     "mound": {"rise": 0.9, "step": 2},
     "exact": [(0, 0, 16, 16)]}]

# ── Route 109's beach ─────────────────────────────────────────────────────
#
# The Seashore House is the towns' house kit, five cells wide, on the sand.
# The parasols are two cells by three: a canopy 29 rows across the middle of
# which its pole comes down eight rows to the sand, over a round shadow. The
# canopy is a dome held on the pole (a spec's `parasol`), 22 rows up - where
# a disc as wide as it is drawn, seen from the GBA's 45 degrees, shows that
# much pole under its front rim - and the shadow stays on the sand. The sun
# loungers and the air beds are low: a bed five rows off the sand.
SAND = 0x124
SPECS += [
    {"name": "route109_seashore_house",
     "layout": "LAYOUT_ROUTE109",
     "rect": (10, 2, 5, 4),
     "ground": [SAND],
     "parts": lambda: kit_house(80),
     "exact": kit_house_exact(80)},
] + [
    {"name": "beach_parasol_%s" % name,
     "layout": "LAYOUT_ROUTE109",
     "rect": (x, y, 2, 3),
     "ground": [SAND],
     # the sand's three colours: its grain is drawn differently under a parasol
     "clear": ("decd83", "d5b46a", "eee6a4"),
     "parasol": {"shadow": ("cd9c52",), "canopy": 32, "pole": (14, 18), "foot": 40,
                 "shaft": (33, 38), "high": 22, "rise": 0.5, "step": 2},
     # all but the pole: its shaft is repeated up to the canopy, not projected
     "exact": [(0, 0, 32, 26)]}
    for (name, x, y) in (("orange", 9, 6), ("blue", 11, 8), ("green", 13, 14))
] + [
    {"name": "beach_%s" % name,
     "components": {
         "primary": "gTileset_General",
         "layouts": ["LAYOUT_ROUTE109"],
         "tiles": tiles,
         "height": high,
     },
     "ground": [SAND]}
    for (name, tiles, high) in (("lounger", {0x2E1, 0x2E9, 0x2F1}, 5),
                                ("air_bed", {0x2E0, 0x2E8, 0x2F0}, 4))
]

SEASHORE_FLOOR = ("e6e6b4", "c5cd94", "b4b48b", "f6f6cd", "52ac94", "7bc5b4", "b4deff")
SEASHORE_WALL = ("e6c562", "ffe67b", "bd9c4a", "414a6a", "83838b")


def seashore_house():
    """The Seashore House: a boarded wall two cells tall with the swimming
    rings hung on it, a post at each end, two chilled cabinets standing half
    a cell out of it, a folding chair and a table with the kettle, and the
    low tables in three rows across the room."""
    fl, wall = SEASHORE_FLOOR, SEASHORE_WALL + SEASHORE_FLOOR
    side = (144, 0, 160, 32)
    tables = [piece("table_%d_%d" % (row, k), [(x0, y, x1, y + 16)], 4, leave=fl, solid=True)
              for row, y in enumerate((64, 96, 128))
              for k, (x0, x1) in enumerate(((1, 32), (48, 96), (128, 176), (208, 239)))
              if row < 2 or k in (0, 3)]
    return tables + [
        piece("chair", [(97, 32, 111, 47)], 8, leave=fl, solid=True),
        piece("kettle_table", [(112, 32, 128, 48)], 8, leave=fl, solid=True),
        # the kettle on it stays on the wall behind: a card of it left two
        # pixels of its outline to the wall
        piece("cabinet_w", [(16, 16, 48, 48)], 24, leave=wall, back=40),
        piece("cabinet_e", [(192, 16, 224, 48)], 24, leave=wall, back=40),
        piece("post_w", [(0, 3, 8, 40)], 32, back=32),
        piece("post_e", [(232, 3, 240, 40)], 32, back=32),
        piece("wall", [(0, 0, 240, 32)], 32, fill=16, foot=32, side=side),
        piece("side_w", [], 32, side=side, walls=[((0, 160), (0, 32))]),
        piece("side_e", [], 32, side=side, walls=[((240, 32), (240, 160))]),
    ]


SPECS += [
    {"name": "seashore_house",
     "interior": {"layout": "LAYOUT_ROUTE109_SEASHORE_HOUSE", "ground": [0x225],
                  "pieces": own_shell(seashore_house())}},
]

# Slateport's sailing boats, moored at the quay: each its drawing stood up as
# a card, the sea cleared from round it - as a box it was a square of sea
# lifted with the boat. One whole, two with the quay across their hulls, and
# the bow of one the map's edge cuts.
SEA_COLOURS = ("526ad5", "6a83d5", "8394de", "839cde")
SPECS += [
    {"name": "slateport_boat_%s" % name,
     "layout": "LAYOUT_SLATEPORT_CITY",
     "rect": (x, y, w, h),
     "owned": {(i, j) for j in range(h) for i in range(w)},
     "repeat_at": at,
     "ground": [0x170],
     "clear": SEA_COLOURS,
     # and the sea between the dots of the shadow under its hull
     "drop": SEA_COLOURS,
     "card": True,
     "exact": []}
    # the bow the map's edge cuts (39, 44) lies as drawn: a card of one
    # tile of a boat was a brown bar standing in the sea
    for (name, x, y, w, h, at) in (("whole", 34, 44, 3, 3, [(34, 44)]),
                                   ("moored", 36, 37, 3, 2, [(36, 37), (35, 48)]),
                                   # the two-master by the harbour's doors
                                   ("two_master", 33, 35, 3, 4, [(33, 35)]))
]

# ── Route 110 ─────────────────────────────────────────────────────────────
#
# The two gatehouses of the Seaside Cycling Road, yellow brick under a flat
# grey roof, and the Trick House, each a box under its roof as it is drawn;
# and the route's kerbs and fences, the General tileset's.
SPECS += [
    {"name": "route110_gate_%s" % name,
     "layout": "LAYOUT_ROUTE110",
     "rect": (x, y, 6, 5),
     "ground": [GRASS],
     "parts": lambda: box_building(96, 80, 38),
     "exact": [(0, 0, 96, 80, True)]}
    for (name, x, y) in (("north", 14, 12), ("south", 15, 84))
] + [
    {"name": "route110_trick_house",
     "layout": "LAYOUT_ROUTE110",
     "rect": (9, 61, 5, 6),
     "ground": [GRASS],
     "parts": lambda: box_building(80, 96, 70),
     "exact": []},
    # The cycling road lies as it is drawn; what stands on it is modelled
    # piece by piece. First its railings along the spans that run east and
    # west, drawn from in front: twelve rows tall.
    {"name": "route110_rails",
     "components": {
         "secondary": "gTileset_Mauville",
         "layouts": ["LAYOUT_ROUTE110"],
         "tiles": {0x2F1, 0x2F2, 0x2F3, 0x34C, 0x30A, 0x309, 0x30B, 0x306, 0x307, 0x351, 0x352,
                   0x344, 0x345},
         "height": 12, "block": 2,
     },
     "ground": [0x170, GRASS, 0x171]},
] + [
    # Step two: where a railing turns - the curved corner tiles, half road
    # and half railing. The road's own colours are cleared from the tile's
    # edge in, and what is left, the railing, is read column by column.
    {"name": "route110_curve_%03x" % tile,
     "layout": "LAYOUT_ROUTE110",
     "rect": (x, y, 1, 1),
     "owned": {(0, 0)},
     # (on the road: what is cleared from under the railing is road)
     "ground": [0x2FE],
     "clear": ("9cb4de", "bdcde6", "dee6ee"),
     "relief": {"height": 12}}
    for (tile, x, y) in ((0x334, 20, 10), (0x335, 23, 10), (0x336, 26, 79), (0x337, 14, 32))
] + [
    {"name": "route110_kerbs",
     "components": {
         "primary": "gTileset_General",
         "layouts": ["LAYOUT_ROUTE110"],
         "tiles": {0x045, 0x047, 0x04E, 0x03E, 0x040, 0x03D, 0x03F, 0x04D, 0x04F},
         "height": 6, "block": 2,
     },
     "ground": [GRASS]},
    {"name": "route110_posts",
     "components": {
         "primary": "gTileset_General",
         "layouts": ["LAYOUT_ROUTE110"],
         "tiles": {0x132, 0x133, 0x134, 0x138, 0x139, 0x140, 0x141, 0x142, 0x148, 0x14A, 0x14C},
         "height": 10, "block": 2,
     },
     "ground": [GRASS]},
]

# The rowing boat pulled up on the grass by the harbour: a hull rounded off
# its own drawing, low.
SPECS += [
    {"name": "slateport_rowing_boat",
     "layout": "LAYOUT_SLATEPORT_CITY",
     "rect": (21, 35, 3, 2),
     "ground": [GRASS],
     # the lawn, and the grey of the shadow drawn under its hull: the light
     # casts the boat's own
     "clear": GRASS_COLOURS + ("73737b",),
     "mound": {"rise": 0.45, "step": 4},
     "exact": []},
]

# ── Route 108: the Abandoned Ship ─────────────────────────────────────────
#
# A small drawing of a whole ship aground on the shoal: a hull eleven rows
# out of the water, its deck laid back from the top of its side; the cabin's
# roof four rows over the deck, flush with the side its portholes are in; the
# gangway and the hull's shadow on the water, which lie there.

def raised_part(name, x0, x1, base, foot, facade_top, top):
    """box_part standing `base` rows up, on another box's lid."""
    wall = foot - facade_top
    front = foot + base
    back = front - (facade_top - top)
    side = Tile(x0, facade_top, x0 + 8, foot, top=wall)
    return Prism(name, x0, x1,
                 [(front, base), (front, base + wall), (back, base + wall), (back, base)],
                 edges={0: Proj(facade_top, foot), 1: Proj(top, facade_top), 2: side}, skip=(3,),
                 caps=[Band(base, base + wall + 1, side, front)])


def abandoned_ship():
    """Twice the size it is drawn, about the foot of its gangway: as drawn
    its hull stood to the player's knee, and it is a liner one walks into."""
    return [Scaled("ship", [box_part("hull", 0, 88, 44, 33, 16),
                            raised_part("cabin", 22, 61, 11, 33, 29, 10),
                            raised_part("stack", 61, 75, 11, 33, 31, 13)], 2.0, 40, 48),
            box_part("gangway", 29, 51, 56, 55, 48)]


SPECS += [
    {"name": "route108_ship",
     "layout": "LAYOUT_ROUTE108",
     "rect": (27, 3, 6, 4),
     "owned": {(i, j) for j in range(4) for i in range(6)} - {(0, 0), (5, 0), (0, 3), (4, 3), (5, 3)},
     "ground": [0x19E],
     "clear": ("9ca4bd", "acc5e6", "6a83d5"),
     "drop": ("9ca4bd", "acc5e6", "6a83d5"),
     "parts": abandoned_ship,
     "exact": []},
]

# ── The Abandoned Ship, inside ────────────────────────────────────────────
#
# Its corridors: two halves of a deck side by side, each under a wall of
# portholes two cells tall, with the block of cabins in its middle - a white
# roof laid back from a front 28 rows tall with the cabins' doors in it.
SHIP_FLOOR = ("948341", "8394bd", "c58b5a", "9cacd5")


def ship_corridors_1f():
    fl = SHIP_FLOOR
    west, east = (0, 0, 16, 32), (128, 0, 144, 32)
    return [
        piece("cabins_w", [(32, 57, 80, 160)], 28, leave=fl, solid=True),
        piece("cabins_e", [(160, 57, 256, 160)], 28, leave=fl, solid=True),
        piece("wall_w", [(0, 0, 112, 32)], 32, fill=16, foot=32, side=west),
        piece("wall_e", [(128, 0, 288, 32)], 32, fill=16, foot=32, side=east),
        piece("side_w", [], 32, side=west, walls=[((0, 192), (0, 32)), ((112, 32), (112, 192))]),
        piece("side_e", [], 32, side=east, walls=[((128, 192), (128, 32)), ((288, 32), (288, 192))]),
    ]


SPECS += [
    {"name": "ship_corridors_1f",
     "interior": {"layout": "LAYOUT_ABANDONED_SHIP_CORRIDORS_1F", "ground": [0x202],
                  "pieces": own_shell(ship_corridors_1f())}},
]

def ship_corridors(layout_id):
    """A corridor deck read off its layout: the wall along its back wherever
    the top two rows are wall, and every block of cabins - its white roof
    (230-232) over the front its doors are in - as a box 28 rows tall. A
    block the layout's bottom edge cuts has no front drawn and stays flat."""
    import voxel_building as vb
    lay = vb.LayoutArt(layout_id)
    roof = {0x230, 0x231, 0x232}
    front = {0x225, 0x223, 0x224, 0x222, 0x226, 0x22D, 0x22B, 0x22C, 0x22A, 0x22E, 0x233, 0x2AE, 0x2B6}
    blocked = lambda c, r: bool(lay.blocks[r * lay.w + c] & 0xC00)
    pieces, seen = [], set()
    for y in range(lay.h):
        for x in range(lay.w):
            if (x, y) in seen or lay.metatile(x, y) not in roof | front:
                continue
            todo, cells = [(x, y)], {(x, y)}
            while todo:
                cx, cy = todo.pop()
                for q in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if (0 <= q[0] < lay.w and 0 <= q[1] < lay.h and q not in cells
                            and lay.metatile(*q) in roof | front):
                        cells.add(q)
                        todo.append(q)
            seen |= cells
            x0, x1 = min(c[0] for c in cells), max(c[0] for c in cells) + 1
            y0, y1 = min(c[1] for c in cells), max(c[1] for c in cells) + 1
            # A block the layout's bottom edge cuts has no front drawn: it
            # stands all the same, its roof's last rows its front - a white
            # slab lying on the floor was no block of cabins. (One too
            # shallow for that stays flat.)
            if not any(lay.metatile(*c) in front for c in cells) and (
                    y1 < lay.h or y1 * 16 - max(0, y0 * 16 - 7) < 36):
                continue
            pieces.append(piece("cabins_%d_%d" % (x0, y0),
                                [(x0 * 16, max(0, y0 * 16 - 7), x1 * 16, y1 * 16)], 28,
                                leave=SHIP_FLOOR, solid=True))
    run = None
    for c in range(lay.w + 1):
        wall = (c < lay.w and blocked(c, 0) and blocked(c, 1)
                and lay.metatile(c, 0) not in roof | {0x201} and lay.metatile(c, 0) in (0x208, 0x209, 0x2A8, 0x2A9, 0x221))
        if wall and run is None:
            run = c
        if not wall and run is not None:
            side = (run * 16, 0, run * 16 + 16, 32)
            pieces.append(piece("wall_%d" % run, [(run * 16, 0, c * 16, 32)], 32, fill=16, foot=32, side=side))
            run = None
    for pc in pieces:
        pc["alone"] = True
    return pieces


SPECS += [
    {"name": "ship_" + layout.lower(),
     "interior": {"layout": "LAYOUT_ABANDONED_SHIP_" + layout, "ground": [0x202],
                  "pieces": ship_corridors("LAYOUT_ABANDONED_SHIP_" + layout)}}
    for layout in ("CORRIDORS_B1F", "HIDDEN_FLOOR_CORRIDORS")
]


def captains_office():
    """The captain's office: the cabinet by the west wall. Its consoles, its
    shelf with the model ship and its chart table are the Facility tileset's,
    modelled in Stern's shipyard (shipyard_1f) and found here as they are."""
    fl = SHIPYARD_FLOOR
    return only_here([piece("cabinet", [(0, 48, 16, 80)], 16, leave=fl, solid=True)],
                     "cabinet") + plain_room(9, 7, 5, False)


SPECS += [
    {"name": "ship_captains_office",
     "interior": {"layout": "LAYOUT_ABANDONED_SHIP_CAPTAINS_OFFICE", "ground": [0x202],
                  "shade": [0x203, 0x204], "pieces": own_shell(captains_office())}},
]


# The two flooded rooms: a wall of portholes two cells tall, the rest water.
SPECS += [
    {"name": "ship_" + layout.lower(),
     "interior": {"layout": "LAYOUT_ABANDONED_SHIP_" + layout, "ground": [0x2CF],
                  "shade": [0x2C9], "pieces": own_shell(plain_room(width, height, 1, False))}}
    for layout, width, height in (("UNDERWATER1", 8, 8), ("UNDERWATER2", 21, 7))
]


def ship_cabins(layout_id):
    """The ship's cabins, several to a layout, read off the layout itself. A
    cabin begins at its top-left corner tile (236) and is as wide as the row
    runs to 237. Along its back, a panelled wall two cells tall, open where a
    passage comes through it. Down its sides, the white lines are its side
    walls' tops: each a wall six pixels thick under that line, ending in the
    grey face of a doorway where the border has an open cell. They lay
    painted in the black between the cabins, and a passage's floor was
    painted up the wall it goes through."""
    import voxel_building as vb
    lay = vb.LayoutArt(layout_id)
    blocked = lambda c, r: bool(lay.blocks[r * lay.w + c] & 0xC00)
    pieces, k = [], 0
    for y in range(lay.h):
        for x in range(lay.w):
            if lay.metatile(x, y) != 0x236:
                continue
            x2 = x + 1
            while x2 < lay.w and lay.metatile(x2, y) != 0x237:
                x2 += 1
            if x2 >= lay.w:
                continue
            y2 = y + 2
            while y2 < lay.h and lay.metatile(x, y2) in (0x23E, 0x246, 0x24E) :
                y2 += 1
            X, Y, XE = x * 16, y * 16, x2 * 16
            side = (X + 16, Y, X + 32, Y + 32)
            # the back wall, between the passages through it
            run = None
            # (open where a passage comes through from the cabin north of
            # it; a door of the wall's own - walked into, drawn on it -
            # leaves the wall whole)
            through = lambda c: not blocked(c, y + 1) and y > 0 and not blocked(c, y - 1)
            for c in list(range(x + 1, x2)) + [x2]:
                solid = c < x2 and not through(c)
                if solid and run is None:
                    run = c
                if not solid and run is not None:
                    # in stretches of six cells at most: a wall thirteen
                    # cells long, six rooms of them, put the layout's page
                    # past the console's 512x512
                    for a in range(run, c, 6):
                        b = min(c, a + 6)
                        pieces.append(piece("wall_%d_%d" % (k, a), [(a * 16, Y, b * 16, Y + 32)], 32,
                                            fill=16, foot=Y + 32, side=side))
                    run = None
            # the side walls
            for tag, c, s0, s1, wx in (("w", x, X + 10, X + 16, X + 16), ("e", x2, XE, XE + 6, XE)):
                r = y
                while r < y2:
                    if not blocked(c, r):
                        r += 1
                        continue
                    r0 = r
                    while r < y2 and blocked(c, r):
                        r += 1
                    if r0 == y and (r - r0) * 16 > 32:
                        pieces.append(piece("jamb_%d_%s" % (k, tag), [(s0, r0 * 16, s1, r * 16)], 32, solid=True,
                                            side=side))
                    elif r0 > y:
                        a, b = (wx, r * 16), (wx, r0 * 16)
                        pieces.append(piece("side_%d_%s_%d" % (k, tag, r0), [], 32, side=side,
                                            walls=[(a, b) if tag == "w" else (b, a)],
                                            cells=[(c, q) for q in range(r0, r)]))
            # A passage between two cabins crosses the black between them:
            # nothing is drawn there, and from the console's camera it was a
            # hole to the void on either hand. A wall closes it - across the
            # gap between the two side walls where a door goes east, and
            # down both sides of a passage that comes through the back wall.
            for r in range(y, y2):
                if not blocked(x2, r) and x2 + 1 < lay.w and not blocked(x2 + 1, r):
                    pieces.append(piece("lintel_%d_%d" % (k, r), [], 32, side=side,
                                        walls=[((XE + 6, r * 16), (XE + 26, r * 16))]))
                    pieces[-1]["added"] = True
            for c in range(x + 1, x2):
                if through(c):
                    top = (y - 1) * 16
                    pieces.append(piece("pass_%d_%d" % (k, c), [], 32, side=side,
                                        walls=[((c * 16, Y + 32), (c * 16, top)),
                                               ((c * 16 + 16, top), (c * 16 + 16, Y + 32))]))
            k += 1
    # and what stands in them, each found by its tile: a bed on its cream
    # platform (its first row seven rows up the cell above), a table, a bin,
    # a chair
    fl = ("dea462", "c56241", "de7b52", "bd5a41", "bd7341")
    for y in range(lay.h):
        for x in range(lay.w):
            m, X, Y = lay.metatile(x, y), x * 16, y * 16
            if m in (0x250, 0x254):
                pieces.append(piece("bed_%d_%d" % (x, y), [(X, Y - 7, X + 32, Y + 32)], 8, leave=fl, solid=True))
            # (20F: the table's top in the wall's shade; 299: the desk with
            # its chair; 235 and 268: the bin in the wall's shade)
            elif m in (0x256, 0x20F):
                pieces.append(piece("table_%d_%d" % (x, y), [(X, Y, X + 32, Y + 32)], 8, leave=fl, solid=True))
            elif m == 0x299:
                pieces.append(piece("desk_%d_%d" % (x, y), [(X, Y, X + 32, Y + 32)], 8, leave=fl, solid=True))
            elif m in (0x262, 0x235, 0x268):
                pieces.append(piece("bin_%d_%d" % (x, y), [(X + 2, Y, X + 14, Y + 16)], 8, leave=fl, solid=True))
            elif m in (0x260, 0x261):
                pieces.append(piece("chair_%d_%d" % (x, y), [(X + 2, Y, X + 14, Y + 16)], 6, leave=fl, solid=True))
    for pc in pieces:
        pc["alone"] = True
    return pieces


SPECS += [
    {"name": "ship_" + layout.lower(),
     "interior": {"layout": "LAYOUT_ABANDONED_SHIP_" + layout, "ground": [0x238],
                  "shade": [0x23B, 0x23D, 0x23A, 0x23C],
                  "pieces": ship_cabins("LAYOUT_ABANDONED_SHIP_" + layout)}}
    for layout in ("ROOMS_1F", "ROOMS2_1F", "ROOM_B1F", "ROOMS_B1F", "ROOMS2_B1F", "HIDDEN_FLOOR_ROOMS")
]

# A model somebody is trying out in devtools/workbench.py: the file $VOXEL_DRAFT
# names, a list of {name, layout, rect, kind, ground, clear, drop, height} -
# and, of kind "stack", {cut, low, high, deep} (gen_voxel_buildings: `stack`).
# Built only for its preview (devtools/model_view.sh); a request that is to
# stay becomes a spec of its own above.
def draft_specs(path):
    import json
    out = []
    for d in json.load(open(path, encoding="utf-8")):
        x, y, w, h = d["rect"]
        spec = {"name": d["name"], "layout": d["layout"], "rect": (x, y, w, h),
                "owned": {(i, j) for j in range(h) for i in range(w)}, "repeat_at": [(x, y)],
                "ground": [int(d.get("ground", GRASS))], "exact": []}
        if d.get("clear"):
            spec["clear"] = tuple(d["clear"])
        if d.get("drop"):
            spec["drop"] = tuple(d["clear"])
        kind = d.get("kind", "card")
        if kind == "card":
            spec["card"] = True
        elif kind == "dome":
            spec["mound"] = {"rise": float(d.get("rise", 0.9)), "step": 2}
        elif kind == "stack":
            spec["stack"] = {"cut": int(d.get("cut", h * 8)), "low": d.get("low", "box"),
                             "high": d.get("high", "dome"), "deep": int(d.get("deep", 8))}
        else:
            tall = max(1, min(int(d.get("height", 16)), h * 16 - 1))
            spec["parts"] = (lambda W, H, T: (lambda: box_building(W, H, H - T)))(w * 16, h * 16, tall)
        out.append(spec)
    return out


if os.environ.get("VOXEL_DRAFT"):
    SPECS += draft_specs(os.environ["VOXEL_DRAFT"])

# Where a room's drawing is not judged: a thing made by hand stands there
# (a piece's `made`), which the drawing shows otherwise.
REMADE = {}

for _spec in SPECS:
    _room = _spec.get("interior")
    if _room and _room["layout"] in REMADE:
        _room["remade"] = REMADE[_room["layout"]]
    if _room and _room["layout"] in EXTRA_PIECES:
        _room["pieces"] = EXTRA_PIECES[_room["layout"]]() + list(_room["pieces"])
