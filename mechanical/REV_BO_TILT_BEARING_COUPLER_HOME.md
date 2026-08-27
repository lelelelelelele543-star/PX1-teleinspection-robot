# PX-1 Rev.BO — TILT bearings, coupler and HOME sensor

Status: prototype component freeze for TILT subassembly.

## Worm-shaft bearings
Selected standard size: 693, 3x8x4 mm.
For the sealed camera head, shielded 693-ZZ is acceptable because this bearing is inside the dry module and is not itself the water barrier.
ChipDip documentation lists CNIC 1000093 / 693 ZZ variants.

## Worm shaft
- shaft diameter: 3.0 mm
- two 693 bearings
- bearing span target: 14–18 mm
- axial movement target after assembly: <=0.10 mm
- worm is installed between bearings where practical so radial gear load is carried by both bearings.

## Coupling to N20
Do not depend on a rare purchased 3x3 mm coupling.
Prototype uses a simple machined rigid sleeve coupling:
- OD 6 mm
- length 10 mm
- bore 3.00 H7 through
- two M2 radial grub screws at 90° axial offset
- material: brass or stainless steel

The exact N20 output shaft form must be measured on the purchased motor before final machining. If it is D-shaped, one grub screw must bear on the flat.

## HOME sensor
Preferred architecture: non-contact Hall home switch + small permanent magnet on the TILT rotating member.
Candidate sensor: AH3364Q-class unipolar Hall switch.
Key characteristics:
- 3–28 V supply
- open-drain output
- active with south-pole magnetic field
- automotive temperature range

Because AH3364Q is NRND/EOL-family, it is a prototype candidate only. Production BOM must use an active equivalent with the same electrical function and package.

## Electrical interface to STM32
- sensor supplied from 5 V or 3.3 V only after exact selected part check;
- open-drain output pulled up to 3.3 V;
- 1–10 kΩ pull-up target, 4.7 kΩ nominal;
- optional 100 nF local decoupling;
- firmware applies debounce / stable-state filtering.

## HOME geometry
- magnet placed so HOME triggers slightly before mechanical zero reference;
- firmware then moves slowly to the calibrated zero offset;
- hard mechanical stops remain outside the commanded -105..+105 degree range;
- HOME sensor is not used as the only overtravel protection.

## Release holds
1. measure actual N20 output shaft geometry;
2. verify 693-ZZ running friction in the assembled worm carrier;
3. choose active-production Hall sensor replacement;
4. set exact magnet size and air gap from physical test;
5. verify repeatability of HOME over 100 cycles.
