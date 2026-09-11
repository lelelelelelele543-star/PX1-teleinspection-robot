# PX-1 Rev.B — WB13A camera/reel rotary electrical interfaces

Date: 2026-09-11
Status: REEL CANDIDATE RETAINED / CAMERA ROTARY ARCHITECTURE CORRECTED / SIGNAL QUALIFICATION HOLD

## 1. Scope

WB13A controls two different rotary interfaces:
1. continuous internal ROLL interface inside the camera head;
2. manual RMP300-style reel interface for the six-core tether.

It does not change the main-tether functional allocation:
- HV+ / HV-;
- RS485_A / RS485_B;
- VIDEO+ / VIDEO-.

## 2. Source comparison retained

MiniCam CAM026 source `ASS-001-920 / ASM011` contains a `COM-001-800 SLIP RING 6 WAY` inside separately sealed rotate-connector metalwork.

RMP300 source `ASS-004-094` contains a separate protected slip-ring assembly and a 12-pole ring.

PX-1 keeps two physically independent rotary interfaces. Neither slip ring is itself a sewer pressure boundary.

## 3. Reel candidate — unchanged

Preferred Rev.B reel candidate remains SenRing `M220-0205-12S`:
- OD 22 mm;
- length 40 mm;
- two 5 A power circuits;
- twelve signal circuits;
- up to 240 VAC/VDC class;
- IP51 only, therefore installed inside the protected reel enclosure.

Reel functional allocation:
- P1 = HV+;
- P2 = HV-;
- S1/S2 = RS485_A / RS485_B;
- S3/S4 = VIDEO+ / VIDEO-;
- unused signal rings individually insulated.

The extra physical rings do not create extra tether conductors.

## 4. Camera-load correction from WB14

WB13 originally treated PAN/ROLL motor current and LED current as if they crossed the continuous camera ROLL interface. That was wrong for the active mechanical architecture.

Current camera-head architecture is:
- fixed sealed outer shell;
- fixed-shell LED annulus;
- TILT and ROLL actuators/drivers on the non-rotating side of the internal ROLL interface;
- ordinary integrated inner ROLL spindle/carrier on two bearings;
- only the RunCam sensor/lens carrier rotates continuously.

Therefore the internal ROLL slip ring does **not** carry:
- LED current;
- LED PWM;
- TILT motor current;
- ROLL motor current;
- local fixed-side controller power.

## 5. Correct internal ROLL functions

The rotating RunCam requires four functional conductors:
1. `+12V_CAM_ROT`;
2. `GND_CAM_ROT`;
3. `CVBS_SIGNAL`;
4. `CVBS_RETURN`.

A six-ring device is intentionally retained so two physical contacts remain spare.

Local UART used between crawler and camera-head fixed electronics does **not** cross the continuous ROLL interface.

This is the key distinction between:
- the external six-pin camera-head quick connector; and
- the internal continuous four-function ROLL transfer.

## 6. Camera slip-ring selection correction

SenRing `M125-06` becomes the Rev.B engineering candidate for the internal ROLL interface.

Manufacturer-controlled data:
- model: `M125-06`;
- OD: 12.5 mm;
- body length: 13.5 mm;
- six circuits;
- max current: 1.5 A per circuit;
- lead wire: silver-plated PTFE AWG30;
- standard lead length: 150 mm;
- speed class: 250 rpm;
- gold-gold contact system;
- IP51;
- manufacturer electrical-noise figure: <0.01 ohm.

Packaging reason:
- current ROLL bearings are 6803 / 61803, ID 17 mm;
- M125 OD 12.5 mm passes through the 17 mm central bore;
- nominal radial clearance inside the bearing bore is `(17 - 12.5)/2 = 2.25 mm` before any support sleeve/lead protection;
- the previously proposed M220 OD 22 mm cannot pass through the 17 mm bearing bore and is rejected for the camera.

## 7. Camera current margin

RunCam Phoenix 2 design reservation remains 12 V / 120 mA until the purchased sample is measured.

Rev.B internal-ROLL design current envelope:
- expected camera normal current: approximately 0.08...0.12 A;
- provisional qualification envelope: <=0.25 A including startup/tolerance;
- M125-06 circuit rating: 1.5 A.

This gives large current margin provided no motor/light/controller loads are later moved across the interface.

Any future architecture change that adds such a load automatically invalidates the M125-06 freeze and reopens WB13.

## 8. M125-06 allocation

Use after incoming continuity mapping:
- ring 1: `+12V_CAM_ROT`;
- ring 2: `GND_CAM_ROT`;
- ring 3: `CVBS_SIGNAL`;
- ring 4: `CVBS_RETURN`;
- ring 5: SPARE insulated;
- ring 6: SPARE insulated.

Final physical ring order may be changed before harness release if video crosstalk testing shows a better arrangement. Spare rings are not paralleled and are not used as improvised shields.

## 9. Signal-integrity rule

M125 electrical-noise/contact-resistance data does not prove a controlled 75-ohm video path.

Required validation:
- RunCam direct into 75 ohm baseline;
- through static M125;
- through continuously rotating M125;
- then through fixed-side Delta-Opti balun;
- then through 40 m tether;
- then through reel ring;
- then 100/150 m equivalent;
- repeat with traction PWM, ROLL/TILT motors and LED PWM active.

Reject the M125 if rotation creates visible bands, sync loss, chroma errors or unacceptable amplitude change even if DC continuity is perfect.

## 10. Mechanical rule

M125 is non-structural.

- two 6803 bearings carry the ROLL spindle loads;
- slip ring is supported by its own normal clamp/holder;
- leads receive strain relief;
- no radial bearing load is transferred through the plastic M125 housing;
- replacement must not disturb the front optical-window seal.

No cartridge/cassette architecture is permitted.

## 11. Sealing

M125 is IP51 and must remain completely inside the separately sealed camera-head volume.

It is not a pressure boundary and is never exposed directly to sewer water.

## 12. Incoming inspection

For each purchased M125:
1. photograph model/lead colours;
2. map every stator/rotor lead by continuity;
3. record static contact resistance;
4. rotate and monitor all used contacts;
5. run a protected 0.25 A camera-power test first;
6. perform raw-CVBS rotating test before assembly release.

## 13. WB13A decisions

- Reel: retain `M220-0205-12S` candidate.
- Camera internal ROLL: replace impossible Ø22 M220 with `M125-06` Ø12.5 x 13.5 mm candidate.
- Internal ROLL uses only camera power + raw CVBS; two rings remain spare.
- External camera-head connector remains a separate six-function interface and is controlled by WB15.
- Full video qualification remains mandatory.

## Change log

### 2026-09-11 — WB13
- selected mixed M220 reel candidate;
- initially overestimated rotating camera load and proposed M220 for camera.

### 2026-09-11 — WB13A / correction after WB14
- identified that LED and axis-drive currents do not cross internal ROLL;
- identified hard geometric conflict: Ø22 M220 cannot pass through 6803 ID17;
- restored compact M125-06 as camera internal ROLL candidate;
- reduced internal ROLL functions from six assumed functions to four real functions;
- kept two unused rings as insulated service spares;
- preserved reel selection and six-core main-tether architecture unchanged.
