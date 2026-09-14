# PX-1 current crawler BOM — Rev.B

Date: 2026-09-14  
Purpose: one consolidated build list for the single current Proteus-derived PX-1 crawler master.

This file contains the parts that control the current build. Historical alternatives remain in their old engineering notes only. A part is marked HOLD when its exact article or manufacturing dimension has not yet been verified.

## 1. Main housing / pressure body

| Qty | Item | Current PX-1 choice / source logic | State |
|---:|---|---|---|
| 1 | Main crawler pressure housing | PX-1 machined EN AW-6082-T6, Proteus CRP150 architecture from DRW-002-375 | integrated CAD PASS / machining HOLD |
| 1 | Rear motor/electronics pressure extension | same P0 dry volume; current master ends at **X410 mm** | integrated CAD PASS / pressure HOLD |
| 1 | Upper dry electronics tunnel | X300…410, width 60 mm, Z65…117; integrated into pressure body, not a cassette | packaging PASS / pressure HOLD |
| 1 | Main weight / ballast plate | source FSS-002-060 concept; final mass after assembled weigh-in | detail HOLD |
| 2 | Z40 bevel gears | source GEA-002-530 architecture; final hardened matched pair with Z16 | supplier drawing HOLD |
| 2 | Z40 shafts | source FSS-002-066 logic, PX-1 machined shafts | exact shoulders HOLD |
| 2 | Shaft seals | **18 x 30 x 7** from DRW-002-375 | source-confirmed standard size |
| 2 | Bearings | **61800-2RS, 10 x 19 x 5** from DRW-002-375 | source-confirmed standard size |
| 2 | O-rings | 16 x 1 | source-confirmed size; material chemical check |
| 2 | O-rings | 38 x 1.5 | source-confirmed size; material chemical check |
| 2 | Lift holding plates | source FSS-002-084 logic / PX-1 machined | exact drawing HOLD |
| 2 | Lift axles | source FSS-002-373 logic / PX-1 machined | exact drawing HOLD |
| 2 | Bushings | 12-14-4 | source-confirmed size |
| 4 | Steel bushings | 8-10-4.5 | source-confirmed size |

## 2. Side drive — both sides total

Source basis: `DRW-002-374`. The quantities and standard bearing/seal sizes below are now present in the current master; only exact machined shoulder lengths remain HOLD where detail drawings are absent.

| Qty | Item | Current requirement | State |
|---:|---|---|---|
| 2 | Side covers | PX-1 machined, source FAL-002-062 logic | drawing HOLD |
| 4 | Idle gears Z50 | m1 Z50 | source architecture fixed |
| 6 | Wheel/axle gears Z50 | m1 Z50 | source architecture fixed |
| 2 | Rear long axles | source FSS-002-064 logic, X250 drive input | exact shoulder drawing/measurement HOLD |
| 4 | Short wheel axles | source FSS-002-063 logic | exact shoulder drawing/measurement HOLD |
| 2 | Bearings 61801-2RS | **12 x 21 x 5**, rear long-axle path | source-confirmed size |
| 6 | Bearings 61903-2RS | **17 x 30 x 7** | source-confirmed size |
| 6 | Axle flanges | source FSS-002-061 logic / PX-1 machined | exact thickness/shoulders HOLD |
| 6 | X-rings | **18.72 x 2.62** | source-confirmed size; sample material HOLD |
| 6 | Static axle-flange O-rings | 32 x 1.5 | source-confirmed size |
| 4 | Idler bushings | 10-12-4 | source-confirmed size |
| 2 | Side-cover O-rings | 190 x 1.5 | source-confirmed size; final groove HOLD |
| 6 | Wheel retaining assemblies | source ASS-002-103: wheel disk + M6 x 14 + spring washer + 10 x 1.8 O-ring | PX-1 interface drawing HOLD |
| 6 | 90 mm wheels | MiniCam `QRW90SR/150` class or measured equivalent | **exact outer profile HOLD** |

## 3. Traction motor unit

Source basis: `DRW-002-386`. The Proteus rule is retained: each Z16 has a separately supported shaft with a 61801; the bevel load is not hung directly on the gearmotor output shaft.

| Qty | Item | Current article / requirement | State |
|---:|---|---|---|
| 2 + 1 spare | 24 V gearmotor | ISL `PGM-32P-24-100-60-02 / MOT-IG32PGM 100`, Ø32, 100:1 | leading prototype candidate; physical sample measurement required |
| 2 | Z16 bevel gears | hardened matched m1 Z16, paired with Z40, ratio 2.5:1 | final supplier drawing/torque rating HOLD |
| 2 | Z16 input shafts | PX1-441 concept, Ø6 coupling stub / Ø12 bearing journal | front gear seat and mounting distance HOLD |
| 2 | Pinion bearings | 61801-2RS, 12 x 21 x 5 | source-confirmed size |
| 2 + 1 spare | Rigid couplings | NBK `MLR-20C-6-6`, Ø20 x 24, 6/6 mm | current prototype baseline |
| 1 | Twin motor holder | PX1-440, EN AW-6082-T6 | drawing HOLD pending measured motor |
| 2 | DIN 471 circlips | shaft 12 mm, 1.0 mm | PX-1 retention candidate |

Motor-control rule: software/current limiting must protect the bevel pair. Full theoretical motor stall torque is not an operating target.

## 4. Manual camera lift

Source basis: `DRW-002-744`.

| Qty | Item | Current choice / source logic | State |
|---:|---|---|---|
| 2 | Side lever/link plates | PX-1 geometry following Proteus manual-lift principle | current CAD PASS |
| 2 | Opposite upper/lower link members | current four-arm geometry | current CAD PASS |
| 1 | 150 N gas spring | ACE `GS-12-20-V4A` class, 150 N target | sample/end-fitting HOLD |
| 1 | M8 clamping lever | source manual lock principle | purchasable part |
| 3 | Belleville washers | DIN 2093 20 x 10.2 x 1.1 | source-confirmed stack |
| 1 | Lever sheet / clamp structure | PX-1 machined | drawing HOLD |
| 1 set | Pivot axles / washers / circlips | source-style ordinary service parts | drawing HOLD |
| 1 | Fixed camera carrier | separates four-bar lift from TILT axis | current CAD PASS |

Current PX-1 lift datums: body pivot X200, pivot heights Z92/Z109, link length 90 mm, arm planes Y±31 mm.

## 5. Camera / lift service cover

| Qty | Item | Current article / requirement | State |
|---:|---|---|---|
| 1 | PRESSURE/CAMERA service cover | EN AW-6082-T6, 86 x 44 x 6 mm | packaging PASS / machining HOLD |
| 2 | Cover screws | A4 M4, retained preferred | exact length/torque HOLD |
| 1 | Cover seal | FKM 2 mm cord or molded equivalent | exact groove depth HOLD |
| 1 | Cable gland | LAPP SKINTOP MS-M `53112000`, M12x1.5, cable 3.5-7 mm | current candidate |
| 1 | Flush pressure valve cartridge | PX-1 implementation of Proteus ball/spring/O-ring principle | pressure-test HOLD |
| 1 | Valve ball | Ø4 mm stainless | standard candidate |
| 2 | Valve O-rings | 3 x 1 FKM candidate | standard candidate |
| 1 | Valve outer O-ring | 6 x 1.5 FKM candidate | standard candidate |
| 1 | Valve spring | wire 0.5 / OD 3.7 / free length ≈7.9 mm | standard candidate |
| 1 | Valve protective cap | exposed envelope ≤Ø12 x 1.5 mm target | detail HOLD |

## 6. Local camera harness — exactly six insulated cores

| Qty | Item | Current article / requirement | State |
|---:|---|---|---|
| 1 | Local cable | 6 x 0.25 mm² class, preferred OD 5.5-6.0 mm, hard max 6.5 mm | flex/EMC test HOLD |
| 1 sample | Continuous-flex candidate | LAPP `0028679`, 6 x 0.25 mm², Ø≈5.4 mm, unshielded | A/B sample; EMC HOLD |
| 1 sample | Shielded size benchmark | LAPP `0034406`, 6 x 0.25 mm², Ø≈6.0 mm | flex-life HOLD |
| 1 | Dry receptacle | Molex Micro-Fit 3.0 `43025-0600` | candidate |
| 1 | Dry plug | Molex Micro-Fit 3.0 `43020-0601` | candidate |
| 6 | Female contacts | Molex `43030-0007` | candidate |
| 6 | Male contacts | Molex `43031-0007` | candidate |
| 1 | Wet powered plug | WEIPU `SP1310/S6I-N`, female sockets | candidate |
| 1 | Camera panel connector | WEIPU `SP1312/P6-C`, male pins | candidate |
| 1 | Arm harness guard | removable, drain-open, 10 mm outside envelope | CAD PASS |

Function order remains: +12 V / GND / UART TX / UART RX / CVBS signal / CVBS return. Shield is EMC only.

## 7. Internal crawler electronics

The current master uses the **realistic package envelope**, not the earlier undersized traction-driver placeholders.

| Qty | Item | Current article / reserve | State |
|---:|---|---|---|
| 1 | Main controller | STM32 `NUCLEO-F446RE` | selected |
| 2 | Traction H-bridge | BTS7960 / IBT-2 module, **modeled 50 x 50 x 43 mm each** | selected prototype architecture / exact purchased-board measurement later |
| 1 | Main HV-to-24 V DC/DC | Cincon `CQB150W-110S24` | packaged candidate |
| 1 | HV bulk capacitor | Nichicon `UCS2D221MHD1TN`, 220 uF / 200 V | packaged candidate |
| 1 | Video balun/interface | Delta-Opti `TR-1D*P2` | packaged candidate |
| 1 | Input protection assembly | ready-made/discrete serviceable modules | detail HOLD |
| 1 | Pressure sensor | **not yet selected** | exact article + mounting HOLD; no fit claim |
| 1 | RS-485 interface | MAX485-class ready-made module | prototype selected |
| 1 | 24→12 V converter | LM2596 ready-made module | prototype selected |
| 1 | 12→5 V converter | MP1584 ready-made module | prototype selected |

Current BTS centers in master: X330/Y0/Z91.5 and X382/Y0/Z91.5. Their upper dry tunnel remains part of the same pressure body; it is not a removable cassette.

## 8. Rear tether / crawler connector

Source basis: `ASS-002-090` plus the recovered Proteus tether-end/strain-relief family.

| Qty | Item | Current rule | State |
|---:|---|---|---|
| 1 | Crawler-side 6-contact connector | PX-1 replacement preserving six-contact/service logic | exact connector HOLD |
| 1 | Contact spring / strain-isolation stack | retain source functional principle | source detail search in progress |
| 1 | Cable housing / nut | ordinary machined/serviceable hardware | exact dimensions HOLD |
| 1 set | Static seals / gland | matched to purchased tether OD | tether sample HOLD |
| 1 | PU sleeve / mechanical strain relief | terminate tether pull mechanically, never through electrical contacts | exact dimensions HOLD |
| 1 | Reinforced main tether | professional six-core copper + aramid/Kevlar strength path | exact article HOLD |

Initial tether release length: 40 m. Do not release 100-150 m until conductor resistance, camera voltage and video tests pass.

## 9. Parts to obtain first — before machining final body

1. **One real QRW90SR/150 wheel or an original 90 mm Proteus wheel** for exact profile/width/hub measurement.
2. 3 x ISL PGM-32P motors (2 build + 1 spare/sample backup).
3. 3 x NBK MLR-20C-6-6 couplings (2 build + 1 spare/test).
4. 4+ x 61801-2RS bearings; 6+ x 61903-2RS; 2+ x 61800-2RS, with sensible spares.
5. Six X-rings 18.72 x 2.62 + spares and the static O-rings from the source stack.
6. One prototype matched Z16/Z40 pair for dimensional/backlash fitting; final loaded pair must satisfy the hardened torque gate.
7. 1 x ACE GS-12-20-V4A class spring with chosen end fittings.
8. 2 x LAPP 53112000 glands.
9. 2 x WEIPU six-pin pairs.
10. Molex six-way Micro-Fit housings + contacts for two harnesses.
11. Short samples of both six-core cable candidates.
12. FKM seal samples and pressure-valve ball/spring/O-rings.
13. A real pressure-sensor module selected by article before adding its holder to CAD.

## 10. Current master truth

The controlling master now contains:
- six wheel positions and ten Z50;
- source-size 61903 / 61801 / 61800 bearing envelopes;
- source-size X-rings and 18x30x7 shaft seals;
- two Z40 paths and two supported Z16 motor-input paths;
- two real-size 50x50x43 BTS7960 envelopes;
- NUCLEO, Cincon, bulk capacitor, video interface and input-protection envelopes;
- manual lift, camera, pressure/service cover, six-core harness and rear tether envelope.

Current status is an integrated packaging/architecture PASS, **not machining release**. Remaining hard unknowns are physical/detail dimensions, not permission to invent another robot.
