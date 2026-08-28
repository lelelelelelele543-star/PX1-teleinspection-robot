# PX-1 Rev.PF — RMP300 serviceable replacement baseline

Status: ACTIVE PROTEUS-LIKE REEL BASELINE; prototype, not procurement freeze.

## Source architecture retained
The PX-1 reel keeps the MiniCam RMP300 mechanical architecture from ASS-004-097 / ASS-004-094 / ASS-004-095 / ASS-002-696:
- manual drum;
- manual brake;
- mechanical level-wind;
- sprung measuring-wheel unit;
- main shaft with slip-ring interface;
- no powered reel motor.

## Standard mechanical parts retained directly
These are already standard catalogue parts in the source RMP300 and should remain standard parts in PX-1:

Left/slip-ring side:
- 61904-2RS, 20x37x9;
- 16006-2RS, 30x55x9;
- shaft seal 30x42x7;
- DIN 472 internal circlip 55x2.

Right/brake side:
- 61804-2RS, 20x32x7;
- 6203-2RS, 17x40x12;
- standard M6/M8 fasteners;
- simple spring-loaded mechanical brake retained.

Meter counter:
- 2x 618/8, 8x16x4;
- standard bushings and O-rings retained where dimensions match the rebuilt housing.

## Slip-ring replacement
Source item:
- 12-pole A6023-12 slip ring on ASS-004-094.

PX-1 candidate class:
- flange slip ring, body about Ø22 mm;
- 12 circuits;
- >=2 A per circuit;
- >=60 VDC working capability (candidate found is rated much higher);
- low-speed duty only.

Provisional channel allocation for the Proteus-style 6-core tether:
- circuits 1+2 paralleled = PWR+;
- circuits 3+4 paralleled = PWR-;
- circuit 5 = RS485_A;
- circuit 6 = RS485_B;
- circuit 7 = VIDEO+;
- circuit 8 = VIDEO-;
- circuits 9..12 = spare / future / redundancy.

Reason for paralleling power paths: a common inexpensive 12-way ring at ~2 A per circuit is adequate for the current elevated-voltage tether concept when two tracks are paralleled per pole, while retaining four independent signal circuits. Final release still depends on measured tether current and slip-ring temperature/noise testing.

## Distance measurement replacement
The original meter-counter mechanics are retained:
- measuring wheel FAL-002-145;
- sprung roller contact from ASS-002-696;
- measuring axle FSS-002-147;
- 618/8 bearing pair.

Deleted:
- proprietary `PCB Meterzähler`.

Preferred simple electronic replacement:
- AS5600-class contactless magnetic angle sensor module;
- diametrically magnetized magnet on the measuring axle;
- MCU counts 0/360 degree wraps and direction;
- no gears and no optical disk required.

Why this is preferred:
- no contact wear;
- inexpensive and replaceable;
- 12-bit absolute angle per revolution;
- I2C/PWM/analog capable depending module;
- measuring calibration is done in software from actual cable travel per wheel revolution.

Calibration rule:
1. mark cable at 0 m;
2. pull exactly 5.000 m through the meter unit under normal spring pressure;
3. record total angle/revolutions;
4. store `mm_per_rev` / effective rolling circumference in controller EEPROM;
5. repeat forward and reverse; reject if hysteresis exceeds the agreed limit.

This deliberately avoids assuming the exact FAL-002-145 effective diameter because the available assembly drawing does not dimension it.

## Deleted RMP300 electronics
PX-1 does not reproduce:
- proprietary slip-ring PCB;
- proprietary meter counter PCB;
- any reel motor controller.

The reel electronics reduce to:
- passive 12-way slip ring;
- AS5600-class sensor + magnet;
- small connector/harness only.

## Release gates
- measure purchased slip-ring torque/contact resistance and noise under video + RS485 + power load;
- confirm current sharing between paralleled power tracks;
- verify AS5600 survives stray field from nearby reel steelwork and magnet placement;
- 1000-cycle reel rotation test;
- 40 m cable distance calibration repeatability test;
- retain manual fallback distance marks on tether for first prototype.
