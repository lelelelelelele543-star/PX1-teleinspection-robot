# PX-1 Rev.DQ — corrected DN150 wheel-contact + camera recheck

Status: geometry correction; supersedes the pipe-axis assumption in Rev.DG.

## Error found in the earlier DN150 model
Rev.DG placed the DN150 pipe axis at the wheel-axis height Z=45 mm. That makes the modeled Ø90 wheels float inside the pipe instead of touching the lower pipe quadrants.

The pipe position must be solved from the actual tapered wheel contact profile.

Using the Rev.DL wheel candidate:
- wheel axis Z = 45 mm;
- full Ø90 crown reaches local radius 45 mm around |Y|=51…54 mm;
- critical contact occurs near |Y|=54 mm;
- DN150 radius = 75 mm.

The resulting pipe-axis height is:

`Z_pipe ≈ 45 - 45 + sqrt(75² - 54²) ≈ 52.05 mm`.

## Corrected non-wheel clearance
With pipe axis Z≈52.05 mm:
- main body envelope retains >10 mm nominal radial clearance at its rectangular corners;
- current side-cover envelope retains approximately 5 mm nominal radial clearance at its worst lower corner before adding real screw heads and bosses.

This is much more meaningful than the old overall-width check.

## Camera model
Current digital camera envelope retained for packaging:
- cylinder OD = 52 mm;
- length = 72 mm;
- TILT range = -105…+105°;
- camera carrier centered in Y;
- TILT axis modeled transverse to the crawler, so the camera optical/body axis sweeps in the X-Z plane.

For a cylindrical envelope centered at camera-axis height Zc, the worst radial reach through unrestricted TILT is approximately:

`|Zc-Zpipe| + sqrt((L/2)^2 + (D/2)^2)`

with `sqrt(36²+26²) ≈ 44.41 mm`.

## Recalculated positions
Using Zpipe≈52.05 mm:
- LOW camera axis Z≈60.3 mm -> nominal worst camera clearance ≈22.3 mm;
- previous DN150_SAFE Z≈69.7 mm -> nominal worst clearance ≈12.9 mm;
- Z=72 mm -> nominal worst clearance ≈10.6 mm.

Thus the previous 72 mm mechanical stop was overly conservative because it came from the incorrect pipe-axis assumption.

## New DN150-SAFE target
Do not immediately use the theoretical 3 mm maximum because the real camera has:
- LED/window bezel;
- quick-release protrusions;
- yoke/pivot hardware;
- cable bends;
- manufacturing and wheel-compression tolerances.

New provisional mechanical SAFE stop:
- **camera axis Z <= 76 mm**.

At Z=76 mm the simple Ø52x72 cylindrical envelope still retains about 6.6 mm nominal radial clearance in the corrected ideal DN150 pipe.

This provides useful allowance for real external camera features before physical tube testing.

## HIGH position
HIGH remains mechanically blocked for DN150.
It is only enabled by moving/removing the pipe-size stop for larger pipes.

## Required full-solid gate
The next release test must include simultaneously:
- all six real tapered wheels;
- cover screw heads and bearing bosses;
- complete lift arms/pivot fasteners;
- camera yoke;
- actual LED/window face;
- quick release;
- protected cable loop;
- tail hardware that can enter the pipe envelope.

No production lift-stop dimension is released until this complete solid check and a real DN150 tube test both pass.
