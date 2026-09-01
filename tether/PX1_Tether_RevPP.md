# PX-1 TETHER — Rev.PP

Date: 2026-09-01
Status: ACTIVE TETHER ARCHITECTURE

## Mission
Use one lightweight, reinforced, field-repairable six-core copper inspection cable in the same system class as Mini-Cam Proteus. Preserve the mechanical/electrical reason for the high-voltage tether while using serviceable modern electronics at each end.

## Physical cable requirements
- exactly six copper conductors in one overall inspection cable;
- integrated aramid/Kevlar-class tensile reinforcement;
- abrasion-, water- and mud-resistant jacket;
- flexible enough for the manual reel;
- field strip and retermination possible;
- tensile load is terminated structurally before the electrical contacts;
- no coaxial core;
- no optical fibre;
- no Ethernet patch cable or bundle of independent ordinary twisted pairs substituted for the inspection cable.

Target physical class remains approximately 6.5-7 mm OD and <=60 g/m where achievable, with the Proteus cable used as the reference rather than a mandatory copied construction.

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

## Power rationale
Reference Proteus operation demonstrates the useful principle: transport roughly 100 W-class crawler power at high DC voltage so line current remains around the 1 A class rather than several amperes at 24 V.

PX-1 therefore does not plan to deliver the full crawler load through a 24/48 V line at 100-150 m.

The exact source setpoint inside the 100-120 VDC design class remains dependent on the selected commercial CCU converter, crawler converter and actual cable resistance. All insulation, connectors, slip-ring circuits and protection are selected for the maximum released line voltage plus appropriate transient margin.

## Initial length and scale-up
First complete system: 40 m.

Longer target: 100-150 m.

The same signal allocation and protection philosophy must survive the scale-up. A longer cable does not justify switching to coax, fibre or Ethernet patch cable.

## Reel/slip-ring requirement
Slip ring must carry:
- the two HV power conductors with sufficient voltage/current rating;
- RS-485 A/B with acceptable contact noise;
- balanced video +/− with acceptable noise/bandwidth.

A multi-circuit ring may parallel contacts for HV+/return, provided the manufacturer permits parallel use and current sharing is validated. Spare circuits are desirable.

The reel measuring encoder is surface-local and does not consume tether cores.

## Crawler tail termination
Required sequence:

`outer jacket bend support -> aramid/Kevlar structural clamp -> relaxed copper-core service loop -> sealed electrical connector/bulkhead`.

No copper conductor or connector contact is used as a towing or recovery member.

The termination must be repairable after cutting damaged cable back by a practical service length.

## Signal rules
### RS-485
- half duplex;
- controlled termination/bias;
- CRC/sequence;
- watchdog;
- test under motor reversal and lighting PWM.

### Balanced CVBS
- transmitter at camera/crawler side;
- receiver in CCU;
- test through camera rotating interface, reel slip ring and full tether;
- OSD is added at the CCU side after reception.

No separate signal cable is allowed to bypass the six-core tether in normal operation.

## Qualification sequence
Before long-cable release:
1. verify insulation and conductor continuity of the selected 40 m cable;
2. verify structural tail pull load separately from electrical connector;
3. verify RS-485 at 40 m with traction/lighting noise present;
4. verify balanced CVBS image quality at 40 m through the actual slip ring;
5. verify HV conductor temperature/drop with a protected dummy load;
6. verify E-STOP removes CCU-side HV;
7. verify line discharge after shutdown;
8. verify crawler converter startup/inrush through the 40 m cable;
9. repeat with 100-150 m equivalent only after 40 m passes.

## Release constraint
This document freezes the architecture and core functions, not a cable vendor or exact conductor gauge. The selected cable must be qualified as a complete six-core inspection cable rather than inferred from nominal wire cross-section alone.
