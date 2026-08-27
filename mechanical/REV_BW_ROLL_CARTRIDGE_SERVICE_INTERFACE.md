# PX-1 Rev.BW — ROLL cartridge service interface

Status: engineering candidate, not machining RELEASE.

## Cartridge retention
- rotating cartridge OD: 30 mm nominal;
- support: 2x 6803-2RS (17x26x5);
- front bearing locates against a machined shoulder;
- rear bearing retained by a removable threaded/service ring;
- no adhesive is used as the primary axial bearing retention;
- light axial preload only: avoid loading the miniature bearings unnecessarily.

## ROLL gear adjustment
The N20 ROLL motor mount receives slotted adjustment approximately ±0.75 mm in the gear center-distance direction. Nominal m0.5 z17/z51 center distance remains 17.0 mm. Backlash is set during assembly, then the motor bracket is locked mechanically.

Do not eliminate all backlash: the gear pair must rotate freely through 360 degrees without tight spots after the head reaches operating temperature.

## Service interface
Rear service ring is accessible only after the complete camera head has been removed from the lift quick-release. Normal ROLL cartridge servicing therefore does not require opening the crawler main pressure body.

Disassembly order:
1. remove camera head from lift;
2. remove rear dry-side service cap;
3. disconnect internal service connector;
4. remove bearing-retaining ring;
5. withdraw rotating cartridge as a module.

## Wiring through TILT
A protected hollow/service passage is reserved through the TILT axis. Wiring must not cross a pinch point through the full -105..+105 degree range. Minimum prototype rule: leave a controlled service loop at neutral position and mechanically constrain it away from worm/gear teeth.

ROLL itself remains continuous and therefore cannot use this service loop for rotating camera conductors; the video/power path across ROLL must pass through the rotary electrical transfer.

## Connector philosophy
Inside the removable camera head use one small keyed service connector between fixed-head harness and TILT/ROLL module. Exact connector is HOLD until conductor count/current and final rotary-transfer leads are frozen.

## Release gates
- exact retaining-ring thread and shoulder tolerances;
- exact 6803 fits for selected housing/shaft materials;
- measured ROLL backlash/current across 360 degrees;
- verified TILT wiring sweep without rubbing/pinching;
- final rotary video transfer;
- complete pressure/leak test of assembled head.
