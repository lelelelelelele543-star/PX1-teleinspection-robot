# PX-1 Rev.ET — machinable three-cavity pressure body baseline

Status: first machining-oriented body candidate; still prototype only.

## Design intent
Replace the Rev.EQ rectangular packaging box with one milled aluminum body that contains three separated pressure volumes:
- P0 central electronics/motor volume;
- P1 left sealed side-drive cavity;
- P2 right sealed side-drive cavity.

The body is one structural part. P1/P2 are opened from the sides and closed by rigid side covers. P0 is serviced from the top/rear through a separate sealed cover.

## Outer datum
Current nominal outer stock envelope:
- X length: 307 mm;
- Y width: 92 mm;
- Z: 8…90 mm;
- material candidate: EN AW-6082-T6.

These remain prototype dimensions, not a released drawing.

## P0 cavity
Central cavity target:
- X≈8…299 mm;
- Y≈-31…+31 mm;
- bottom Z≈14 mm;
- local roof/top geometry depends on camera recess and service opening.

Nominal minimum structural material retained:
- bottom under P0 ≈6 mm;
- end walls ≈8 mm;
- P0-to-side-drive bulkheads ≈4 mm minimum between Y31 and Y35.

## P1/P2 gear cavities
Each side-drive bay is milled from the outer side face toward the P0 bulkhead.

Candidate cavity envelope per side:
- X≈16…291 mm;
- inner Y boundary≈35 mm from centerline;
- outer opening at body side Y=46 mm;
- Z≈12…78 mm.

This matches the current five Z50 gear envelopes centered around Y≈38 mm with 8 mm face width while preserving a real metal bulkhead to P0.

Side covers attach to the outer body face at Y=±46 and form the pressure boundary of P1/P2.

## Front LOW-camera recess
The front upper body must be shaped around the folded camera rather than forcing the camera above a rectangular roof.

With Rev.ES motor relocation, the traction motor bodies move rearward and the camera recess can occupy approximately X≈40…125 mm without motor interference.

Important: the recess must NOT simply open P0 to atmosphere. The final body needs either:
- a locally lowered but still closed P0 roof below the external recess, or
- a dedicated sealed front/lift cover forming the pressure wall.

Preferred first prototype direction: locally lowered integral P0 roof under the folded camera, with lift bosses machined into the body side rails.

## Top service opening
Keep the large service opening primarily behind the camera recess, candidate X≈130…292 mm. It is closed by a rigid O-ring-sealed top cover.

The opening must allow removal of:
- paired traction motor holder;
- controller/electronics tray;
- DC/DC and power protection;
without removing the wheel-drive side covers.

## Side input boundaries
At X200 each P0/P1 and P0/P2 bulkhead receives one sealed transverse traction-output penetration. This is the only normal rotating drive penetration from P0 into each side bay.

Wheel shafts remain entirely within P1/P2 and therefore do not pierce P0.

## Machining strategy
Preferred sequence for first body:
1. rough outer billet and establish X/Y/Z datums;
2. machine P0 central cavity/opening;
3. machine left/right side-drive cavities from side faces;
4. machine P0/P1/P2 bulkhead bearing/seal bores in one setup per transverse axis where possible;
5. machine top and side static seal lands;
6. machine front camera/lift recess and bosses;
7. drill/tap cover fasteners and dowel holes;
8. deburr without rounding precision seal edges;
9. finish sealing faces after roughing distortion is removed.

## Tolerancing intent
- bearing bores: ISO fit selected per actual bearing mounting, typically H7 candidate;
- dynamic seal bores: supplier-controlled tolerance;
- opposite transverse output bores coaxiality target <=0.03 mm before qualification;
- top/side sealing-face flatness <=0.08…0.10 mm class;
- static O-ring lands Ra <=1.6 µm target;
- dynamic seal shaft surfaces much finer, controlled on shaft drawings.

## Qualification gates
- final wall-thickness review after all pockets/threads;
- FEA or conservative pressure proof analysis;
- empty-body pressure proof before electronics installation;
- P0/P1/P2 independently leak-tested;
- DN150 solid check including covers, screw heads and wheels;
- no machining release until exact motors, connector and pressure hardware are measured.
