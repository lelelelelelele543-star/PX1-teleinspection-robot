# PX1 Rev.PL — common service modules / simplify spares

Status: ACTIVE SERVICEABILITY BASELINE.

## Rule
Where possible the console and crawler use the same replaceable module family. The objective is to carry a small spare set instead of unique MiniCam proprietary boards.

## Controller
Primary family: STM32 NUCLEO-F446RE.
Use one in the crawler and one in the console where packaging permits.
Firmware differs, hardware spare is common.

## RS-485
Selected prototype module family: galvanically isolated `TTL TO RS485 (C)` ready module.
Reference data:
- 3.3–5 V logic/power;
- isolated DC/DC and digital barrier on board;
- TVS/surge protection and resettable fuse;
- selectable/on-board 120R termination;
- 42.8 x 15.2 x 4.75 mm;
- half duplex RS-485;
- manufacturer documentation gives about 1200 m RS-485 distance under suitable cabling/conditions.

Use the same module at console and crawler.

## Joysticks
Production-quality candidate family: APEM 4000 Series, two-axis spring-centred potentiometer joystick.
Reasons:
- industrial metal mechanism;
- >5 million operations;
- IP65 above panel;
- simple analog interface directly to MCU ADC;
- no CAN/USB/proprietary electronics required.

Current generic closed-frame envelope used in packaging: approximately 60 x 60 x 53 mm. Exact configured article and panel cutout remain HOLD until supplier stock/price is frozen.

Low-cost bench prototype may use inexpensive two-axis analog joysticks only for firmware development; they are NOT the intended field-console part.

## Console common low-voltage module set
- NUCLEO-F446RE;
- TTL TO RS485 (C);
- 24->5 V ready buck;
- MAX7456-class OSD module;
- balanced video receiver;
- standard 24 V relay/socket and fuse holder;
- GF-AM071 7-inch monitor.

## Crawler common low-voltage module set
- NUCLEO-F446RE;
- TTL TO RS485 (C);
- same 24->5 V buck family where suitable;
- standard motor driver modules;
- pressure sensor;
- balanced video transmitter.

## Spare kit target
Field spare box should eventually need only:
1. 1x NUCLEO-F446RE pre-flashed or flashable;
2. 1x TTL TO RS485 (C);
3. 1x common 24->5 V buck;
4. 1x traction driver module;
5. 1x camera dual motor driver;
6. standard fuses/relay;
7. common seals/bearings used by the crawler.

This is deliberately the opposite of the original Proteus proprietary PCB stack: mechanics stay Proteus-like, electronics become modular and replaceable.
