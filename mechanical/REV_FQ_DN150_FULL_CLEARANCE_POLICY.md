# PX-1 Rev.FQ — DN150 complete clearance policy

Status: prototype design rule.

## Why this is required
An ideal cylinder check of the camera alone is not enough. The actual limiting points are now spread across side covers, flush fasteners, lift pivots, yoke cheeks, camera retainer and cable/boot envelopes.

## Reference geometry
Current ideal DN150 model:
- pipe radius 75.0 mm;
- pipe axis Z ≈52.048 mm from current Ø90 profiled-wheel contact model;
- wheel crown contact is intentional and excluded from clearance calculations.

## Current verified numeric margins
From executed project checks:
- camera Ø52 x 72 at LOW Z75 with TILT -105..+105: ~7.64 mm minimum ideal clearance;
- upper lift-pivot hardware envelope after Rev.FM lowering: ~7.51 mm nominal;
- side-cover lower corner from Rev.FF class geometry: ~5.6 mm ideal;
- side-cover upper corner: ~10.8 mm ideal.

Therefore the side-cover lower region remains the present nominal hard point, not the camera cylinder.

## Design rules
For every non-wheel external solid in DN150 configuration:
- preferred ideal CAD clearance >=5 mm;
- absolute prototype CAD minimum >=3 mm only where tolerance stack is explicitly reviewed;
- screw heads may not project outside the validated envelope;
- no cable loop is allowed to become the lowest-clearance item;
- all removable DN150-stop hardware must remain captive and inside the envelope.

Physical qualification must be stricter than ideal CAD because real pipe can be oval, dirty, jointed or locally reduced.

## Fastener policy for DN150
- lower side-cover screws: flush/countersunk or recessed below cover surface;
- lift pivot retention: low-profile/countersunk/circlip solution; no tall socket head toward pipe wall;
- yoke fasteners: heads toward centerline where possible;
- front window retainer screws: recessed/flush;
- no exposed threaded stud at camera sides.

## LOW camera configuration
DN150 mechanical stop locks the lift in LOW.

Allowed:
- full TILT -105..+105 only after complete solid sweep confirms it;
- continuous internal ROLL because the external shell does not rotate around the pipe axis.

Not allowed in DN150:
- MID lift;
- HIGH lift;
- removal/defeat of DN150 stop during operation.

## Cable loop
A flexible electrical loop is still necessary between lift cradle and camera head/body.

DN150 rules:
- loop retained on pipe-centerline side of arm/yoke;
- minimum bend radius follows selected cable;
- loop cannot hang below the camera or outboard of yoke cheek;
- physical sweep includes worst-case loop from TILT extremes.

## Physical tube gate
Before any drawing is stamped RELEASE:
1. manufacture/obtain a rigid ID150 test tube at least 1 m long;
2. verify actual ID at several angular positions;
3. install complete crawler with production-intent wheels, all screws, tail boot and camera cable;
4. push/pull manually through tube with motors off;
5. run full TILT sweep at LOW every 100 mm;
6. drive forward/reverse under power;
7. repeat with representative wet grit/deposit simulator;
8. photograph and record any witness marks.

No contact is allowed except intended wheel tread.

## Release consequence
Any change to:
- wheel profile;
- side-cover thickness/width;
- screw-head style;
- lift pivot position;
- yoke width;
- camera external diameter/length;
- rear/front cable routing
requires rerunning DN150 clearance qualification.