# PX-1 Rev.B — WB23A local head harness envelope

Date: 2026-09-13  
Status: **PASS_STATIC_PACKAGING / FLEX TEST HOLD / MANUFACTURING HOLD / PROCUREMENT HOLD**

## Scope

WB23A re-solves the local camera harness after WB22A corrected the lift geometry. WB21 clamp coordinates and the 52.8 mm free-flex length are therefore superseded mechanically.

WB22A hard geometry remains unchanged:
- 3 axles / 6 wheels;
- X50 / X150 / X250;
- ten Z50 side gears;
- body pivot X200;
- lift pivots Z92/Z109;
- link length 90 mm;
- arm planes Y=±31 mm;
- arm section 4 x 14 mm.

## Source-derived topology

MiniCam source drawings show a smaller local cable class and a protected lift-arm route:
- `CAB-002-461` is an M12x1.5 cable fitting for approximately 3.5...5 mm cable in `DRW-002-752`, `DRW-002-745` and `ASS-002-890`;
- `FSS-003-127 LIFT ARM COVER` is present in `ASS-003-121` / `DRW-003-121`.

Repair photographs are used only as topology evidence. No PX-1 dimensions are scaled from photos.

## Controlled PX-1 static run

The prototype local-harness envelope is reduced to **<=5.0 mm OD** and routed on the inner side of the +Y lower lift arm.

Controlled geometry:
- cable centre Y = 25.5 mm;
- 25 mm setback from each pivot reserved for future flex zones;
- protected static middle run = 40 mm;
- protective cover screen = 7 mm Y thickness x 7 mm XZ height;
- nominal cover wall target = 1 mm.

This removes the need to move the validated WB22A body pivot from X200 merely to package the old Ø8 WB21 cable.

## Executed validation

Executable CAD:
`mechanical/cadquery/PX1_WB23A_LocalHarnessEnvelope_RevB.py`

Executed result:
`mechanical/cadquery/REV_B_WB23A_VALIDATION.json`

The full lift was sampled at 43 solid states from -17.7916° to +66.4435°. Results:
- cable vs body: 0 mm³;
- cable vs ten Z50: 0 mm³;
- cable vs four arms: 0 mm³;
- cable vs carrier at LOW/MID/HIGH: 0 mm³;
- cover vs body/Z50/arms/carrier: 0 mm³;
- minimum cable-to-wet-floor clearance: 24.565 mm;
- minimum cover-to-wet-floor clearance: 24.765 mm.

A separate 1001-position lift check against the conservative complete TILT swept envelope gives:
- minimum cable margin: 3.319 mm;
- minimum cover margin: 2.319 mm.

The critical static-run condition is HIGH, with camera axis approximately X133.284 / Z185 mm.

## DN150 LOW

At LOW:
- static cable start ≈ X176.196 / Y25.5 / Z84.361 mm;
- static cable end ≈ X138.109 / Y25.5 / Z72.139 mm;
- ideal-DN150 cable clearance ≈ 31.410 mm;
- ideal-DN150 cover clearance ≈ 29.744 mm.

Therefore this static harness section is not the DN150 limiting hard part. The moving TILT head remains the limiting WB22A geometry.

## Electrical/procurement candidates

Electrical allocation remains eight insulated conductors:
- two parallel +12 V;
- two parallel GND;
- UART TX/RX;
- CVBS signal/return;
- shield used only for EMC, never DC return.

Body gland candidate: `LAPP SKINTOP MS-M M12x1.5 53112000`, 3.5...7 mm cable class. It is not pressure released.

Prototype donor-cable candidate: `Autonics CID9S-2`, approximately Ø5 mm, eight insulated conductors plus shield. No accepted continuous-flex life/radius data has been frozen, so it remains a test-gated prototype candidate.

## Open gates

WB23A does not release the complete harness. Remaining work:
1. body-side pivot flex zone;
2. carrier-side pivot flex zone and transition to the fixed camera connector;
3. purchased-cable OD/resistance/flex qualification;
4. wet/grit lift-cycle test;
5. cover drainage, fasteners and anti-snag details;
6. M12 pressure boss and +0.25 bar leak proof;
7. CVBS interference test with TILT/ROLL motors and LED PWM.

Next controlled block: **WB23B — pivot flex zones and final head-connector transition.**

## Change log

### 2026-09-13 — WB23A
- retained WB22A lift geometry and six-wheel hard lock;
- replaced the obsolete WB21 Ø8 local packaging assumption with a <=Ø5 protected local-harness envelope;
- reserved two 25 mm flex zones and validated the 40 mm protected static run;
- retained FLEX/PROCUREMENT/MANUFACTURING holds until physical cycling and pressure tests are complete.
