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
- [ ] Houses: the front edge of the tatami platform (the yellow band by the door) lies flat
- [ ] Town Hall: only its walls stand

<!-- audit:DewfordTown -->
### DewfordTown - audit of 2026-10-07

- [ ] **DewfordTown**: 1 flat cell(s) in 1 object(s) - `build/audit/DewfordTown.png`
  - [ ] (11, 16), 1 cell(s), tiles 210
- [x] **DewfordTown_Hall**: nothing blocked lies flat
- [x] **DewfordTown_PokemonCenter_1F**: nothing blocked lies flat
- [ ] **DewfordTown_Gym**: 48 flat cell(s) in 7 object(s) - `build/audit/DewfordTown_Gym.png`
  - [ ] (0, 0)-(1, 27), 30 cell(s), tiles 20F 21C 21E 221 226 229 231 238 239
  - [ ] (3, 0)-(4, 2), 6 cell(s), tiles 239 23B 23C 243 244
  - [ ] (5, 0)-(6, 4), 6 cell(s), tiles 21C 22D 22E 235 236 239
  - [ ] (17, 0)-(17, 1), 2 cell(s), tiles 20C 23A
  - [ ] (2, 3)-(2, 4), 2 cell(s), tiles 22A 232
  - [ ] (4, 24), 1 cell(s), tiles 227
  - [ ] (7, 24), 1 cell(s), tiles 227
- [x] **DewfordTown_House1**: nothing blocked lies flat
- [x] **DewfordTown_House2**: nothing blocked lies flat

49 blocked cell(s) still flat in this area.
<!-- /audit:DewfordTown -->
