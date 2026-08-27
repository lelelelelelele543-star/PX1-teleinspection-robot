# PX-1 Rev.EX — integrated status after machining-oriented mechanical pass

Status: PROTOTYPE ENGINEERING BASELINE. Not serial/machining release.

## Major correction completed
The traction bevel input is moved from X150 to the **X200 side-drive idler station**. Both JGB37 motors are oriented with output shafts toward the front and motor bodies extending rearward from the X200 bevel plane.

Reason: this removes the previously hidden conflict between the LOW/DN150 folded camera/lift envelope and the forward longitudinal motor bodies.

The five equal Z50 side gears and 100 mm wheel pitch remain unchanged.

## New machining-oriented parts
### Main pressure body — Rev.ET
One milled aluminum structural body with:
- P0 central pressure cavity;
- P1/P2 side-drive pressure cavities;
- ~4 mm nominal metal bulkheads between P0 and P1/P2 before local bosses;
- side covers sealing P1/P2;
- rear/central top service cover for P0;
- lowered closed front roof under the folded camera recess.

### Wheel station — Rev.EU
Each of six stations now has a machinable stack concept:
- Ø12 inner shaft journal;
- Z50 gear;
- 61801 inner supports;
- Ø17 outer wheel-load/seal journal;
- removable axle flange;
- 61903 outer bearing;
- FKM dynamic seal candidate;
- labyrinth;
- profiled Ø90 wheel;
- independent M6 axial wheel retention.

Wheel shafts remain inside P1/P2 and do not pierce P0.

### Manual lift — Rev.EV
Rod envelopes are replaced by plate-arm solids:
- 4 mm stainless arm candidate;
- Ø8 bushed pivots;
- structural body bosses;
- M8 clamp stack;
- mechanical DN150 stop;
- 150 N gas-spring class remains a sizing candidate.

## New integrated CAD master
`mechanical/freecad/PX1_CRP150_6W_Master_RevEW.py`

This integrates:
- three-zone body solid;
- side covers;
- five Z50 gears each side;
- stepped wheel shafts/flanges;
- X200 bevel input;
- rearward paired motor pack;
- front low-profile electronics/power envelopes;
- LOW plate-arm lift;
- digital camera envelope;
- rugged rear tether boot/load-path reference.

## Current mechanical datums retained
- body length 307 mm class;
- body width 92 mm class before covers/wheels;
- wheel centers X50/X150/X250;
- idlers X100/X200;
- wheel axis Z45;
- Ø90-class profiled wheels;
- camera target Ø52x72;
- LOW camera axis Z75;
- lift main pivot X200/Z94;
- isolated positive-pressure zones P0/P1/P2.

## Immediate blockers before first metal body
1. actual JGB37 overall length and output-face dimensions;
2. exact dynamic wheel seal article and housing dimensions;
3. exact rear tether connector and pressure-port footprints;
4. exact camera module/slip-ring drawings;
5. complete DN150 interference run with real screw heads, lift yoke, cable loop and rear tail;
6. top/side O-ring actual articles and groove standards;
7. pressure proof calculation/test plan;
8. final machining datum/tolerance drawing set.

## Next work sequence
- finish X200 bevel-output/idler bearing stack as a real solid;
- make real top and side cover O-ring paths and fastener patterns;
- make camera yoke/latch/window/LED-ring solids;
- integrate rear connector, fill valve and three-zone manifold footprints;
- rerun DN150 and service-tool-clearance checks;
- then start drawing candidates for body, side cover, axle flange, wheel shaft and lift arm.
