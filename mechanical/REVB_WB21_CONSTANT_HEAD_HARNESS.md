# PX-1 Rev.B — WB21 constant-length local camera harness

Date: 2026-09-11  
Status: **PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**

## 1. Scope

WB21 re-solves the camera-head local harness after the WB20 wet-bay/TILT correction.

The objective is not to find a different shortest cable path for LOW/MID/HIGH. A real harness has one fixed cut length. WB21 therefore creates one controlled flex zone at the lower lift pivot while the rest of the harness is statically supported.

No change is made to:
- 3 axles / 6 wheels;
- X50 / X150 / X250 wheel stations;
- ten Z50 side gears;
- rear X250 drive input;
- manual four-bar lift;
- sealed Ø52 camera/TILT/ROLL architecture;
- six functional head circuits;
- main six-core inspection tether.

## 2. Source-derived principle

The MiniCam source package supports the architecture, not PX-1 dimensions:

- `DRW-002-752 LIFT HOUSING` contains a separate `FSS-002-085 Camera Connector`, `FAL-002-071 Housing Cameraconnector` and `CAB-002-461 cable fitting M12x1.5 d3.5-5mm`;
- `ASS-002-890 Top Housing Assy` independently contains both a camera connector and an M12 gland;
- `ASS-003-121 Lift Arm Assy` contains a dedicated lift-arm cover.

PX-1 interpretation:

`sealed body ingress -> fixed support/fairlead -> one controlled pivot flex -> protected static arm run -> removable head connector`.

This supersedes the WB19 idea of storing a large free loop above the controller saddle.

## 3. Cable selection

Technical baseline candidate:

**igus chainflex CF99.PLUS.01.08**

Controlled manufacturer data used by WB21:
- construction: `(8 x 0.14 mm2)C`;
- shielded;
- TPE jacket;
- outside diameter: 8.0 mm;
- maximum conductor resistance at 20 C: 140 ohm/km;
- catalogue current reference for one 0.14 mm2 conductor: 2.5 A at 30 C, subject to installation/loaded-core derating;
- at -25...+80 C: minimum radius 3xd for 5 million double strokes, 5xd for 40 million, 6xd for 100 million.

WB21 uses **R >= 40 mm = 5xd** as the geometry gate. This is deliberately much more cycle capability than the manual lift requires.

### Important sourcing correction

Do not use `CF99.PLUS.02.04` to infer an eight-core 0.25 mm2 cable. Current public igus marketing tables and controlled data sheets have shown contradictory core-count text for that article. WB21 does not depend on it.

`CF99.PLUS.01.08` is the only CF99.PLUS candidate used here because its 8 x 0.14 construction and Ø8 mm envelope are consistent in the controlled data used for the calculation.

### Procurement hold

The cable is technically controlled and currently an active igus family, but a source compliant with the PX-1 ChipDip/marketplace procurement rule has not yet been frozen. Therefore this is a **technical baseline, not a released purchase item**.

Do not silently replace it with an unknown marketplace drag-chain cable merely because the printed cross-section is similar.

## 4. Eight-core allocation

The six functional circuits remain unchanged while power uses parallel conductors:

- two 0.14 mm2 cores in parallel -> `+12V_HEAD`;
- two 0.14 mm2 cores in parallel -> `GND_HEAD`;
- one core -> `HEAD_UART_TX`;
- one core -> `HEAD_UART_RX`;
- one core -> `CVBS_SIGNAL`;
- one core -> `CVBS_RETURN`;
- overall braid -> shield/functional EMC bond as qualified; **never DC power return**.

At the six-contact head connector, the two +12 V conductors terminate to the one +12 V contact and the two GND conductors to the one GND contact. Purchased SP13 hardware must prove that this doubled termination fits and survives wet vibration before release.

## 5. Electrical screen

Conservative transient head-current reservation:
- TILT N20 stall: 1.10 A;
- ROLL N20 stall: 1.10 A;
- RunCam reservation: 0.12 A;
- two LED channels: 0.60 A;
- total screen: **2.92 A**.

With two equal 0.14 mm2 conductors in parallel per power leg:
- current/core at the 2.92 A transient = about 1.46 A;
- effective resistance of one power leg = 70 ohm/km;
- for a conservative 0.40 m complete local harness, loop resistance = about 0.056 ohm;
- voltage drop at 2.92 A = about 0.164 V, or 1.36% of 12 V.

This is an electrical screen only. Final current distribution, contact heating and motor-start video noise require the physical harness.

## 6. Body ingress

Selected mechanical candidate:

**LAPP SKINTOP MS-M M16x1.5, article 53112010**

Controlled dimensions used:
- cable range: 4.5...10 mm;
- M16x1.5;
- wrench size 20 mm;
- outer body envelope approximately Ø22 mm;
- thread length 7 mm;
- manufacturer protection class IP68/IP69.

Because LAPP tables/data-sheet revisions show 31...33 mm total-length presentation, WB21 deliberately screens a conservative **26 mm external length** beyond the threaded mounting plane.

Current mounting screen datum:
- pressure-roof mount: `X180 / Y0 / Z60 mm`;
- fixed fairlead: `X190.5097 / Y-13 / Z95.7383 mm`;
- conservative gland end: `X186.9257 / Y-8.5668 / Z83.5509 mm`.

Ideal DN150 clearances:
- gland envelope: ~38.82 mm;
- Ø26 mounting-boss screen: ~56.00 mm;
- fixed cable section to fairlead: ~28.32 mm.

The M16 boss is a new pressure-boundary feature and is **not machining released** until pressure analysis/proof and leak testing are complete.

## 7. Controlled flex geometry

The moving clamp is placed on the inner side of the lower left lift arm:
- distance from lower body pivot: **60.0 mm**;
- Y datum: **-13.0 mm**.

The fixed fairlead is intentionally offset from the pivot axle so the Ø8 cable does not occupy the Ø8-class pivot hardware envelope.

Free flex centreline length:
- nominal: **52.8 mm**;
- assembly screen tolerance: **±0.5 mm**.

### LOW
- moving clamp: `X141.7784 / Y-13 / Z77.5 mm`;
- endpoint chord: 52.0324 mm;
- nominal circular free-flex radius: 89.19 mm;
- radius with +0.5 mm worst slack: 70.30 mm;
- cable-to-wet-deck screen: 22.81 mm;
- ideal DN150 cable clearance: 25.42 mm.

### MID
- moving clamp: `X141.4253 / Y-13 / Z105.0 mm`;
- endpoint chord: 49.9506 mm;
- nominal radius: **46.01 mm**;
- radius with +0.5 mm worst slack: **42.99 mm**.

MID is the bend-radius limiting position. It still exceeds the 40 mm / 5xd WB21 gate.

### HIGH
- moving clamp: `X167.6002 / Y-13 / Z142.5 mm`;
- endpoint chord: 52.0721 mm;
- nominal radius: 91.60 mm;
- radius with +0.5 mm worst slack: 71.43 mm.

HIGH is not a DN150 operating position. Its negative ideal DN150 pipe-clearance number is expected and is not a WB21 failure.

## 8. Executed collision screen

CadQuery 2.8.0 checks were run with:
- four lift arms at LOW/MID/HIGH;
- ten Z50 gear solids;
- WB20 gas-spring geometry;
- Ø22 gland envelope;
- Ø26 pressure-boss envelope;
- Ø12 fixed guide/support envelope;
- Ø8 dynamic cable;
- WB20 fixed camera/yoke package;
- moving camera package across TILT `-105...+105 deg` sampled every 1 degree.

Executed result:
- dynamic cable vs all four arms: 0 mm3;
- cable vs Z50: 0 mm3;
- cable vs gas spring: 0 mm3;
- gland/boss/support vs lift arms: 0 mm3;
- support vs gas spring: 0 mm3;
- cable vs fixed camera package: 0 mm3;
- cable vs moving camera throughout the 1-degree TILT sweep: 0 mm3.

Status: **PASS_SCREEN**.

## 9. Why this is better than WB19

WB19 proved that a free cable routed over the upper body could be made geometrically possible, but it required a large change in shortest path between lift positions and left only small dirty-pipe margins.

WB21 instead localizes motion to one small flex zone next to the lift pivot. The rest of the cable can be clamped to the arm and therefore moves as part of the linkage rather than storing/removing a large loop.

This is both closer to the source MiniCam service philosophy and easier to protect with a lift-arm cover.

## 10. Remaining HOLDs

1. obtain `CF99.PLUS.01.08` from an allowed procurement source or explicitly approve a special-cable sourcing exception;
2. measure purchased cable OD and real free-bend behaviour;
3. set 52.8 ±0.5 mm free length on a physical LOW/MID/HIGH jig;
4. perform wet/grit cycle test; project minimum is 500 lift cycles, with inspection for jacket polish/cracking/migration;
5. detail fairlead material, dirt drainage, fasteners and anti-chafe radius;
6. pressure-proof the M16 body boss and leak-test the assembled gland;
7. prove doubled +12/GND terminations fit the selected SP13 contacts;
8. qualify shield bond and CVBS with TILT/ROLL motor starts and LED PWM;
9. run physical dirty/oval DN150 sweep;
10. WB22 must close the **static** run from the moving clamp to the final camera connector without changing the WB21 pivot-flex datum unless a demonstrated collision requires it.

## 11. Next work block

**WB22 — moving-arm static harness / final SP13 interface.**

WB22 will design:
- cable support along the lower lift arm;
- lift-arm cover / anti-snag protection;
- transition from `Y=-13` flex clamp to the camera-side connector;
- final SP13/SP1324 decision based on actual purchasable six-contact hardware;
- service replacement sequence without opening the crawler pressure body.

## Change log

### 2026-09-11 — WB21
- discarded the WB19 upper-body slack-loop concept for manufacturing;
- recovered MiniCam's separate camera-connector + lift-housing-gland principle from source drawings;
- rejected unverified `CF10.02.06` and conflicting `CF99.PLUS.02.04` assumptions;
- selected `CF99.PLUS.01.08` as the controlled technical cable candidate;
- allocated two parallel conductors each to +12 V and GND;
- selected LAPP 53112010 M16 gland as body-ingress candidate;
- optimized fixed fairlead and 60 mm moving-clamp datum;
- established 52.8 ±0.5 mm constant free-flex length;
- executed LOW/MID/HIGH solid collisions and full 1-degree TILT cable sweep;
- retained manufacturing and procurement holds.
