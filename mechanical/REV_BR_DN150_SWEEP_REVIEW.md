# PX-1 Rev.BR — DN150 dynamic sweep review

Status: engineering clearance study, not release.

## What changed
The DN150 check is now dynamic rather than a simple static diameter comparison. The current combined head envelope is Ø52 x 78 mm and is sampled through TILT angles from -105 to +105 degrees in both LOW and DN150_SAFE lift positions.

## Acceptance target
For LOW and DN150_SAFE positions the nominal geometric clearance to a true Ø150 mm pipe must remain at least 3.0 mm through the complete TILT range.

## Important limitation
The exact vertical and longitudinal location of the camera pivot relative to the wheel contact plane is not yet frozen. Therefore Rev.BR uses a provisional lift pivot datum and cannot honestly declare DN150 PASS/FAIL for production yet.

This is intentional: the model will not be adjusted to force a PASS before the exact lift brackets and camera mounting geometry are finalized.

## Next required geometry
1. freeze the front-cover lift pivot coordinates relative to body datum;
2. model real 90 mm wheel contact plane and body attitude in a Ø150 pipe;
3. replace 68 mm arm/link envelopes with actual lift plates and pivots;
4. add full camera shell, light ring and quick-release hardware;
5. sweep TILT in 2-degree increments from -105 to +105;
6. check both straight pipe and small body roll/pitch offsets representing real travel.

Only after this sweep passes with >=3 mm nominal clearance may the DN150_SAFE label be treated as a validated operating position.
