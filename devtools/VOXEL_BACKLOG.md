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
  - [ ] painted on the floor: pixels (176, 83)-(184, 88), 40 px
  - [ ] painted on the floor: pixels (176, 91)-(184, 96), 40 px
  - [ ] painted on the floor: pixels (176, 99)-(184, 104), 40 px
  - [ ] painted on the floor: pixels (176, 67)-(184, 72), 40 px
  - [ ] painted on the floor: pixels (176, 75)-(184, 80), 40 px
  - [ ] painted on the floor: pixels (176, 51)-(184, 56), 40 px
  - [ ] painted on the floor: pixels (176, 59)-(184, 64), 40 px
  - [ ] painted on the floor: pixels (176, 107)-(184, 112), 40 px
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

<!-- audit:summary -->
## The whole game - audit of 2026-10-07

`python devtools/voxel_audit.py --all`. An area is a map and those named after it. *Flat cells*: blocked cells nothing stands on. *Rooms without a model*: indoor maps whose walls and furniture are all painted on the floor. *Painted*: things the modelled rooms still have drawn on their floors (rugs and shadows among them). *Not audited*: maps that did not load from a bare warp.

| Area | Maps | Flat cells | Objects | Rooms without a model | Painted | Not audited |
|---|---:|---:|---:|---:|---:|---:|
| Underwater | 12 | 29809 | 19 | 0 | 0 | 0 |
| MagmaHideout | 8 | 6940 | 13 | 0 | 0 | 0 |
| BattleFrontier | 47 | 3206 | 267 | 39 | 55 | 3 |
| ShoalCave | 7 | 3929 | 41 | 0 | 0 | 0 |
| EverGrandeCity | 16 | 3127 | 56 | 12 | 74 | 0 |
| VictoryRoad | 3 | 3125 | 15 | 0 | 0 | 0 |
| AquaHideout | 6 | 2895 | 29 | 3 | 0 | 0 |
| NavelRock | 22 | 2841 | 28 | 2 | 0 | 0 |
| MeteorFalls | 5 | 2794 | 29 | 0 | 0 | 0 |
| SeafloorCavern | 10 | 2670 | 20 | 0 | 0 | 0 |
| SecretBase | 24 | 1689 | 24 | 24 | 0 | 0 |
| DesertUnderpass | 1 | 2520 | 9 | 0 | 0 | 0 |
| CaveOfOrigin | 6 | 2328 | 11 | 0 | 0 | 0 |
| MtPyre | 8 | 2018 | 90 | 6 | 0 | 0 |
| ArtisanCave | 2 | 2099 | 8 | 0 | 0 | 0 |
| LilycoveCity | 24 | 1531 | 128 | 13 | 101 | 0 |
| Route110 | 14 | 1416 | 167 | 9 | 14 | 2 |
| GraniteCave | 4 | 1611 | 6 | 0 | 0 | 0 |
| SootopolisCity | 16 | 1276 | 74 | 4 | 92 | 0 |
| AbandonedShip | 13 | 1424 | 48 | 0 | 0 | 0 |
| SlateportCity | 15 | 864 | 114 | 9 | 61 | 0 |
| FarawayIsland | 2 | 1082 | 14 | 2 | 0 | 0 |
| TrainerHill | 7 | 857 | 33 | 7 | 0 | 0 |
| NewMauville | 2 | 1103 | 8 | 0 | 0 | 0 |
| FieryPath | 1 | 1059 | 2 | 0 | 0 | 0 |
| TerraCave | 2 | 907 | 5 | 0 | 0 | 0 |
| SkyPillar | 8 | 886 | 59 | 0 | 0 | 0 |
| MossdeepCity | 14 | 639 | 70 | 5 | 71 | 0 |
| MarineCave | 2 | 747 | 5 | 0 | 0 | 0 |
| RusturfTunnel | 1 | 687 | 1 | 0 | 0 | 0 |
| MirageTower | 4 | 684 | 11 | 0 | 0 | 0 |
| SealedChamber | 2 | 620 | 10 | 0 | 0 | 0 |
| FortreeCity | 11 | 553 | 37 | 1 | 69 | 0 |
| Route122 | 1 | 552 | 3 | 0 | 0 | 0 |
| MauvilleCity | 9 | 414 | 24 | 3 | 62 | 0 |
| AlteringCave | 1 | 495 | 1 | 0 | 0 | 0 |
| LavaridgeTown | 8 | 327 | 12 | 3 | 62 | 0 |
| Route114 | 4 | 361 | 96 | 2 | 5 | 0 |
| Route112 | 2 | 327 | 51 | 1 | 0 | 0 |
| Route119 | 4 | 268 | 47 | 2 | 4 | 0 |
| FallarborTown | 9 | 221 | 12 | 3 | 62 | 0 |
| BirthIsland | 2 | 225 | 13 | 2 | 0 | 0 |
| Route121 | 2 | 237 | 45 | 1 | 0 | 0 |
| VerdanturfTown | 10 | 152 | 18 | 3 | 74 | 0 |
| AncientTomb | 1 | 270 | 8 | 0 | 0 | 0 |
| DesertRuins | 1 | 270 | 8 | 0 | 0 | 0 |
| IslandCave | 1 | 270 | 8 | 0 | 0 | 0 |
| SSTidalRooms | 1 | 230 | 13 | 1 | 0 | 0 |
| SafariZone | 7 | 205 | 56 | 1 | 0 | 0 |
| Route113 | 2 | 240 | 190 | 0 | 5 | 0 |
| RustboroCity | 18 | 186 | 64 | 1 | 357 | 0 |
| ScorchedSlab | 1 | 189 | 1 | 0 | 0 | 0 |
| BattleColosseum | 2 | 104 | 2 | 2 | 0 | 0 |
| Route117 | 2 | 118 | 25 | 1 | 0 | 0 |
| SSTidalCorridor | 1 | 109 | 3 | 1 | 0 | 0 |
| SSTidalLowerDeck | 1 | 96 | 8 | 1 | 0 | 0 |
| Route131 | 1 | 116 | 8 | 0 | 0 | 0 |
| MtChimney | 2 | 72 | 2 | 1 | 0 | 0 |
| ContestHall | 1 | 67 | 3 | 1 | 0 | 0 |
| ContestHallBeauty | 1 | 67 | 3 | 1 | 0 | 0 |
| ContestHallCool | 1 | 67 | 3 | 1 | 0 | 0 |
| ContestHallCute | 1 | 67 | 3 | 1 | 0 | 0 |
| ContestHallSmart | 1 | 67 | 3 | 1 | 0 | 0 |
| ContestHallTough | 1 | 67 | 3 | 1 | 0 | 0 |
| Route109 | 2 | 59 | 11 | 1 | 0 | 0 |
| Route123 | 2 | 96 | 16 | 0 | 3 | 0 |
| RecordCorner | 1 | 54 | 4 | 1 | 0 | 0 |
| PetalburgWoods | 1 | 88 | 8 | 0 | 0 | 0 |
| TradeCenter | 1 | 48 | 2 | 1 | 0 | 0 |
| UnionRoom | 1 | 30 | 1 | 1 | 0 | 0 |
| Route115 | 1 | 67 | 33 | 0 | 0 | 0 |
| Route120 | 1 | 63 | 18 | 0 | 0 | 0 |
| BattlePyramidSquare13 | 1 | 22 | 8 | 1 | 0 | 0 |
| BattlePyramidSquare07 | 1 | 19 | 5 | 1 | 0 | 0 |
| BattlePyramidSquare08 | 1 | 19 | 4 | 1 | 0 | 0 |
| BattlePyramidSquare09 | 1 | 19 | 5 | 1 | 0 | 0 |
| BattlePyramidSquare12 | 1 | 19 | 5 | 1 | 0 | 0 |
| BattlePyramidSquare11 | 1 | 18 | 5 | 1 | 0 | 0 |
| BattlePyramidSquare10 | 1 | 17 | 6 | 1 | 0 | 0 |
| BattlePyramidSquare02 | 1 | 16 | 4 | 1 | 0 | 0 |
| BattlePyramidSquare03 | 1 | 16 | 3 | 1 | 0 | 0 |
| BattlePyramidSquare14 | 1 | 16 | 16 | 1 | 0 | 0 |
| BattlePyramidSquare15 | 1 | 16 | 16 | 1 | 0 | 0 |
| InsideOfTruck | 1 | 15 | 1 | 1 | 0 | 0 |
| BattlePyramidSquare01 | 1 | 14 | 2 | 1 | 0 | 0 |
| BattlePyramidSquare06 | 1 | 14 | 6 | 1 | 0 | 0 |
| PacifidlogTown | 8 | 53 | 13 | 0 | 147 | 0 |
| BattlePyramidSquare05 | 1 | 12 | 2 | 1 | 0 | 0 |
| JaggedPass | 1 | 52 | 23 | 0 | 0 | 0 |
| Route124 | 2 | 12 | 2 | 1 | 0 | 0 |
| BattlePyramidSquare04 | 1 | 10 | 2 | 1 | 0 | 0 |
| UnusedContestHall1 | 1 | 1 | 1 | 1 | 0 | 0 |
| UnusedContestHall2 | 1 | 1 | 1 | 1 | 0 | 0 |
| UnusedContestHall3 | 1 | 1 | 1 | 1 | 0 | 0 |
| UnusedContestHall4 | 1 | 1 | 1 | 1 | 0 | 0 |
| UnusedContestHall5 | 1 | 1 | 1 | 1 | 0 | 0 |
| UnusedContestHall6 | 1 | 1 | 1 | 1 | 0 | 0 |
| BattlePyramidSquare16 | 1 | 0 | 0 | 1 | 0 | 0 |
| Route104 | 5 | 38 | 11 | 0 | 16 | 0 |
| Route111 | 3 | 33 | 20 | 0 | 10 | 0 |
| Route126 | 1 | 33 | 32 | 0 | 0 | 0 |
| PetalburgCity | 8 | 32 | 9 | 0 | 82 | 0 |
| Route127 | 1 | 29 | 6 | 0 | 0 | 0 |
| SouthernIsland | 2 | 27 | 12 | 0 | 0 | 0 |
| Route116 | 2 | 17 | 1 | 0 | 5 | 0 |
| Route108 | 1 | 12 | 1 | 0 | 0 | 0 |
| LittlerootTown | 6 | 4 | 4 | 0 | 10 | 0 |
| Route118 | 1 | 4 | 2 | 0 | 0 | 0 |
| Route106 | 1 | 3 | 3 | 0 | 0 | 0 |
| Route130 | 1 | 3 | 1 | 0 | 0 | 0 |
| Route102 | 1 | 2 | 1 | 0 | 0 | 0 |
| DewfordTown | 7 | 0 | 0 | 0 | 8 | 0 |
| OldaleTown | 6 | 0 | 0 | 0 | 62 | 0 |
| Route101 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route103 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route105 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route107 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route125 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route128 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route129 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route132 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route133 | 1 | 0 | 0 | 0 | 0 | 0 |
| Route134 | 1 | 0 | 0 | 0 | 0 | 0 |
| **all** | 518 | 97519 | 2517 | 199 | 1511 | 5 |
<!-- /audit:summary -->

<!-- audit:GraniteCave -->
### GraniteCave - audit of 2026-10-07

- [ ] **GraniteCave_1F**: 7 flat cell(s) in 4 object(s) - `build/audit/GraniteCave_1F.png`
  - [ ] (19, 5)-(19, 6), 2 cell(s), tiles 21A 21B
  - [ ] (28, 5)-(28, 6), 2 cell(s), tiles 218 21C
  - [ ] (35, 6)-(35, 7), 2 cell(s), tiles 218 21C
  - [ ] (4, 10), 1 cell(s), tiles 202
- [ ] **GraniteCave_B1F**: 7 flat cell(s) in 3 object(s) - `build/audit/GraniteCave_B1F.png`
  - [ ] (27, 11), 1 cell(s), tiles 203
  - [ ] (23, 13)-(23, 15), 3 cell(s), tiles 210 218
  - [ ] (26, 17)-(26, 19), 3 cell(s), tiles 210 218
- [ ] **GraniteCave_B2F**: 19 flat cell(s) in 9 object(s) - `build/audit/GraniteCave_B2F.png`
  - [ ] (8, 1)-(8, 2), 2 cell(s), tiles 210 253
  - [ ] (10, 1)-(10, 2), 2 cell(s), tiles 212 21A
  - [ ] (12, 11)-(12, 13), 3 cell(s), tiles 210 218 220
  - [ ] (15, 11), 1 cell(s), tiles 262
  - [ ] (18, 12)-(18, 13), 2 cell(s), tiles 212 21A
  - [ ] (22, 15)-(22, 16), 2 cell(s), tiles 21A 21B
  - [ ] (12, 16)-(12, 17), 2 cell(s), tiles 21A 21B
  - [ ] (7, 17)-(7, 19), 3 cell(s), tiles 212 21A 21B
  - [ ] (11, 20)-(11, 21), 2 cell(s), tiles 21F 227
- [ ] **GraniteCave_StevensRoom**: 1 flat cell(s) in 1 object(s) - `build/audit/GraniteCave_StevensRoom.png`
  - [ ] (7, 10), 1 cell(s), tiles 202

34 blocked cell(s) still flat in this area.
<!-- /audit:GraniteCave -->
