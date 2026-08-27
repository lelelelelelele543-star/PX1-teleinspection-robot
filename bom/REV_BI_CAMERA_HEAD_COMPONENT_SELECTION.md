# PX-1 Rev.BI — camera-head component selection

Status: engineering selection for prototype, not final release.

## Camera
Selected baseline: RunCam Phoenix 2 analog camera module.
- sensor: 1/2 in CMOS
- video: CVBS, PAL/NTSC switchable
- horizontal resolution: 1000 TVL
- supply: 5–36 V
- current: about 120 mA at 12 V
- module envelope: 19 x 19 x 20 mm
- lens: M12, 2.1 mm baseline
Reason: compact, widely available, analog CVBS compatible with the PX-1 tether/console architecture, and much smaller than 32x32 mm CCTV boards.

## TILT motor
Prototype family: GM12-N20 / N20 all-metal micro gearmotor, 12 V.
Target gearbox output: 30–60 rpm unloaded.
Target motor envelope: about 12 x 10 x 36 mm including gearbox body, excluding output shaft.
Control: external H-bridge, PWM speed control; no controller PCB inside camera head.
Reason: inexpensive, common, reversible, small and easy to replace.

## ROLL motor
Same N20 12 V family as TILT to reduce spare-part count.
Target output: 30–60 rpm, with final spur reduction selected after torque/friction prototype measurement.
No continuous-rotation wiring may pass through a fixed pigtail.

## ROLL bearings
Selected geometry: 2x 6803-2RS / 61803-2RS.
- 17 mm bore
- 26 mm OD
- 5 mm width
Reason: leaves a 17 mm central passage while keeping OD only 26 mm, allowing a compact hollow roll spindle around the rotary electrical interface.

## Continuous ROLL electrical interface
Two-tier decision:

### Preferred production direction
A purpose-built video-capable rotary joint/slip ring with controlled 75 ohm video path plus power/control channels. JINPAT explicitly offers video slip rings with controlled 75 ohm impedance and compact diameters starting around 18 mm in relevant product families.

### Prototype-only fallback
12.5 mm capsule slip ring, 6 circuits, <=2 A/circuit, gold-contact type such as SenRing M125 / JINPAT LPM-06 class.
This fallback is acceptable for mechanical prototyping and low-speed electrical testing only.
It is NOT frozen for final CVBS because a generic six-wire capsule does not guarantee 75 ohm characteristic impedance and can introduce video noise/reflections.

## Architecture consequence
The head remains <=52 mm OD target. A 17 mm hollow roll spindle is retained as the current mechanical baseline. The final rotary-video part determines the exact spindle ID and rear-head length.

## Procurement priority
1. ChipDip where a suitable standardized part exists.
2. Ozon / Wildberries / AliExpress for N20 motors and prototype slip ring.
3. Specialist industrial supplier for the final video-rated rotary joint if marketplace versions cannot document signal integrity.

## HOLD items
- exact N20 supplier/gear ratio;
- exact 6803 brand/suffix;
- final video-rated rotary joint model;
- final roll gear ratio;
- final camera lens/FOV after real pipe-image test.
