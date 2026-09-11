# PX-1 Rev.B — WB12 balanced CVBS video path

Date: 2026-09-11
Status: ARCHITECTURE FROZEN / COMPLETE-LINK QUALIFICATION HOLD

## 1. Scope and frozen constraints

WB12 closes the main video architecture without changing the six-functional-core tether.

Frozen rules:
- main tether has exactly `VIDEO+` and `VIDEO-` for video;
- no coaxial conductor is added to the main tether;
- no fibre is added;
- camera remains a separately sealed assembly;
- CCU monitor/OSD remain ordinary 75-ohm CVBS equipment;
- prototype uses replaceable commercial modules, no custom video PCB.

A short local 75-ohm coax/pigtail **inside the sealed camera/crawler/CCU assembly** is allowed where required by a commercial balun. The project prohibition is specifically against coax in the main tether.

## 2. Proteus/CAM026 source comparison

Uploaded CAM026 source confirms:
- camera housing contains `COM-000-003 PAL DSP CAMERA MODULE`;
- rotate connector assembly contains `COM-001-800 SLIP RING 6 WAY`;
- the slip-ring assembly also contains a camera-side connection PCB;
- no separate coaxial tether conductor is introduced by the CAM026 mechanical assembly.

This proves the original camera architecture had to move analog camera functions through a compact 6-way rotary interface. The source assembly sheets do **not** give a controlled electrical pinout or characteristic-impedance rating for COM-001-800, so PX-1 does not invent one.

PX-1 keeps the six-function rotary-interface concept, but the modern slip ring and video link are qualified independently.

## 3. Main tether video electrical standard

Target source:
- analog composite video, PAL/NTSC CVBS;
- nominal source/load system: 1 Vpp into 75 ohm;
- fixed-focus camera preferred for the first prototype;
- no digital encoder required in crawler.

Balanced transport:
- one dedicated internal twisted pair in the six-core tether;
- nominal pair impedance target: 100 ohm;
- conductor target: 24 AWG;
- pin functions remain `VIDEO+ / VIDEO-`;
- no DC current is intentionally carried on the video pair;
- video pair is not bonded to logic ground or tether HV return.

CCU side returns to ordinary 75-ohm CVBS before OSD/monitor.

## 4. Selected Rev.B passive balun pair

### Delta-Opti `TR-1D*P2`

Selected as the **first prototype video-balun pair** because it has both controlled technical data and a current marketplace purchasing route.

Manufacturer/model:
- Delta-Opti;
- `TR-1D*P2`;
- EAN 5902887011313;
- supplied as a two-piece pair.

Controlled data:
- passive, 1 channel;
- supports CVBS PAL/NTSC;
- 75-ohm side: 1 Vpp;
- balanced side: 100 ohm;
- claimed CVBS range on Cat5e: up to 400 m;
- attenuation for the complete pair:
  - 4.43 MHz: 0.43 dB;
  - 11 MHz: 0.65 dB;
  - 21 MHz: 0.93 dB;
  - 38 MHz: 1.54 dB;
  - 42 MHz: 1.90 dB;
  - 67.5 MHz: 2.10 dB;
- CMRR: 60 dB @ 5 MHz;
- BNC plug on ~90 mm local lead;
- balanced connection: two cable terminals;
- body: approximately 16 x 15 x 43 mm;
- mass: ~18 g each;
- operating temperature: -10...+55 C.

Manufacturer manual:
`https://s3-eu-west-1.amazonaws.com/gasiashopstore/uploads/0a2a57cf-6fea-4168-abc5-f51ecbfcfe5f/Delta-Opti%20Instruction-TR-1D_P2.pdf`

Marketplace route checked in Rev.B:
- Allegro currently lists new `TR-1D*P2` pairs.

### Why passive first

A passive pair:
- adds no switching converter or amplifier inside the camera/crawler;
- does not add a new local power branch;
- provides the required 75/100-ohm transformation;
- is field replaceable;
- is inexpensive enough to qualify several samples;
- keeps active gain/AGC out of the first 40 m demonstrator.

Its 400 m Cat5e claim is **not** treated as proof that PX-1 will work through two slip rings and a custom inspection tether. Only the full-link test can release 150 m.

## 5. Balun placement decision

The complete Delta body can geometrically fit a Ø60-class camera cavity only when inclined, but the 90 mm BNC lead, BNC mating connector, camera MCU, PAN driver, LED electronics and service access make a rotating-side installation unnecessarily difficult.

Therefore Rev.B preferred placement is:

`camera CVBS -> short dedicated CVBS_SIGNAL/CVBS_RETURN through camera slip ring -> fixed-side Delta balun -> VIDEO+/VIDEO- main tether`.

At the CCU:

`VIDEO+/VIDEO- -> second Delta balun -> 75-ohm CVBS -> OSD -> GF-AM071 monitor`.

This is a **camera-local revision only**. It does not alter the main tether pinout or the crawler power/control architecture.

Reason for the revision:
- removes bulky commercial BNC hardware from the continuously rotating sealed camera volume;
- reduces rotating mass and wire bend stress;
- makes the balun a normal service item accessible from the crawler electronics side;
- keeps the main 100/150 m run balanced;
- preserves the original CAM026-style six-way rotary-interface principle.

### Camera slip-ring six functions after WB12

1. +12 V rotating-camera supply
2. power/control GND
3. local UART TX
4. local UART RX
5. CVBS_SIGNAL
6. CVBS_RETURN

`CVBS_RETURN` is dedicated to the video source/75-ohm path and is not used as PAN-motor return.

The fixed-side balun converts these last two conductors to `VIDEO+ / VIDEO-` immediately after the rotary interface.

## 6. Important service/wiring rule

The commercial Delta unit has a BNC plug. PX-1 must not bury a loose BNC-to-BNC joint where it cannot be serviced.

Fixed crawler-side installation shall provide:
- a short 75-ohm BNC female pigtail/jack from the camera rotary connector to the Delta balun;
- positive cable support so the BNC connector does not carry vibration load;
- insulated clip/bracket for the 16x15x43 mm balun body;
- tool-accessible two-wire balanced terminals;
- polarity marking for `VIDEO+ / VIDEO-` because passive video baluns are polarity sensitive.

Do not cut open or depopulate the commercial balun for Rev.B. If a later production design requires a bare transformer, that is a Rev.C component redesign and must be separately qualified.

## 7. CCU installation

The second `TR-1D*P2` is mounted inside the control unit, not on the reel.

Chain:
`reel VIDEO pair -> CCU Delta balun -> short 75-ohm coax -> OSD -> GF-AM071 AV input`.

Rules:
- balun body clipped to the service panel;
- BNC side uses a short 75-ohm cable only;
- OSD input/output remain 75-ohm terminated as intended by the selected module;
- no video transformer is placed in the reel unless later measurement proves one is required.

## 8. Active receiver fallback — not baseline

If passive/passive video fails the 100/150 m full-system test despite a compliant 100-ohm pair, the controlled fallback is an **active receiver in the CCU only**.

Reference:
- MuxLab `500124 LongReach II Active CCTV Receiver Balun`;
- balanced input 100 ohm;
- 75-ohm 1.1 Vpp output;
- 20 Hz...8 MHz video bandwidth;
- AGC;
- automatic polarity correction;
- ground-loop isolation;
- specified for much longer Cat5e/6 runs when paired with a passive camera-end balun.

This fallback is allowed because it changes only the surface receiver; it does not change the robot, tether or slip rings.

Do not promote it unless physical measurements show the passive pair lacks amplitude/equalization margin.

## 9. Why catalog cable distance is not the release criterion

The Delta specification is measured on Cat5e. PX-1 uses a custom moving inspection tether and two rotary interfaces.

Potential degradation sources:
- actual 24 AWG pair impedance tolerance;
- pair capacitance and attenuation;
- connector transitions;
- camera slip-ring contact resistance/noise;
- reel slip-ring contact resistance/noise;
- untwisted lead length through the slip rings;
- coupling from 120 V tether power;
- BTS7960 PWM;
- PAN/ROLL motor commutation;
- LED PWM/current driver;
- reel rotation/contact modulation.

Therefore the full chain, not an isolated 150 m cable sample, is the qualification article.

## 10. Required oscilloscope/video tests

Test order is frozen:

1. camera directly into 75-ohm monitor/test load;
2. Delta pair on a short known 100-ohm pair;
3. add camera rotary connector/slip ring;
4. add 40 m actual tether;
5. add reel slip ring;
6. repeat with 100 m equivalent/actual cable;
7. repeat with 150 m equivalent/actual cable;
8. repeat while rotating camera continuously;
9. repeat while rotating reel;
10. repeat while traction PWM, PAN/ROLL, and LED PWM are active.

At each stage record:
- CVBS amplitude into 75 ohm;
- sync-tip stability;
- black/white level stability;
- PAL/NTSC burst/chroma integrity;
- visible hum bars/noise;
- intermittent dropouts during slip-ring rotation;
- polarity;
- before/after connector movement.

Final release thresholds are derived from the selected camera/monitor CVBS specification and oscilloscope measurements; do not accept a link only because an image is barely visible.

## 11. Camera output acceptance gate

Before integrating the balun, the exact purchased camera module must be measured.

Required:
- actual mode confirmed as CVBS PAL or NTSC;
- output approximately 1 Vpp into a real 75-ohm load;
- separate VIDEO and VIDEO_RETURN identified;
- camera supply/current measured;
- fixed-focus field of view checked in the physical head.

The old MiniCam `COM-000-003 PAL DSP CAMERA MODULE` is source evidence, not a PX-1 procurement part.

## 12. Video pair termination and grounding

- no 100/120-ohm resistor is placed directly across `VIDEO+/VIDEO-` in addition to the selected balun unless required by that balun's documented design;
- the passive balun provides the impedance interface;
- no connection from `VIDEO+` or `VIDEO-` to chassis, HV return or logic ground;
- local 75-ohm video return exists only on the unbalanced side of the balun;
- camera slip-ring `CVBS_RETURN` is dedicated and does not carry motor current.

## 13. Packaging screen

Delta body only:
- 43 x 16 x 15 mm.

A simple rectangular-envelope check against the existing Ø60 x 40 mm reference cavity shows the body itself can fit if tilted roughly >=48 degrees relative to the cavity axis. At ~50 degrees the calculated axial projection is ~39.1 mm and the maximum radial-corner radius is ~22.7 mm, inside a 30 mm cavity radius.

This result is **not used as a release justification**, because the BNC lead/connector and other rotating electronics still make the rotating-side implementation poor for service. It simply confirms the selected part is not fundamentally too large for prototype bench/mock-up work.

## 14. Procurement

Prototype quantity:
- 2 complete `TR-1D*P2` pairs recommended.

Use:
- one working pair;
- one spare/test pair for destructive/open-bench comparison and fault isolation.

Source priority:
1. marketplace listing of exact Delta-Opti article;
2. Polish/Czech electronics/security distributor carrying exact article;
3. do not substitute an unbranded balun without measured comparison.

## 15. Errors/corrections recorded

1. Earlier Rev.PM implicitly placed the balanced-video transmitter on the rotating side without a frozen real commercial module. WB12 corrects this by moving the first commercial balun to the fixed crawler side after the camera slip ring.
2. A commercial statement such as `400 m Cat5e` is not proof of PX-1 150 m performance through two slip rings.
3. The main-tether no-coax rule does not prohibit a short local 75-ohm pigtail inside a sealed/serviceable assembly.
4. Video return must not share PAN-motor current merely to save one rotary circuit.
5. A generic slip ring's `<0.01 ohm electrical noise` statement is not equivalent to a controlled 100-ohm video channel specification.

## 16. WB12 closure gates

WB12 is production-released only after:
1. exact CVBS camera is purchased and measured into 75 ohm;
2. exact Delta pair is purchased and checked for polarity/isolation/continuity;
3. camera slip ring is selected and qualified with unbalanced CVBS;
4. 40 m complete-link test passes while all motors/LEDs switch;
5. reel slip ring is selected and qualified;
6. 100 m and 150 m complete-link tests pass;
7. camera and reel are rotated during video tests;
8. thermal/noise test is repeated after one endurance cycle;
9. final harness and connector pin labels are frozen;
10. only then is passive/passive retained for Rev.C; otherwise use the controlled CCU active-receiver fallback.

## Change log

### 2026-09-11 — WB12
- retained balanced `VIDEO+/VIDEO-` over the main tether;
- selected Delta-Opti TR-1D*P2 as the first real purchasable passive pair;
- corrected the rotating-side balun assumption from Rev.PM;
- moved the balun to the fixed crawler side to improve packaging and serviceability;
- reserved dedicated CVBS signal/return across the camera slip ring;
- retained MuxLab 500124 only as a CCU-side fallback;
- defined full-link video qualification through both rotary interfaces.
