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

<!-- audit:SlateportCity -->
### SlateportCity - audit of 2026-10-07

- [ ] **SlateportCity**: 526 flat cell(s) in 28 object(s) - `build/audit/SlateportCity.png`
  - [ ] (15, 3)-(15, 8), 6 cell(s), tiles 141 142 14A
  - [ ] (21, 3)-(21, 8), 6 cell(s), tiles 139 140 148
  - [ ] (25, 7)-(31, 12), 41 cell(s), tiles 268 269 295 296 297 29D 29E 29F 2A5 2A6 2A7 2AD 2AF 2B5 2B6 2B7 2BD 2BE 2BF 2C5 2D7
  - [ ] (3, 8)-(3, 21), 14 cell(s), tiles 141 142 14A
  - [ ] (7, 8)-(13, 12), 31 cell(s), tiles 243 371 372 373 374 375 379 37A 37B 37C 37D 381 382 383 384 385 389 38A 38B 38C 38D 391 392 393 394 395
  - [ ] (16, 9), 1 cell(s), tiles 263
  - [ ] (20, 9), 1 cell(s), tiles 264
  - [ ] (32, 16)-(37, 16), 6 cell(s), tiles 04E
  - [ ] (22, 18)-(24, 26), 11 cell(s), tiles 139 140 245
  - [ ] (1, 21)-(16, 57), 95 cell(s), tiles 045 133 141 142 20B 214 21B 223 22B 23D 240 241 242 248 249 24A 250 251 252 253 254 258 259 25B 25C 27E 28D 2B9 2BA 2BB 32E 32F 336 337 33F 344
  - [ ] (26, 22)-(35, 26), 36 cell(s), tiles 243 245 24D 255 2FB 303 308 309 30A 30B 30C 310 311 312 313 314 318 319 31A 31B 31C 320 321 322 323 324 328 329 32B 32C
  - [ ] (25, 23)-(25, 24), 2 cell(s), tiles 234 255
  - [ ] (25, 23)-(36, 30), 19 cell(s), tiles 23C 24D 25D 2CF 2FE 2FF
  - [ ] (21, 29)-(38, 42), 94 cell(s), tiles 140 148 220 221 222 228 229 22A 23C 245 24D 25D 298 299 29A 29B 2A0 2A1 2A2 2A8 2A9 2AA 2AB 2B0 2B1 2B2 2FF 300 301 302 32D 338 339 33A 340 341 342 346 347 34E 34F 356 357 35E 35F 368 370 378 380
  - [ ] (8, 32), 1 cell(s), tiles 263
  - [ ] (10, 32)-(14, 50), 28 cell(s), tiles 133 13A 142 22B 23F 26B 28E 33E 33F
  - [ ] (12, 32), 1 cell(s), tiles 264
  - [ ] (3, 33)-(7, 39), 21 cell(s), tiles 20B 20C 213 21B 21C 22B 32E 336 33E 344
  - [ ] (9, 34)-(12, 39), 12 cell(s), tiles 20B 213 21B 22B 32F 337 33F
  - [ ] (6, 41)-(8, 43), 5 cell(s), tiles 21B 22B 26C 33E 344
  - [ ] (20, 43)-(32, 51), 28 cell(s), tiles 045 23C 245 25D 2FF 32D
  - [ ] (34, 44)-(36, 46), 9 cell(s), tiles 338 339 33A 340 341 342 348 349 34A
  - [ ] (6, 45)-(8, 47), 6 cell(s), tiles 20C 223 26C 33F 344
  - [ ] (28, 48)-(37, 57), 26 cell(s), tiles 23C 245 24D 255 2B8 2B9 338 339 33A 340 341 342
  - [ ] (8, 50)-(8, 51), 2 cell(s), tiles 223 22B
  - [ ] (12, 51)-(13, 51), 2 cell(s), tiles 21C 26C
  - [ ] (32, 53)-(33, 54), 4 cell(s), tiles 256 257 25E 25F
  - [ ] (20, 54)-(31, 57), 18 cell(s), tiles 047 234 2B8 2B9 2BA
- [x] **SlateportCity_PokemonCenter_1F**: nothing blocked lies flat
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
- [x] **SlateportCity_Mart**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
- [ ] **SlateportCity_SternsShipyard_1F**: 70 flat cell(s) in 10 object(s) - `build/audit/SlateportCity_SternsShipyard_1F.png`
  - [ ] (1, 2), 1 cell(s), tiles 217
  - [ ] (4, 2)-(15, 9), 44 cell(s), tiles 209 20A 20C 20D 210 211 214 215 220 224 233 234 235 236 23B 23C 23D 23E 23F 243 244 245 246 247 24C 24D 24F 255 256 25B 25C 263 264 2D0 2D1 2D2 2D3 2D5 2D6 2D7
  - [ ] (19, 4)-(19, 6), 3 cell(s), tiles 21F 227 22F
  - [ ] (1, 5), 1 cell(s), tiles 24A
  - [ ] (1, 8), 1 cell(s), tiles 24A
  - [ ] (1, 11), 1 cell(s), tiles 24A
  - [ ] (6, 11)-(9, 14), 11 cell(s), tiles 20A 211 21F 227 22F 237
  - [ ] (18, 11)-(19, 13), 6 cell(s), tiles 21F 227 22F
  - [ ] (10, 12), 1 cell(s), tiles 257
  - [ ] (14, 12), 1 cell(s), tiles 257
  - [ ] painted on the floor: pixels (64, 32)-(320, 240), 47432 px
  - [ ] painted on the floor: pixels (32, 224)-(64, 240), 512 px
  - [ ] painted on the floor: pixels (16, 32)-(48, 56), 512 px
  - [ ] painted on the floor: pixels (16, 75)-(32, 96), 335 px
  - [ ] painted on the floor: pixels (16, 123)-(32, 144), 335 px
  - [ ] painted on the floor: pixels (16, 171)-(32, 192), 335 px
  - [ ] painted on the floor: pixels (82, 81)-(94, 95), 128 px
  - [ ] painted on the floor: pixels (18, 97)-(30, 111), 128 px
  - [ ] painted on the floor: pixels (18, 193)-(30, 207), 128 px
  - [ ] painted on the floor: pixels (66, 129)-(78, 143), 128 px
- [ ] **SlateportCity_BattleTentLobby**: 42 flat cell(s) in 7 object(s) - `build/audit/SlateportCity_BattleTentLobby.png`
  - [ ] (0, 0)-(1, 4), 7 cell(s), tiles 202 203 20A 20B 212 21A 222
  - [ ] (7, 0)-(12, 5), 20 cell(s), tiles 206 207 208 20E 20F 216 217 21F 227 26E 26F 277 27C 27D 27E 27F 284 285 286 287
  - [ ] (2, 2)-(5, 5), 11 cell(s), tiles 268 269 270 278 279 27A 27B 280 281 282 283
  - [ ] (0, 8), 1 cell(s), tiles 295
  - [ ] (12, 8), 1 cell(s), tiles 230
  - [ ] (1, 9), 1 cell(s), tiles 228
  - [ ] (11, 9), 1 cell(s), tiles 228
  - [ ] painted on the floor: pixels (112, 0)-(208, 96), 4359 px
  - [ ] painted on the floor: pixels (32, 32)-(96, 104), 2274 px
  - [ ] painted on the floor: pixels (0, 0)-(32, 79), 1751 px
  - [ ] painted on the floor: pixels (96, 144)-(128, 160), 512 px
- [x] **SlateportCity_PokemonFanClub**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (32, 64)-(192, 144), 10752 px
  - [ ] painted on the floor: pixels (96, 160)-(128, 176), 512 px
- [x] **SlateportCity_OceanicMuseum_1F**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (189, 32)-(219, 43), 246 px
  - [ ] painted on the floor: pixels (141, 32)-(171, 43), 246 px
  - [ ] painted on the floor: pixels (181, 41)-(187, 47), 24 px
  - [ ] painted on the floor: pixels (129, 37)-(135, 43), 24 px
  - [ ] painted on the floor: pixels (169, 37)-(175, 43), 24 px
  - [ ] painted on the floor: pixels (77, 33)-(83, 39), 24 px
  - [ ] painted on the floor: pixels (253, 33)-(259, 39), 24 px
  - [ ] painted on the floor: pixels (241, 133)-(247, 139), 24 px
  - [ ] painted on the floor: pixels (81, 37)-(87, 43), 24 px
  - [ ] painted on the floor: pixels (257, 37)-(263, 43), 24 px
  - [ ] painted on the floor: pixels (45, 41)-(51, 47), 24 px
  - [ ] painted on the floor: pixels (37, 41)-(43, 47), 24 px
- [x] **SlateportCity_NameRatersHouse**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
  - [ ] painted on the floor: pixels (32, 43)-(128, 48), 480 px
  - [ ] painted on the floor: pixels (32, 35)-(128, 40), 480 px
- [ ] **SlateportCity_Harbor**: 67 flat cell(s) in 2 object(s) - `build/audit/SlateportCity_Harbor.png`
  - [ ] (3, 4)-(22, 10), 29 cell(s), tiles 268 347 34D 34E 356 357
  - [ ] (9, 10)-(22, 14), 38 cell(s), tiles 228 22A 260 2B1 346 355 356 3D8 3D9 3DA 3DB 3DC 3DD 3DE 3DF
  - [ ] painted on the floor: pixels (48, 64)-(368, 240), 41327 px
  - [ ] painted on the floor: pixels (176, 224)-(208, 240), 512 px
  - [ ] painted on the floor: pixels (242, 177)-(254, 191), 126 px
  - [ ] painted on the floor: pixels (146, 177)-(158, 191), 126 px
  - [ ] painted on the floor: pixels (194, 177)-(206, 191), 126 px
- [x] **SlateportCity_House**: nothing blocked lies flat
  - [ ] painted on the floor: pixels (48, 112)-(80, 128), 512 px
  - [ ] painted on the floor: pixels (48, 35)-(112, 40), 320 px
  - [ ] painted on the floor: pixels (48, 43)-(112, 48), 320 px
- [x] **SlateportCity_PokemonCenter_2F**: nothing blocked lies flat
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
- [ ] **SlateportCity_SternsShipyard_2F**: 79 flat cell(s) in 4 object(s) - `build/audit/SlateportCity_SternsShipyard_2F.png`
  - [ ] (7, 3)-(15, 12), 70 cell(s), tiles 205 20C 20D 214 215 228 229 22A 23B 23C 23D 23E 243 244 245 246 24B 24C 24D 24E 250 251 252 255 256 260 263 264 268 269 26A 26B 26C 28D 297 335
  - [ ] (1, 5)-(3, 5), 3 cell(s), tiles 249 24A
  - [ ] (1, 8)-(3, 8), 3 cell(s), tiles 248 24A
  - [ ] (1, 11)-(3, 11), 3 cell(s), tiles 248 24A
  - [ ] painted on the floor: pixels (128, 49)-(256, 223), 19226 px
  - [ ] painted on the floor: pixels (80, 32)-(256, 40), 1408 px
  - [ ] painted on the floor: pixels (16, 72)-(64, 96), 1045 px
  - [ ] painted on the floor: pixels (16, 171)-(64, 192), 1005 px
  - [ ] painted on the floor: pixels (16, 123)-(64, 144), 1005 px
  - [ ] painted on the floor: pixels (16, 32)-(48, 40), 256 px
  - [ ] painted on the floor: pixels (114, 176)-(126, 192), 166 px
  - [ ] painted on the floor: pixels (114, 113)-(126, 127), 128 px
  - [ ] painted on the floor: pixels (18, 97)-(30, 111), 128 px
  - [ ] painted on the floor: pixels (18, 193)-(30, 207), 128 px
  - [ ] painted on the floor: pixels (130, 65)-(142, 79), 128 px
  - [ ] painted on the floor: pixels (50, 193)-(62, 207), 128 px
- [ ] **SlateportCity_OceanicMuseum_2F**: 2 flat cell(s) in 1 object(s) - `build/audit/SlateportCity_OceanicMuseum_2F.png`
  - [ ] (10, 2)-(10, 3), 2 cell(s), tiles 22D 235
  - [ ] painted on the floor: pixels (128, 32)-(179, 67), 900 px
  - [ ] painted on the floor: pixels (237, 32)-(275, 43), 328 px
  - [ ] painted on the floor: pixels (285, 32)-(304, 43), 164 px
  - [ ] painted on the floor: pixels (181, 41)-(187, 47), 24 px
  - [ ] painted on the floor: pixels (237, 129)-(243, 135), 24 px
  - [ ] painted on the floor: pixels (61, 129)-(67, 135), 24 px
  - [ ] painted on the floor: pixels (213, 33)-(219, 39), 24 px
  - [ ] painted on the floor: pixels (205, 33)-(211, 39), 24 px
  - [ ] painted on the floor: pixels (97, 125)-(103, 131), 24 px
  - [ ] painted on the floor: pixels (53, 129)-(59, 135), 24 px
  - [ ] painted on the floor: pixels (21, 33)-(27, 39), 24 px
  - [ ] painted on the floor: pixels (197, 33)-(203, 39), 24 px

786 blocked cell(s) still flat in this area.
<!-- /audit:SlateportCity -->
