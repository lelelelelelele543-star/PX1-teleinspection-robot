# A0/A1 traction driver — motor-class gate

Status: ACTIVE ELECTRICAL STUDY. Motor class is not allowed to change silently.

## Rule
The traction driver is selected **after** the A0 motor package is locked:
- brushed DC motor -> H-bridge class driver;
- 2250S024BX4 or other 3-phase BLDC -> BLDC controller with Hall inputs.

BTS7960 / Pololu G2 are brushed H-bridges. They cannot commutate the FAULHABER 2250S024BX4.

## BLDC candidate for the 2250 path
ADI/Trinamic `TMCM-1640`, quantity 2, remains the preferred ready-made study module.

Published characteristics relevant to PX1:
- one 3-phase BLDC axis per module;
- nominal 24 V, operating range 12...28.5 V;
- programmable motor current up to 5 A RMS, 7 A peak with proper cooling;
- +5 V digital/open-collector Hall sensor interface;
- RS485 + USB;
- about 42 × 42 × 15 mm class;
- current manufacturer status: recommended for new designs.

This is electrically compatible with the standard 2250S024BX4 Hall/phase interface class. It is **not yet a BUY item** until permitted-seller stock, exact module revision, connectors and thermal mounting are confirmed.

## Brushed fallback path
If A0 instead freezes a brushed 24 V motor package, retain the compact dual H-bridge architecture. The current Pololu G2 model is a packaging study; BTS7960 modules remain unsuitable for the dry body unless a new mounting volume is deliberately created because two common IBT-2/BTS7960 modules are too bulky for the current internal envelope.

Do not change the six-core tether because of motor type. Motor commutation wiring is local inside the crawler.

## Main six-core tether remains
1. crawler power +
2. crawler power return
3. RS485 A
4. RS485 B
5. CVBS signal
6. CVBS return

## Internal BLDC architecture when used
`tether RS485 -> isolated tether transceiver -> STM32 safety supervisor -> local RS485 -> LEFT motor controller + RIGHT motor controller`.

The STM32 remains responsible for:
- tether command watchdog;
- global traction enable;
- pressure and supply telemetry;
- lighting/head commands;
- fault aggregation;
- forcing zero traction on stale/corrupt commands.

## A0 limits for 2250 path
- supply: 24 V;
- begin below 1000 motor rpm;
- increase speed only after current/temperature check;
- do not use controller maximum current as the motor continuous-current setting;
- 2250S024BX4 rated current is about 0.85 A, so initial current limiting must be conservative;
- first mechanical tests do not need full crawler speed.

## Failsafe
- valid tether command age >250 ms -> zero left/right traction request;
- parser/CRC/version fault -> no new motion command accepted;
- local motor controller must not retain non-zero velocity indefinitely after supervisor reset/link loss;
- console E-stop removes crawler traction power.

## Procurement gate
Before promotion to BUY, record:
- actual seller/source;
- exact part revision;
- dimensions including connectors;
- thermal mounting requirement;
- Hall input electrical compatibility;
- command interface and startup state;
- quantity = 2.

A0 may use an external bench motor controller while the mechanical train is being proven. That does not release it for the final crawler.
