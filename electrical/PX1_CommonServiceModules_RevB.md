# PX-1 Rev.B — common service modules

Date: 2026-09-11
Status: ACTIVE REV.B SERVICEABILITY BASELINE
Supersedes `PX1_CommonServiceModules_RevPL.md` where low-voltage converter or RS-485 implementation differs.

## 1. Service philosophy

PX-1 deliberately avoids a proprietary Mini-Cam-style single electronics stack for the first prototype.

Field-replaceable ready modules are used wherever practical so a failed function can be exchanged without replacing the mechanical crawler or desoldering a custom PCB.

Mechanical architecture remains Proteus-inspired; electronics are modern and replaceable.

## 2. Controller family

Primary crawler controller:
- STM32 NUCLEO-F446RE.

Console may use the same family where packaging/function remains appropriate.

Benefits:
- common programming/debug equipment;
- common firmware toolchain;
- replaceable stocked board;
- no proprietary custom PCB required for the prototype.

Crawler NUCLEO power:
- regulated 5 V to E5V;
- never apply the 24 V crawler rail directly to E5V;
- follow ST UM1724 external-power/USB jumper and power-sequence rules.

## 3. Common isolated RS-485 module

Selected Rev.B module family:
- Waveshare `TTL TO RS485 (C)`;
- SKU `27479`;
- 3.3...5 V TTL-side supply/logic class;
- isolated DC/DC on module;
- digital galvanic isolation;
- TVS/protection network;
- half-duplex RS-485;
- optional onboard 120 ohm termination;
- approximately 42.8 x 15.2 x 4.75 mm;
- ready module with no custom PCB.

Quantity:
- crawler: 1;
- CCU: 1;
- recommended field spare: 1.

Crawler MCU interface:
- PC10 / USART3_TX;
- PC11 / USART3_RX;
- no external DE GPIO because the selected ready module handles direction internally.

PA2/PA3 remain available for NUCLEO ST-LINK VCP debug.

Important release note:
- the main tether intentionally carries A/B only and has no seventh signal-common core;
- RS-485 common-mode margin over the complete 40/100/150 m link remains a qualification HOLD;
- never bond the isolated line-side reference to tether HV return merely to make a bench test pass.

## 4. 12 V converter service module

Selected:
- Pololu `D42V55F12`;
- item `5577`;
- input 12...60 V;
- output fixed 12 V;
- typical continuous current class 4.5 A;
- 25.4 x 25.4 x 9 mm;
- soft start;
- reverse-input, over-current and thermal protection;
- EN and PG pins.

Primary crawler use:
- camera electronics;
- two 12 V camera-axis motor-driver branches;
- balanced-video transmitter if its selected article uses 12 V.

Quantity:
- crawler: 1;
- recommended field spare: 1 shared spare for any crawler built with the same rail.

## 5. 5 V converter service module

Selected:
- Pololu `D42V55F5`;
- item `5571`;
- input 5...60 V;
- output fixed 5 V;
- typical continuous current class 6 A;
- 25.4 x 25.4 x 9 mm;
- soft start;
- reverse-input, over-current and thermal protection;
- EN and PG pins.

It is intentionally oversized for current logic consumption. The reasons are input-voltage headroom, robust service margin and the common physical family with the 12 V converter.

Primary crawler use:
- NUCLEO E5V;
- isolated RS-485 TTL side;
- current sensors;
- low-voltage pressure/temperature/interface electronics.

Quantity:
- crawler: 1;
- recommended field spare: 1.

## 6. Traction current sensors

Prototype measurement layer:
- 2 x INA226 R010-class ready module;
- one per LEFT/RIGHT traction branch;
- 0...36 V silicon bus-measurement class;
- I2C interface;
- unique addresses on one bus;
- current direction measurement required.

MCU bus:
- PB8 / I2C1_SCL;
- PB9 / I2C1_SDA.

Incoming-inspection rule:
- verify the actual shunt marking and current path;
- verify I2C address jumpers;
- calibrate every module against a bench ammeter/load;
- generic marketplace board current ratings are not accepted as calibration data.

The sensor module is therefore a Rev.B prototype service part, not a production metrology freeze.

## 7. Camera local communications

Reserved local UART:
- PC12 / UART5_TX;
- PD2 / UART5_RX.

This connects crawler electronics to the local camera-node controller and does not use additional main tether conductors.

The rotating camera node may still use the previously documented RP2040-Zero / ready H-bridge approach after camera-head mechanical validation.

## 8. Driver modules

Traction:
- two BTS7960/IBT-2 modules remain Rev.B prototype-only;
- production lifecycle/quality risk remains open because original BTS7960 silicon is obsolete.

Camera axes:
- ready DRV8871-class modules remain the present camera-node prototype family;
- exact purchased board must be matched to the selected 12 V N20 motors and physically measured before camera-head production release.

## 9. Common-spare target

Minimum Rev.B field electronics spare kit should converge toward:
- 1 x NUCLEO-F446RE;
- 1 x Waveshare 27479 isolated RS-485 module;
- 1 x Pololu 5577 12 V buck;
- 1 x Pololu 5571 5 V buck;
- 1 x traction-driver module from the qualified batch;
- 1 x camera-axis driver module;
- 1 x calibrated INA226-class current-sensor module;
- standard branch fuses;
- commonly used crawler seals/bearings outside this electrical document.

## 10. Sourcing rule

The selected Rev.B auxiliary modules were chosen only after checking controlled manufacturer information and an allowed marketplace route.

Current examples:
- Waveshare 27479 is listed on Allegro;
- Pololu 5577 is represented by an Allegro product listing;
- Pololu 5571 is represented by an Allegro product listing.

Availability and price must be rechecked at purchase time. A marketplace listing is evidence of a real purchasing route, not a permanent inventory guarantee.

## 11. Controlled references

- `electrical/REVB_WB09_LOW_VOLTAGE_COMMS.md`
- `electrical/PX1_SystemWiring_RevB.md`
- `electronics/REVB_WB08_24V_BUS_REGEN_PROTECTION.md`
- `firmware/crawler/board_map_f446.h`

## Change log

### 2026-09-11 — Rev.B
- replaced the old unspecified 24->5 V common buck with a 60 V-input service family;
- selected separate Pololu 5577 and 5571 rails;
- retained one Waveshare 27479 module family at crawler and CCU ends;
- removed external RS-485 DE from the crawler wiring baseline;
- added current-sensor I2C and local camera UART allocations;
- preserved ready-module/no-custom-PCB service philosophy.
