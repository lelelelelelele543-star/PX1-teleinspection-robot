# PX-1 Rev.GQ — Ø90 prototype wheel manufacturing route

Status: prototype process baseline; exact elastomer compound remains a test variable.

## Common mechanical wheel core
Keep one mechanical interface for every DN150 wheel type:
- current Rev.GF dished/tapered external envelope;
- Ø17 keyed wheel seat;
- 4 mm key torque path;
- recessed M8 axial retention;
- hub/retainer remain inside the DN150 envelope;
- wheel is changed as a complete wheel assembly.

Do not make the tire itself a field-service cassette/module. The service item is the normal complete wheel.

## Prototype core material
Preferred first metal-core candidate:
- 6082-T6 or equivalent machinable corrosion-resistant aluminium for low rotating mass;
- final material remains open until key-seat wear and wet-service tests.

If aluminium key-seat wear appears during the first traction tests, move the hub/core to stainless or add a steel keyed insert rather than enlarging the whole wheel.

## Elastomer retention
Do not rely on smooth-surface glue alone.

First cast-core should include:
- degreased/abraded bonding surface;
- two shallow circumferential mechanical retention grooves in the tire bond land;
- generous edge radii so elastomer is not cut by the metal core;
- elastomer primer/adhesive system matched to the selected casting compound.

Exact groove dimensions are HOLD until the chosen elastomer system and minimum remaining core wall are known.

Average transmitted interface shear is small compared with normal elastomer bond capability; the mechanical grooves are primarily protection against peel, water ingress and long-term debonding.

## SR wheel — normal pipe
Geometry:
- same active Rev.GF outer profile;
- no protruding lugs outside the validated envelope;
- smooth/compliant traction crown in the first mold;
- tiny mold vent/parting witness must be trimmed below the working envelope.

Use for:
- dry/wet PVC;
- ordinary clay/concrete;
- baseline rolling-current and vibration tests.

Exact Shore hardness is not frozen.

## HG wheel — wet/greasy pipe
Geometry:
- same outer profile as SR;
- 18 transverse slots cut inward in Rev.GO geometry;
- slot screen: ~1.4 mm circumferential width, ~1.8 mm depth, approximately every 20 degrees;
- no feature projects beyond the SR outer envelope.

Purpose:
- break water/grease film;
- create repeated traction edges;
- preserve the same DN150 clearance.

This is PX-1 geometry and is not a copy of Minicam's proprietary high-grip wheel.

A later abrasive/carborundum or carbide-grit surface is an optional severe-service experiment only after rubber/PU testing; it is not the default wheel because aggressive grit can damage some pipe surfaces.

## Manufacturing route for first traction tests
1. Machine one common metal core.
2. Verify keyed fit and M8 retention on WS-01 before adding elastomer.
3. Print a two-piece mold on the Chiron from the validated outer profile.
4. Print separate SR and HG mold inserts so the expensive metal core geometry does not change.
5. Cast/overmold the candidate elastomer onto the prepared core.
6. Cure per material supplier procedure.
7. Trim only flash; do not hand-grind the traction profile into shape.
8. Measure OD/profile runout.
9. Balance only if vibration appears at operating speed; crawler wheel RPM is low.
10. Run PX1-TP-020.

## 3D-printed tire rule
TPU prints are useful for:
- DN150 fit;
- wheel-removal practice;
- mold verification;
- low-load gear-train rolling tests.

A printed TPU tire is NOT accepted as evidence for final wet traction or lifetime. Layer orientation, infill and surface finish strongly affect grip and wear.

## Test variable strategy
Change one variable at a time.

Recommended first comparison:
- same core;
- same outer profile;
- same ballast = 0;
- SR smooth vs HG grooved;
- identical pipe/surface state.

Only after geometry is compared should compound/hardness be varied. Otherwise the source of a traction change cannot be identified.

## Measurement gates
For each wheel set save:
- actual mass;
- max OD/profile scan;
- radial/axial runout on crawler shaft;
- dry stable pull;
- wet stable pull;
- detergent-film stable pull;
- rolling drag;
- visible slip mode;
- tread damage after test;
- any debonding at core interface.

## Current architecture references
Current Minicam documentation confirms separate 90 mm soft-rubber, high-grip and carbide wheel families for 150 mm-class crawlers and describes high-grip wheels for wet/greasy conditions. PX-1 uses that only as system-level evidence that interchangeable wheel surfaces are useful; dimensions and tread geometry remain PX-1-specific.
