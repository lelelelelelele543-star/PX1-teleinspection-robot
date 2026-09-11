# PX-1 Rev.B — CAM026-inspired camera electrical baseline

Date: 2026-09-11
Status: ACTIVE CAMERA ELECTRICAL BASELINE / SLIP-RING+VIDEO QUALIFICATION HOLD
Supersedes `PX1_CAM026_Electrical_RevPM.md` where video-balun location, rotating electronics or camera rotary pinout differs.

## 1. Source-derived architecture retained

MiniCam CAM026 source evidence shows:
- `COM-000-003 PAL DSP CAMERA MODULE` in the camera housing;
- `COM-001-800 SLIP RING 6 WAY` in the rotate connector assembly;
- camera-side connection PCB around the rotary interface;
- separate camera-axis mechanisms;
- six-way rotary electrical architecture.

PX-1 keeps the proven idea of a compact six-circuit rotary interface, but does not copy proprietary MiniCam electronics.

## 2. Mechanical/electrical interpretation corrected in WB14

Active PX-1 head mechanics are:
- static sealed outer shell relative to the internal continuous ROLL joint;
- whole head TILT handled outside the ROLL interface;
- LED annulus fixed to the static outer shell;
- TILT/ROLL motors, drivers, sensors and lighting control fixed-side relative to the ROLL slip ring;
- only the camera sensor/module itself requires continuous electrical transfer.

Therefore camera lighting and motor current must **not** be routed through the ROLL slip ring.

This correction removes an unnecessary high-current requirement and reduces rotating mass/wiring.

## 3. Rev.B ROLL slip-ring functions

Preferred physical device remains six circuits for source-like service/spares, but only four are used:

1. `+12V_CAM`
2. `GND_CAM`
3. `CVBS_SIGNAL`
4. `CVBS_RETURN`
5. SPARE — insulated
6. SPARE — insulated

Important:
- `CVBS_RETURN` carries only camera video return/current;
- it never carries motor or LED current;
- no UART is required through the ROLL interface for the fixed-focus Rev.B camera;
- camera setup/menu is performed before deployment;
- main tether remains balanced `VIDEO+ / VIDEO-` after the fixed-side balun.

## 4. Camera module baseline

Selected family:
- RunCam Phoenix 2 analog CVBS camera;
- 1/2 in CMOS;
- PAL/NTSC switchable;
- 5...36 V input;
- conservative 12 V design-current reservation 120 mA until purchased sample is measured;
- 19 x 19 x approximately 19...20 mm standard-camera envelope;
- stock M12 2.1 mm wide-angle lens retained only for first optical test.

Exact current product/listing and final lens are controlled in `REVB_WB14_CAMERA_AND_LIGHTING.md`.

## 5. Camera slip-ring candidate

Leading engineering candidate after WB13A correction:
- SenRing `M125-06`;
- Ø12.5 x 13.5 mm;
- 6 circuits;
- 1.5 A per circuit;
- AWG30 silver-plated PTFE leads;
- gold-gold contacts;
- IP51, therefore kept entirely inside the sealed camera head.

Why M125 instead of the earlier M220 camera proposal:
- current rotating load is only camera power, not lighting/motors;
- M125 fits through the current 6803 bearing ID17 central passage with 2.25 mm nominal radial clearance;
- M220 OD22 cannot pass the active ID17 central passage and is therefore rejected for the camera.

M220 mixed power/signal remains a reel candidate; this correction applies only to the camera.

## 6. Fixed-side local head electronics

Camera-head control architecture may still use a small local controller on the **fixed side** of the ROLL joint to reduce quick-connector pin count and centralize camera-axis control.

Fixed-side functions:
- receive local camera commands from crawler MCU over the reserved UART;
- drive TILT and ROLL H-bridges as mechanically assigned;
- read fixed-side/home/angle sensors;
- generate LED PWM;
- supervise local camera-head faults.

Current prototype controller family:
- RP2040-Zero class remains acceptable as a ready-module candidate;
- it is no longer placed on the continuously rotating camera carrier.

The main crawler MCU reserved UART remains:
- PC12 / UART5_TX;
- PD2 / UART5_RX.

Exact local head controller and its 12->5 V supply remain packaging/procurement HOLD until the head fixed-side electronics carrier is finalized.

## 7. Lighting

Illumination is fixed to the static outer shell and is governed by WB14.

Current architecture:
- six XP-family white emitters;
- six 8 mm-class commercial MCPCBs around PCD40;
- two independent 3-LED strings;
- two ready P4115adj constant-current modules;
- starting current ~300 mA/string;
- common PWM command;
- LEDs thermally clamped to the aluminium front carrier;
- no light power/control crosses the ROLL slip ring.

## 8. Video path

Rotating side:
`RunCam CVBS -> M125-06 CVBS_SIGNAL/CVBS_RETURN`.

Fixed camera-head/crawler side:
`M125 raw CVBS -> short 75-ohm pigtail -> Delta-Opti TR-1D*P2 -> balanced VIDEO+/VIDEO-`.

Main tether:
`VIDEO+/VIDEO- balanced pair`.

CCU:
`VIDEO+/VIDEO- -> second TR-1D*P2 -> 75-ohm CVBS -> OSD -> GF-AM071`.

No coaxial conductor exists in the main tether. Short local 75-ohm interconnect inside sealed/serviceable assemblies is allowed.

## 9. Video qualification

A generic gold-contact slip ring is not a guaranteed 75-ohm rotary joint.

Required physical sequence:
- RunCam direct into 75 ohm;
- through M125 stationary;
- through M125 rotating continuously;
- add Delta balun pair;
- add 40 m tether;
- add reel slip ring;
- repeat at 100/150 m equivalent;
- run TILT/ROLL motor switching, traction PWM and LED PWM during test.

M125 is rejected for production video if rotation produces unacceptable amplitude modulation, sync loss, chroma errors or visible bands/dropouts.

## 10. Fixed-side motor/axis rule

Current Rev.B mechanical camera architecture uses TILT and continuous ROLL.

The ROLL motor is not on the rotating camera carrier; it drives that carrier mechanically from the fixed head side. Therefore motor power does not cross the roll slip ring.

Likewise the LED ring is fixed and does not rotate with the image sensor.

Any later proposal that adds a motor or controller to the continuously rotating carrier is an architecture change and must reopen the rotary-current, thermal and slip-ring gates.

## 11. Failure behavior

- crawler-to-head local UART timeout -> TILT/ROLL commands zero and light to configured safe state;
- invalid axis sensor -> affected camera axis stops;
- crawler main-command timeout -> traction and camera-axis commands stop;
- video failure does not disable hardware E-STOP;
- hardware CCU E-STOP removes crawler/tether power independently of camera-head software.

## 12. Service rule

The camera head remains separately sealed and field removable without opening P1/P2 side-drive pressure zones.

The fixed-side video balun remains accessible without opening the inner rotating camera carrier.

The ROLL slip ring is an internal service component, not a pressure seal or structural bearing.

The inner ROLL carrier is an ordinary integrated spindle/bearing assembly. It is not a cartridge/cassette module.

## 13. Controlled references

- `REVB_WB12_BALANCED_CVBS_VIDEO.md`
- `REVB_WB13A_CAMERA_SLIP_RING_CORRECTION.md`
- `REVB_WB14_CAMERA_AND_LIGHTING.md`
- `../mechanical/REV_BH_CAMERA_HEAD_INTERNAL_LAYOUT.md`
- `../mechanical/REV_BK_CAMERA_MOTOR_SELECTION.md`
- `../bom/REV_BI_CAMERA_HEAD_COMPONENT_SELECTION.md`

## Change log

### 2026-09-11 — Rev.B / WB12
- moved 75/100-ohm balun to fixed crawler side;
- retained balanced main tether video.

### 2026-09-11 — Rev.B / WB14 correction
- recognized that active LED ring and camera-axis motors are fixed-side relative to ROLL;
- removed LED/motor current and UART from the ROLL slip ring;
- reduced used ROLL circuits to camera 12 V/GND + raw CVBS signal/return;
- corrected camera slip-ring candidate from geometrically incompatible Ø22 M220 to Ø12.5 M125-06;
- moved optional local controller to fixed side;
- preserved six physical rings with two insulated spares;
- explicitly rejected old cartridge/cassette interpretation.
