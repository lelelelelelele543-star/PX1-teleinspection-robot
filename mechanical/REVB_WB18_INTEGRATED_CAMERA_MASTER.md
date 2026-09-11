# PX-1 Rev.B — WB18 integrated camera/yoke master

Date: 2026-09-11
Status: **PASS_SCREEN / MANUFACTURING HOLD**

## 0. Mandatory crawler architecture

WB18 is tied to the active PX-1 hard lock:
- 3 wheel stations per side;
- 6 wheels total;
- X50 / X150 / X250;
- rear X250 drive input;
- no 4-wheel / 2-axle interpretation is valid.

The executable WB18 model explicitly instantiates all six wheel references and aborts if the architecture differs.

## 1. Purpose

Replace the earlier camera-envelope-only studies with one executable camera/yoke package containing the current Rev.B hard parts:
- Ø52 x 78 mm optical pressure shell;
- real WB17 TILT side-stack lengths;
- Ø8 fixed pivots, Ø4 bore on cable side;
- 8x16x7 FKM seal envelopes;
- 618/8 8x16x4 bearing envelopes;
- m0.5 Z40 / Ø8 fixed TILT wheel;
- moving worm + N20 TILT drive;
- RunCam Phoenix 2 envelope;
- 2x 6803 ROLL bearings;
- m0.5 z51 ROLL gear + z17 pinion screen;
- N20 ROLL motor envelope;
- SenRing M125-06;
- Ø28 x 3 optical window;
- 6 x 8 mm LED MCPCB footprints on PCD40;
- fixed yoke cheeks and rear bridge;
- WEIPU SP1312/P6-C + operational SP1310/S6II-N plug envelope.

This is still an engineering packaging model. Purchased samples control final machining dimensions.

## 2. TILT side-stack correction

The old ±34 mm yoke-envelope study did not honestly reserve the complete seal/bearing stack.

WB18 uses, per side:
- 8x16x7 seal = 7.0 mm;
- controlled spacer = 1.0 mm;
- 618/8 bearing = 4.0 mm;
- retainer allowance = 1.5 mm;
- additional service/tolerance allowance = 0.5 mm.

Result:
- shell side radius = 26.0 mm;
- rotating boss outer face = |Y| 40.0 mm;
- fixed yoke inner face = |Y| 40.75 mm;
- yoke centre plane = |Y| 43.5 mm;
- boss/yoke hard gap = 0.75 mm;
- usable side-stack margin after nominal components = 0.5 mm.

This is a justified packaging correction, not an axle-count or drivetrain architecture change.

## 3. TILT drive interpretation

The WB17 fixed-pivot architecture is retained.

Gear side:
- Ø8 pivot is fixed to the yoke;
- m0.5 Z40 / Ø8 wheel is fixed to that pivot;
- worm + N20 are attached to the tilting P3 shell;
- when the worm turns, the moving shell walks around the stationary Z40 while centre distance remains constant.

This resolves the apparent conflict between a fixed pivot and a driven TILT shell without introducing a wet external gear or a TILT slip ring.

Current screen:
- wheel module 0.5;
- Z40;
- screen OD 21.5 mm;
- worm pitch diameter screen 9 mm;
- centre distance screen 14.5 mm;
- wheel centre shifted to Y=-16.75 mm so its inner face remains clear of the central ROLL package while minimizing external pod radius.

The TILT N20/worm live in an **integrated cylindrical P3 bulge**, not a cartridge/cassette:
- OD 18 mm;
- length 56 mm;
- internal screen diameter 15 mm;
- wall class 1.5 mm before local machining/FEA refinement.

## 4. ROLL package result

The following all fit the central Ø47 mm-class dry cavity at envelope level:
- RunCam Phoenix 2 19x19x20;
- two 6803 17x26x5 bearings;
- m0.5 z51 gear OD26.5;
- SenRing M125-06 Ø12.5 x 13.5;
- N20 34x10x10 screen;
- z17 pinion screen.

Validation results:
- component volume outside intended cavity: 0 for every listed ROLL item;
- unintended internal hard collisions: 0;
- Z40 TILT wheel collision with centered ROLL package: 0;
- M125 radial margin through 17 mm bearing ID: 2.25 mm.

The actual motor shaft, connectors, mounting screws and wire exits remain sample-driven.

## 5. Fixed yoke / connector correction

WEIPU SP13 remains **fixed relative to the yoke**, never attached to the ±105° tilting optical shell.

WB18 places the rear bridge above the optical axis:
- bridge centre X ≈ 141.56 mm;
- bridge/connector centre Z = 95 mm;
- SP1312 panel half on the bridge;
- SP1310/S6II operational plug points rearward (+X).

Reason for raising the bridge/connector:
- keep the rigid 49 mm plug out of the TILT sweep;
- reduce likelihood of conflict with the lower wet deck / pressure roof;
- preserve axial service extraction.

Full crawler-body/lift-arm collision with the external LAPP R55 harness is still a separate HOLD. The current operational plug end reaches approximately X204.1 mm and must be checked against the final lift/body solids before release.

## 6. DN150 result

CadQuery 2.8.0 was executed through the complete commanded TILT range:
- -105° ... +105°;
- 1° sampling increment.

Results:
- minimum moving camera hard-part clearance to ideal DN150: **3.0405 mm**;
- worst sampled angle: approximately **-61°**;
- fixed yoke + SP13 hard-part clearance to ideal DN150: **5.3458 mm**;
- unintended moving-vs-fixed collision volume: **0 mm³**.

The 3.04 mm minimum is a screen PASS, not a field-clearance release.

For a 5 mm engineering allowance, the current ideal model provides two safe ranges:
- approximately -105° ... -81°;
- approximately -43° ... +105°.

For a 3 mm allowance, the complete -105° ... +105° range passes.

The non-monotonic 5 mm region is caused by the local TILT-drive bulge sweeping nearest the pipe wall around the -61° sector.

## 7. DN150 operating policy

Do not hard-code a final software limit from the ideal CAD alone.

Prototype sequence:
1. physically build the real TILT housing and purchased components;
2. put the crawler in a representative DN150 tube;
3. map real available TILT angle with wheel tread compressed normally;
4. repeat with representative weld/ovality/debris allowances;
5. then define `DN150_SAFE_TILT_MIN/MAX` or a piecewise prohibited sector if needed.

Full ±105° remains the camera capability for larger pipe classes unless physical tests require a global correction.

## 8. Front stack

WB18 retains:
- optical window Ø28 x 3 mm target;
- six 8 mm-class LED MCPCBs on PCD40;
- illumination fixed to the TILT shell but fixed relative to internal continuous ROLL.

Window O-ring groove, LED retainer screws and final optical separator are still release-HOLD because real screw heads can consume the remaining DN150 margin.

## 9. Release holds

WB18 is not a machining release until:
- exact 618/8 bearings and exact FKM 8x16x7 seals are purchased/measured;
- exact Z40/Ø8 wheel + matched worm are purchased and contact/backlash checked;
- exact N20 bodies/output shafts are measured;
- M125 passes CVBS while rotating;
- SP13 passes installed +0.25 bar pressure and submerged tests;
- real fastener heads, stops and home sensor are added;
- WB16 LAPP 0027429 R55 path/clamps are integrated with the complete lift;
- final master uses real wheel solids, not simple Ø90 wheel cylinders;
- physical DN150 sweep is passed.

## 10. Controlled files

Executable CAD:
`mechanical/cadquery/PX1_WB18_CameraMaster_RevB.py`

Validation:
`mechanical/REV_B_WB18_VALIDATION.json`

Architecture lock:
`docs/PX1_HARD_ARCHITECTURE_LOCK_6W_3AXLE.md`

## Change log

### 2026-09-11 — WB18
- explicitly retained 3 axles / 6 wheels X50/X150/X250;
- replaced the old ±34 yoke envelope with a stack-driven yoke at ±43.5 mm centre planes;
- provided 0.5 mm nominal side-stack service allowance;
- integrated fixed Z40 + moving-worm TILT kinematics;
- converted the TILT-drive outer envelope to a cylindrical integrated P3 pod;
- packed RunCam/6803/Z51/M125/ROLL N20 with zero envelope collisions;
- moved SP13 to a non-TILT upper rear bridge;
- executed full 1° TILT sweep;
- achieved 3.0405 mm minimum ideal-DN150 moving hard clearance and 5.3458 mm fixed-yoke clearance;
- kept physical DN150 and real-part manufacturing release on HOLD.
