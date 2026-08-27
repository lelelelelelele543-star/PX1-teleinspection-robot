# PX-1 Rev.GE — integrated status after autonomous large-block pass

Status: PROTOTYPE ENGINEERING BASELINE; not serial/machining release.

## Major correction completed
A hidden packaging conflict between the previous Ø37 motor pair and the source-like independently sealed side-drive bays was resolved by moving the traction envelope to the 32 mm planetary class. This preserves the CRP150-like pressure architecture without widening the crawler outside the DN150 envelope.

## Active mechanical geometry
- body length 307 mm;
- body width 92 mm before side covers;
- P0 internal width 68 mm;
- P1/P2 side bays 8 mm deep in 12 mm side walls;
- 4 mm nominal pressure membrane between P0 and each side bay;
- side covers 286 x 80 x 5, outer Y +/-51;
- 6 x Ø90-class dished/tapered wheels;
- wheel centers X=50/150/250, Z=45;
- 5 x m1 Z50 gears per side at gear plane Y +/-42;
- X200 sealed bevel output;
- 2 x Ø32 x <=95 mm 24 V planetary motor envelopes at Y +/-16.5;
- manual four-bar lift LOW axis X~83.557/Z75;
- digital camera target Ø52 x 72, TILT +/-105, continuous internal ROLL.

## Source-derived CRP150 lessons retained
Uploaded CRP150 drawings support:
- 3 wheel shafts per side and 5 Z50 side gears;
- 61801 + 61903 bearing architecture;
- X-ring 18.72 x 2.62 and axle-flange O-ring 32 x 1.5;
- side-cover O-ring 190 x 1.5;
- separate crawler-housing bevel-output 61800 bearings and 18x30x7 shaft seals;
- paired motor unit with supported small bevel shafts;
- layered cable termination with multiple seals/strain-management elements.

PX-1 uses those as architecture/service references, not copied proprietary geometry.

## CAD execution state
Successful CadQuery 2.8.0 execution:
- `mechanical/cadquery/PX1_GroupB_RevGC.py`;
- `mechanical/cadquery/PX1_FullCrawler_RevGD.py`.

Integrated ideal-DN150 collision checks are zero for all non-contact solids and all six wheel solids. Gear/body, wheel/flange and motor/body intersections are also zero.

## Current critical measured/calculated margins
- side-cover lower corner: ~6.29 mm ideal DN150;
- upper lift hardware: ~7.51 mm;
- camera full tilt: no solid intersection in ideal DN150;
- motor-to-P0 inner wall clearance: 1.5 mm each side.

## Next work that does not need architectural re-discussion
1. revise Group-A DRW-PX1-433 cover drawing candidate to Rev.GC dimensions;
2. convert DRW-PX1-431/432/434/435/436 into CAD-derived 2D manufacturing sheets;
3. create real body section drawings through wheel station and X200;
4. complete detailed wheel solid/hub/key interface rather than envelope only;
5. finalize the camera front retainer/rear closure/bearing cartridge once exact camera/rotary parts are bought;
6. choose and purchase exact 32 mm traction motor samples and seals;
7. bench-test current/rpm/temperature and update motor driver selection;
8. physical DN150 sweep and pressure tests before any machining-release stamp.
