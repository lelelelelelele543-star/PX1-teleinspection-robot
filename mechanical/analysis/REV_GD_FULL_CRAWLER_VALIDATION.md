# PX-1 Rev.GD — integrated full crawler validation

Status: full prototype solid validation, not manufacturing release.

The integrated model combines:
- Rev.GC P0/P1/P2 pressure body and covers;
- five Z50 gears per side in the separated side bays;
- six dished/tapered Ø90-class wheels;
- six local axle-flange envelopes;
- two Ø32 x <=95 mm traction-motor envelopes;
- manual four-bar lift;
- Ø52 x 72 digital camera envelope;
- front retainer/rear camera closure;
- 150 N gas-spring envelope;
- rear connector adapter, fill/sensor bosses and towing clevis.

## Wheel profile correction
The wheel is no longer modeled as a plain Ø90 x 18 cylinder.
Current prototype envelope:
- max tread OD Ø90 at the inboard edge;
- axial width 16 mm;
- strong taper to ~Ø42 at outer edge;
- Ø56 x 4 mm central inboard relief clears the Ø50 axle flange;
- central hub starts outboard of the flange.

This allows the wheel to wrap around the side-cover/flange package without moving the complete drive bay outward.

## Executed checks
`mechanical/cadquery/PX1_FullCrawler_RevGD.py` executes successfully in CadQuery 2.8.0.

Ideal DN150 solid results:
- body outside pipe: 0 mm^3;
- both side covers: 0;
- six axle flanges: 0;
- lift arms/yoke/bridge: 0;
- camera/front/rear parts: 0;
- six wheel solids: 0;
- full camera TILT sweep -105..+105 deg: 0 outside volume;
- gear intersection with P0 body: 0 for all 10 Z50 gears;
- wheel/flange intersection: 0 for all six stations;
- motor/body intersection: 0 left/right.

Nominal numeric hard points:
- side-cover lower corner clearance: ~6.29 mm;
- upper lift hardware Y31/Z112 clearance: ~7.51 mm;
- LOW camera axis: X~83.557 / Z75.

The wheel tread is intentionally close to/tangent with the ideal pipe envelope; wheel traction is therefore qualified physically, not by a positive radial clearance requirement.

## Remaining real-world allowance gate
The zero-interference ideal-cylinder result does NOT yet include:
- pipe ovality;
- deposits/weld beads/offset joints;
- real screw-head protrusion tolerance;
- real tire deformation;
- camera cable loop;
- actual connector boot;
- manufacturing tolerances stack.

Physical DN150 tube sweep remains mandatory before machining release.
