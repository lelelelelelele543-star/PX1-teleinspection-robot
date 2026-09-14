# PX-1 current crawler BOM — Rev.B

Date: 2026-09-14
Purpose: one consolidated build list for the current Proteus-derived PX-1 crawler master.

This is not a list of every historical candidate. It contains the parts actually controlling the current build, plus clearly marked HOLD items that must be measured before machining.

## 1. Main housing / pressure body

| Qty | Item | Current PX-1 choice / source logic | State |
|---:|---|---|---|
| 1 | Main crawler pressure housing | PX-1 machined EN AW-6082-T6, geometry derived from DRW-002-375 and current master | CAD PASS / machining HOLD |
| 1 | Rear motor pressure extension | integrated with main dry volume, end X384 | CAD PASS / pressure HOLD |
| 1 | Main weight / ballast plate | source concept FSS-002-060; PX-1 mass to be tuned after assembled weigh-in | detail HOLD |
| 2 | Z40 bevel gears | source GEA-002-530 geometry, final hardened matched pair with Z16 | supplier drawing HOLD |
| 2 | Z40 shafts | source FSS-002-066 logic, PX-1 machined shafts | detail HOLD |
| 2 | Shaft seals | 18 x 30 x 7 | standard part |
| 2 | Bearings | 61800-2RS, 10 x 19 x 5 | standard part |
| 2 | O-rings | 16 x 1 NBR/FKM after chemical check | standard part |
| 2 | O-rings | 38 x 1.5 NBR/FKM after chemical check | standard part |
| 2 | Lift holding plates | source FSS-002-084 logic / PX-1 machined | detail HOLD |
| 2 | Lift axles | source FSS-002-373 logic / PX-1 machined | detail HOLD |
| 2 | Bushings | 12-14-4 | standard part |
| 4 | Steel bushings | 8-10-4.5 | standard/machined |

## 2. Side drive — both sides total

Source basis: DRW-002-374.

| Qty | Item | Current requirement | State |
|---:|---|---|---|
| 2 | Side covers | PX-1 machined, source FAL-002-062 logic | drawing HOLD |
| 4 | Idle gears Z50 | m1 Z50 | geometry controlled |
| 6 | Wheel/axle gears Z50 | m1 Z50 | geometry controlled |
| 2 | Rear long axles | source FSS-002-064 logic, X250 drive input | drawing HOLD |
| 4 | Short wheel axles | source FSS-002-063 logic | drawing HOLD |
| 2 | Bearings 61801-2RS | 12 x 21 x 5, long-axle path | standard part |
| 6 | Bearings 61903-2RS | 17 x 30 x 7 | standard part |
| 6 | Axle flanges | source FSS-002-061 logic / PX-1 machined | drawing HOLD |
| 6 | X-rings | 18.72 x 2.62 | seal sample HOLD |
| 6 | Static axle-flange O-rings | 32 x 1.5 | standard part |
| 4 | Idler bushings | 10-12-4 | standard part |
| 2 | Side-cover O-rings | 190 x 1.5 | groove/sample HOLD |
| 6 | Wheel retaining assemblies | source ASS-002-103 M6-lock logic | exact PX-1 drawing HOLD |
| 6 | 90 mm wheels | QRW90SR/150 class or PX-1 equivalent profiled wheel | exact profile HOLD |

## 3. Traction motor unit

Source basis: DRW-002-386. The source architecture is retained: the Z16 pinion shaft has its own 61801 support bearing and is not cantilevered directly from the gearmotor.

| Qty | Item | Current article / requirement | State |
|---:|---|---|---|
| 2 + 1 spare | 24 V gearmotor | ISL `PGM-32P-24-100-60-02 / MOT-IG32PGM 100`, Ø32 class, 100:1 | leading prototype candidate; sample measurement required |
| 2 | Z16 bevel gears | hardened matched m1 Z16, paired with Z40, ratio 2.5:1 | supplier drawing HOLD |
| 2 | Z16 input shafts | PX1-441, Ø6 coupling stub / Ø12 bearing journal candidate | front gear interface HOLD |
| 2 | Pinion bearings | FAG `61801-2RSR-HLC` class, 12 x 21 x 5 | sample candidate |
| 2 + 1 spare | Rigid couplings | NBK `MLR-20C-6-6`, Ø20 x 24, 6/6 mm | current baseline |
| 1 | Twin motor holder | PX1-440, EN AW-6082-T6 | drawing HOLD pending real motor |
| 2 | DIN 471 circlips | shaft 12 mm, 1.0 mm | candidate retention |

Motor-control limit: final software/current limit must protect the bevel pair. Do not use the motor's theoretical stall torque as an operating target.

## 4. Manual camera lift

Source basis: DRW-002-744.

| Qty | Item | Current choice / source logic | State |
|---:|---|---|---|
| 2 | Side lever/link plates | PX-1 geometry; source manual lift principle | current CAD PASS |
| 2 | Opposite upper/lower link members | current four-arm WB22A geometry | current CAD PASS |
| 1 | 150 N gas spring | ACE `GS-12-20-V4A` class, 150 N target | sample/end-fitting HOLD |
| 1 | M8 clamping lever | source manual lock principle | purchasable part |
| 3 | Belleville washers | DIN 2093 20 x 10.2 x 1.1 source stack | standard part |
| 1 | Lever sheet / clamp structure | PX-1 machined | drawing HOLD |
| 1 set | Pivot axles / washers / circlips | source-style ordinary service parts | drawing HOLD |
| 1 | Fixed camera carrier | separates four-bar from TILT axis | current CAD PASS |

Current hard PX-1 lift datums: body pivot X200, pivots Z92/Z109, link length 90 mm, arms Y±31 mm.

## 5. Camera / lift service cover

| Qty | Item | Current article / requirement | State |
|---:|---|---|---|
| 1 | PRESSURE/CAMERA service cover | EN AW-6082-T6, 86 x 44 x 6 mm | packaging PASS / machining HOLD |
| 2 | Cover screws | A4 M4, retained preferred | length/torque HOLD |
| 1 | Cover seal | FKM 2 mm cord or molded equivalent | groove depth HOLD |
| 1 | Cable gland | LAPP SKINTOP MS-M `53112000`, M12x1.5, cable 3.5-7 mm | current candidate |
| 1 | Flush pressure valve cartridge | PX-1 Proteus-like ball/spring/O-ring architecture | pressure-test HOLD |
| 1 | Valve ball | Ø4 mm stainless | standard candidate |
| 2 | Valve O-rings | 3 x 1 FKM candidate | standard candidate |
| 1 | Valve outer O-ring | 6 x 1.5 FKM candidate | standard candidate |
| 1 | Valve spring | d0.5 / De3.7 / L0≈7.9 mm | standard candidate |
| 1 | Valve protective cap | exposed envelope ≤Ø12 x 1.5 mm target | detail HOLD |

## 6. Local camera harness — exactly six insulated cores

| Qty | Item | Current article / requirement | State |
|---:|---|---|---|
| 1 | Local cable | 6 x 0.25 mm² class, preferred OD 5.5-6.0 mm, hard max 6.5 mm | flex/EMC test HOLD |
| 1 sample | Continuous-flex cable candidate | LAPP `0028679` 6 x 0.25 mm², Ø5.4 mm, unshielded | A/B sample, EMC HOLD |
| 1 sample | Shielded size benchmark | LAPP `0034406` 6 x 0.25 mm², Ø6.0 mm | flex-life HOLD |
| 1 | Dry receptacle | Molex Micro-Fit 3.0 `43025-0600` | candidate |
| 1 | Dry plug | Molex Micro-Fit 3.0 `43020-0601` | candidate |
| 6 | Female contacts | Molex `43030-0007` | candidate |
| 6 | Male contacts | Molex `43031-0007` | candidate |
| 1 | Wet powered plug | WEIPU `SP1310/S6I-N`, female sockets | candidate |
| 1 | Camera panel connector | WEIPU `SP1312/P6-C`, male pins | candidate |
| 1 | Arm harness guard | removable, drain-open, 10 mm outside envelope | CAD PASS |

Function order remains: +12 V / GND / UART TX / UART RX / CVBS signal / CVBS return.

## 7. Internal crawler electronics

These envelopes are already packaged inside the single current master with 0 mm³ outside the dry volume and no pairwise overlap.

| Qty | Item | Current article / reserve | State |
|---:|---|---|---|
| 1 | Main controller | STM32 `NUCLEO-F446RE` | selected |
| 2 | Traction H-bridge channel | BTS7960 modules for prototype | selected prototype architecture |
| 1 | Main HV-to-24 V DC/DC | Cincon `CQB150W-110S24` | packaged candidate |
| 1 | HV bulk capacitor | Nichicon `UCS2D221MHD1TN`, 220 uF / 200 V | packaged candidate |
| 1 | Video balun/interface | Delta-Opti `TR-1D*P2` envelope | packaged candidate |
| 1 | Input protection assembly | ready-made/discrete serviceable modules | component detail HOLD |
| 1 | Pressure sensor | module reserve already packaged | exact article HOLD |
| 1 | RS-485 interface | MAX485-class ready-made module | prototype selected |
| 1 | 24→12 V converter | LM2596 ready-made module | prototype selected |
| 1 | 12→5 V converter | MP1584 ready-made module | prototype selected |

## 8. Rear tether / crawler connector

Source basis: ASS-002-090 + ASS-002-364 functional stack.

| Qty | Item | Current rule | State |
|---:|---|---|---|
| 1 | Crawler-side 6-contact connector | PX-1 replacement preserving six-contact/service logic | exact connector HOLD |
| 1 | Contact spring / strain-isolation stack | retain source functional principle | detail HOLD |
| 1 | Cable housing / nut | ordinary machined/serviceable hardware | detail HOLD |
| 1 set | Static seals / gland | matched to purchased tether OD | tether sample HOLD |
| 1 | PU sleeve / mechanical strain relief | terminate pull mechanically, not at contacts | detail HOLD |
| 1 | Reinforced main tether | professional six-core copper + aramid/Kevlar strength path | exact cable article HOLD |

Initial tether release length: 40 m. Do not release 100-150 m until real conductor resistance/video/power measurements pass.

## 9. Parts to obtain first — before machining final body

1. 3 x ISL PGM-32P motors (2 build + 1 spare/sample backup).
2. 3 x NBK MLR-20C-6-6 couplings (2 build + 1 spare/test).
3. 4 x quality 61801-2RS bearings (2 motor input + 2 long axle; plus spares recommended).
4. 6 x 61903-2RS wheel bearings + spares.
5. 2 x 61800-2RS bearings + spares.
6. One matched prototype Z16/Z40 pair for dimensional/backlash fitting; final full-load pair must satisfy hardened torque requirement.
7. 1 x ACE GS-12-20-V4A class spring with chosen end fittings.
8. 2 x LAPP 53112000 glands.
9. 2 x WEIPU six-pin pairs.
10. Molex six-way Micro-Fit housings + enough contacts for two harnesses.
11. Short samples of both six-core cable candidates.
12. FKM seal samples and pressure-valve ball/spring/O-rings.
13. One real 90 mm QRW90SR/150 wheel or equivalent wheel sample for exact profile measurement.

## 10. What is already ready in the master

The current STEP contains the complete crawler assembly envelope and packaged electronics. The remaining HOLD items above are not reasons to invent a different robot; they are simply the physical samples/dimensions needed to turn the current source-derived assembly into machining drawings.
