# PX1 engineering decisions — 2026-09-16

These decisions control Rev.A unless a physical test disproves them.

## D-001 — six-wheel base is mandatory
Rev.A remains 6×6. Wheel stations X50/X150/X250 and five m1 Z50 stations per side are frozen.

## D-002 — stop adapting the crawler around the Pololu 25D motor
For A0, switch the mechanical traction baseline to the source-envelope-matched FAULHABER 2250S024BX4 + 26/1 S three-stage package. The 66:1 version is the working ratio candidate. The old Pololu5707 adaptation remains fallback/history only.

Reason: the source motor-unit drawing and the 53 mm dry cavity are naturally explained by two Ø26 gearheads on 27 mm centres. This removes a large amount of invented motor-mount geometry.

## D-003 — preserve the separately supported Z16 axle
Do not hang Z16 directly on the motor/gearhead output. Keep ASS-002-386 logic: gearhead output -> supported FSS-002-083-like axle -> 61801 -> Z16.

## D-004 — BLDC driver path
A complete Hall-capable 24 V driver module is required if D-002 passes. TMCM-1640 is the preferred engineering candidate because it combines BLDC commutation, Hall input, current/velocity control and RS485 in 42x42x15 mm. Actual allowed-seller availability remains a procurement gate.

## D-005 — no low-torque generic bevel pair for qualification
The m1 Z16/Z40, 1:2.5 geometry is source-supported and standard 20° reference geometry is useful for packaging. However A0 full-load testing requires a gear pair with adequate material/heat treatment and torque capacity. A generic unhardened catalogue pair is not accepted solely on matching module/tooth count.

## D-006 — accelerate with a separate A0 fixture
Do not wait for the pressure body. A0 uses printable/machinable fixture plates with exact 50 mm Z50 centres and bench bearings. This fixture is explicitly disposable and cannot release final body/bearing/seal dimensions.
