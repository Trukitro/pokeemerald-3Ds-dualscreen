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
- [x] **LittlerootTown_MaysHouse_1F**: nothing blocked lies flat that is not left so on purpose
  - left flat, 2 cell(s): the moving boxes of the game's first minutes, which a script puts there
  - [ ] painted on the floor: pixels (67, 91)-(157, 141), 2452 px
  - [ ] painted on the floor: pixels (17, 129)-(47, 143), 420 px
- [x] **LittlerootTown_BrendansHouse_1F**: nothing blocked lies flat that is not left so on purpose
  - left flat, 2 cell(s): the moving boxes of the game's first minutes, which a script puts there
  - [ ] painted on the floor: pixels (19, 91)-(109, 141), 2212 px
  - [ ] painted on the floor: pixels (129, 129)-(159, 143), 420 px
- [x] **LittlerootTown_ProfessorBirchsLab**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (96, 192)-(128, 208), 512 px
  - [ ] painted on the floor: pixels (16, 128)-(64, 136), 90 px
  - [ ] painted on the floor: pixels (80, 32)-(96, 40), 30 px
  - [ ] painted on the floor: pixels (160, 32)-(176, 40), 30 px
- [x] **LittlerootTown_MaysHouse_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (19, 51)-(77, 109), 3364 px
- [x] **LittlerootTown_BrendansHouse_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (67, 51)-(125, 109), 3364 px

0 blocked cell(s) still flat in this area.
<!-- /audit:LittlerootTown -->

<!-- audit:PetalburgCity -->
### PetalburgCity - audit of 2026-10-07

- [x] **PetalburgCity**: nothing blocked lies flat
- [x] **PetalburgCity_House1**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (19, 51)-(125, 109), 4579 px
  - [ ] painted on the floor: pixels (48, 128)-(80, 144), 512 px
  - [ ] painted on the floor: pixels (64, 35)-(128, 40), 320 px
  - [ ] painted on the floor: pixels (64, 43)-(128, 48), 320 px
- [x] **PetalburgCity_WallysHouse**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
  - [ ] painted on the floor: pixels (48, 35)-(112, 40), 320 px
  - [ ] painted on the floor: pixels (48, 43)-(112, 48), 320 px
- [x] **PetalburgCity_Gym**: nothing blocked lies flat that is not left so on purpose
  - left flat, 4 cell(s): the leader's mat: the corners of its low border
  - [ ] painted on the floor: pixels (24, 1504)-(120, 1568), 6144 px
  - [ ] painted on the floor: pixels (24, 1296)-(120, 1360), 6144 px
  - [ ] painted on the floor: pixels (24, 256)-(120, 320), 6144 px
  - [ ] painted on the floor: pixels (24, 672)-(120, 736), 6144 px
  - [ ] painted on the floor: pixels (24, 1088)-(120, 1152), 6144 px
  - [ ] painted on the floor: pixels (24, 464)-(120, 528), 6144 px
  - [ ] painted on the floor: pixels (24, 880)-(120, 944), 6144 px
  - [ ] painted on the floor: pixels (38, 37)-(106, 53), 1088 px
  - [ ] painted on the floor: pixels (65, 1777)-(95, 1791), 420 px
  - [ ] painted on the floor: pixels (49, 58)-(95, 60), 92 px
  - [ ] painted on the floor: pixels (49, 62)-(95, 64), 92 px
  - [ ] painted on the floor: pixels (96, 35)-(110, 61), 91 px
- [x] **PetalburgCity_PokemonCenter_1F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (96, 128)-(128, 144), 512 px
  - [ ] painted on the floor: pixels (192, 32)-(208, 35), 48 px
  - [ ] painted on the floor: pixels (97, 81)-(103, 87), 36 px
  - [ ] painted on the floor: pixels (97, 89)-(103, 95), 36 px
  - [ ] painted on the floor: pixels (121, 81)-(127, 87), 36 px
  - [ ] painted on the floor: pixels (129, 89)-(135, 95), 36 px
  - [ ] painted on the floor: pixels (113, 81)-(119, 87), 36 px
  - [ ] painted on the floor: pixels (121, 89)-(127, 95), 36 px
  - [ ] painted on the floor: pixels (105, 81)-(111, 87), 36 px
  - [ ] painted on the floor: pixels (113, 73)-(119, 79), 36 px
  - [ ] painted on the floor: pixels (105, 73)-(111, 79), 36 px
  - [ ] painted on the floor: pixels (89, 89)-(95, 95), 36 px
- [x] **PetalburgCity_House2**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
  - [ ] painted on the floor: pixels (32, 43)-(128, 48), 480 px
  - [ ] painted on the floor: pixels (32, 35)-(128, 40), 480 px
- [x] **PetalburgCity_Mart**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
- [x] **PetalburgCity_PokemonCenter_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (82, 90)-(94, 96), 44 px
  - [ ] painted on the floor: pixels (155, 84)-(167, 90), 42 px
  - [ ] painted on the floor: pixels (161, 103)-(173, 109), 42 px
  - [ ] painted on the floor: pixels (145, 73)-(151, 79), 32 px
  - [ ] painted on the floor: pixels (65, 65)-(71, 71), 32 px
  - [ ] painted on the floor: pixels (73, 65)-(79, 71), 32 px
  - [ ] painted on the floor: pixels (145, 81)-(151, 87), 32 px
  - [ ] painted on the floor: pixels (65, 73)-(71, 79), 32 px
  - [ ] painted on the floor: pixels (73, 73)-(79, 79), 32 px
  - [ ] painted on the floor: pixels (17, 65)-(23, 71), 32 px
  - [ ] painted on the floor: pixels (25, 65)-(31, 71), 32 px
  - [ ] painted on the floor: pixels (169, 65)-(175, 71), 32 px

0 blocked cell(s) still flat in this area.
<!-- /audit:PetalburgCity -->

<!-- audit:Route104 -->
### Route104 - audit of 2026-10-07

- [x] **Route104**: nothing blocked lies flat that is not left so on purpose
  - left flat, 1 cell(s): a patch of bare soil the cartridge blocks
  - left flat, 9 cell(s): a small tree's crown top drawn over the fence: the tree south of it stands
  - left flat, 1 cell(s): a corner of the cliff's foot
- [x] **Route104_MrBrineysHouse**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (16, 128)-(176, 144), 2248 px
  - [ ] painted on the floor: pixels (145, 83)-(159, 96), 156 px
  - [ ] painted on the floor: pixels (48, 32)-(128, 36), 129 px
  - [ ] painted on the floor: pixels (48, 46)-(128, 48), 120 px
- [x] **Route104_PrettyPetalFlowerShop**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (32, 128)-(64, 144), 512 px
  - [ ] painted on the floor: pixels (98, 48)-(110, 62), 136 px
  - [ ] painted on the floor: pixels (162, 48)-(174, 62), 136 px
  - [ ] painted on the floor: pixels (80, 32)-(96, 40), 128 px
  - [ ] painted on the floor: pixels (32, 32)-(48, 39), 108 px
  - [ ] painted on the floor: pixels (104, 32)-(112, 39), 54 px

0 blocked cell(s) still flat in this area.
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
- [x] **RustboroCity_Gym**: nothing blocked lies flat that is not left so on purpose
  - left flat, 4 cell(s): the leader's dais: the corners of its low border
  - [ ] painted on the floor: pixels (80, 304)-(112, 320), 512 px
  - [ ] painted on the floor: pixels (111, 39)-(128, 64), 157 px
  - [ ] painted on the floor: pixels (48, 39)-(65, 64), 139 px
  - [ ] painted on the floor: pixels (73, 36)-(103, 47), 96 px
- [x] **RustboroCity_Flat1_1F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (135, 55)-(208, 105), 2022 px
  - [ ] painted on the floor: pixels (96, 112)-(128, 128), 512 px
  - [ ] painted on the floor: pixels (153, 32)-(208, 47), 498 px
  - [ ] painted on the floor: pixels (135, 53)-(208, 54), 73 px
  - [ ] painted on the floor: pixels (135, 108)-(208, 109), 73 px
  - [ ] painted on the floor: pixels (135, 106)-(208, 107), 73 px
  - [ ] painted on the floor: pixels (135, 51)-(208, 52), 73 px
  - [ ] painted on the floor: pixels (58, 80)-(62, 96), 56 px
  - [ ] painted on the floor: pixels (18, 48)-(22, 64), 56 px
  - [ ] painted on the floor: pixels (131, 55)-(132, 105), 50 px
  - [ ] painted on the floor: pixels (133, 55)-(134, 105), 50 px
  - [ ] painted on the floor: pixels (73, 32)-(80, 39), 49 px
- [x] **RustboroCity_Mart**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
- [x] **RustboroCity_PokemonCenter_1F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (96, 128)-(128, 144), 512 px
  - [ ] painted on the floor: pixels (192, 32)-(208, 35), 48 px
  - [ ] painted on the floor: pixels (97, 81)-(103, 87), 36 px
  - [ ] painted on the floor: pixels (97, 89)-(103, 95), 36 px
  - [ ] painted on the floor: pixels (121, 81)-(127, 87), 36 px
  - [ ] painted on the floor: pixels (129, 89)-(135, 95), 36 px
  - [ ] painted on the floor: pixels (113, 81)-(119, 87), 36 px
  - [ ] painted on the floor: pixels (121, 89)-(127, 95), 36 px
  - [ ] painted on the floor: pixels (105, 81)-(111, 87), 36 px
  - [ ] painted on the floor: pixels (113, 73)-(119, 79), 36 px
  - [ ] painted on the floor: pixels (105, 73)-(111, 79), 36 px
  - [ ] painted on the floor: pixels (89, 89)-(95, 95), 36 px
- [x] **RustboroCity_PokemonSchool**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (80, 160)-(112, 176), 512 px
  - [ ] painted on the floor: pixels (112, 48)-(176, 54), 384 px
  - [ ] painted on the floor: pixels (16, 48)-(80, 54), 384 px
  - [ ] painted on the floor: pixels (16, 96)-(32, 104), 82 px
  - [ ] painted on the floor: pixels (48, 160)-(64, 168), 82 px
  - [ ] painted on the floor: pixels (128, 160)-(144, 168), 82 px
  - [ ] painted on the floor: pixels (128, 128)-(143, 136), 82 px
  - [ ] painted on the floor: pixels (48, 128)-(64, 136), 82 px
  - [ ] painted on the floor: pixels (48, 96)-(64, 104), 82 px
  - [ ] painted on the floor: pixels (128, 96)-(144, 104), 82 px
  - [ ] painted on the floor: pixels (160, 128)-(176, 136), 82 px
  - [ ] painted on the floor: pixels (160, 160)-(176, 168), 82 px
- [x] **RustboroCity_DevonCorp_1F**: nothing blocked lies flat that is not left so on purpose
  - left flat, 6 cell(s): an alcove's side wall: its thickness, drawn as a strip beside the wall that stands
  - [ ] painted on the floor: pixels (81, 129)-(111, 143), 420 px
  - [ ] painted on the floor: pixels (204, 0)-(208, 48), 192 px
  - [ ] painted on the floor: pixels (44, 0)-(48, 48), 192 px
- [x] **RustboroCity_House1**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (135, 55)-(185, 89), 1696 px
  - [ ] painted on the floor: pixels (80, 112)-(112, 128), 512 px
  - [ ] painted on the floor: pixels (137, 32)-(192, 48), 378 px
  - [ ] painted on the floor: pixels (16, 32)-(64, 47), 291 px
  - [ ] painted on the floor: pixels (149, 33)-(171, 40), 152 px
  - [ ] painted on the floor: pixels (34, 64)-(38, 96), 112 px
  - [ ] painted on the floor: pixels (106, 64)-(110, 80), 56 px
  - [ ] painted on the floor: pixels (135, 53)-(185, 54), 50 px
  - [ ] painted on the floor: pixels (135, 92)-(185, 93), 50 px
  - [ ] painted on the floor: pixels (135, 51)-(185, 52), 50 px
  - [ ] painted on the floor: pixels (135, 90)-(185, 91), 50 px
  - [ ] painted on the floor: pixels (73, 32)-(80, 39), 49 px
- [x] **RustboroCity_CuttersHouse**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (23, 55)-(73, 105), 2496 px
  - [ ] painted on the floor: pixels (80, 128)-(112, 144), 512 px
  - [ ] painted on the floor: pixels (121, 32)-(160, 47), 323 px
  - [ ] painted on the floor: pixels (16, 32)-(63, 47), 246 px
  - [ ] painted on the floor: pixels (114, 80)-(118, 96), 56 px
  - [ ] painted on the floor: pixels (23, 106)-(73, 107), 50 px
  - [ ] painted on the floor: pixels (21, 55)-(22, 105), 50 px
  - [ ] painted on the floor: pixels (23, 51)-(73, 52), 50 px
  - [ ] painted on the floor: pixels (19, 55)-(20, 105), 50 px
  - [ ] painted on the floor: pixels (74, 55)-(75, 105), 50 px
  - [ ] painted on the floor: pixels (23, 108)-(73, 109), 50 px
  - [ ] painted on the floor: pixels (76, 55)-(77, 105), 50 px
- [x] **RustboroCity_House2**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (55, 55)-(137, 105), 2382 px
  - [ ] painted on the floor: pixels (80, 128)-(112, 144), 512 px
  - [ ] painted on the floor: pixels (89, 32)-(144, 47), 340 px
  - [ ] painted on the floor: pixels (16, 32)-(48, 47), 286 px
  - [ ] painted on the floor: pixels (153, 32)-(176, 47), 121 px
  - [ ] painted on the floor: pixels (55, 108)-(137, 109), 82 px
  - [ ] painted on the floor: pixels (55, 51)-(137, 52), 82 px
  - [ ] painted on the floor: pixels (55, 53)-(137, 54), 82 px
  - [ ] painted on the floor: pixels (55, 106)-(137, 107), 82 px
  - [ ] painted on the floor: pixels (51, 55)-(52, 105), 50 px
  - [ ] painted on the floor: pixels (138, 55)-(139, 105), 50 px
  - [ ] painted on the floor: pixels (53, 55)-(54, 105), 50 px
- [x] **RustboroCity_Flat2_1F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (32, 128)-(64, 144), 512 px
  - [ ] painted on the floor: pixels (169, 32)-(208, 47), 323 px
  - [ ] painted on the floor: pixels (186, 48)-(190, 80), 112 px
  - [ ] painted on the floor: pixels (130, 48)-(134, 80), 112 px
  - [ ] painted on the floor: pixels (97, 40)-(104, 47), 49 px
  - [ ] painted on the floor: pixels (185, 128)-(192, 135), 49 px
  - [ ] painted on the floor: pixels (25, 32)-(32, 39), 49 px
  - [ ] painted on the floor: pixels (105, 128)-(112, 135), 49 px
  - [ ] painted on the floor: pixels (97, 88)-(104, 95), 49 px
  - [ ] painted on the floor: pixels (137, 128)-(144, 135), 49 px
  - [ ] painted on the floor: pixels (105, 96)-(112, 103), 49 px
  - [ ] painted on the floor: pixels (145, 136)-(152, 143), 49 px
- [x] **RustboroCity_House3**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (55, 55)-(137, 105), 2382 px
  - [ ] painted on the floor: pixels (80, 128)-(112, 144), 512 px
  - [ ] painted on the floor: pixels (89, 32)-(144, 47), 340 px
  - [ ] painted on the floor: pixels (16, 32)-(48, 47), 286 px
  - [ ] painted on the floor: pixels (153, 32)-(176, 47), 121 px
  - [ ] painted on the floor: pixels (55, 108)-(137, 109), 82 px
  - [ ] painted on the floor: pixels (55, 51)-(137, 52), 82 px
  - [ ] painted on the floor: pixels (55, 53)-(137, 54), 82 px
  - [ ] painted on the floor: pixels (55, 106)-(137, 107), 82 px
  - [ ] painted on the floor: pixels (51, 55)-(52, 105), 50 px
  - [ ] painted on the floor: pixels (138, 55)-(139, 105), 50 px
  - [ ] painted on the floor: pixels (53, 55)-(54, 105), 50 px
- [x] **RustboroCity_Flat1_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (119, 71)-(185, 121), 1760 px
  - [ ] painted on the floor: pixels (137, 32)-(208, 48), 433 px
  - [ ] painted on the floor: pixels (149, 33)-(187, 40), 264 px
  - [ ] painted on the floor: pixels (90, 64)-(94, 96), 112 px
  - [ ] painted on the floor: pixels (119, 67)-(185, 68), 66 px
  - [ ] painted on the floor: pixels (119, 122)-(185, 123), 66 px
  - [ ] painted on the floor: pixels (119, 69)-(185, 70), 66 px
  - [ ] painted on the floor: pixels (119, 124)-(185, 125), 66 px
  - [ ] painted on the floor: pixels (18, 64)-(22, 80), 56 px
  - [ ] painted on the floor: pixels (115, 71)-(116, 121), 50 px
  - [ ] painted on the floor: pixels (188, 71)-(189, 121), 50 px
  - [ ] painted on the floor: pixels (186, 71)-(187, 121), 50 px
- [x] **RustboroCity_PokemonCenter_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (82, 90)-(94, 96), 44 px
  - [ ] painted on the floor: pixels (155, 84)-(167, 90), 42 px
  - [ ] painted on the floor: pixels (161, 103)-(173, 109), 42 px
  - [ ] painted on the floor: pixels (145, 73)-(151, 79), 32 px
  - [ ] painted on the floor: pixels (65, 65)-(71, 71), 32 px
  - [ ] painted on the floor: pixels (73, 65)-(79, 71), 32 px
  - [ ] painted on the floor: pixels (145, 81)-(151, 87), 32 px
  - [ ] painted on the floor: pixels (65, 73)-(71, 79), 32 px
  - [ ] painted on the floor: pixels (73, 73)-(79, 79), 32 px
  - [ ] painted on the floor: pixels (17, 65)-(23, 71), 32 px
  - [ ] painted on the floor: pixels (25, 65)-(31, 71), 32 px
  - [ ] painted on the floor: pixels (169, 65)-(175, 71), 32 px
- [x] **RustboroCity_DevonCorp_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (64, 32)-(224, 48), 2160 px
  - [ ] painted on the floor: pixels (256, 32)-(288, 48), 432 px
  - [ ] painted on the floor: pixels (16, 32)-(32, 64), 432 px
  - [ ] painted on the floor: pixels (226, 81)-(238, 95), 98 px
  - [ ] painted on the floor: pixels (34, 97)-(46, 111), 98 px
  - [ ] painted on the floor: pixels (98, 129)-(110, 143), 98 px
  - [ ] painted on the floor: pixels (98, 81)-(110, 95), 98 px
  - [ ] painted on the floor: pixels (50, 97)-(62, 111), 98 px
  - [ ] painted on the floor: pixels (226, 129)-(238, 143), 98 px
  - [ ] painted on the floor: pixels (162, 81)-(174, 95), 98 px
  - [ ] painted on the floor: pixels (162, 129)-(174, 143), 98 px
  - [ ] painted on the floor: pixels (18, 81)-(30, 95), 98 px
- [x] **RustboroCity_Flat2_2F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (96, 32)-(127, 47), 136 px
  - [ ] painted on the floor: pixels (178, 64)-(182, 80), 56 px
  - [ ] painted on the floor: pixels (177, 40)-(184, 47), 49 px
  - [ ] painted on the floor: pixels (185, 128)-(192, 135), 49 px
  - [ ] painted on the floor: pixels (105, 128)-(112, 135), 49 px
  - [ ] painted on the floor: pixels (97, 88)-(104, 95), 49 px
  - [ ] painted on the floor: pixels (137, 128)-(144, 135), 49 px
  - [ ] painted on the floor: pixels (105, 96)-(112, 103), 49 px
  - [ ] painted on the floor: pixels (145, 136)-(152, 143), 49 px
  - [ ] painted on the floor: pixels (153, 32)-(160, 39), 49 px
  - [ ] painted on the floor: pixels (193, 136)-(200, 143), 49 px
  - [ ] painted on the floor: pixels (89, 128)-(96, 135), 49 px
- [x] **RustboroCity_DevonCorp_3F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (64, 32)-(288, 48), 3128 px
  - [ ] painted on the floor: pixels (112, 112)-(192, 120), 616 px
  - [ ] painted on the floor: pixels (80, 72)-(96, 104), 476 px
  - [ ] painted on the floor: pixels (272, 72)-(288, 104), 468 px
  - [ ] painted on the floor: pixels (240, 112)-(272, 120), 250 px
  - [ ] painted on the floor: pixels (16, 32)-(32, 48), 216 px
- [x] **RustboroCity_Flat2_3F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (119, 55)-(185, 73), 1184 px
  - [ ] painted on the floor: pixels (80, 32)-(128, 47), 444 px
  - [ ] painted on the floor: pixels (181, 33)-(208, 40), 188 px
  - [ ] painted on the floor: pixels (169, 32)-(208, 48), 178 px
  - [ ] painted on the floor: pixels (119, 76)-(185, 77), 66 px
  - [ ] painted on the floor: pixels (119, 53)-(185, 54), 66 px
  - [ ] painted on the floor: pixels (119, 74)-(185, 75), 66 px
  - [ ] painted on the floor: pixels (119, 51)-(185, 52), 66 px
  - [ ] painted on the floor: pixels (81, 72)-(88, 79), 49 px
  - [ ] painted on the floor: pixels (97, 40)-(104, 47), 49 px
  - [ ] painted on the floor: pixels (185, 128)-(192, 135), 49 px
  - [ ] painted on the floor: pixels (137, 128)-(144, 135), 49 px

0 blocked cell(s) still flat in this area.
<!-- /audit:RustboroCity -->
