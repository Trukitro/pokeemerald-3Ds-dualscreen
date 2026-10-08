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
### DewfordTown - audit of 2026-10-08

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

- [x] **GraniteCave_1F**: nothing blocked lies flat
- [x] **GraniteCave_B1F**: nothing blocked lies flat
- [x] **GraniteCave_B2F**: nothing blocked lies flat
- [x] **GraniteCave_StevensRoom**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:GraniteCave -->

<!-- audit:RusturfTunnel -->
### RusturfTunnel - audit of 2026-10-07

- [x] **RusturfTunnel**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:RusturfTunnel -->

<!-- audit:MeteorFalls -->
### MeteorFalls - audit of 2026-10-07

- [x] **MeteorFalls_1F_1R**: nothing blocked lies flat
- [x] **MeteorFalls_1F_2R**: nothing blocked lies flat
- [x] **MeteorFalls_B1F_1R**: nothing blocked lies flat
- [x] **MeteorFalls_B1F_2R**: nothing blocked lies flat
- [x] **MeteorFalls_StevensCave**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:MeteorFalls -->

<!-- audit:VictoryRoad -->
### VictoryRoad - audit of 2026-10-07

- [x] **VictoryRoad_1F**: nothing blocked lies flat
- [x] **VictoryRoad_B1F**: nothing blocked lies flat
- [x] **VictoryRoad_B2F**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:VictoryRoad -->

<!-- audit:ShoalCave -->
### ShoalCave - audit of 2026-10-07

- [x] **ShoalCave_HighTideEntranceRoom**: nothing blocked lies flat
- [x] **ShoalCave_HighTideInnerRoom**: nothing blocked lies flat
- [x] **ShoalCave_LowTideEntranceRoom**: nothing blocked lies flat
- [x] **ShoalCave_LowTideIceRoom**: nothing blocked lies flat
- [ ] **ShoalCave_LowTideInnerRoom**: 6 flat cell(s) in 6 object(s) - `build/audit/ShoalCave_LowTideInnerRoom.png`
  - [ ] (31, 8), 1 cell(s), tiles 358
  - [ ] (6, 9), 1 cell(s), tiles 359
  - [ ] (41, 10), 1 cell(s), tiles 359
  - [ ] (16, 13), 1 cell(s), tiles 359
  - [ ] (41, 20), 1 cell(s), tiles 359
  - [ ] (14, 26), 1 cell(s), tiles 358
- [ ] **ShoalCave_LowTideLowerRoom**: 1 flat cell(s) in 1 object(s) - `build/audit/ShoalCave_LowTideLowerRoom.png`
  - [ ] (18, 2), 1 cell(s), tiles 358
- [ ] **ShoalCave_LowTideStairsRoom**: 1 flat cell(s) in 1 object(s) - `build/audit/ShoalCave_LowTideStairsRoom.png`
  - [ ] (11, 11), 1 cell(s), tiles 358

8 blocked cell(s) still flat in this area.
<!-- /audit:ShoalCave -->

<!-- audit:SeafloorCavern -->
### SeafloorCavern - audit of 2026-10-07

- [x] **SeafloorCavern_Entrance**: nothing blocked lies flat
- [x] **SeafloorCavern_Room1**: nothing blocked lies flat
- [x] **SeafloorCavern_Room2**: nothing blocked lies flat
- [x] **SeafloorCavern_Room3**: nothing blocked lies flat
- [x] **SeafloorCavern_Room4**: nothing blocked lies flat
- [x] **SeafloorCavern_Room5**: nothing blocked lies flat
- [ ] **SeafloorCavern_Room6**: 206 flat cell(s) in 2 object(s) - `build/audit/SeafloorCavern_Room6.png`
  - [ ] (0, 0)-(23, 22), 181 cell(s), tiles 276 278 27A 27E 281 289 28A 28D 28E 290 292 293 294 298 299 29A 29B 29C 2C3 2C5
  - [ ] (11, 5)-(17, 8), 25 cell(s), tiles 275 276 277 27D 27E 27F 280 282 285 286 287 288 289 28A 28F 297 2C3 2C5
- [ ] **SeafloorCavern_Room7**: 180 flat cell(s) in 1 object(s) - `build/audit/SeafloorCavern_Room7.png`
  - [ ] (0, 0)-(22, 24), 180 cell(s), tiles 273 274 276 278 279 27A 27E 280 281 282 288 289 28A 28D 28E 290 292 293 294 298 299 29A 29C
- [x] **SeafloorCavern_Room8**: nothing blocked lies flat
- [x] **SeafloorCavern_Room9**: nothing blocked lies flat

386 blocked cell(s) still flat in this area.
<!-- /audit:SeafloorCavern -->

<!-- audit:CaveOfOrigin -->
### CaveOfOrigin - audit of 2026-10-07

- [x] **CaveOfOrigin_1F**: nothing blocked lies flat
- [x] **CaveOfOrigin_B1F**: nothing blocked lies flat
- [x] **CaveOfOrigin_Entrance**: nothing blocked lies flat
- [x] **CaveOfOrigin_UnusedRubySapphireMap1**: nothing blocked lies flat
- [x] **CaveOfOrigin_UnusedRubySapphireMap2**: nothing blocked lies flat
- [x] **CaveOfOrigin_UnusedRubySapphireMap3**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:CaveOfOrigin -->

<!-- audit:AlteringCave -->
### AlteringCave - audit of 2026-10-07

- [x] **AlteringCave**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:AlteringCave -->

<!-- audit:AncientTomb -->
### AncientTomb - audit of 2026-10-07

- [ ] **AncientTomb**: 1 flat cell(s) in 1 object(s) - `build/audit/AncientTomb.png`
  - [ ] (8, 20), 1 cell(s), tiles 235

1 blocked cell(s) still flat in this area.
<!-- /audit:AncientTomb -->

<!-- audit:ArtisanCave -->
### ArtisanCave - audit of 2026-10-07

- [x] **ArtisanCave_1F**: nothing blocked lies flat
- [x] **ArtisanCave_B1F**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:ArtisanCave -->

<!-- audit:DesertRuins -->
### DesertRuins - audit of 2026-10-07

- [ ] **DesertRuins**: 1 flat cell(s) in 1 object(s) - `build/audit/DesertRuins.png`
  - [ ] (8, 20), 1 cell(s), tiles 235

1 blocked cell(s) still flat in this area.
<!-- /audit:DesertRuins -->

<!-- audit:DesertUnderpass -->
### DesertUnderpass - audit of 2026-10-07

- [x] **DesertUnderpass**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:DesertUnderpass -->

<!-- audit:IslandCave -->
### IslandCave - audit of 2026-10-07

- [ ] **IslandCave**: 1 flat cell(s) in 1 object(s) - `build/audit/IslandCave.png`
  - [ ] (8, 20), 1 cell(s), tiles 235

1 blocked cell(s) still flat in this area.
<!-- /audit:IslandCave -->

<!-- audit:MarineCave -->
### MarineCave - audit of 2026-10-07

- [x] **MarineCave_End**: nothing blocked lies flat
- [x] **MarineCave_Entrance**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:MarineCave -->

<!-- audit:ScorchedSlab -->
### ScorchedSlab - audit of 2026-10-07

- [x] **ScorchedSlab**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:ScorchedSlab -->

<!-- audit:SealedChamber -->
### SealedChamber - audit of 2026-10-07

- [x] **SealedChamber_InnerRoom**: nothing blocked lies flat
- [ ] **SealedChamber_OuterRoom**: 1 flat cell(s) in 1 object(s) - `build/audit/SealedChamber_OuterRoom.png`
  - [ ] (10, 2), 1 cell(s), tiles 235

1 blocked cell(s) still flat in this area.
<!-- /audit:SealedChamber -->

<!-- audit:SkyPillar -->
### SkyPillar - audit of 2026-10-07

- [ ] **SkyPillar_1F**: 63 flat cell(s) in 2 object(s) - `build/audit/SkyPillar_1F.png`
  - [ ] (0, 0)-(13, 1), 27 cell(s), tiles 227 22F 23B 23C 23D 243 245
  - [ ] (4, 5)-(9, 10), 36 cell(s), tiles 238 239 23A 240 241 242 249 24A 24D
- [ ] **SkyPillar_2F**: 62 flat cell(s) in 2 object(s) - `build/audit/SkyPillar_2F.png`
  - [ ] (0, 0)-(13, 1), 26 cell(s), tiles 227 22F 23B 23C 23D 243 245
  - [ ] (4, 5)-(9, 10), 36 cell(s), tiles 238 239 23A 240 241 242 249 24A 24D
- [ ] **SkyPillar_3F**: 67 flat cell(s) in 3 object(s) - `build/audit/SkyPillar_3F.png`
  - [ ] (0, 0)-(13, 2), 27 cell(s), tiles 217 227 22F 23B 23C 23D 243 245
  - [ ] (4, 3)-(9, 10), 39 cell(s), tiles 20F 21F 238 239 23A 240 241 249 24A 24D
  - [ ] (9, 3), 1 cell(s), tiles 20F
- [ ] **SkyPillar_4F**: 73 flat cell(s) in 4 object(s) - `build/audit/SkyPillar_4F.png`
  - [ ] (0, 0)-(13, 3), 34 cell(s), tiles 207 20F 21F 227 22F 23B 23C 23D 243 245
  - [ ] (0, 4)-(1, 4), 2 cell(s), tiles 217 21F
  - [ ] (10, 4), 1 cell(s), tiles 20F
  - [ ] (4, 5)-(9, 10), 36 cell(s), tiles 238 239 23A 240 241 242 249 24A 24D
- [ ] **SkyPillar_5F**: 92 flat cell(s) in 2 object(s) - `build/audit/SkyPillar_5F.png`
  - [ ] (0, 0)-(13, 2), 27 cell(s), tiles 217 227 22F 23B 23C 23D 243 245
  - [ ] (3, 3)-(10, 11), 65 cell(s), tiles 21F 238 239 23A 240 241 242 249 24A 24D
- [x] **SkyPillar_Entrance**: nothing blocked lies flat
- [ ] **SkyPillar_Outside**: 4 flat cell(s) in 3 object(s) - `build/audit/SkyPillar_Outside.png`
  - [ ] (9, 1), 1 cell(s), tiles 2B7
  - [ ] (21, 1)-(22, 1), 2 cell(s), tiles 2B7
  - [ ] (7, 2), 1 cell(s), tiles 2B7
- [ ] **SkyPillar_Top**: 272 flat cell(s) in 42 object(s) - `build/audit/SkyPillar_Top.png`
  - [ ] (11, 3)-(17, 3), 7 cell(s), tiles 2AD
  - [ ] (20, 4), 1 cell(s), tiles 20F
  - [ ] (24, 4), 1 cell(s), tiles 20F
  - [ ] (1, 5), 1 cell(s), tiles 20F
  - [ ] (5, 5), 1 cell(s), tiles 20F
  - [ ] (19, 5), 1 cell(s), tiles 20F
  - [ ] (23, 5), 1 cell(s), tiles 20F
  - [ ] (2, 6), 1 cell(s), tiles 20F
  - [ ] (6, 6), 1 cell(s), tiles 20F
  - [ ] (8, 6), 1 cell(s), tiles 20F
  - [ ] (18, 6), 1 cell(s), tiles 20F
  - [ ] (20, 6), 1 cell(s), tiles 20F
  - [ ] (3, 7), 1 cell(s), tiles 20F
  - [ ] (7, 7), 1 cell(s), tiles 20F
  - [ ] (17, 7), 1 cell(s), tiles 20F
  - [ ] (25, 7), 1 cell(s), tiles 20F
  - [ ] (0, 8), 1 cell(s), tiles 20F
  - [ ] (6, 8), 1 cell(s), tiles 20F
  - [ ] (8, 8), 1 cell(s), tiles 20F
  - [ ] (12, 8)-(12, 9), 2 cell(s), tiles 20F
  - [ ] (16, 8)-(16, 9), 2 cell(s), tiles 20F
  - [ ] (20, 8), 1 cell(s), tiles 20F
  - [ ] (24, 8), 1 cell(s), tiles 20F
  - [ ] (1, 9), 1 cell(s), tiles 20F
  - [ ] (9, 9), 1 cell(s), tiles 20F
  - [ ] (23, 9), 1 cell(s), tiles 20F
  - [ ] (2, 10), 1 cell(s), tiles 20F
  - [ ] (4, 10), 1 cell(s), tiles 20F
  - [ ] (6, 10), 1 cell(s), tiles 20F
  - [ ] (13, 10), 1 cell(s), tiles 20F
  - [ ] (24, 10), 1 cell(s), tiles 20F
  - [ ] (3, 11), 1 cell(s), tiles 20F
  - [ ] (21, 11), 1 cell(s), tiles 20F
  - [ ] (25, 11), 1 cell(s), tiles 20F
  - [ ] (0, 12)-(10, 14), 25 cell(s), tiles 20F 227 22F 26A 26D
  - [ ] (13, 12)-(26, 15), 30 cell(s), tiles 207 20F 227 22F 23B 23C 23D 243 245 26B 26E
  - [ ] (2, 16), 1 cell(s), tiles 20F
  - [ ] (4, 16), 1 cell(s), tiles 20F
  - [ ] (21, 16), 1 cell(s), tiles 20F
  - [ ] (23, 16), 1 cell(s), tiles 20F
  - [ ] (25, 16), 1 cell(s), tiles 20F
  - [ ] (0, 17)-(26, 23), 170 cell(s), tiles 20F 25B 2A2

633 blocked cell(s) still flat in this area.
<!-- /audit:SkyPillar -->

<!-- audit:TerraCave -->
### TerraCave - audit of 2026-10-07

- [x] **TerraCave_End**: nothing blocked lies flat
- [x] **TerraCave_Entrance**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:TerraCave -->

<!-- audit:LittlerootTown -->
### LittlerootTown - audit of 2026-10-07

- [x] **LittlerootTown**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:LittlerootTown -->

<!-- audit:PetalburgCity -->
### PetalburgCity - audit of 2026-10-07

- [x] **PetalburgCity**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:PetalburgCity -->

<!-- audit:Route104 -->
### Route104 - audit of 2026-10-07

- [ ] **Route104**: 10 flat cell(s) in 6 object(s) - `build/audit/Route104.png`
  - [ ] (34, 6)-(36, 6), 3 cell(s), tiles 14C
  - [ ] (3, 25), 1 cell(s), tiles 10C
  - [ ] (22, 41)-(24, 41), 3 cell(s), tiles 14C
  - [ ] (14, 50), 1 cell(s), tiles 32F
  - [ ] (5, 54), 1 cell(s), tiles 17B
  - [ ] (5, 68), 1 cell(s), tiles 17B
  - left flat, 1 cell(s): a patch of bare soil the cartridge blocks
  - left flat, 9 cell(s): a small tree's crown top drawn over the fence: the tree south of it stands
  - left flat, 1 cell(s): a corner of the cliff's foot

10 blocked cell(s) still flat in this area.
<!-- /audit:Route104 -->

<!-- audit:PetalburgWoods -->
### PetalburgWoods - audit of 2026-10-07

- [x] **PetalburgWoods**: nothing blocked lies flat that is not left so on purpose
  - left flat, 38 cell(s): grass the cartridge blocks under the wood's canopy: nothing is drawn on it

0 blocked cell(s) still flat in this area.
<!-- /audit:PetalburgWoods -->

<!-- audit:RustboroCity -->
### RustboroCity - audit of 2026-10-07

- [x] **RustboroCity**: nothing blocked lies flat that is not left so on purpose
  - left flat, 15 cell(s): the top of the bank along the sea: the drop is at its edge, in the relief

0 blocked cell(s) still flat in this area.
<!-- /audit:RustboroCity -->

<!-- audit:SlateportCity -->
### SlateportCity - audit of 2026-10-07

- [ ] **SlateportCity**: 39 flat cell(s) in 11 object(s) - `build/audit/SlateportCity.png`
  - [ ] (16, 9), 1 cell(s), tiles 263
  - [ ] (20, 9), 1 cell(s), tiles 264
  - [ ] (32, 16)-(37, 16), 6 cell(s), tiles 04E
  - [ ] (36, 25)-(36, 27), 3 cell(s), tiles 2CF
  - [ ] (8, 32), 1 cell(s), tiles 263
  - [ ] (12, 32), 1 cell(s), tiles 264
  - [ ] (21, 35)-(23, 36), 6 cell(s), tiles 220 221 222 228 229 22A
  - [ ] (33, 35)-(35, 38), 12 cell(s), tiles 346 347 34E 34F 356 357 35E 35F 368 370 378 380
  - [ ] (20, 48)-(20, 50), 3 cell(s), tiles 045
  - [ ] (20, 54)-(20, 57), 4 cell(s), tiles 047
  - [ ] (16, 57), 1 cell(s), tiles 045

39 blocked cell(s) still flat in this area.
<!-- /audit:SlateportCity -->

<!-- audit:Route109 -->
### Route109 - audit of 2026-10-08

- [ ] **Route109**: 2 flat cell(s) in 1 object(s) - `build/audit/Route109.png`
  - [ ] (38, 0)-(39, 0), 2 cell(s), tiles 158 159
- [x] **Route109_SeashoreHouse**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (96, 144)-(128, 160), 512 px
  - [ ] painted on the floor: pixels (16, 80)-(224, 83), 448 px
  - [ ] painted on the floor: pixels (16, 55)-(224, 58), 444 px
  - [ ] painted on the floor: pixels (32, 128)-(208, 130), 352 px
  - [ ] painted on the floor: pixels (128, 32)-(192, 35), 144 px
  - [ ] painted on the floor: pixels (48, 32)-(96, 35), 108 px
  - [ ] painted on the floor: pixels (96, 104)-(128, 106), 64 px
  - [ ] painted on the floor: pixels (176, 104)-(208, 106), 64 px
  - [ ] painted on the floor: pixels (32, 104)-(48, 106), 32 px

2 blocked cell(s) still flat in this area.
<!-- /audit:Route109 -->

<!-- audit:Route108 -->
### Route108 - audit of 2026-10-08

- [x] **Route108**: nothing blocked lies flat

0 blocked cell(s) still flat in this area.
<!-- /audit:Route108 -->

<!-- audit:AbandonedShip -->
### AbandonedShip - audit of 2026-10-08

- [ ] **AbandonedShip_CaptainsOffice**: 22 flat cell(s) in 3 object(s) - `build/audit/AbandonedShip_CaptainsOffice.png`
  - [ ] (0, 0)-(8, 2), 16 cell(s), tiles 20E 20F 216 217 21B 21C 223 224 2B8 2B9 2F8 300
  - [ ] (0, 3)-(0, 4), 2 cell(s), tiles 3B4 3B5
  - [ ] (3, 5)-(4, 6), 4 cell(s), tiles 20C 20D 214 215
- [ ] **AbandonedShip_Corridors_1F**: 2 flat cell(s) in 1 object(s) - `build/audit/AbandonedShip_Corridors_1F.png`
  - [ ] (7, 0)-(7, 1), 2 cell(s), tiles 201
- [ ] **AbandonedShip_Corridors_B1F**: 73 flat cell(s) in 4 object(s) - `build/audit/AbandonedShip_Corridors_B1F.png`
  - [ ] (0, 0)-(12, 4), 53 cell(s), tiles 221 222 223 224 225 226 229 22A 22B 22C 22D 22E 230 231 232 233 29F 2A7
  - [ ] (12, 6), 1 cell(s), tiles 2AC
  - [ ] (0, 8), 1 cell(s), tiles 2AD
  - [ ] (4, 8)-(12, 9), 18 cell(s), tiles 230 231 232
- [ ] **AbandonedShip_Deck**: 308 flat cell(s) in 3 object(s) - `build/audit/AbandonedShip_Deck.png`
  - [ ] (0, 0)-(22, 15), 273 cell(s), tiles 210 218 21F 220 227 228 22A 22F 260 262 265 266 268 269 26A 2A1 2C3 2C4 2C5 2CB 2CD 35D 3B3 3C8 3C9 3CA 3CB
  - [ ] (11, 10), 1 cell(s), tiles 3C8
  - [ ] (15, 11)-(22, 15), 34 cell(s), tiles 218 220 265 269 3C8 3C9 3CA 3CB
- [ ] **AbandonedShip_HiddenFloorCorridors**: 74 flat cell(s) in 5 object(s) - `build/audit/AbandonedShip_HiddenFloorCorridors.png`
  - [ ] (0, 0)-(12, 1), 26 cell(s), tiles 208 209 210 211 2A8 2A9 2B0 2B1
  - [ ] (0, 3), 1 cell(s), tiles 2AD
  - [ ] (2, 4)-(10, 8), 45 cell(s), tiles 222 223 224 225 226 22A 22B 22C 22D 22E 230 231 232 233
  - [ ] (12, 4), 1 cell(s), tiles 2AC
  - [ ] (0, 5), 1 cell(s), tiles 2AD
- [ ] **AbandonedShip_HiddenFloorRooms**: 330 flat cell(s) in 9 object(s) - `build/audit/AbandonedShip_HiddenFloorRooms.png`
  - [ ] (0, 0)-(43, 14), 310 cell(s), tiles 201 20F 217 227 22F 235 236 237 23E 23F 246 247 24E 24F 256 257 25E 25F 262 263 268 295 296 297 299 29A 29D 29E 2A0 2A2 2AA 2AB
  - [ ] (33, 3), 1 cell(s), tiles 262
  - [ ] (3, 4)-(4, 5), 4 cell(s), tiles 256 257 25E 25F
  - [ ] (38, 5), 1 cell(s), tiles 262
  - [ ] (10, 11)-(11, 12), 4 cell(s), tiles 256 257 25E 25F
  - [ ] (25, 11), 1 cell(s), tiles 262
  - [ ] (35, 11)-(36, 12), 4 cell(s), tiles 256 257 25E 25F
  - [ ] (16, 13)-(17, 14), 4 cell(s), tiles 256 257 25E 25F
  - [ ] (33, 14), 1 cell(s), tiles 262
- [ ] **AbandonedShip_Room_B1F**: 10 flat cell(s) in 2 object(s) - `build/audit/AbandonedShip_Room_B1F.png`
  - [ ] (0, 0)-(0, 7), 8 cell(s), tiles 236 23E
  - [ ] (8, 0)-(8, 1), 2 cell(s), tiles 237 23F
- [ ] **AbandonedShip_Rooms2_1F**: 21 flat cell(s) in 3 object(s) - `build/audit/AbandonedShip_Rooms2_1F.png`
  - [ ] (0, 0)-(0, 16), 17 cell(s), tiles 201 236 23E
  - [ ] (8, 0)-(8, 1), 2 cell(s), tiles 237 23F
  - [ ] (8, 9)-(8, 10), 2 cell(s), tiles 237 23F
- [ ] **AbandonedShip_Rooms2_B1F**: 79 flat cell(s) in 2 object(s) - `build/audit/AbandonedShip_Rooms2_B1F.png`
  - [ ] (0, 0)-(17, 7), 71 cell(s), tiles 227 22F 236 237 23E 23F 240 241 242 243 244 245 246 247 248 249 24A 24B 24C 24D 24E 24F 250 251 254 255 256 257 258 259 25C 25D 25E 25F 2AA 2AB
  - [ ] (7, 5)-(10, 7), 8 cell(s), tiles 23E 23F 262 2AB
- [ ] **AbandonedShip_Rooms_1F**: 41 flat cell(s) in 5 object(s) - `build/audit/AbandonedShip_Rooms_1F.png`
  - [ ] (0, 0)-(0, 16), 17 cell(s), tiles 201 236 23E
  - [ ] (8, 0)-(9, 12), 17 cell(s), tiles 201 236 237 23E 23F 246 24E
  - [ ] (17, 0)-(17, 1), 2 cell(s), tiles 237 23F
  - [ ] (17, 9)-(17, 10), 2 cell(s), tiles 237 23F
  - [ ] (9, 14)-(9, 16), 3 cell(s), tiles 23E
- [ ] **AbandonedShip_Rooms_B1F**: 115 flat cell(s) in 5 object(s) - `build/audit/AbandonedShip_Rooms_B1F.png`
  - [ ] (0, 0)-(3, 7), 19 cell(s), tiles 236 23E 240 248 250 251 258 259 26B 273 295 29D 2AB
  - [ ] (5, 0)-(21, 7), 72 cell(s), tiles 201 227 22F 240 245 248 24D 250 251 254 255 258 259 25C 25D 263 26B 26D 273 275 295 296 297 29D 29E 2AA
  - [ ] (23, 0)-(26, 7), 19 cell(s), tiles 237 23F 245 24D 254 255 25C 25D 26D 275 296 29E 2AA
  - [ ] (2, 5)-(3, 6), 4 cell(s), tiles 256 257 25E 25F
  - [ ] (24, 6), 1 cell(s), tiles 262
- [ ] **AbandonedShip_Underwater1**: 16 flat cell(s) in 1 object(s) - `build/audit/AbandonedShip_Underwater1.png`
  - [ ] (0, 0)-(7, 1), 16 cell(s), tiles 2CC 2CD 2CE 2D4 2D5 2D6 2D7
- [ ] **AbandonedShip_Underwater2**: 41 flat cell(s) in 1 object(s) - `build/audit/AbandonedShip_Underwater2.png`
  - [ ] (0, 0)-(20, 1), 41 cell(s), tiles 2CC 2CD 2CE 2D4 2D5 2D6 2D7 2D8 2D9 2DA 2DB 2DD

1132 blocked cell(s) still flat in this area.
<!-- /audit:AbandonedShip -->
