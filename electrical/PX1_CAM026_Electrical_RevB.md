# PX-1 Rev.B — CAM026-inspired camera electrical baseline

Date: 2026-09-11
Status: ACTIVE CAMERA ELECTRICAL BASELINE / WB13A+WB14+WB15+WB16 SYNCHRONIZED
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
Between crawler/lift cradle and complete removable camera-head assembly:
1. `+12V_HEAD`
2. `GND_HEAD`
3. `HEAD_UART_TX`
4. `HEAD_UART_RX`
5. `CVBS_SIGNAL`
6. `CVBS_RETURN`

Controlled by WB15/WB16.

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

## 3. Mechanical/electrical interpretation corrected in WB14/WB16

Active head mechanics are:
- static sealed outer shell relative to internal continuous ROLL;
- whole optical shell TILT handled outside the internal ROLL interface;
- LED annulus fixed to that shell;
- TILT/ROLL motors, drivers, sensors and lighting control fixed-side relative to ROLL slip ring;
- only camera sensor/module rotates continuously in ROLL.

Therefore camera lighting, axis motor current and local UART do **not** cross the internal ROLL slip ring.

WB16 further separates the removable-head connector from the optical TILT sweep:
- SP1312 belongs on the non-TILT rear support/yoke-base portion of the removable head assembly;
- the external lift harness moves with the manual parallelogram;
- the internal wiring/feedthrough that accommodates ±105 deg TILT is a separate detailed work block.

This prevents the ~49 mm straight SP1310 body from being falsely added to the tilting Ø52 optical-shell sweep.

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

This UART crosses the external removable-head interface but terminates on fixed-side head electronics; it does not cross continuous ROLL.

## 7. External removable-head connector and lift harness — WB15/WB16

Panel half retained:
- camera-head rear support/yoke-base: WEIPU `SP1312/P6-C`;
- male pins;
- six contacts;
- 5 A/contact;
- 125 V class;
- rear-nut panel mount;
- cutout Ø13 with 11.8 mm anti-rotation flat dimension.

Cable half corrected by WB16:
- crawler/lift harness: WEIPU `SP1310/S6II-N`;
- female sockets;
- six contacts;
- 5 A/contact;
- 125 V class;
- cable range 5...8 mm.

Reason for changing `S6I-N` -> `S6II-N`:
- selected LAPP harness is nominal Ø6.7 mm;
- I version ends at 6.5 mm;
- II version covers 5...8 mm.

Selected external flexible lift cable:
- LAPP `UNITRONIC FD CY 0027429`;
- 7 x 0.25 mm²;
- nominal OD 6.7 mm;
- tinned-copper overall braid;
- continuous-flex product;
- maximum conductor resistance 79 ohm/km;
- manufacturer dynamic minimum bend radius 50.3 mm;
- PX-1 design route minimum R55 mm;
- maximum prototype one-way harness length 0.50 m until final route is frozen.

Only six cores are used. Seventh blue core is insulated `NC_SPARE_HEAD`.

Intended colour/function map:
- WH +12V_HEAD;
- BN GND_HEAD;
- GN HEAD_UART_TX;
- YE HEAD_UART_RX;
- GY CVBS_SIGNAL;
- PK CVBS_RETURN;
- BU NC_SPARE_HEAD.

Numeric SP13 contact numbers remain HOLD until the purchased male/female pair is continuity-mapped from an explicitly defined view.

Shield never carries load current and never substitutes for CVBS_RETURN/GND_HEAD. Final shield bonding is an EMC-test item.

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

Inside/removable head:
`raw CVBS -> internal TILT-compatible wiring -> SP1312/P6-C`.

Manual-lift service harness:
`SP1312/P6-C -> SP1310/S6II-N -> LAPP 0027429 (GY/PK)`.

Crawler fixed side:
`raw CVBS -> short service pigtail -> Delta-Opti TR-1D*P2 -> balanced VIDEO+/VIDEO-`.

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
- internal TILT wiring;
- WEIPU SP13 removable-head connector;
- <=0.50 m LAPP 0027429 lift harness;
- Delta balun pair;
- 40 m tether;
- reel slip ring;
- 100/150 m equivalent;
- TILT/ROLL, traction PWM and LED PWM active.

Neither M125, SP13 nor LAPP 0027429 is assumed to be a controlled 75-ohm video component from DC specifications alone.

## 11. Failure behavior

- crawler-to-head UART timeout -> TILT/ROLL commands zero and light to safe state;
- invalid axis sensor -> affected axis stop;
- crawler command timeout -> traction and camera-axis commands stop;
- video failure does not disable hardware E-STOP;
- hardware CCU E-STOP removes crawler/tether power independently of head software.

## 12. Service rule

- camera head remains separately sealed;
- complete head assembly removable without opening crawler P0/P1/P2;
- external SP13 unplugged before mechanical latch release;
- connector carries no bending/impact load;
- external harness follows the manual lift and remains externally inspectable;
- internal M125 is non-structural and is not a pressure seal;
- inner ROLL carrier is an ordinary integrated spindle/bearing assembly, not a cartridge/cassette.

## 13. Controlled references

- `REVB_WB12_BALANCED_CVBS_VIDEO.md`
- `REVB_WB13_ROTARY_INTERFACES.md`
- `REVB_WB14_CAMERA_AND_LIGHTING.md`
- `REVB_WB16_CAMERA_HEAD_HARNESS.md`
- `../mechanical/REVB_WB15_CAMERA_QUICK_CONNECT.md`
- `../mechanical/REV_BH_CAMERA_HEAD_INTERNAL_LAYOUT.md`
- `../mechanical/REV_BE_CAMERA_LIFT_INTERFACE.md`
- `../bom/REVB_CAMERA_HEAD_BOM_WB15.md`

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
- selected WEIPU SP13 six-pin pair;
- retired four-contact LEMO 0K.304 placeholder;
- added connector pressure/video qualification gates.

### 2026-09-11 — WB16
- selected LAPP 0027429 for external manual-lift harness;
- corrected cable plug to SP1310/S6II-N for Ø6.7 mm cable;
- separated external lift harness from internal TILT wiring;
- placed external SP13 on non-TILT rear support/yoke-base portion of removable camera assembly;
- added R55 routing, <=0.50 m length and shield rules.
