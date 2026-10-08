# What gets a 3D model of its own, and of which kind

The rule: a thing with a shape of its own is modelled as that shape, from the
game's own drawing, without the ground or sea drawn round it and without its
painted shadow (the Voxel view casts shadows itself). A box with the drawing
on its lid is the last resort, for things that are boxes.

Look at every new model with `bash devtools/model_view.sh SPEC_NAME` and read
`build/audit/model_lint.txt` before it goes to the emulator; then compare a
2D and a voxel capture of the same place (`devtools/autotest.py`).

| Thing | Kind of model | Spec key / helper | State |
|---|---|---|---|
| Trees | one card per tree, crown and trunk | `voxel_tree.c` | done (General, Dewford, Rustboro shade) |
| Flowers, tall grass | card per cell, tileset's own drawing | `voxel_tree.c` | flowers done; grass is still our own drawing |
| Round bushes, domes, tents, sea rocks | dome lifted off the drawing | `"mound"` | Slateport bushes, Battle Tent, rocks |
| Parasols | dome on a pole | `"parasol"` | Route 109 |
| Jars, bowls, bunches, Poke Balls, bollards, sailing boats | card cut from its ground, lit as open ground | `"card": True` (+ `clear`, `drop`) | Slateport market and boats |
| Crates, loungers, beds, tables, bins, counters | low box | `piece(..., solid=True)` / `components` | rooms done so far |
| Fences, hedges, kerbs, railings | run of tiles read column by column | `components` | Route 104, Petalburg, Slateport |
| Signs, lamps | standing sign | `voxel_sign.c` | done |
| Houses, marts, centres, gyms | kit / box under its roof | `kit_house`, `box_building` | towns done so far; roofs are flat lids |
| Pillars, stalls, awnings | slab on posts | `market_stall`, `box_part` | Slateport |
| Ships | boxes, scaled where the drawing is a miniature | `Scaled`, `raised_part` | Route 108 outside |
| Room walls, doorways, passages | walls read off the layout | `plain_room`, `ship_cabins`, `ship_corridors` | see VOXEL_BACKLOG.md |
| Stairs, PCs, fountains, bridges, the rocket, satellite dishes | not defined yet | - | to do |
