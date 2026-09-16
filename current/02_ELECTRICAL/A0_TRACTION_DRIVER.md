# A0/A1 traction driver — BLDC source-match path

Status: ACTIVE ELECTRICAL STUDY. Do not delete the existing brushed-driver files until A0 motor tests pass.

## Why the traction electronics changes
The selected A0 source-match motor 2250S024BX4 is a three-phase BLDC motor with digital Hall sensors. BTS7960 / Pololu G2 brushed H-bridges cannot commutate it. Therefore they cannot remain the traction drivers if the source-match motor package passes A0.

## Preferred ready-made driver candidate
ADI/Trinamic `TMCM-1640`, quantity 2.

Relevant published data:
- one BLDC axis per board;
- 12...28.5 V supply, nominal 24 V;
- programmable motor current up to 5 A RMS, 7 A peak with appropriate cooling;
- Hall sensor input;
- RS485 + USB;
- 42 x 42 x 15 mm;
- 100 W continuous class;
- current manufacturer status: recommended for new designs.

Why it is preferred over a generic six-step board for this prototype:
- it accepts the motor's digital Hall feedback directly;
- current and velocity can be limited in firmware;
- RS485 control removes PWM/DIR wiring across the crawler;
- two 42 x 42 mm boards can be placed sequentially in the long dry body rather than side-by-side;
- it is a complete module, so PX1 still follows the no-custom-main-PCB rule.

## Bus architecture
Keep the main six-core tether unchanged:
1. crawler power +
2. crawler power return
3. RS485 A
4. RS485 B
5. CVBS signal
6. CVBS return

Inside crawler:
`tether RS485 -> isolated tether transceiver -> STM32 -> internal RS485 -> TMCM-1640 LEFT + TMCM-1640 RIGHT`.

The internal motor bus is local wiring only and consumes no extra tether conductors. The STM32 remains the safety supervisor for command timeout, pressure, lighting/head functions and system telemetry.

## Initial limits for A0
- supply 24 V;
- motor speed target for first runs <=1000 rpm;
- increase in steps only after current/temperature check;
- normal A0 ceiling 3500 rpm;
- absolute configured gearhead ceiling <=4000 rpm;
- begin with conservative current limit, then increase only to the value required for the load test; do not use the controller's 5 A capability as the motor's continuous current rating.

The 2250S024BX4 published rated current is 0.85 A. Controller phase-current semantics must be verified during commissioning before a final current-limit value is frozen.

## Failsafe
The crawler STM32 must command zero speed if valid tether command age exceeds 250 ms. The motor drivers must also be configured so a local controller/reset condition cannot leave a nonzero velocity command latched indefinitely. Hardware E-stop at the console removes crawler power.

## Procurement gate
TMCM-1640 is technically suitable and documented in the Chip&Dip document library, but actual permitted-seller stock/price must be confirmed before the BOM changes from STUDY to BUY. A0 may use an external bench BLDC controller to prove the mechanics before the two final crawler modules are purchased.
