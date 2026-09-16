# PX1 engineering decisions — 2026-09-16

These decisions control Rev.A unless a physical test disproves them.

## D-001 — six-wheel base is mandatory
Rev.A remains 6×6. Wheel stations X50/X150/X250 and five m1 Z50 stations per side are frozen.

## D-002 — motor package is a gated interface, not an assumed identity
Stop adapting the crawler around oversized motor packages, but do not claim that MiniCam `MOT-001-760` was a specific FAULHABER assembly.

The source proves two motors, a common holder, separate supported Z16 shafts and a compact approximately Ø26-gearhead / Ø22-motor envelope class. Two candidate paths are maintained only at the motor interface:
- existing/known-compatible FAULHABER 2250S024BX4 + 26/1 S 66:1 stock assembly, if the actual parts are mechanically compatible as a unit;
- current manufacturer-supported 2250S024BX4 + 26A package in the same approximate Ø26 / 96 mm envelope.

The six-wheel side drive and rear X250 input are developed independently so this decision cannot block A0/A1 chassis work.

## D-003 — preserve the separately supported Z16 axle
Do not hang Z16 directly on the motor/gearhead output. Keep ASS-002-386 logic: gearhead output -> supported FSS-002-083-like axle -> 61801 -> Z16.

## D-004 — traction electronics follow motor class
If a 2250 BLDC package passes A0, use a Hall-capable 24 V BLDC driver. TMCM-1640 remains the preferred ready-made engineering candidate, but is STUDY until stock/revision/connectors/thermal mounting are confirmed.

If a brushed motor package is ultimately frozen, retain a compact H-bridge path instead. BTS7960/Pololu G2 must never be used to commutate a 2250 BX4 BLDC motor.

## D-005 — no low-torque generic bevel pair for qualification
The m1 Z16/Z40, 1:2.5 geometry is source-supported and standard 20° reference geometry is useful for packaging. However A0 full-load testing requires a gear pair with adequate material/heat treatment and torque capacity. A generic unhardened catalogue pair is not accepted solely on matching module/tooth count.

## D-006 — accelerate with a separate A0 fixture
Do not wait for the pressure body. A0 uses printable/machinable fixture plates with exact 50 mm Z50 centres and bench bearings. This fixture is explicitly disposable and cannot release final body/bearing/seal dimensions.

## D-007 — A1 rolling chassis may precede the final motor package
A printable six-wheel rolling fixture is allowed before final motor/gearhead release. It preserves X50/X150/X250, the five Z50 stations and rear X250 drive input, but uses bench shafts/bearings and non-production wheel screens. Its purpose is to prove the complete left/right gear trains, rolling resistance and differential steering while H01/H02/H04 remain open.
