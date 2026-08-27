# PX-1 Rev.GA — project status after Group A production-detail pass

Status: PROTOTYPE ENGINEERING BASELINE; not serial machining release.

## Newly completed in Rev.FX–FZ
- executable CadQuery model for the six first rotating/sealing production candidates;
- successful solid validation for DRW-PX1-431 through DRW-PX1-436;
- detailed dimension/CTQ sheet for each Group A part;
- prototype dimensional inspection plan;
- first-lot machining sequence designed to learn from one station before duplicating errors across all six wheel stations.

## Group A parts now modeled
1. DRW-PX1-431 wheel shaft — 54 mm, Ø12/Ø17/Ø19/Ø21/Ø17 stepped architecture.
2. DRW-PX1-432 axle flange — Ø50 x 12, external projection limited to 3 mm, 61903 pocket.
3. DRW-PX1-433 side cover — 286 x 86 x 5, three flange pilots, 12 M3 holes, face-seal groove candidate.
4. DRW-PX1-434 X200 output shaft — 42 mm, Ø10/Ø10/Ø14/Ø18/Ø12.
5. DRW-PX1-435 X200 bearing/seal boss — Ø38 x 15, 61800 + 18x30x7 architecture.
6. DRW-PX1-436 bevel pinion shaft — 39 mm, Ø6/Ø8/Ø12 support architecture.

All six CAD solids execute and validate successfully in CadQuery 2.8.0.

## Important open supplier gates
- exact wheel X-ring article and gland standard;
- exact static axle-flange O-ring;
- exact side-cover FKM O-ring article;
- purchased 61801/61903/61800 bearings measured against proposed fits;
- exact 18x30x7 seal article;
- actual KHK bevel pair mounting/contact pattern;
- actual JGB37 motor/coupling shaft dimensions.

Therefore seal-groove geometry and several supplier-controlled fits remain CANDIDATE, not release.

## Frozen engineering rules carried forward
- six Ø90-class profiled wheels;
- three wheels per side, pitch 100 mm;
- five equal m1 Z50 gears per side;
- X200 bevel input, 2.5:1 candidate;
- P0/P1/P2 independently sealed and positively pressurized;
- CRP-style manual parallelogram camera lift;
- digital camera only, no CVBS/coax;
- rugged tether with independent tensile member and electrical connector unloaded from towing force.

## Next block
Group B pressure structure:
- DRW-PX1-100 main P0 pressure body;
- DRW-PX1-101 top service cover + static seal path;
- DRW-PX1-102 rear structural bulkhead / tether anchor;
- DRW-PX1-103 replaceable connector adapter;
- integrate exact Group A bearing/seal bosses into the body solid;
- run full DN150 clearance again with real lower screw recesses and all service covers.