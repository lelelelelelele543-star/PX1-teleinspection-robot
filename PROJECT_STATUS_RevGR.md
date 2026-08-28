# PX-1 Rev.GR — first-article metrology + solver definition

Status: ENGINEERING CONTROL BASELINE; not machining release.

## Completed in Rev.GR
Three process/analysis documents now turn the Rev.GQ build plan into measurable gates:
- `manufacturing/INS-PX1-WS01_RevGR.md` — first wheel-station inspection sheet;
- `manufacturing/INS-PX1-LH-DRIVE_RevGR.md` — complete left side-drive inspection sheet;
- `mechanical/analysis/REV_GR_FEA_LOAD_CASES.md` — FreeCAD/CalculiX load and boundary-condition specification.

A strong exact motor reference candidate is also documented in:
- `bom/REV_GR_32MM_TRACTION_MOTOR_REFERENCE.md`.

## WS-01 metrology baseline
The first wheel station now has formal datums and measurement fields for:
- actual purchased 6701/61801/61903 dimensions;
- shaft journals and runout;
- X-ring land/gland;
- axle-flange bearing pockets;
- endplay;
- seal breakaway/running drag;
- keyed Ø90 wheel fit;
- M8 retention;
- wet rotation / pressure decay / 20 service cycles.

The important rule remains: final bearing fits and seal glands are not cut from nominal catalog dimensions before the exact samples are measured.

## Left-drive first-article baseline
The five-Z50 left train is now controlled by explicit station records at X50/X100/X150/X200/X250 and functional checks for:
- adjacent center distances;
- X200 endplay/runout;
- Z16/Z40 contact pattern;
- X200-to-neighbor face overlap;
- 20-revolution no-tight-spot hand test;
- powered no-load current/speed map;
- 30+30 minute thermal run;
- individual short current-limited blocked-wheel tests;
- 100 controlled reversals before right-side duplication.

## FEA definition
Rev.GR defines separate solver cases instead of one arbitrary pressure run:
- 0.60 bar reverse submerged pressure differential;
- P1/P2 individual pressure-loss cases;
- reverse zone-differential cases;
- bare-body 1.0 bar structural proof screen;
- X200 nominal and 2x shock reactions;
- 200 N wheel obstacle load;
- 2 kN centered tether proof pull;
- 2 kN pull at 30 and 50 mm eccentricity;
- Rev.GP ballast static + 5g screening load;
- selected combined operational cases.

Pressure-only FEA uses minimal rigid-body restraint rather than fixing large faces and creating false stress. Local tether/wheel cases use their real reaction path.

## Exact Ø32 motor reference result
ISL `PGM-32P-24-100-60-02 / MOT-IG32PGM 100` is the first exact commercial reference found that matches the active CAD envelope:
- Ø32 mm;
- 92 mm length class;
- 24 V;
- ~49-54 rpm rated range depending source revision;
- ~1.37-1.77 N.m published rated torque range;
- Ø6 output shaft;
- 4 x M3 mounting pattern on ~Ø26 PCD in the older drawing.

However, current supplier data and an older official datasheet disagree on rated torque/speed/stall data. Therefore it is **not frozen**. A physical sample + current drawing must be measured before the final motor holder is drilled.

## Newly identified documentation issue
Legacy tether document Rev.CH still describes an ROV-style cable made from power conductors plus separate shielded twisted pairs. This conflicts with the later project requirement to use a Proteus-style reinforced lightweight **single 6-core copper inspection cable**.

Rev.CH is therefore considered stale for the physical cable architecture and will be superseded in the next block. The long-link electronics may still assign two conductors as a balanced differential channel, but the physical tether is not to become a bundle of ordinary pair cables, coax or fiber.

## Next autonomous block — Rev.GS
- supersede Rev.CH with the Proteus-style 6-core copper tether baseline using current public Mini-Cam mechanical data;
- correct the stale four-traction-motor power budget to the active two Ø32 motor architecture;
- recompute 48 V source current / cable-loop-resistance limits for 40/100/150 m;
- keep 10BASE-T1L/data allocation conditional on the real six-core cable passing impedance/link testing;
- define the exact tether sample measurements required before rear collet/connector machining;
- then continue FreeCAD/CalculiX preparation and exact purchased bearing/seal sourcing.
