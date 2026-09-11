# PX-1 TETHER — Rev.PP

Date: 2026-09-01
Last reviewed: 2026-09-11 / Rev.B WB06
Status: ACTIVE TETHER ARCHITECTURE

## Mission
Use one lightweight, reinforced, field-repairable six-core copper inspection cable in the same system class as Mini-Cam Proteus. Preserve the mechanical/electrical reason for the high-voltage tether while using serviceable modern electronics at each end.

## Physical cable requirements
- exactly six functional copper conductors in one overall inspection cable;
- integrated aramid/Kevlar-class tensile reinforcement;
- abrasion-, water- and mud-resistant jacket;
- flexible enough for the manual reel;
- field strip and retermination possible;
- tensile load is terminated structurally before the electrical contacts;
- no coaxial core;
- no optical fibre;
- no Ethernet patch cable or bundle of independent ordinary twisted pairs substituted for the inspection cable.

Internal twisting of the four signal conductors into two differential pairs is allowed and preferred. They remain part of the single six-core inspection tether and are not separate cables.

Preferred physical class remains approximately 7-8 mm OD and <=60 g/m where achievable, with <=8.5 mm an absolute prototype target for the replacement cable. The existing Proteus-class cable is used for the first 40 m demonstrator and must be measured rather than assumed.

## Active conductor allocation

| Core | Function | Electrical class |
|---|---|---|
| 1 | HV+ | 100-120 VDC system class |
| 2 | HV return | 100-120 VDC system class |
| 3 | RS485_A | differential data |
| 4 | RS485_B | differential data |
| 5 | VIDEO+ | balanced analog CVBS |
| 6 | VIDEO- | balanced analog CVBS |

This allocation supersedes the older 10BASE-T1L/service-pair experiment.

## Rev.B preferred replacement construction

The current long-run replacement target is:
- 2 x 22 AWG (~0.33 mm²) tinned fine-stranded copper power cores;
- 2 x 2 x 24 AWG (~0.205 mm²) controlled differential signal pairs;
- pair impedance around 100 ohm nominal;
- no coax and no fibre;
- no extra drain conductor requiring another connector or slip-ring path;
- aramid/Kevlar or equivalent strength member;
- low-friction abrasion/hydrolysis/oil-resistant polyether PUR outer jacket;
- minimum documented breaking load >=1.5 kN, >=3.0 kN preferred.

This geometry is not invented: current ROV/sewer tether manufacturers offer 2x22AWG + 2x2x24AWG families and allow Kevlar/jacket/shield customization. A European heavier reference, Novacavi 6XM524, confirms the same basic six-conductor hybrid architecture at 2x16AWG + 2x(2x24AWG), but its ~10.1 mm OD is larger than preferred for PX-1.

See `REVB_WB06_TETHER_POWER_SIGNAL_FREEZE.md` and `procurement/RFQ_PX1_6CORE_TETHER_RevB.md`.

## Power rationale
Reference Proteus operation demonstrates the useful principle: transport roughly 100 W-class crawler power at high DC voltage so line current remains around the 1 A class rather than several amperes at 24 V.

PX-1 therefore does not plan to deliver the full crawler load through a 24/48 V line at 100-150 m.

Rev.B WB06 now gives a preferred long-run source operating point of approximately 120 VDC within the existing 100-120 VDC class. With a 22 AWG power pair and a 111.1 W crawler-input screen, the 150 m / 60°C calculation gives approximately 99.2 V at the crawler and ~23.3 W cable loss before connector/slip-ring tolerance. Therefore the final crawler HV->24 V converter should tolerate at least about 90-125 VDC operating input with transient margin if 150 m operation is required.

The exact source setpoint and converter remain commercial-component gates. All insulation, connectors, slip-ring circuits and protection are selected for the maximum released line voltage plus appropriate transient margin.

## Initial length and scale-up
First complete system: 40 m using the existing professional six-core Proteus-class tether after measurement/qualification.

Longer target: 100-150 m using the controlled replacement construction above only after a 5-10 m supplier sample passes electrical, signal and tensile tests.

The same signal allocation and protection philosophy must survive the scale-up. A longer cable does not justify switching to coax, fibre or Ethernet patch cable.

## Connector-contact consequence
For the preferred 22/24 AWG replacement construction, one common gold-plated H-D 1.6 contact size serves all six copper cores:
- male crawler contact: LAPP `13162500`, 0.14...0.37 mm²;
- female cable contact: LAPP `13163500`, 0.14...0.37 mm²;
- stripping length: 8 mm.

This simplifies field retermination and spare inventory.

These exact contact articles are **not** automatically applied to the existing Proteus cable until its conductor size is measured.

## Reel/slip-ring requirement
Slip ring must carry:
- the two HV power conductors with sufficient voltage/current rating;
- RS-485 A/B with acceptable contact noise;
- balanced video +/− with acceptable noise/bandwidth.

A multi-circuit ring may parallel contacts for HV+/return only if the manufacturer permits parallel use and current sharing is validated. Spare circuits are desirable.

No shield/drain conductor may silently consume a seventh functional slip-ring path under the six-core baseline.

The reel measuring encoder is surface-local and does not consume tether cores.

## Crawler tail termination
Required sequence:

`outer jacket bend support -> aramid/Kevlar structural clamp -> relaxed copper-core service loop -> sealed electrical connector/bulkhead`.

No copper conductor or connector contact is used as a towing or recovery member.

The termination must be repairable after cutting damaged cable back by a practical service length.

Current first-prototype mechanical limits:
- normal tether tension target <100 N;
- investigate sustained >150 N;
- recovery limit 500 N until complete tether/tail qualification;
- tail hardware proof target 1.0 kN.

## Signal rules
### RS-485
- one dedicated internal 24 AWG pair in the replacement cable;
- half duplex;
- isolated transceiver architecture preferred because there is no seventh reference/core;
- controlled termination/bias after measuring pair impedance;
- CRC/sequence;
- watchdog;
- test under motor reversal and lighting PWM.

### Balanced CVBS
- one dedicated internal 24 AWG pair;
- balanced transmitter/receiver designed for ~100 ohm pair;
- test through camera rotating interface, reel slip ring and full tether;
- OSD is added at the CCU side after reception.

No separate signal cable is allowed to bypass the six-core tether in normal operation.

## Qualification sequence
Before long-cable release:
1. verify insulation and conductor continuity of the selected 40 m cable;
2. measure actual 40 m power-loop resistance and mass/OD;
3. verify structural tail pull load separately from electrical connector;
4. verify RS-485 at 40 m with traction/lighting noise present;
5. verify balanced CVBS image quality at 40 m through the actual slip ring;
6. verify HV conductor temperature/drop with a protected dummy load;
7. verify E-STOP removes CCU-side HV;
8. verify line discharge after shutdown;
9. verify crawler converter startup/inrush through the 40 m cable;
10. obtain and qualify a replacement-cable sample;
11. repeat the full chain at 100 m and then 150 m only after shorter tests pass.

## Release constraint
The architecture and preferred 22/24 AWG replacement construction are now frozen at Rev.B screening level. The exact cable vendor/article is not production-released until a supplier-controlled drawing and physical sample confirm OD, mass, conductor resistance, pair impedance/capacitance, jacket, tensile strength and field retermination.
