# PX-1 Rev.GR — exact Ø32 traction-motor reference candidate

Status: STRONG REFERENCE CANDIDATE; **not procurement freeze** and not permission to machine the final motor holder.

## Candidate
**ISL Products PGM-32P-24-100-60-02 / reference MOT-IG32PGM 100**

This is the first readily documented commercial motor found that matches the active Rev.GB/GL CAD envelope almost exactly.

## Current supplier-page data (2026 search)
Current ISL shop listing states:
- brushed planetary gearmotor;
- 24 VDC;
- diameter 32 mm;
- length 92 mm;
- no-load speed 60 rpm;
- no-load current 0.13 A;
- rated speed 54 rpm;
- rated torque 14 kg.cm (~1.37 N.m);
- stall torque 116 kg.cm (~11.38 N.m);
- stall current 5.5 A;
- 100:1 product variant;
- listed as in stock at time of research.

These figures are an excellent match to the active PX-1 target of <=32 mm diameter, <=95 mm length, roughly 45-65 rpm and >=1.1 N.m rated output torque.

## Mechanical drawing data from the older MOT-IG32PGM 100 datasheet
The available ISL mechanical drawing / distributor copy shows:
- gearbox/front diameter: Ø32 mm class;
- output shaft: Ø6 mm;
- shaft protrusion: approximately 16.3 mm;
- four M3 mounting holes, approximately 5.5 mm thread depth;
- mounting PCD: Ø26 mm;
- total motor/gearbox assembly dimensions consistent with roughly 92 mm overall class;
- drawing includes 34.9 mm and 57.1 mm axial body sections whose sum is 92.0 mm.

Therefore the Rev.GL generic Ø32 x 92 envelope is not arbitrary: this exact documented motor family physically fits it.

## Important specification conflict
Do **not** treat the catalog values as frozen.

An older official/distributor datasheet for the same MOT-IG32PGM 100 reference gives different performance data:
- rated speed 49 rpm;
- rated torque 18 kg.cm (~1.77 N.m);
- rated current 1.06 A;
- stall torque 98 kg.cm;
- no-load current <0.30 A;
- max power 15 W.

The current supplier page instead gives 54 rpm / 14 kg.cm / 116 kg.cm stall / 5.5 A stall.

Possible causes include product revision, different motor winding under the same commercial reference, or catalog maintenance. Until an actual sample and current drawing/datasheet are obtained, **both data sets are treated only as reference ranges**.

## PX-1 performance implication
With the current 2.5:1 bevel stage and 85% screening efficiency:

Using the current-page 54 rpm / 14 kg.cm values:
- theoretical wheel speed at Ø90: ~6.11 m/min;
- rated motor torque: ~1.37 N.m;
- theoretical side-train torque after bevel: ~2.92 N.m;
- ideal tangential force per side before later drivetrain/tire losses: ~64.8 N.

Using the older 49 rpm / 18 kg.cm values:
- theoretical wheel speed: ~5.54 m/min;
- rated motor torque: ~1.77 N.m;
- theoretical side-train torque after bevel: ~3.75 N.m;
- ideal tangential force per side: ~83.4 N.

Actual crawler tractive force remains tire-adhesion limited well before either ideal number in many wet-pipe conditions.

## Current-limit implication
PX-1 currently protects the custom compact bevel candidate with a provisional command ceiling equivalent to **1.0 N.m motor output torque**.

A crude linear interpolation between no-load and stall current predicts roughly 0.6-0.8 A motor current around 1.0 N.m for the two conflicting published data sets. This is **not** a firmware setpoint.

The real current-to-output-torque relation must be measured on the purchased motor/gearbox because gearbox friction, brush drop, winding revision and temperature make a catalog-linear estimate unreliable.

## Procurement / metrology gate
Before machining the final motor holder or coupling:
1. obtain one exact motor sample;
2. obtain the seller/manufacturer drawing corresponding to that sample/revision;
3. measure OD, overall length, mounting pilot, PCD, hole depth, shaft OD, D-flat/key if any, shaft protrusion and endplay;
4. measure no-load rpm/current at 24 V;
5. measure controlled loaded current/speed/torque points;
6. perform only a short protected stall/current characterization if the test fixture safely allows it;
7. check case temperature during a 30 min representative duty run;
8. verify brush/terminal arrangement fits the Rev.GP rear wiring corridor;
9. update the CAD motor holder from measured values.

## Purchasing constraint
This part is retained primarily as an **engineering reference/specification target**. Final PX-1 motor procurement should still follow the project's allowed motor purchasing route where practical. An alternative seller motor is acceptable if the physical sample meets or exceeds the measured envelope/performance requirements.

## Decision
Rev.GR does **not** change the crawler geometry.

The current Ø32 x 92 rear motor envelope is validated against a real commercial family and remains active. The exact motor holder drilling remains HOLD until a physical sample is measured.
