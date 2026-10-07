# Voxel backlog

What is still flat, missing or wrong in the voxel view, area by area. Two kinds
of entry:

- **Reported**: seen on the console or in a capture, written down by hand.
- **Audit**: written by `python devtools/voxel_audit.py <Map>`, which asks the
  running game which blocked cells have nothing standing on them. Its sections
  are rewritten on every run; do not edit them by hand.

An area is done when its audit has no open item that is a real object and
every reported item is ticked. Work one area to the end before the next.

## Dewford Town

### Reported

- [x] The trees inside the town lie flat, and the wood round it is blocks of tree tiles
- [x] The gym is its drawing on the sand
- [x] Houses: jars, furniture, low tables and the corner posts are painted on the floor
- [x] Houses: the front edge of the tatami platform (the yellow band by the door) lies flat
- [x] Town Hall: only its walls stand
- [x] The gym's sign lies on the sand beside it (found by the audit)
- [x] Gym interior: rock blocks, the front wall's ends, the statues and the shelves lie flat (found by the audit)
- [ ] Not blocked, so not seen by the audit, and still flat: cushions and chairs in the houses and the hall, the gym leader's dais

<!-- audit:DewfordTown -->
### DewfordTown - audit of 2026-10-07

- [x] **DewfordTown**: nothing blocked lies flat
- [x] **DewfordTown_Hall**: nothing blocked lies flat
- [x] **DewfordTown_PokemonCenter_1F**: nothing blocked lies flat
- [x] **DewfordTown_Gym**: nothing blocked lies flat that is not left so on purpose
  - left flat, 28 cell(s): the rock west of the maze's edge wall: outside the room, and a block of it puts the page past 512x512
  - left flat, 10 cell(s): the rock behind the leader's place: with it the layout's page is past the console's 512x512
  - left flat, 2 cell(s): the corner of the rock east of the edge wall, outside the room
  - left flat, 2 cell(s): the leader's dais: a low platform, its corner posts drawn on it
  - left flat, 2 cell(s): the leader's dais and the shelf's foot beside it
- [x] **DewfordTown_House1**: nothing blocked lies flat
- [x] **DewfordTown_House2**: nothing blocked lies flat
- [x] **DewfordTown_PokemonCenter_2F**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:DewfordTown -->
