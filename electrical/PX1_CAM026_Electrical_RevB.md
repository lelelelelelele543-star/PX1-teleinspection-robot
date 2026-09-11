# PX-1 Rev.B — CAM026-inspired camera electrical baseline

Date: 2026-09-11
Status: ACTIVE CAMERA ELECTRICAL BASELINE / WB13A+WB14+WB15 SYNCHRONIZED
Supersedes `PX1_CAM026_Electrical_RevPM.md` where video-balun location, rotating electronics or camera rotary pinout differs.

## 1. Source-derived architecture retained

MiniCam CAM026 source evidence shows:
- `COM-000-003 PAL DSP CAMERA MODULE` in the camera housing;
- `COM-001-800 SLIP RING 6 WAY` in the rotate connector assembly;
- camera-side connection PCB around the rotary interface;
- separate camera-axis mechanisms;
- separately sealed connector/bearing metalwork.

PX-1 keeps the serviceable rotary-interface principle but uses ready modern electronics and its own dimensions.

## 2. Two electrical interfaces are deliberately different

### External removable-head connector — six functions
Between crawler/lift cradle and complete removable camera head:
1. `+12V_HEAD`
2. `GND_HEAD`
3. `HEAD_UART_TX`
4. `HEAD_UART_RX`
5. `CVBS_SIGNAL`
6. `CVBS_RETURN`

Controlled by WB15.

### Internal continuous ROLL transfer — four used functions
Between fixed head electronics and continuously rotating RunCam carrier:
1. `+12V_CAM`
2. `GND_CAM`
3. `CVBS_SIGNAL`
4. `CVBS_RETURN`
5. spare ring
6. spare ring

Controlled by WB13A in `REVB_WB13_ROTARY_INTERFACES.md`.

This split is mandatory. The six-pin external head connector must not be confused with the four-function internal ROLL transfer.

## 3. Mechanical/electrical interpretation corrected in WB14

Active head mechanics are:
- static sealed outer shell relative to internal continuous ROLL;
- whole head TILT handled outside the internal ROLL interface;
- LED annulus fixed to static outer shell;
- TILT/ROLL motors, drivers, sensors and lighting control fixed-side relative to ROLL slip ring;
- only camera sensor/module rotates continuously.

Therefore camera lighting, axis motor current and local UART do **not** cross the internal ROLL slip ring.

## 4. Camera module baseline

Selected family:
- RunCam Phoenix 2 analog CVBS camera;
- 1/2 in CMOS;
- PAL/NTSC switchable;
- 5...36 V input;
- conservative 12 V current reservation 120 mA until sample measurement;
- about 19 x 19 x 19...20 mm;
- stock M12 2.1 mm lens only for first optical test.

Exact source/final lens are controlled by WB14.

## 5. Internal camera ROLL slip ring

Selected engineering candidate:
- SenRing `M125-06`;
- Ø12.5 x 13.5 mm;
- 6 circuits x 1.5 A;
- AWG30 silver-plated PTFE leads;
- gold-gold contacts;
- IP51 only, therefore completely inside sealed camera head.

Why:
- rotating load is only camera sensor power + raw CVBS;
- M125 fits through 6803 bearing ID17 with 2.25 mm nominal radial clearance;
- previous camera M220 OD22 proposal is geometrically incompatible with ID17.

M220 mixed power/signal candidate remains a reel-only selection.

## 6. Fixed-side head electronics

Fixed/non-continuous head side may use:
- RP2040-Zero-class ready controller;
- TILT/ROLL ready driver modules;
- position/home sensor interfaces;
- two P4115adj LED-current drivers;
- six fixed-shell LEDs;
- local filtering/protection.

Crawler MCU local camera UART remains:
- PC12 / UART5_TX;
- PD2 / UART5_RX.

This UART crosses the external head connector but terminates on fixed head electronics; it does not cross continuous ROLL.

## 7. External removable-head connector — WB15

Selected prototype pair:
- camera-head panel side: WEIPU `SP1312/P6-C`, male pins;
- crawler/lift harness side: WEIPU `SP1310/S6I-N`, female sockets.

Controlled data:
- 6 contacts;
- 5 A/contact;
- 125 V class;
- SP13 family IP68 when correctly assembled/mated;
- head panel cutout Ø13 with 11.8 mm anti-rotation flat dimension;
- panel connector OD about 19.5 mm;
- cable plug OD about 18.8 mm, length about 49 mm;
- plug version I cable range 4.0...6.5 mm OD.

Mechanical rules:
- connector does not carry head structural loads;
- rear Ø36 register/latch carries loads;
- local connector panel thickness target 3.0 mm;
- >=60 mm axial service/extraction envelope reserved;
- numeric contact numbering waits for physical sample/front-rear orientation verification.

Pressure rule:
- IP68 is not accepted as pressure-feedthrough proof by itself;
- connector installed in the real rear bulkhead must pass the camera-head +0.25 bar dry/submerged tests.

The old LEMO `0K.304` placeholder is retired because its controlled insert has only four LV contacts and cannot carry the current six-function external interface.

## 8. Lighting

Controlled by WB14:
- six XP-family emitters;
- six 8 mm-class commercial MCPCBs on PCD40;
- two independent 3-LED strings;
- two P4115adj modules;
- initial ~300 mA/string;
- fixed-shell heat path;
- no LED current/PWM across internal ROLL.

## 9. Video path

Rotating side:
`RunCam CVBS -> M125-06 -> raw CVBS`.

Removable-head interface:
`raw CVBS -> SP13 pins -> short local 75-ohm-class pigtail`.

Crawler/lift fixed side:
`raw CVBS -> Delta-Opti TR-1D*P2 -> balanced VIDEO+/VIDEO-`.

Main tether:
`VIDEO+/VIDEO- balanced pair`.

CCU:
`VIDEO+/VIDEO- -> second TR-1D*P2 -> 75-ohm CVBS -> OSD -> GF-AM071`.

No coaxial conductor exists in the main tether. Short local 75-ohm interconnect inside serviceable assemblies is allowed.

## 10. Video qualification

Required sequence:
- RunCam direct into 75 ohm;
- M125 static;
- M125 rotating;
- WEIPU SP13 removable-head connector;
- Delta balun pair;
- 40 m tether;
- reel slip ring;
- 100/150 m equivalent;
- TILT/ROLL, traction PWM and LED PWM active.

Neither M125 nor SP13 is assumed to be a controlled 75-ohm component from DC specifications alone.

## 11. Failure behavior

- crawler-to-head UART timeout -> TILT/ROLL commands zero and light to safe state;
- invalid axis sensor -> affected axis stop;
- crawler command timeout -> traction and camera-axis commands stop;
- video failure does not disable hardware E-STOP;
- hardware CCU E-STOP removes crawler/tether power independently of head software.

## 12. Service rule

- camera head remains separately sealed;
- head removable without opening crawler P0/P1/P2;
- external SP13 unplugged before mechanical latch release;
- connector carries no bending/impact load;
- internal M125 is non-structural and is not a pressure seal;
- inner ROLL carrier is an ordinary integrated spindle/bearing assembly, not a cartridge/cassette.

## 13. Controlled references

- `REVB_WB12_BALANCED_CVBS_VIDEO.md`
- `REVB_WB13_ROTARY_INTERFACES.md`
- `REVB_WB14_CAMERA_AND_LIGHTING.md`
- `../mechanical/REVB_WB15_CAMERA_QUICK_CONNECT.md`
- `../mechanical/REV_BH_CAMERA_HEAD_INTERNAL_LAYOUT.md`
- `../mechanical/REV_BE_CAMERA_LIFT_INTERFACE.md`
- `../bom/REVB_CAMERA_HEAD_BOM_WB14.md`

## Change log

### 2026-09-11 — WB12
- moved 75/100-ohm balun to fixed crawler side;
- retained balanced main-tether video.

### 2026-09-11 — WB13A/WB14
- removed LEDs/motors/UART from internal ROLL;
- reduced internal used rings to camera 12 V/GND + CVBS signal/return;
- corrected camera slip ring to M125-06;
- kept local controller fixed-side;
- removed cartridge/cassette interpretation.

### 2026-09-11 — WB15
- separated external six-function head disconnect from internal four-function ROLL transfer;
- selected exact WEIPU SP13 six-pin pair for prototype;
- retired four-contact LEMO 0K.304 placeholder;
- added connector pressure/video qualification gates and 60 mm service envelope.
