# PX-1 Rev.B — WB17 sealed TILT pivots / cable feedthrough

Date: 2026-09-11
Status: ARCHITECTURE FROZEN / PART-LEVEL PROTOTYPE CANDIDATES / FULL CAD SWEEP HOLD

## 0. Crawler architecture lock

All WB17 work belongs to the active **three-axle / six-wheel PX-1 crawler**:
- X50 front wheel station;
- X150 centre wheel station;
- X250 rear wheel/input station;
- three wheels per side, six total.

No four-wheel/two-axle model is valid design evidence. See `docs/PX1_HARD_ARCHITECTURE_LOCK_6W_3AXLE.md`.

## 1. CAM026 source lesson retained

Uploaded CAM026 source confirms two distinct TILT/PAN sides:
- `FSS-001-822 CAMERA AXLE (CABLE SIDE)`;
- `FSS-001-823 CAMERA AXLE (GEAR SIDE)`;
- side-frame `FBR-001-850 SEALRING (CABLE SIDE)`;
- side-frame `FBR-001-851 SEALRING (GEAR SIDE)`;
- `BEA-001-852 618/8 BEARING`;
- separate side cover plates and O-rings.

PX-1 keeps that proven service principle without copying proprietary dimensions.

## 2. Rev.B TILT mechanical architecture

The camera/yoke uses two opposed **fixed yoke pivots**:
- cable side: hollow Ø8 / Ø4 mm pivot;
- gear side: solid Ø8 mm pivot.

The sealed camera shell rotates around these fixed pivots through approximately -105...+105 deg.

Each side uses:
`wet yoke side -> polished Ø8 pivot -> radial shaft seal -> 618/8 bearing -> dry P3 camera volume`.

Consequences:
- bearings carry head radial load;
- shaft seals form the dynamic water/pressure barrier;
- no external hinge penetrates an unsealed dry space;
- no slip ring is needed for limited-angle TILT;
- continuous electrical rotation remains only at the internal ROLL axis.

## 3. Pressure zone P3

Camera pressure zone `P3 CAMERA` includes:
- optical shell;
- internal ROLL mechanism;
- dry cable-side feedthrough chamber;
- hollow Ø8/Ø4 TILT pivot bore.

P3 is separate from crawler P0/P1/P2.

Normal pressure class remains:
- +0.20...+0.30 bar gauge;
- +0.25 bar typical.

The cable-side fixed chamber must be statically sealed with a removable O-ring cover. The gear-side pivot has no open bore to the wet exterior.

## 4. Bearing candidate

Preferred source-compatible bearing:
- manufacturer: SKF or EZO;
- designation: `618/8` / `688` open;
- dimensions: **8 x 16 x 4 mm**;
- quantity: 2 per camera head.

Reason:
- exact bearing family is present in CAM026 source;
- open 618/8 stays inside dry P3 behind the dedicated radial shaft seal;
- open 4-mm width avoids the dimensional ambiguity of some 2RS miniature variants that grow to 5 mm width.

Published 618/8 reference capacity is roughly:
- dynamic C: ~819 N;
- static C0: ~300 N.

Even a 5g screen on a 0.25 kg head gives only ~12.3 N total external inertial load before geometry factors, so bearing capacity is not the governing issue.

Installation candidate:
- shaft journal: Ø8 h6/g6 class after final fit review;
- housing bearing seat: Ø16 H7 candidate;
- bearing outer ring seats against an internal machined shoulder;
- removable side retainer controls axial service retention.

Final fits follow the exact purchased bearing manufacturer's tolerance data.

## 5. Dynamic seal candidate

Target geometry:
- radial shaft seal 8 x 16 x 7 mm;
- FKM preferred;
- spring-energized primary lip;
- protective/dust lip preferred.

Commercial FKM 8x16x7 AS/TC/WAS-class seals are current standard catalog items. Dichtomatik's radial-shaft-seal family states standard pressure capability up to about 0.5 bar depending on operating conditions, which covers the PX-1 nominal +0.25 bar class but does not replace application testing.

Mounting order:
- seal is outboard of the bearing;
- seal lip runs on a dedicated polished Ø8 shaft land;
- bearing stays on the dry side;
- side cover/retainer prevents seal walkout and allows replacement.

Shaft seal land requirements:
- no keyway/thread/cross hole under the lip;
- surface finish target Ra <=0.4 um;
- no sharp lead-in edge;
- corrosion-resistant hardened/polishable shaft material.

## 6. TILT pivot parts

### PX1-460 cable-side pivot
Quantity: 1.

Geometry candidate:
- OD: 8 mm seal/bearing class;
- through bore: 4 mm;
- polished seal land;
- dry-side wire exit with large radius/chamfer;
- yoke-side positive anti-rotation feature outside the seal track.

Material candidate:
- 17-4PH / 1.4542 stainless preferred;
- final heat treatment selected to give a hard, polishable seal surface without brittle service behavior.

### PX1-461 gear-side pivot
Quantity: 1.

Geometry candidate:
- OD: 8 mm seal/bearing class;
- solid shaft;
- dry-side drive/hub seat for Z40 TILT worm wheel;
- wet-side yoke retention/anti-rotation outside the seal track.

Same material family as PX1-460 preferred.

## 7. Shaft strength screen

Cable-side hollow shaft section: Ø8 / Ø4 mm.

Section properties:
- I ≈ 188.50 mm^4;
- J ≈ 376.99 mm^4;
- section modulus Z ≈ 47.12 mm^3.

Using the existing 0.25 kg head and 30 mm CG eccentricity:
- 3g moment ≈ 0.221 N.m -> nominal bending stress ≈ 4.68 MPa;
- 5g moment ≈ 0.368 N.m -> nominal bending stress ≈ 7.81 MPa.

A 0.221 N.m torsion screen on the hollow Ø8/Ø4 section gives only ≈2.35 MPa nominal torsional shear.

Conclusion: shaft strength is not the limiting item. Seal surface, hub retention, impact geometry and cable fatigue dominate.

## 8. Seal speed screen

At a deliberately fast 30 deg/s TILT rate, Ø8 seal circumferential speed is only about:
- 0.0021 m/s.

This is extremely low relative to ordinary radial-shaft-seal speed capability. Wear risk is governed more by contamination, surface finish, dry starts and oscillating motion than by speed.

## 9. Cable-side feedthrough

Six external head functions remain:
- +12V_HEAD;
- GND_HEAD;
- UART_TX;
- UART_RX;
- CVBS_SIGNAL;
- CVBS_RETURN.

Inside the TILT feedthrough, use individual highly flexible conductors rather than the complete outer 6/7-core external cable.

Candidate internal wires:
- 2 x 0.25 mm2 high-flex wire for +12 V/GND;
- 4 x 0.14 mm2 high-flex wire for UART and CVBS pairs;
- HELUKABEL LifY-class individual conductors are the current reference family.

With representative finished ODs of ~1.3 mm for the two power wires and ~1.0 mm for four signal wires, theoretical bundle-area fill inside an Ø4 bore is ~46.1%.

This is acceptable as a packaging screen but the wires must not be tightly packed or potted through the moving bend zone.

## 10. TILT wire-flex geometry

The hollow axle itself is fixed to the yoke. The rotating head therefore needs a dry internal flex loop immediately after the axle exit.

Rules:
- no wire twist is accumulated through the full +/-105 deg motion;
- conductors form a controlled clock-spring/flex loop inside P3;
- minimum design loop radius starts at ~12 mm;
- 210 deg total angular travel at R12 corresponds to ~44 mm arc travel;
- reserve at least ~55 mm effective free flex length including end transitions;
- use two physical pairs for UART and CVBS where practical;
- CVBS pair stays away from LED/motor PWM conductors;
- strain relief on both stationary and rotating ends;
- no solder joint in the active flex zone.

The exact loop becomes production-valid only after 500-cycle and then endurance testing with the selected wire.

## 11. TILT drive correction

Old Rev.BM Z20 / 3 mm-bore worm wheel is incompatible with the Ø8 sealed pivot and is superseded.

Revised drive target:
- m0.5 worm;
- Z40 wheel;
- 8 mm wheel bore;
- one-start worm preferred;
- ~40:1 reduction;
- wheel pitch diameter ~20 mm;
- wheel OD ~21...21.5 mm class.

A current commercial brass m0.5 / 40T / 8-mm-bore wheel exists, proving that this geometry is obtainable.

At 200 rpm motor output:
- 40:1 -> 5 rpm TILT;
- equivalent max angular speed ~30 deg/s;
- normal command remains ~10...25 deg/s.

The worm wheel sits on the gear-side pivot **inside dry P3**. The seal land remains untouched by wheel retention geometry.

## 12. Axial seal/bearing stack

Candidate each side, wet-to-dry:
1. external fixed Ø8 pivot/yoke interface;
2. removable wet-side retainer/guard;
3. 8x16x7 FKM shaft seal;
4. thin controlled spacer/grease relief as required;
5. 618/8 bearing, 8x16x4;
6. internal shoulder/retainer;
7. dry P3 volume.

Because both seal and bearing share Ø16 OD, the housing must include a real axial shoulder/retainer strategy. Do not rely on friction alone.

Preferred machining concept:
- common Ø16 precision bore;
- internal bearing shoulder with opening <16 mm and >8 mm;
- bearing installed from outside;
- controlled spacer;
- seal installed after bearing;
- removable external retaining cover captures the seal.

## 13. Service sequence

1. remove complete camera assembly from crawler via WB15 quick connector + mechanical latch;
2. depressurize P3;
3. remove cable-side or gear-side yoke cover;
4. remove axle retention;
5. withdraw affected pivot;
6. extract seal and bearing individually;
7. inspect/polish or replace shaft;
8. replace seal/bearing as needed;
9. rebuild with measured grease/seal lubrication procedure;
10. pressure test P3 before crawler installation.

No wheel-drive P0/P1/P2 housing must be opened for camera TILT service.

## 14. Release gates

1. buy and measure two 618/8 bearings;
2. buy and measure four 8x16x7 FKM seal candidates;
3. machine one Ø8/Ø4 cable pivot and one solid Ø8 gear pivot;
4. surface-finish verification of seal lands;
5. dry +0.25 bar oscillating TILT leak test;
6. submerged +/-105 deg cycling;
7. 500-cycle cable loop test with video/UART powered;
8. then extended endurance test;
9. buy/measure exact m0.5 Z40 Ø8 worm wheel and matched worm;
10. verify >=0.221 N.m power-off holding requirement;
11. integrate exact pivots, covers, SP13, cable loop and Z40 wheel into camera CAD;
12. rerun complete LOW-position DN150 sweep on the **six-wheel three-axle crawler master**.

## Change log

### 2026-09-11 — WB17
- hard-linked camera development to the three-axle/six-wheel crawler master;
- recovered CAM026 cable-side/gear-side pivot architecture from source PDFs;
- selected fixed Ø8 pivots with hollow Ø4 cable side;
- selected source-compatible 618/8 bearing geometry;
- established 8x16x7 FKM dynamic-seal geometry;
- defined P3 camera pressure zone including the cable-side feedthrough chamber;
- proved Ø8/Ø4 pivot stress is negligible versus seal/cable concerns;
- defined ~55 mm internal high-flex loop requirement;
- rejected old Z20 worm wheel and revised TILT to m0.5 Z40 / Ø8 bore / ~40:1.
