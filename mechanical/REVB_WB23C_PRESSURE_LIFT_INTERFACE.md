# PX-1 Rev.B — WB23C Proteus-style pressure/service cover and camera-lift harness

Date: 2026-09-14
Status: **PASS_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**

## 1. Purpose and correction

WB23A proved that a thin protected local harness can fit the lift, but the following WB23B study started to over-engineer cable motion with two dedicated flex chambers and imposed-radius loops. Repair evidence and MiniCam source drawings show a simpler, more serviceable topology.

WB23C therefore supersedes the WB23B flex-fan / dual-flex-chamber direction and returns to the source architecture:

`dry crawler body -> removable sealed service cover -> pressure valve + cable gland -> short flexible harness -> protected lift run -> fixed camera connector -> sealed removable camera`.

No crawler axle, wheel, Z50 gear, lift pivot or camera geometry is changed by WB23C.

## 2. Proteus source basis

The source package controls topology, not PX-1 manufacturing dimensions:

- `DRW-002-752 LIFT HOUSING`: camera connector, connector housing, M12x1.5 cable fitting for 3.5–5 mm cable, lift cover and multiple O-rings.
- `DRW-002-745 Crawler Cover Parts`: M12x1.5 cable fitting, holder, spring-loaded camera/pressure-valve components and electronic cover.
- `ASS-002-890 LIFT HOUSING UNIT - CRP300`: lift housing, lift-housing cover, M12 gland, camera connector and protection sheet.
- `DRW-003-121 / ASS-003-121`: dedicated `CAMERA LIFT ARM COVER`, side arms and lift-housing holding plates.
- repair-photo set 2025-03-14: integrated pressure body, serviceable upper/lift opening, perimeter seal land, camera connector and open dry electronics.

The current evidence does **not** conclusively prove that the exact CRP150 small cover marked `PRESSURE` is held by exactly two bolts. PX-1 uses two M4 screws as an independent compact-service-cover design choice, subject to prototype sealing and stiffness tests.

## 3. WB22A architecture retained

- 3 wheel stations per side / 6 wheels total.
- X50 / X150 / X250 wheel stations.
- ten m1 Z50 side gears total.
- rear X250 drive input.
- body pivot X = 200 mm.
- lift pivots Z = 92 / 109 mm.
- four-bar link = 90 mm.
- arm planes Y = ±31 mm, screen section 4 x 14 mm.
- sealed camera shell Ø52 x 78 mm.
- LOW optical axis X = 83.5569 mm, Z = 75 mm.

WB23C explicitly rejects the earlier trial move to X207.5.

## 4. PX-1 pressure/camera service cover

Packaging-screen cover:

- material target: EN AW-6082-T6 aluminium;
- outer envelope: **78 x 42 x 6 mm**;
- centre: X257 / Y0;
- service opening below cover: **58 x 24 mm**;
- target seal cord: 2.0 mm;
- provisional face-groove study: 2.5 mm wide x 1.5 mm deep;
- fasteners: **2 x M4 A4 stainless** into blind body threads/bosses;
- screen screw X positions: X224 and X290, Y0;
- marking: `PRESSURE / CAMERA SERVICE`.

The groove dimensions are **not machining-release dimensions**. Final gland, seal material/hardness, surface finish and measured flatness control the released drawing.

### Pressure-force sanity check

The 58 x 24 mm opening area gives approximately:

- 34.8 N separating force at +0.25 bar gauge;
- 139.2 N at +1.0 bar gauge;
- 69.6 N per screw at +1.0 bar if shared equally.

Fastener tensile capacity is therefore not the primary concern. Plate bending, gasket compression uniformity, thread engagement, impact and sealing remain physical-test gates.

## 5. Pressure fill point

Proteus source architecture uses a compact spring-loaded pressure-valve concept. PX-1 retains that service intent without copying an unavailable proprietary part.

Current packaging envelope:

- exposed OD <= 14 mm;
- exposed height above cover <= 6 mm;
- screen centre X268 / Y0;
- candidate thread class M10x1 or G1/8;
- compressor-gun / Schrader-compatible or equivalent industrial fill interface;
- metal protective cap or recessed protection required.

Exact valve article remains **PROCUREMENT HOLD**. The valve is the limiting fixed DN150 item in the current screen at about **4.70 mm** ideal clearance, so its height must not grow casually.

## 6. Cable gland

Controlled candidate:

- LAPP `SKINTOP MS-M 53112000`;
- M12 x 1.5;
- cable range 3.5–7.0 mm;
- hard body OD screen 17.6 mm;
- overall length screen 26.5 mm;
- thread length screen 6.5 mm.

WB23C places the gland **horizontally / forward-facing**, approximately X218.25, Y+12, Z103. A vertical gland consumes excessive DN150 roof clearance. The horizontal envelope leaves about 13.86 mm ideal-DN150 clearance.

The gland is a pressure-boundary cable seal, **not an electrical connector**.

## 7. Local camera/lift harness

Target OD: **<= 5.0 mm**.

Preferred content:

1. +12V_HEAD A
2. +12V_HEAD B
3. GND_HEAD A
4. GND_HEAD B
5. HEAD_UART_TX
6. HEAD_UART_RX
7. CVBS_SIGNAL
8. CVBS_RETURN
9. overall shield if available — EMC only, never DC return.

Protected lower-arm run:

- cable centre Y target +25.5 mm;
- screen arm-coordinate protected region s ≈ 20...72 mm;
- simple removable anti-snag cover over the straight run;
- no artificial constant-radius loop frozen in CAD.

Service slack targets are about 35 mm body-side and 35 mm head-side. Real bend shape is established on the physical lift with the selected cable.

## 8. Internal dry connector

Prototype candidate:

- JST `B8P-VH-B` 8-position header;
- JST `VHR-8N` housing;
- contacts selected for the purchased conductor cross-section.

Purpose: the external cover/gland/lift-harness assembly can be disconnected inside the dry body without unsoldering or removing the main electronics.

Rules:

- keyed/polarized orientation;
- separate strain relief before connector;
- connector does not support gland cable mechanically;
- label `J_CAM_LIFT`;
- contact numbering frozen only after the real pair is in hand.

## 9. Camera connector

WB15 remains controlling:

- camera panel: WEIPU `SP1312/P6-C`, male pins;
- powered harness: WEIPU `SP1310/S6I-N`, female sockets, if final cable OD is within its 4.0–6.5 mm range;
- six functions: +12V, GND, UART TX, UART RX, CVBS signal, CVBS return.

If purchased cable OD falls outside the S6I range, the plug size is reselected before procurement without changing the six-function interface.

## 10. Executed DN150 packaging result

CadQuery WB23C result:

- service cover: ~7.69 mm clearance;
- low-profile fill-valve envelope: ~4.70 mm;
- horizontal M12 gland: ~13.86 mm;
- two M4 head envelopes: ~7.93 mm;
- protected local cable / guard in LOW: ~30.20 / 29.23 mm.

MID and HIGH lift positions are not required to remain inside DN150 because they are larger-pipe operating positions. DN150 release is controlled in LOW, consistent with WB22A.

## 11. Field-service concept

1. Power crawler off.
2. Fully depressurize.
3. Clean and dry service area.
4. Disconnect camera SP13.
5. Remove two retained M4 service-cover screws.
6. Lift cover with gland/harness still attached.
7. Disconnect `J_CAM_LIFT` inside dry body.
8. Withdraw cover/gland/harness as one service assembly.
9. Inspect/replace seal.
10. Install replacement assembly.
11. Run pressure-decay and submerged leak test before wet use.

The main electronic stack should not need removal for a damaged camera-lift harness.

## 12. Release gates

WB23C is not manufacturing/procurement release until:

1. exact M12 gland is purchased/measured;
2. <=5 mm 8-core + shield cable is selected/purchased;
3. low-profile fill valve is selected/purchased;
4. SP13 and dry connector samples are measured;
5. service-cover prototype proves access/alignment;
6. +0.25 bar dry pressure-decay passes;
7. submerged leak test passes;
8. if final crawler keeps a 1 bar rating, controlled 1 bar proof passes;
9. LOW-HIGH-LOW lift cycling >=500, target 1000 cycles, passes;
10. wet/grit cycling passes;
11. conductor resistance, shield continuity, UART and CVBS remain healthy;
12. O-ring groove and cover torque are frozen from real parts and flatness;
13. final fastener heads, valve, gland and real wheel solids are checked in the full master.

## 13. Change log

### 2026-09-14 — WB23C

- stopped unnecessary WB23B R16 flex-fan / dual-flex-chamber work;
- retained WB22A X200 mechanics unchanged;
- returned harness topology to verified Proteus service logic;
- introduced compact `PRESSURE / CAMERA SERVICE` cover;
- chose two M4 screws as PX-1 prototype geometry without claiming exact original Proteus count;
- retained source-like M12 gland class and oriented it horizontally for DN150;
- separated cable pressure seal from dry electrical disconnect;
- froze <=5 mm local harness target and simple protected lower-arm run;
- retained WB15 SP13 camera quick-disconnect;
- executed DN150 packaging screen and obtained PASS;
- seal, flex-life and procurement remain explicit HOLDs.
