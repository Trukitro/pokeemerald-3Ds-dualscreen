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
  - [ ] painted on the floor: pixels (48, 32)-(144, 48), 1536 px
  - [ ] painted on the floor: pixels (160, 32)-(211, 120), 1221 px
  - [ ] painted on the floor: pixels (80, 128)-(112, 144), 512 px
  - [ ] painted on the floor: pixels (237, 32)-(256, 64), 321 px
  - [ ] painted on the floor: pixels (208, 112)-(224, 128), 136 px
- [x] **DewfordTown_PokemonCenter_1F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (64, 64)-(168, 72), 804 px
  - [ ] painted on the floor: pixels (96, 128)-(128, 144), 512 px
  - [ ] painted on the floor: pixels (192, 32)-(208, 40), 84 px
  - [ ] painted on the floor: pixels (121, 105)-(127, 111), 36 px
  - [ ] painted on the floor: pixels (97, 81)-(103, 87), 36 px
  - [ ] painted on the floor: pixels (97, 89)-(103, 95), 36 px
  - [ ] painted on the floor: pixels (105, 105)-(111, 111), 36 px
  - [ ] painted on the floor: pixels (121, 81)-(127, 87), 36 px
  - [ ] painted on the floor: pixels (129, 89)-(135, 95), 36 px
  - [ ] painted on the floor: pixels (113, 113)-(119, 119), 36 px
  - [ ] painted on the floor: pixels (129, 97)-(135, 103), 36 px
  - [ ] painted on the floor: pixels (97, 105)-(103, 111), 36 px
- [x] **DewfordTown_Gym**: nothing blocked lies flat that is not left so on purpose
  - left flat, 28 cell(s): the rock west of the maze's edge wall: outside the room, and a block of it puts the page past 512x512
  - left flat, 10 cell(s): the rock behind the leader's place: with it the layout's page is past the console's 512x512
  - left flat, 2 cell(s): the corner of the rock east of the edge wall, outside the room
  - left flat, 2 cell(s): the leader's dais: a low platform, its corner posts drawn on it
  - left flat, 2 cell(s): the leader's dais and the shelf's foot beside it
  - [ ] painted on the floor: pixels (0, 0)-(32, 448), 7680 px
  - [ ] painted on the floor: pixels (32, 0)-(112, 80), 3712 px
  - [ ] painted on the floor: pixels (48, 144)-(160, 272), 2568 px
  - [ ] painted on the floor: pixels (192, 208)-(272, 320), 1800 px
  - [ ] painted on the floor: pixels (48, 288)-(192, 368), 1764 px
  - [ ] painted on the floor: pixels (96, 48)-(192, 96), 1508 px
  - [ ] painted on the floor: pixels (112, 96)-(200, 144), 1444 px
  - [ ] painted on the floor: pixels (224, 144)-(272, 208), 1024 px
  - [ ] painted on the floor: pixels (208, 48)-(256, 112), 996 px
  - [ ] painted on the floor: pixels (144, 256)-(184, 344), 904 px
  - [ ] painted on the floor: pixels (160, 144)-(200, 232), 904 px
  - [ ] painted on the floor: pixels (208, 352)-(256, 368), 740 px
- [x] **DewfordTown_House1**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (16, 112)-(144, 128), 1988 px
  - [ ] painted on the floor: pixels (48, 32)-(80, 48), 512 px
  - [ ] painted on the floor: pixels (49, 51)-(63, 64), 165 px
  - [ ] painted on the floor: pixels (97, 51)-(111, 64), 165 px
  - [ ] painted on the floor: pixels (97, 67)-(111, 80), 165 px
  - [ ] painted on the floor: pixels (49, 67)-(63, 80), 165 px
- [x] **DewfordTown_House2**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (16, 128)-(144, 144), 1988 px
  - [ ] painted on the floor: pixels (80, 32)-(128, 48), 768 px
  - [ ] painted on the floor: pixels (97, 83)-(111, 96), 165 px
  - [ ] painted on the floor: pixels (33, 51)-(47, 64), 165 px
- [x] **DewfordTown_PokemonCenter_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (64, 64)-(80, 80), 256 px
  - [ ] painted on the floor: pixels (16, 64)-(48, 72), 256 px
  - [ ] painted on the floor: pixels (96, 64)-(128, 72), 228 px
  - [ ] painted on the floor: pixels (160, 64)-(192, 72), 228 px
  - [ ] painted on the floor: pixels (144, 64)-(152, 88), 192 px
  - [ ] painted on the floor: pixels (80, 88)-(96, 104), 134 px
  - [ ] painted on the floor: pixels (160, 96)-(175, 111), 133 px
  - [ ] painted on the floor: pixels (153, 82)-(168, 96), 126 px

0 blocked cell(s) still flat in this area.
<!-- /audit:DewfordTown -->
