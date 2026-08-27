# PX-1 Rev.BT — DN150 swept-clearance gate

Status: engineering check, not machining release.

## What changed
The DN150 check now uses the current Rev.BS lift coordinates and the Rev.BQ head package (Ø52 x 78 mm) through a full TILT sweep from -105 to +105 degrees in 2-degree increments, with the exact endpoints included.

The check also includes the two lift links as Ø10 solid proxies and the body/wheel reference geometry.

## Acceptance requirement
For LOW and DN150_SAFE positions:
- minimum nominal clearance to the DN150 inner wall: >=3.0 mm;
- no solid intersection with pipe wall;
- no lift-link intersection with pipe wall;
- no interference between head sweep and crawler body/lift hardware.

## Important limitation
The script must be executed in FreeCAD to obtain the numerical worst-case clearance. GitHub stores the geometry generator, but does not execute FreeCAD itself.

Even after the envelope sweep passes, DN150 is not RELEASED until these details replace their placeholders:
1. exact camera-head outer shell;
2. lens/window retaining ring;
3. LED/light protrusions;
4. quick-release latch;
5. ROLL waterproof rotary boundary;
6. actual lift fasteners and bushings.

## Decision rule
If the measured worst-case clearance is below 3.0 mm, do not shrink the safety margin. First adjust lift pivot Z, link angle, or head axial position. The Ø52 head limit should only be reduced if the real internal packaging allows it without compromising serviceability.
