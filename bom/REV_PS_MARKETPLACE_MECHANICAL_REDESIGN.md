# PX-1 Rev.PS — marketplace mechanical redesign and procurement gates

Date: 2026-09-02  
Status: prototype procurement baseline; SAMPLE/MEASURE gates remain mandatory.

## Design decision

PX-1 keeps the CRP-150 service logic but is rebuilt around current standard parts. Custom machining cannot be eliminated honestly: the DN150 pressure body, seal flanges, wheel cores, shafts, side covers, lift arms and camera pressure housing are geometry-specific safety parts. Everything that is sensibly standardised is assigned a catalog interface.

No cassette or cartridge is used anywhere in the crawler, camera, reel or tether tail.

## Purchasable interface matrix

| Assembly | Rev.PS purchasable item / interface | Qty | Source class | Release state |
|---|---|---:|---|---|
| Traction | Ø32 mm, 24 V, about 50–60 rpm industrial planetary gearmotor; documented reference PGM-32P-24-100-60-02 / MOT-IG32PGM-100 | 2 | industrial distributor / marketplace equivalent | SAMPLE + MEASURE |
| Motor alternative | JGB37-520/555 24 V marketplace gearmotor, selected by measured speed/current/shaft | 2 | Ozon/marketplaces | ADAPTER PATH, not bulk order |
| Side train | spur gear m1, Z50, 20° PA, steel, machinable hub | 10 | standard gear supplier / marketplace | SAMPLE + bore machining |
| Bevel input | matched straight-bevel set Z16/Z40, 2.5:1; module and face width frozen only after paired sample | 2 pairs | gear supplier / marketplace | HOLD exact article |
| Pinion support | 61801-2RS, 12x21x5 | 2 | bearing distributor | BUY SAMPLE |
| Wheel station | 61903-2RS, 17x30x7 | 6 | bearing distributor | BUY SAMPLE |
| Auxiliary shaft | 61800-2RS, 10x19x5 | 2 | bearing distributor | BUY SAMPLE |
| Dynamic wheel seal | Trelleborg Quad-Ring QRAR04116, 18.72x2.62, FKM V7002 or dimensionally verified equivalent | 6 + 4 spares | seal distributor | RFQ/SAMPLE |
| Static axle seal | O-ring 32x1.5 FKM 75 | 6 + 4 spares | RTI distributor / marketplace | BUY SAMPLE |
| Wheel retention | A4-80 M8 centre screw, wedge-lock washer pair, stainless retaining disk, protective polymer cap | 6 sets | fastener distributor / marketplace | PROVISIONAL |
| Lift lock | M8 adjustable clamping lever, female thread; DIN 2093 20x10.2x1.1 Belleville stack | 1 set | marketplace / industrial fasteners | SAMPLE |
| Lift assist | 150 N gas spring, nominal useful stroke about 80 mm, M6/M8 ball ends | 1 | marketplace | HOLD exact geometry |
| Lift pivots | shoulder bolts/pins + DIN 471/472 circlips + polymer thrust washers | set | fastener/bearing distributor | PROVISIONAL |
| Tether connector | WEIPU SP21 12-contact sealed pair; current per contact and creepage to be verified against tether HV | 1 pair | ChipDip | ELECTRICAL HOLD |
| Reel bearings | 61804/6203/16006/61904 classes, sealed where appropriate | set | bearing distributor | SAMPLE |
| Reel rotary transfer | 12-circuit slip ring, voltage/current derated and hipot-tested | 1 | marketplace / industrial slip-ring supplier | HOLD exact article |

ChipDip listings are availability leads, not automatic design approval. In particular, an IP68 label does not by itself prove submerged pressure capability, tether high-voltage creepage, mating-cycle life or strain-relief strength.

## Custom mechanical parts retained

| Part | Rev.PS redesign rule | Preferred process/material |
|---|---|---|
| Main pressure body | single dry central body with rear motor extension; X250 driven station | CNC, Al 6082-T6, hard anodise after validation |
| Side covers | removable, flat service gasket/O-ring path, all five Z50 gears accessible | CNC, Al 6082-T6 |
| Axle seal carriers | identical at six wheels; sized around 61903 and QRAR04116 interface | CNC, Al 6082-T6 or stainless wear insert |
| Wheel shafts | common Ø17 bearing/drive seat, 5x5 key, internal M8 retention only after fatigue proof | 17-4PH/420 stainless, ground journals |
| Wheel cores | Ø90 family, keyed replaceable hub, replaceable wet-traction tyre | CNC aluminium core + cast/replaceable PU tread |
| Lift arms/bosses | external paired parallelogram, local body bosses, mechanical stops | CNC/waterjet 6082-T6 + stainless pins |
| Camera yoke/housing | serviceable two-axis CAM026-like form with standard bearings/seals | CNC aluminium/stainless |
| Reel frame/drum | manual open frame, brake, level wind, meter wheel | laser-cut/bent aluminium/stainless + standard bearings |

## Wheel quick-change interface

- wheel bore: Ø17 H7 candidate, keyed 5x5;
- shaft shoulder carries radial/axial wheel load, not the screw shank;
- central M8 screw supplies axial retention only;
- retaining disk diameter at least 24 mm candidate;
- wedge-lock pair or mechanically captive locking method;
- tool access from outside with one hex key;
- snap-on protective cap keeps grit away from the socket;
- no proprietary cam profile.

Before release, prove the tapped shaft section against bending/fatigue. If margin is inadequate, retain the same one-tool service operation with an external M8 thread and prevailing-torque nut under the cap.

## Prototype buying sequence

1. Buy one motor of each viable family, one matched bevel pair, two Z50 gears, bearing/seal samples and one lift spring.
2. Measure actual shafts, bolt patterns, gear bores/hubs, seal hardness and spring extended/compressed lengths.
3. Build one complete left X250 side drive and test dry torque, stall, backlash and cover access.
4. Perform submerged dynamic seal test and housing proof test.
5. Run DN150 LOW/MID/HIGH lift/camera sweep with real wheels and tether tail.
6. Only then duplicate the right side and buy production quantities.

## Explicit non-release items

- exact marketplace motor seller/article;
- exact Z16/Z40 bevel set;
- exact 150 N gas-spring article;
- wheel tread compound and mould;
- connector voltage/submersion qualification;
- slip-ring article;
- all pressure-rated fits, O-ring grooves and proof pressure.

