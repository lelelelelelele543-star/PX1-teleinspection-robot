# PX-1 Rev.PH — Proteus-faithful system baseline after reel/camera simplification

Status: ACTIVE MASTER BASELINE.

## Project rule
PX-1 is a serviceable replacement for MiniCam Proteus CRP-150, not a new crawler concept.
Preserve proven Proteus mechanical architecture where practical; replace proprietary/unavailable electronics and bought parts with commodity equivalents.

## Crawler drive
Active topology:
- 6 wheels total;
- 5x Z50 per side;
- wheel gears at X50 / X150 / X250;
- idlers at X100 / X200;
- long axle / bevel input is on the rear wheel station X250;
- no separate fourth input shaft;
- 2 motors total through Z16 -> Z40, one motor per side.

Source references: DRW-002-374 / DRW-002-375.

## Camera
CAM026-like external/function target retained:
- pan/rotate form factor;
- continuous rotate function;
- PAN range target +/-135 degrees;
- six front LEDs;
- sealed optical window;
- 6-way internal slip ring.

Simplifications:
- delete autofocus motor and focus PCB;
- delete proprietary PAN/ROTATE motor control PCBs;
- delete proprietary angle encoder PCBs;
- use fixed-focus CVBS board camera;
- one commodity dual H-bridge for PAN/ROTATE;
- commodity magnetic/Hall angle feedback.

## Manual lift
DRW-002-744 topology is retained exactly in principle:
- 150 N gas spring;
- compact side-lever arrangement;
- M8 clamping lever;
- Belleville washer stack and source fastener/seal architecture.

IMPORTANT: Rev.PD provisional dimensions collide with the crawler body during conservative integration. Those guessed dimensions are rejected. The lift is a physical/detail-drawing measurement gate; do not redesign it just to remove the conflict.

## RMP300-like reel
Keep source RMP300 mechanical architecture:
- manual reel;
- mechanical brake;
- chain-driven level-wind;
- 272 mm spindle;
- 362 mm bar;
- sprung measuring-wheel unit;
- standard bearing architecture.

Source chain drive is 670 mm chain with Z30 and Z16 sprockets.

Standard source bearings retained:
- left: 61904-2RS + 16006-2RS + 30x42x7 shaft seal;
- right: 61804-2RS + 6203-2RS;
- meter unit: 2x 618/8.

Simplified electronics:
- source A6023-12 12-pole slip ring replaced by commodity 12-way flange slip ring class;
- proprietary slip-ring PCB deleted;
- proprietary meter-counter PCB deleted;
- AS5600-class magnetic sensor on measuring axle preferred;
- no reel motor.

## Current external candidate evidence
Commodity 12-way flange slip-ring class found with ~Ø22 mm body, 12 circuits, 2 A/circuit, 240 V rating and low-speed suitability. Initial PX-1 power mapping pairs two tracks per power pole, leaving four signal tracks plus spare circuits. Final current/noise testing remains mandatory.

AS5600-class ready modules provide 12-bit absolute angle and are suitable for contactless reel-distance sensing after software calibration.

## Next engineering order
1. lock RMP300 mechanical CAD around source-standard bearings, Z30/Z16 chain and commodity slip-ring envelope;
2. build actual meter-counter replacement around source FAL-002-145 / FSS-002-147 plus AS5600 magnet;
3. bench-test slip-ring video/RS485/power noise architecture before freezing reel wiring;
4. source or physically measure the ten missing CRP150 lift dimensions and then rebuild lift without guesses;
5. integrate real CAM026-like camera and measured lift into DN150 crawler;
6. only after that update the interactive 3D viewer.
