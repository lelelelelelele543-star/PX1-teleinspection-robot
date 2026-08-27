# PX-1 Rev.BN — TILT worm support and torque check

Status: prototype engineering candidate.

## Support concept
The TILT worm is not carried directly on the N20 output shaft. It uses an independent Ø3 mm shaft supported by two miniature bearings. The N20 drives this shaft through a short coupling. This reduces sensitivity to supplier-to-supplier N20 shaft differences and prevents worm mesh loads from acting directly on the motor gearbox output bearing.

## Candidate dimensions
- worm shaft: Ø3 mm, 34 mm long;
- worm envelope: approximately Ø10 x 18 mm;
- two bearing envelopes: 3x8x4 mm;
- coupling envelope: Ø8 x 10 mm;
- selected worm class: m=0.5, one-start, 20:1 target.

Exact bearing and coupling SKUs remain HOLD until purchased motor shaft diameter/flat length are verified.

## Torque requirement
Worst-case camera-head design load used previously:
- effective moving mass: 0.25 kg;
- center-of-mass eccentricity: 30 mm;
- gravity torque = 0.25 x 9.81 x 0.030 = 0.0736 N·m;
- design factor 3 => required holding/output torque target >=0.221 N·m.

The selected N20-class motor has a documented stall-torque class around 0.118 N·m at its gearbox output. With a 20:1 worm stage, even allowing very poor overall worm efficiency, the theoretical available output torque is well above 0.221 N·m. Therefore strength is not the limiting issue; backlash, controllability, heat, tooth durability and actual backdrivability are the critical prototype tests.

## Mandatory bench tests
1. Measure no-load current of N20 + worm stage.
2. Measure current while lifting a 0.25 kg equivalent load at 30 mm offset.
3. Hold the load at 0°, +90° and -90° with power removed for 10 min each.
4. Any visible backdrive with power removed is a FAIL for passive holding; firmware braking cannot be the only retention method.
5. Run 500 full TILT cycles from -105° to +105° and inspect worm/wheel wear and backlash.
6. Record motor case temperature after repeated motion.

## Motion target
With a 200 rpm motor gearbox and 20:1 external worm stage, ideal TILT output is about 10 rpm, or 60°/s. Firmware should normally command far less than full PWM for inspection use. Final target speed: approximately 10–25°/s, with ramping near end stops.

## Position feedback
Use the N20 encoder for relative motion, but add a physical reference/home sensor or hard-stop calibration because power-cycle absolute angle cannot be trusted from incremental counts alone.

## Release hold
Do not machine the final TILT housing until exact bearing SKU, exact motor shaft geometry, matched worm set and home-sensor arrangement are frozen and physically tested.
