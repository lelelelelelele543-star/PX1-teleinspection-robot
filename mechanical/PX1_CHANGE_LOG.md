# PX1 Change Log

## 2026-09-14 - final-current rebuild

- Rejected the prior primitive-box/cylinder representation as a manufacturing release.
- Rebuilt one current assembly around the Proteus CRP-150 drivetrain topology.
- Corrected side-drive bearing quantity to **6 x 61801 per side = 12**, plus 2 x Z16 support bearings = 14 total.
- Replaced smooth Z50 discs by visible 50-tooth m1 gear solids; final tooth system remains supplier/source HOLD.
- Added complete wheel-station stacks: 2 x 61801 + 61903 + X-ring + flange + shaft at all six stations.
- Added two motor paths with the published ISL PGM-32P envelope and NBK MLR-20C-6-6 coupling envelope.
- Added manual parallelogram lift, gas spring, separate sealed camera, six-core harness, pressure cover/valve/gland, SP13 local connector and SP17 rear connector.
- Selected Adafruit MPRLS Product 3965 as the current ready-made absolute pressure sensor candidate and modeled its published envelope.
- Validation now has **no global PASS** while any placeholder/measurement HOLD controls release.
- Full DN150 remains HOLD until a real QRW90SR/150 wheel profile/hub is closed and physically tested.

### CAM026 evidence update

- Incorporated user teardown photos/video of CAM026.
- Recorded the lower/base cylindrical outer diameter as approximately **62.5 mm** from the caliper photo.
- Retired the previous ~Ø52 camera proxy.
- Preserved the observed camera architecture in current CAD: hollow central wiring path, internal ring-gear output, multi-stage reduction and thrust-bearing axial support.
- Internal CAM026 wall thickness, fits, tooth geometry and seal-groove dimensions remain HOLD. They are not inferred from photographs.
- No additional user teardown/measurement work is required; unresolved camera dimensions move to controlled-drawing / supplier-sample / prototype closure.

### Current validation snapshot

- Frozen counts match: 6 wheels, 10 Z50, 12 side-drive 61801, 6 61903, 6 X-rings, 2 Z40, 2 Z16, 2 Z16-support 61801, 2 motors, 6 local camera conductors.
- Current assembly reports no invalid CAD shapes.
- Modeled service-vs-Z50, service-vs-lift, service-vs-camera and motor-vs-camera intersections are 0 mm³.
- CAM026-derived camera LOW ideal-DN150 screen clearance is approximately 20.80 mm.
- Reconstructed pressure-body ideal-DN150 screen clearance is only approximately 1.01 mm and therefore remains a major release HOLD.