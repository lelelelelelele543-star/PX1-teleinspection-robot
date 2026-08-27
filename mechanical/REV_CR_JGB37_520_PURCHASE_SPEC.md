# PX-1 Rev.CR — JGB37-520 purchase specification

Status: prototype procurement specification; exact supplier SKU remains HOLD until purchased sample is measured.

## Required configuration
Order/search only for a motor matching ALL of these:
- family: JGB37-520;
- rated voltage: 24 V DC;
- no-load output speed: 45 rpm nominal (acceptable 40–50 rpm only if documented);
- Hall quadrature encoder: A/B channels;
- encoder supply: 3.3/5 V compatible preferred;
- output shaft: 6 mm D-shaft;
- output shaft length: approximately 14–15.5 mm;
- metal gearbox;
- reversible brushed DC motor.

Do not buy a plain two-wire version without encoder for the PX-1 traction prototype.

## Evidence found during selection
Current market listings confirm that 24 V / 45 rpm / 6 mm shaft variants exist. Listings also show encoder-equipped JGB37-520 variants with 6 mm D-shaft and Hall A/B feedback. However, seller naming is inconsistent, so the exact purchased item must be checked before CAD dimensions are released.

## Encoder interface assumption
Common encoder version uses six connections:
- motor + / motor -;
- encoder VCC / GND;
- Hall A;
- Hall B.
Typical base encoder resolution is stated as 11 pulses per motor revolution; output-shaft resolution therefore depends on actual gearbox ratio. Firmware must determine/verify counts per output revolution experimentally rather than relying only on seller text.

## Incoming inspection
For each purchased motor record:
1. body and gearbox dimensions;
2. D-shaft diameter, flat depth and usable length;
3. mounting-hole pattern;
4. exact no-load rpm at 24.0 V;
5. no-load current;
6. encoder supply compatibility and A/B waveform;
7. encoder counts per output revolution;
8. controlled loaded current;
9. short controlled stall-current pulse;
10. gearbox backlash and audible defects.

Purchase at least 2 identical samples for comparison; 4 identical units are preferred if price permits so spares remain from the same production batch.

## CAD rule
Motor pinion/hub must clamp mechanically on the 6 mm D-shaft and remain replaceable with hand tools. Do not permanently bond the gear to the motor shaft. Final bore tolerance, key/flat geometry, hub length and set-screw location are HOLD until the actual shaft is measured.

## Current candidate search phrase
`JGB37-520 24V 45RPM Hall encoder 6mm D shaft`

## Release gate
No final motor mounting drawing or pinion drawing is RELEASE until a physical motor is measured.