# PX-1 Rev.BM — TILT worm-set selection

Status: REVISED PROTOTYPE CANDIDATE / 8 MM PIVOT COMPATIBLE / NOT MACHINING RELEASE

## 1. Correction reason

The earlier Rev.BM candidate used an m0.5, Z20 worm wheel with a 3 mm bore.

WB17 freezes the TILT pivot/seal architecture around an Ø8 mm shaft. A Z20 m0.5 wheel has only about 10 mm pitch diameter / 11.3 mm OD, so enlarging its bore from 3 mm to 8 mm would leave insufficient hub/root material and is rejected.

This is a component correction, not an architecture change.

## 2. Revised geometry basis

Use a matched m0.5 worm + **Z40 worm wheel** around the TILT axis.

Target:
- module: 0.5;
- pressure angle: 20 deg class;
- worm: one-start preferred for high reduction/holding;
- worm wheel: 40 teeth;
- ratio with one-start worm: 40:1;
- wheel pitch diameter: ~20 mm;
- wheel outside/throat diameter: ~21...21.5 mm class;
- wheel bore: **8 mm**;
- right/left hand must match purchased worm;
- exact centre distance follows the selected matched pair.

A current commercial brass m0.5 / 40-tooth / 8-mm-bore wheel exists in the BOLTTE catalog/market route. This proves the required geometry is commercially obtainable. Exact worm hand/start/centre-distance compatibility remains a purchase gate.

A precision reference pair also exists from Ondrives as PWG0.5-40-1PK (m0.5, Z40, one-start mating system, 20 deg, pitch Ø20, tip Ø21.5, rated torque 1.23 N.m at 100 rpm input condition), although that exact reference wheel has a 6 mm bore and PEEK GF30. It is used only as geometry/strength evidence, not as the PX-1 production article.

## 3. Why Z40 is acceptable

Current motor candidate: DCGM-N20-12V-EN-200RPM.

With a 40:1 one-start worm stage:
- theoretical full-speed TILT output: ~5 rpm;
- equivalent angular speed: ~30 deg/s;
- firmware normal target remains ~10...25 deg/s using PWM/ramping;
- the larger wheel still fits comfortably in the Ø52 camera-head envelope.

The old Z20 geometry is superseded wherever it conflicts with the Ø8 sealed TILT pivot.

## 4. Material target

Preferred prototype/final route:
- worm: steel / stainless or hardened steel class;
- wheel: brass/bronze preferred for a metal pair;
- no printed plastic wheel for final underwater service.

A PEEK precision wheel may be used only as a controlled bench reference if desired; it is not the present production preference.

## 5. TILT axis interface

The worm wheel is mounted concentrically on the **gear-side Ø8 TILT pivot** or its dedicated Ø8 keyed/flat hub section.

Rules:
- bearing/seal running surface remains uninterrupted and polished;
- wheel retention must not place a keyway, set-screw crater or thread under the radial shaft seal lip;
- wheel hub/retainer sits in the dry P3 camera volume;
- yoke-side axle fixation reacts TILT torque mechanically;
- the cable-side Ø8/Ø4 hollow pivot remains free of drive features.

Exact key/flat/clamp geometry is frozen only after the purchased Z40 wheel hub dimensions are measured.

## 6. Holding requirement

Existing design case remains:
- moving camera/head mass target: 0.25 kg;
- CG eccentricity target: 30 mm;
- gravity torque: ~0.0736 N.m;
- 3x holding target: >=0.221 N.m at TILT axis.

A Z40 worm wheel gives ample geometric reduction. Self-locking is still **not assumed** from ratio alone. Lubrication, lead angle, material and tolerances can permit backdrive.

## 7. Release gates

1. purchase/measure the exact m0.5 Z40, 8 mm bore wheel candidate;
2. confirm a truly matched m0.5 worm: start count, hand, profile and centre distance;
3. bench-measure backlash;
4. verify TILT holding >=0.221 N.m with power removed;
5. run 500 cycles -105 to +105 deg;
6. inspect hub/shaft retention and tooth wear;
7. integrate the real Z40 body with WB17 Ø8 seal/bearing stack;
8. rerun Ø52 head and DN150 sweep.

## Change log

### 2026-09-11 — WB17 correction
- rejected old m0.5 Z20 / 3 mm-bore wheel as incompatible with the sealed Ø8 pivot;
- changed the target to m0.5 Z40 / Ø8 bore;
- retained worm-drive TILT architecture;
- changed nominal full-speed TILT from ~60 deg/s to ~30 deg/s, which better matches inspection use;
- retained physical backdrive/holding test as mandatory.
