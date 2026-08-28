# PX-1 Rev.PG — CAM026-like simple electronics baseline

Status: ACTIVE SIMPLIFICATION BASELINE; exact purchased camera module/motors remain procurement HOLD.

## Source functions retained
The CAM026 source architecture shows the functions that must remain:
- front camera module + lens;
- PAN axis;
- continuous ROTATE axis;
- 6-way slip ring in the rotate connector;
- six front LEDs;
- angle feedback for motion control;
- sealed front optical window and sealed rotating interfaces.

Source-specific electronics that PX-1 intentionally deletes:
- focus motor MOT-001-761;
- focus motor PCB PCB-001-651;
- PAN motor control PCB PCB-001-759;
- ROTATE motor control PCB PCB-001-653;
- proprietary angle encoder PCBs/geared encoder electronics.

## PX-1 camera electrical architecture
Only the following active functions remain inside/near the camera:
1. one fixed-focus CVBS board camera;
2. one small PAN gearmotor;
3. one small ROTATE gearmotor;
4. one compact dual H-bridge module for PAN/ROTATE;
5. two contactless angle sensors or simple Hall/home sensors depending final control requirement;
6. six white LEDs with constant-current drive;
7. 6-way slip ring on continuous rotate axis.

No autofocus mechanism.
No camera-specific custom PCB.
No proprietary CAN/video processor.

## Fixed-focus video choice
Target characteristics:
- CVBS 1.0 V / 75 ohm output;
- PAL-compatible or PAL/NTSC selectable;
- 12 V preferred, 5 V acceptable if locally regulated;
- fixed 2.8..3.6 mm lens range;
- horizontal FOV target ~75..100 degrees;
- board/module envelope small enough for the CAM026 head.

A current readily documented analogue camera class exists with CVBS 960H fallback and 12 V supply. Exact board-level product is still HOLD because the currently found ChipDip camera example is a complete IP66 housing and is too large to install directly; it is only proof that simple 12 V CVBS electronics remain readily available.

## Angle feedback simplification
Original CAM026 uses dedicated angle encoder gears/PCBs on PAN and ROTATE.
PX-1 preferred replacement:
- AS5600-class magnetic absolute sensor for PAN where practical;
- for continuous ROTATE, AS5600-class angle feedback can also be used on the stationary/rotating axis if magnet/sensor packaging remains clear of the 6-way slip ring;
- fallback: Hall home sensor + time/current limited motion for PAN, while ROTATE remains continuous without absolute angle if the operator does not need a displayed azimuth.

The AS5600 class provides 12-bit absolute angle and is available as a ready-made module; no custom board is required.

## Motor control
Use one ready-made dual low-current H-bridge rather than separate proprietary camera motor boards.
Required class:
- 2 channels;
- >=12 V motor supply if selected motors are 12 V;
- >=1 A continuous/channel target gives large margin for 10 mm class gearmotors;
- 3.3 V logic compatible or simple level-safe inputs;
- brake/coast control.

TB6612FNG-class module remains acceptable for the prototype if actual camera motor stall current is below its safe channel limit.

## Camera internal conductor budget
The source CAM026 already uses a 6-way slip ring, so PX-1 keeps this architecture.
Preferred six circuits through continuous ROTATE joint:
- 1: camera/LED power +
- 2: ground
- 3: CVBS signal
- 4: PAN motor A
- 5: PAN motor B
- 6: sensor/control line or second supply/control depending final local-driver placement

This pinout is NOT frozen. A better option may be to place the PAN H-bridge on the rotating side so that only low-current power/video/control cross the slip ring. Final choice follows noise testing with real slip ring and CVBS.

## Critical test gate
Before freezing camera wiring:
1. run CVBS through the chosen 6-way slip ring while both PAN/ROTATE motors PWM;
2. run all six LEDs at maximum current;
3. inspect video for bars/noise/ground-loop artefacts;
4. if PWM noise is visible, move motor driver location/filtering or reserve paired conductors/grounding differently.

The objective remains CAM026 functionality with commodity electronics, not replication of MiniCam electronics.
