# PX-1 Rev.B — WB15 removable camera-head electrical connector

Date: 2026-09-11
Status: PROTOTYPE CONNECTOR PAIR SELECTED / PRESSURE+VIDEO QUALIFICATION HOLD

## 1. Scope

WB15 controls the electrical quick disconnect between:
- removable sealed camera head; and
- fixed lift/cradle harness.

It does not control the internal continuous ROLL slip ring. Internal ROLL is WB13A.

The external camera-head connector must carry six functions:
1. +12V_HEAD
2. GND_HEAD
3. HEAD_UART_TX
4. HEAD_UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

The connector is not allowed to carry camera-head mechanical bending/impact loads.

## 2. Previous baseline error

`REV_BE_CAMERA_LIFT_INTERFACE.md` retained a LEMO `0K.304` family placeholder.

Current LEMO controlled data for `0K.304` shows **4 low-voltage contacts**. The active Rev.B removable-head interface needs six conductors.

Therefore `0K.304` is electrically insufficient for the current architecture and is superseded as the camera-head connector baseline.

A larger/different LEMO insert could be engineered later, but changing to another expensive proprietary insert is not justified for the first PX-1 prototype when a compact current six-pin industrial connector is available.

## 3. Selected prototype pair — WEIPU SP13

### Head panel receptacle
Manufacturer: WEIPU
Article: `SP1312/P6-C`
Type:
- rear-nut panel mount;
- male pins;
- 6 contacts;
- solder termination;
- threaded coupling;
- protective cap included (`-C`).

Electrical:
- 5 A/contact;
- 125 VAC class;
- contact resistance class 5 mOhm for six-contact insert;
- conductor size up to approximately 0.75...0.785 mm2 / AWG18 class.

Environmental:
- SP13 family IP68 when correctly assembled/mated;
- operating temperature class -40...+85 C;
- nylon/PC shell, gold-plated brass contacts.

Manufacturer mechanical drawing:
- outer front diameter: approx. 19.5 mm;
- mounting thread: M13 x 1;
- panel cutout: Ø13 mm with anti-rotation flat dimension 11.8 mm;
- maximum panel thickness: 3.5 mm;
- front projection drawing dimension: 9.5 mm;
- total panel-receptacle depth drawing dimension: 19.2 mm.

### Crawler/lift cable plug
Manufacturer: WEIPU
Article: `SP1310/S6I-N`
Type:
- cable plug;
- female sockets;
- 6 contacts;
- solder termination;
- threaded coupling;
- no loose protective cap (`-N`).

Electrical:
- 5 A/contact;
- 125 VAC class.

Mechanical:
- outer diameter: approx. 18.8 mm;
- overall length: approx. 49 mm;
- cable version I range: 4.0...6.5 mm OD.

This exact plug is listed by current distributors as the mate for `SP1312/P6-C`.

## 4. Why the gender/orientation is frozen this way

Use:
- camera head = panel **male pins** `SP1312/P6-C`;
- live crawler/lift harness = cable **female sockets** `SP1310/S6I-N`.

Reason:
- the powered harness does not expose protruding live male pins when the camera head is removed;
- the panel connector is mechanically protected by the rear camera register/spigot;
- replacement head remains a self-contained part with a standardized panel article.

## 5. Rear bulkhead geometry

Current camera rear mechanical register/spigot target: Ø36 mm class.

Selected connector fit:
- SP1312 front OD = 19.5 mm;
- remaining nominal radial guard inside Ø36 spigot = `(36 - 19.5)/2 = 8.25 mm`;
- panel cutout Ø13 leaves nominal radial material to Ø36 = `(36 - 13)/2 = 11.5 mm`;
- selected rear bulkhead local thickness = 3.0 mm;
- manufacturer max panel thickness = 3.5 mm;
- thickness installation margin = 0.5 mm.

Rev.B rear bulkhead therefore keeps:
- Ø36 mechanical register;
- centered SP13 cutout;
- 3.0 mm connector mounting land;
- anti-rotation flats machined to the manufacturer cutout geometry;
- no connector body used as the mechanical head register.

## 6. Connector mounting

Panel side:
1. machine Ø13 / 11.8-flat cutout from controlled drawing;
2. deburr without rounding away anti-rotation flats;
3. install SP1312 from wet/external side;
4. retain manufacturer sealing element/O-ring in its intended location;
5. install rear nut from dry side;
6. starting rear-nut torque follows current WEIPU SP13 rear-nut instruction: 0.5...0.6 N·m;
7. no generic anaerobic threadlocker/sealant is applied to the plastic housing.

WEIPU specifically cautions against arbitrary sealants on its plastic housings. If any auxiliary sealant is ever introduced, it must be one the manufacturer identifies as material-compatible and it remains secondary to the mechanical seal.

Cable plug:
- use a finished cable OD inside 4.0...6.5 mm;
- backshell/main-body tightening: 0.5...0.6 N·m starting value from current WEIPU instruction;
- compression nut: 0.5...0.6 N·m starting value;
- solder joints individually heat-shrunk;
- cable jacket must be captured by the connector strain-relief system, not by conductor solder joints.

## 7. Harness allocation

Logical pin functions are frozen, but numeric contact numbers are not released until the first physical pair is checked against the moulded contact numbering and front/rear-view convention.

Required functions:
- `PWR_HEAD_12V`
- `PWR_HEAD_GND`
- `UART_HEAD_TX`
- `UART_HEAD_RX`
- `CVBS_SIGNAL`
- `CVBS_RETURN`

Harness rule:
- CVBS signal/return remain an adjacent local pair where the physical insert numbering permits;
- UART TX/RX remain paired together;
- power is kept away from the video pair as far as the six-contact geometry permits;
- no connector contact is shared between video return and motor/LED return;
- exact contact-number table is released only after sample inspection.

## 8. Important pressure-boundary rule

IP68 is an ingress rating, not automatic proof that the connector is a qualified pressure-vessel feedthrough for PX-1.

Normal camera-head pressure target remains the project class:
- +0.20...+0.30 bar gauge;
- +0.25 bar typical.

Therefore the SP1312 panel interface is **not production-released as a pressure boundary from the IP68 label alone**.

Prototype qualification must include the connector installed exactly as used in the camera rear bulkhead.

Acceptance sequence:
1. dry pressure-decay test at ~+0.25 bar gauge;
2. 30 min temperature-aware decay recording;
3. submerged static bubble/leak test while mated;
4. disconnect/reconnect cycle and repeat;
5. repeat after vibration/tilt/roll endurance.

If the connector insert or panel seal cannot hold the camera-head pressure target reliably, WB15 reopens and the electrical connector is moved outside a separately proven bulkhead/feedthrough boundary rather than masking the leak with sealant.

## 9. Structural pressure screen

The 3.0 mm Ø36 rear bulkhead with a Ø13 cutout sees only small direct pneumatic force at the normal camera-head pressure.

Annular area around a Ø13 opening inside Ø36 is about 885 mm2.

Equivalent pressure force:
- at +0.30 bar: ~26.6 N;
- at +0.50 bar: ~44.3 N;
- at +1.0 bar: ~88.5 N.

These force values do not constitute a complete plate-stress proof; they only show that connector pressure loading is not the dominant rear-bulkhead structural load. Mechanical latch/yoke impact loads remain separate design cases.

## 10. Mechanical quick-removal sequence

Target field sequence:
1. de-energize camera-head 12 V branch;
2. unscrew and withdraw SP1310 cable plug axially;
3. park/cap the connector as required;
4. release one retained mechanical latch/pin;
5. withdraw complete camera head from its Ø36 register.

The threaded SP13 electrical connector is tool-less but is not a one-motion bayonet. This is accepted for Rev.B because:
- IP68 sealing is prioritized over shaving seconds from service time;
- the head is not normally removed during a live inspection;
- mechanical lift operation remains one-hand and independent of this service connector.

If later field trials show service time is unacceptable, a bayonet SY13 or production push-pull six-contact part may be compared in Rev.C without changing the six-function pinout.

## 11. Service-clearance envelope

SP1310 cable plug is about 49 mm long.

Rev.B CAD must reserve:
- >=55 mm axial solid keep-out behind the panel for the mated plug/body envelope;
- >=60 mm practical axial extraction/service envelope before a fixed obstruction;
- cable bend radius outside the connector backshell according to the selected 6-core head harness.

A 90-degree cable exit is not introduced unless the real lift/yoke model proves the straight plug cannot be serviced.

## 12. Video qualification

SP13 is not a controlled-impedance video connector.

Raw CVBS crosses only a very short six-pin interface, so it is an engineering candidate, not an assumed video-perfect device.

WB12 qualification must include:
- direct RunCam baseline;
- M125 ROLL ring;
- SP13 removable-head connector;
- Delta-Opti balun;
- 40 m tether;
- reel rotary interface;
- 100/150 m equivalent;
- motor/LED PWM interference tests.

If SP13 causes visible reflection/noise/sync problems, do not hide the failure with software filtering. Re-open connector/video topology.

## 13. Procurement status

Current distributor checks show both exact articles as active/orderable:
- `SP1312/P6-C` — current stock exists at multiple distributors;
- `SP1310/S6I-N` — current stock exists at multiple distributors.

TME/DigiKey-class distributors currently list the cable plug as 6-position, 5 A, 125 V, IP68, 4...6.5 mm cable and the panel mate as 6-position, 5 A, 125 V.

Before machining production parts, buy at least:
- 2 complete working pairs;
- 1 spare panel connector;
- 1 spare cable plug;
- protective caps as required for disconnected field service.

## 14. WB15 release gates

1. buy exact SP1312/P6-C + SP1310/S6I-N pair;
2. record moulded pin numbers/front-rear orientation;
3. freeze numeric contact pinout;
4. measure actual OD/length/panel-seal compression;
5. verify rear nut installation on 3.0 mm 6082-T6 coupon;
6. perform +0.25 bar dry leak test;
7. perform submerged mated leak test;
8. mate/unmate at least 50 prototype cycles and repeat leak test;
9. run raw-CVBS through connector during flex/vibration;
10. fit 55/60 mm plug/service envelopes into full yoke/lift CAD;
11. run DN150 LOW and DN150_SAFE solid sweep including plug/harness;
12. only then release the rear bulkhead machining drawing.

## Change log

### 2026-09-11 — WB15
- found old LEMO 0K.304 placeholder has only four contacts and cannot carry current six-function head interface;
- selected WEIPU SP1312/P6-C + SP1310/S6I-N prototype pair;
- fixed safe gender orientation with female sockets on powered harness;
- froze Ø13/11.8-flat cutout and 3.0 mm local panel thickness candidate;
- added manufacturer torque/strain-relief rules;
- explicitly refused to treat IP68 alone as pressure qualification;
- added 60 mm rear service envelope and DN150 re-check gate;
- preserved six-function electrical architecture and independent mechanical latch.
