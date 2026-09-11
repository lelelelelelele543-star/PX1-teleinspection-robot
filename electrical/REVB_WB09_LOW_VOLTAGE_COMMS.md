# PX-1 Rev.B — WB09 low-voltage rails / NUCLEO power / isolated RS-485

Date: 2026-09-11
Status: POWER PASS-SCREEN / RS-485 COMMON-MODE QUALIFICATION HOLD

## 1. Scope

WB09 closes the serviceable low-voltage distribution downstream of the already approved 24 V crawler bus.

It does **not** change:
- the Proteus-style mechanical architecture;
- the 120 V-class six-functional-core tether;
- the 24 V internal traction bus;
- the two-motor LEFT/RIGHT drive architecture;
- the separate camera body;
- the no-custom-PCB prototype rule.

WB09 covers:
- 24 V -> 12 V camera/actuator rail;
- 24 V -> 5 V logic rail;
- NUCLEO-F446RE power entry;
- main tether RS-485 module and MCU UART allocation;
- traction current-sensor bus;
- branch grounding and harness rules;
- preliminary fusing and bring-up tests.

## 2. Why the earlier LM2596/MP1584-class choice is no longer the preferred crawler rail

Older PX-1 notes treated common 24->12 V LM2596 and 12->5 V MP1584 modules as adequate prototype converters.

That is no longer the preferred Rev.B crawler solution for one specific reason: WB08 deliberately protects the 24 V traction bus with a 1.5KE30A transient clamp whose worst published pulse clamp is above 36 V.

A cheap module with a 35/36 V absolute input limit therefore has insufficient engineering headroom if it is connected directly to the same 24 V distribution node.

Decision:
- keep cheap 36 V modules only as bench/development spares on a clean current-limited 24 V supply;
- use >=50 V input-rated modules in the sealed crawler;
- current preferred service family uses 60 V-rated Pololu D42V55Fx modules.

This avoids adding a second special over-voltage protection architecture solely to protect a cheap buck converter.

## 3. Selected 12 V rail

### Pololu D42V55F12 — item 5577

Purpose:
- camera head supply;
- TILT/ROLL camera-axis motor-driver supply;
- balanced-video transmitter supply where its exact module accepts 12 V;
- other low-noise 12 V camera auxiliaries.

Controlled data:
- manufacturer: Pololu;
- article: `D42V55F12`;
- Pololu item: `5577`;
- input: 12...60 VDC;
- output: fixed 12 V;
- typical continuous output-current class: 4.5 A at the manufacturer's stated comparison condition;
- typical efficiency class: about 85...95% depending on operating point;
- switching frequency: approximately 400 kHz under heavy load;
- soft start;
- reverse-input protection;
- over-current and thermal protection;
- Power-Good output;
- Enable input;
- size: 25.4 x 25.4 x 9 mm;
- mass: approximately 6.5 g.

Source status at Rev.B check:
- official product remains active/preferred;
- marketplace product page exists on Allegro for `Pololu 5577 / D42V55F12`;
- official Polish distributor routes also exist, but the approved PX-1 purchase route remains marketplace/ChipDip unless the user explicitly relaxes it.

Official source:
`https://www.pololu.com/product/5577`

Marketplace reference:
`https://allegro.pl/produkt/przetwornica-pololu-5577-1fd77e61-a4e9-478d-bc2e-b226e8ff6c54`

### 12 V load screen

Current camera motor baseline from Rev.BK:
- two 12 V N20-class axes;
- each motor stall-current screen <=1.1 A;
- both simultaneous motor-stall electrical screen <=2.2 A before camera/video electronics.

The D42V55F12 therefore has useful current margin for both axis drivers plus camera electronics.

This does **not** authorize holding either motor at stall. Camera motor drivers still require timeout/current limiting and mechanical end stops.

### Installation

Mount the module on the dry-body electronics carrier using its mounting holes and insulating stand-offs.

Reserve mechanical envelope:
- board: 25.4 x 25.4 x 9 mm;
- CAD/service envelope: 32 x 32 x 15 mm including wiring bend and fastener access.

Place it away from the balanced-video transmitter and camera signal pair. Do not mount it directly under the video balun/transmitter.

## 4. Selected 5 V logic rail

### Pololu D42V55F5 — item 5571

Purpose:
- NUCLEO-F446RE E5V input;
- crawler-side isolated TTL/RS-485 module logic supply;
- INA226-class current sensors;
- pressure/temperature/interface electronics whose final modules accept 5 V;
- service margin for future low-voltage modules.

Controlled data:
- manufacturer: Pololu;
- article: `D42V55F5`;
- Pololu item: `5571`;
- input: 5...60 VDC;
- output: fixed 5 V;
- typical continuous output-current class: 6 A at the manufacturer's stated comparison condition;
- reverse-input protection;
- over-current and thermal protection;
- soft start;
- Power-Good output;
- Enable input;
- size: 25.4 x 25.4 x 9 mm;
- mass: approximately 6.5 g.

The module is electrically oversized for the present logic load. It is selected because:
1. it shares the same family, mounting envelope and service philosophy as the 12 V converter;
2. it has 60 V input headroom;
3. it gives ample margin for NUCLEO + isolated communications + sensors;
4. it is a current production part with a current marketplace route.

Official source:
`https://www.pololu.com/product/5571`

Marketplace reference:
`https://allegro.pl/produkt/przetwornica-pololu-5571-6b01771d-58fb-4873-8789-232e7e5151a6`

At the Rev.B sourcing check the Allegro product page was live and identified the board as Pololu 5571 / D42V55F5.

### Installation

Reserve the same 32 x 32 x 15 mm service envelope as the 12 V module.

Prefer adjacent mounting orientation but keep 5 V logic wiring physically separated from LEFT/RIGHT motor-current loops.

Do not route traction return current through the converter's logic-ground wiring.

## 5. NUCLEO-F446RE power rule

The crawler NUCLEO is powered from the regulated 5 V rail through `E5V`, not from the 24 V bus and not through VIN.

Board rule:
- `5V_LOGIC -> E5V`;
- set the NUCLEO external-5-V supply configuration according to ST UM1724;
- respect the E5V permitted voltage range;
- do not back-feed the board from both USB/ST-LINK power and crawler E5V without following the ST jumper/power-order rules.

For bench debugging:
- verify the NUCLEO jumper configuration before plugging USB into ST-LINK;
- the crawler 5 V source is the master power source during integrated powered tests;
- USB is debug/data only unless intentionally configured otherwise.

Other 5 V devices are connected **in parallel to the 5 V rail**. They are not powered through the NUCLEO E5V pin.

## 6. Main tether RS-485 module freeze

### Waveshare TTL TO RS485 (C)

Selected prototype/service module:
- manufacturer: Waveshare;
- model: `TTL TO RS485 (C)`;
- SKU: `27479`;
- supply/logic level: 3.3...5 V class;
- half-duplex RS-485;
- onboard isolated DC/DC;
- digital galvanic isolation;
- onboard TVS/protection;
- resettable fuse/protection network;
- optional/on-board 120 ohm termination by solder selection;
- physical size: approximately 42.8 x 15.2 x 4.75 mm;
- TTL side: VCC, GND, TXD, RXD;
- line side: A+, B-, PE/reference terminal;
- no separate MCU DE pin is exposed: transmit/receive direction is handled by the ready module.

Use the **same module at both ends** of the tether where practical:
- crawler side;
- CCU side.

This preserves the Rev.PL common-spares concept.

Official reference:
`https://www.waveshare.com/ttl-to-rs485-c.htm`

Marketplace reference:
`https://allegro.pl/produkt/konwerter-ttl-na-rs485-z-izolacja-galwaniczna-komunikacja-half-duplex-c1776ead-a371-4dcd-ab4f-37b76bccdaeb`

Current marketplace search identifies SKU 27479 directly.

## 7. RS-485 MCU pin correction

The old Rev.AJ board map used:
- PA2 / USART2_TX;
- PA3 / USART2_RX;
- PB12 / DE.

That map is not ideal for the selected Rev.B module:
- the module has no external DE input;
- PA2/PA3 are the NUCLEO default ST-LINK virtual-COM USART2 path and are useful for bench diagnostics.

Rev.B crawler allocation becomes:
- `PC10 = USART3_TX -> Waveshare RX/TX interface as required by module labeling`;
- `PC11 = USART3_RX`;
- no DE GPIO;
- PA2/PA3 remain reserved for ST-LINK VCP/debug.

ST's F446 datasheet confirms:
- PC10 supports USART3_TX;
- PC11 supports USART3_RX.

The updated logical map is stored in `firmware/crawler/board_map_f446.h`.

## 8. Camera local UART reservation

Moving main tether RS-485 away from USART2 also avoids blocking other serial work.

Rev.B reserves a separate hardware UART for the local camera node:
- `PC12 = UART5_TX`;
- `PD2 = UART5_RX`.

This UART is local inside the crawler/camera assembly only. It does not consume any additional tether core.

ST's F446 datasheet confirms the PC12 / PD2 UART5 alternate functions.

## 9. Current-sensor I2C bus

Reserve:
- `PB8 = I2C1_SCL`;
- `PB9 = I2C1_SDA`.

Prototype sensor architecture:
- one ready INA226 R010-class module upstream of LEFT traction H-bridge;
- one ready INA226 R010-class module upstream of RIGHT traction H-bridge;
- configure different I2C addresses;
- power logic from the 5 V rail only if the purchased module's pull-ups/logic are verified compatible with the STM32 interface; otherwise use 3.3 V sensor logic/pull-ups.

Important module-quality hold:
- the INA226 silicon itself is a 36 V, 16-bit active TI device and supports multiple programmable addresses;
- generic ready modules have inconsistent shunts/traces/terminal arrangements;
- every bought R010 board must be calibrated against a bench ammeter before being used for torque protection;
- do not use a marketplace board's printed `10 A/20 A` claim as the calibration constant.

Marketplace availability of R010 modules has been confirmed, but exact PCB revision remains a physical incoming-inspection item.

## 10. RS-485 reference/common-mode problem — explicit HOLD

This is the main unresolved electrical risk discovered in WB09.

The active tether has only:
- RS485_A;
- RS485_B;
with no seventh signal-common conductor.

Galvanic isolation eliminates a direct ground loop, but it does **not** make unlimited common-mode voltage disappear. Long cables and different local potentials can move the bus common-mode outside the receiver's allowable range.

Therefore:
- do not connect Waveshare `PE` to tether HV-;
- do not use the HV return as RS-485 reference;
- do not defeat the isolated module by bonding line-side reference to crawler logic GND;
- do not claim 150 m production robustness merely because the module vendor quotes ~1200 m under suitable conditions.

The 2-wire architecture remains allowed for Rev.B **only as a qualification item**.

Required sequence:
1. prove 40 m with both traction sides and LED PWM switching;
2. measure A/B differential waveform and line-side common-mode relative to each isolated transceiver reference;
3. repeat with 100 m equivalent;
4. repeat with 150 m equivalent;
5. deliberately exercise direction reversal, motor jam-limit events, camera motors and lighting PWM;
6. only then promote the two-wire link to production release.

If common-mode margin is inadequate, stop and revise the physical-layer transceiver/reference strategy. Do not silently consume HV- or VIDEO conductors as a reference.

## 11. Termination policy

Point-to-point tether only:
- termination at the two physical ends;
- no termination in the reel/slip-ring middle;
- nominal termination must match the **measured** differential impedance of the final cable pair.

Starting rule:
- if measured pair Z0 is close to 120 ohm, enable the module's onboard 120 ohm termination at both ends;
- if final custom pair is closer to 100 ohm, leave onboard 120 ohm disabled and fit the correct external service resistor at each endpoint.

Do not enable multiple bias networks blindly.

Fail-safe/bias behavior is verified on the actual two purchased modules before adding an external master-side bias network.

## 12. Ground and current-return architecture

Inside the crawler the isolated HV->24 V converter creates the local low-voltage domain.

Use a star distribution point immediately downstream of the 24 V converter output.

Branches:

```text
24V_STAR
 |
 +-- LEFT traction fuse/current sensor/driver/motor return
 |
 +-- RIGHT traction fuse/current sensor/driver/motor return
 |
 +-- 12V buck -> camera/axis-driver domain
 |
 +-- 5V buck -> NUCLEO/RS485/sensors
 |
 +-- lighting constant-current branch
```

Rules:
- LEFT motor current does not flow through RIGHT sensor or logic ground;
- camera/video return does not share the high-current motor harness section;
- RS-485 TTL-side ground belongs to crawler logic ground;
- RS-485 isolated line-side reference remains isolated;
- balanced video pair and its quiet power wiring are kept physically away from BTS7960 switching loops;
- the aluminum pressure body is not used as a normal DC current return conductor.

## 13. Preliminary fuse schedule

Values below are **bring-up starting points**, not production freeze.

### 12 V converter input branch
- 24 V-side fuse starting class: 3.15 A time-delay.
- Reason: enough for the 12 V / 4.5 A converter output class with conversion loss, while remaining a branch/wiring protection device.

### 12 V camera harness
- output fuse starting class: 3.15 A time-delay.
- If simultaneous camera-axis startup repeatedly approaches this value in normal commanded operation, measure the real current before increasing the fuse.

### 5 V logic converter input branch
- 24 V-side fuse starting class: 1.0 A time-delay.

### NUCLEO feed
- E5V harness protection starting class: 0.75 A or lower after real board/peripheral load measurement.

These fuses are not current-control elements. Motor and mechanical protection remains electronic/firmware controlled.

## 14. Low-voltage wiring sizes — prototype minimums

Short internal harness only:
- 24 V feed to 12 V converter: >=0.5 mm2 flexible copper;
- 12 V camera motor branch: >=0.5 mm2 flexible copper;
- 24 V feed to 5 V converter: >=0.35 mm2;
- 5 V logic trunk: >=0.35 mm2;
- individual low-current sensor/UART/I2C leads: 0.14...0.25 mm2 flexible copper;
- LEFT/RIGHT traction power wiring follows WB08/current-test results and is not reduced by this document.

Use ferrules/crimped contacts in screw terminals. No bare stranded wire under service terminals.

## 15. Power-up sequence

1. Apply protected 24 V bench supply with traction drivers disabled.
2. Verify 12.0 V rail unloaded, then under dummy load.
3. Verify 5.0 V rail unloaded, then under dummy load.
4. Power NUCLEO from E5V and verify ST-LINK debug behavior.
5. Add crawler-side RS-485 module and short local link.
6. Add current sensors one at a time and verify unique I2C addresses.
7. Add camera motor drivers and camera electronics.
8. Run logic/video noise test with traction drivers enabled but wheels unloaded.
9. Run 40 m tether RS-485 test.
10. Only after low-voltage system is stable, combine with WB07 high-voltage tether supply.

## 16. Validation gates

WB09 power architecture is PASS-SCREEN because:
- 60 V-rated auxiliary bucks have margin over the Rev.B 24 V bus transient-clamp envelope;
- 12 V current capacity exceeds the current two-axis camera motor screen;
- regulated 5 V is suitable for the NUCLEO E5V supply route when configured per ST documentation;
- all selected blocks are ready-made service modules.

WB09 communications is **not yet fully released** because:
- the tether intentionally has no RS-485 reference conductor;
- the two-wire isolated common-mode behavior must be proven on the physical 40/100/150 m link.

## 17. Rev.B BOM delta

Add for one crawler:
- 1 x Pololu D42V55F12 / 5577;
- 1 x Pololu D42V55F5 / 5571;
- 1 x Waveshare TTL TO RS485 (C) / SKU 27479;
- 2 x INA226 R010-class ready current-sensor module, incoming-inspection/calibration required;
- service fuses/holders according to the preliminary schedule;
- stand-offs and insulated mounting hardware for both Pololu boards.

Add for one CCU:
- 1 x matching Waveshare TTL TO RS485 (C) / SKU 27479.

## Change log

### 2026-09-11 — WB09
- replaced 36 V-class crawler auxiliary-buck assumptions with 60 V-rated service modules;
- selected marketplace-available Pololu 5577 for the 12 V camera/actuator rail;
- selected marketplace-available Pololu 5571 for the 5 V logic rail;
- fixed NUCLEO supply to regulated E5V rather than 24 V/VIN;
- froze Waveshare SKU 27479 as the Rev.B isolated ready-made RS-485 module family;
- removed the obsolete external DE GPIO requirement for that module;
- moved tether RS-485 to USART3 PC10/PC11 and preserved PA2/PA3 for ST-LINK VCP/debug;
- reserved UART5 PC12/PD2 for the local camera node;
- reserved I2C1 PB8/PB9 for per-side current sensors;
- formally recorded the missing RS-485 reference conductor as a common-mode qualification HOLD rather than hiding it;
- prohibited bonding RS-485 PE/reference to tether HV return.
