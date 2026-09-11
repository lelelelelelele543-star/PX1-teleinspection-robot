# PX-1 Rev.B — WB05 sealed tail connector / tether strain relief

Date: 2026-09-11
Status: PACKAGING PASS / SEAL-ELECTRICAL QUALIFICATION HOLD

## 1. Scope

Define the crawler-tail interface for the active six-core reinforced tether without changing the frozen tether architecture.

Required order remains:

`outer jacket support -> aramid/Kevlar structural termination -> relaxed copper service loop -> sealed six-contact electrical interface -> dry P0 wiring`

The electrical contacts are not recovery/towing members.

## 2. Proteus source comparison

### Crawler half — ASS-002-090
The controlled MiniCam source shows:
- one connector housing;
- six `EPIC H-D 1.6` contacts;
- six individual `1.5 x 1` O-rings;
- one additional housing O-ring 15 x 1;
- three small retaining screws.

### Cable half — ASS-002-364 / ASS-003-215
The source cable connector shows:
- six female `EPIC H-D 1.6` contacts;
- multiple static housing O-rings;
- connector nut / cable housing;
- separate cable gland;
- PU tube / hose crimp / adhesive-lined heatshrink in the complete cable-end assembly.

This is strong evidence for the system principle:
**six repairable crimp contacts + local contact seals + separately sealed connector shells + cable mechanical support before the contacts.**

PX-1 preserves that principle but does not copy the proprietary MiniCam metal/insulator dimensions.

## 3. Electrical allocation retained

Pin allocation is still the active Rev.PP tether allocation:

1. HV+ — 100-120 VDC system class
2. HV return — 100-120 VDC system class
3. RS485_A
4. RS485_B
5. VIDEO+
6. VIDEO-

No coax, no optical fibre and no bundle of separate patch/twisted-pair cables is introduced.

## 4. Contact system — modern purchasable continuation

LAPP still manufactures the `EPIC H-D 1.6` contact family used by the original Proteus connector.

The standard H-D connector system using these contacts is published at:
- 250 V AC rms / DC according to IEC;
- 10 A according to IEC;
- conductor range to 2.5 mm² depending contact article.

That system rating is evidence that the contact family is electrically suitable for the PX-1 100-120 VDC class. **It does not automatically certify the custom PX-1 PEEK insert.** The custom connector must pass its own creepage, insulation and wet qualification.

### Preferred contact surface
Use gold-plated turned contacts for the wet-service detachable connector.

Baseline article for a measured 0.50 mm² core:
- crawler male: LAPP `13162600`, H-D SCEM AU 0.5;
- cable female: LAPP `13163600`, H-D BCEM AU 0.5.

If the selected tether conductor differs, use the same H-D 1.6 turned-contact mating family:
- 0.14-0.37 mm²: 13162500 / 13163500;
- 0.75-1.0 mm²: 13162700 / 13163700;
- 1.5 mm²: 13162800 / 13163800;
- 2.5 mm²: 13162900 / 13163900.

The final article is selected from the **measured conductor copper area and insulation diameter**, not guessed from cable outside diameter.

The source-library search did not produce a reliable original Proteus tether conductor cross-section. Therefore the mechanical connector can be frozen around H-D 1.6, but the crimp-barrel article stays procurement-HOLD until the actual 40 m tether sample is stripped and measured.

## 5. New PX-1 contact layout

MiniCam's proprietary insert pattern is not copied.

PX-1 uses a new six-contact circular pattern:
- contact-axis circle radius: 6.0 mm;
- six positions at 60 degree intervals;
- H-D mating metal diameter screened as 1.6 mm;
- adjacent contact center distance: 6.0 mm;
- adjacent metal-to-metal screen clearance: ~4.4 mm;
- HV+ and HV- placed opposite each other: 12.0 mm center distance;
- minimum contact-to-metal-shell distance through the Ø24 PEEK insert screen: ~5.2 mm.

Allocation around the circle:
- 0°: HV+;
- 60°: RS485_A;
- 120°: RS485_B;
- 180°: HV-;
- 240°: VIDEO-;
- 300°: VIDEO+.

Benefits:
- both differential pairs remain adjacent;
- the two HV contacts are maximally separated;
- connector remains symmetric and compact;
- a separate asymmetric mechanical key prevents rotational mis-mating.

## 6. Insulator

Project part: `PX1-451-6P-PEEK-INSERT`
Quantity: 2 per complete connector set (crawler + cable half).

Final material:
- machined PEEK engineering plastic;
- nominal insert envelope: Ø24 x 16 mm in the current CAD screen;
- six contact passages on R6 pattern;
- one asymmetric anti-rotation key/notch.

Prototype fit insert may be printed on the Anycubic Chiron from PETG/PA only for dimensional assembly tests. A printed insert is **not** accepted for the 120 V wet/pressure qualification.

Release requirements:
- actual LAPP contacts physically measured;
- contact-retention method defined;
- creepage/clearance checked from final passage geometry;
- insulation resistance and dielectric test on a machined insert;
- immersion test with connector mated and unmated crawler bulkhead sealed.

## 7. Individual contact seals

Source architecture uses six 1.5 x 1 O-rings around the crawler contacts.

Purchasable PX-1 candidate:
- Dichtomatik `67012207`;
- 1.5 x 1 mm;
- FKM 80 Shore A;
- quantity: 6 per crawler bulkhead plus test/spares.

This size is commercially stocked.

Important: the exact gland diameter/depth is **not released** from the source dimension alone. The modern contact samples must be measured at the intended seal land and a six-hole coupon pressure/immersion tested first.

## 8. Crawler bulkhead connector

Project part: `PX1-450-CRAWLER-6P-BULKHEAD`
Quantity: 1.

Material:
- 1.4404 / 316L stainless preferred for exposed mating/thread surfaces.

Current screening envelope:
- external flange OD: 48 mm;
- flange thickness: 4 mm;
- barrel OD: 32 mm;
- barrel length: 22 mm;
- mating nose OD: 24 mm;
- mating nose length: 10 mm;
- PEEK insert: Ø24 x 16 mm class.

Mounting:
- flange positively seats against the rear pressure wall;
- 4 x M4 A4 countersunk Torx screws on 38 mm PCD;
- screws provide clamp; connector pilot/register controls location;
- blind body threads only — no open screw passage from water into P0.

Purchasable screw candidate:
- ISO 14581, M4 x 12, A4-70, TX20;
- Czech supplier code `W14581-4-4X12`.

The current screen leaves ~2.55 mm solid land between the face-seal groove and M4 clearance hole and ~1.2 mm from the countersunk-head envelope to the flange edge. Final countersink depth is checked on the real screw before drawing release.

## 9. Bulkhead-to-body static seal

Selected commercial candidate:
- Dichtomatik FPM/FKM 80 Shore A;
- 25 x 1.5 mm;
- Czech article code `274457`, catalogue `OK.025,00/1,50 F80`;
- currently a normal stocked item.

Preliminary face groove:
- groove centerline diameter: 26.5 mm;
- depth: 1.15 mm;
- width: 2.00 mm;
- nominal squeeze: ~23.3%;
- nominal gland fill: ~76.8%.

Status: packaging geometry accepted, production groove HOLD until the selected Dichtomatik compound tolerances/handbook are checked and a groove coupon passes.

## 10. Mated connector shell seal

Selected commercial candidate:
- Dichtomatik FKM 80;
- 21 x 1.5 mm;
- current Dichtomatik article family `67013242` / successor family;
- quantity: 1 working + spares per plug.

Preliminary radial gland screen:
- groove bottom diameter: 22.0 mm;
- mating bore: 24.4 mm;
- O-ring ID stretch: ~4.76%;
- radial squeeze: ~20%;
- nominal gland fill: ~73.6%.

This is the primary wet seal between the cable plug and crawler connector shell. Individual contact O-rings remain a second sealing barrier for P0.

## 11. Cable plug / coupling

Project parts:
- `PX1-452-CABLE-PLUG-SHELL` — 316L;
- `PX1-453-CABLE-COUPLING-NUT` — 316L;
- `PX1-454-CABLE-KEY` — integrated mechanical anti-rotation feature.

Current envelope:
- plug-shell OD <=36 mm;
- current packaging length before cable gland: ~50 mm;
- keyed threaded coupling to crawler barrel;
- female H-D contacts on the cable side, matching the safer Proteus principle: the power-source cable end does not expose male live pins.

Final coupling-thread size, anti-loosening feature and exact key dimensions are HOLD until the connector mock-up is printed/machined and contaminated-thread service tests are performed.

Safety interlock rule:
- tether HV is disabled and discharged before connector separation;
- an unplugged crawler has no source of tether HV at its exposed male contacts;
- an unplugged cable end must never be energized by the CCU.

## 12. Jacket seal / bend support

Commercial part selected for the target 6.5-7 mm tether OD class:
- manufacturer: LAPP;
- part: `SKINTOP MS-M 16X1.5`;
- article: `53112010`;
- thread: M16 x 1.5;
- cable clamping range: 4.5...10 mm;
- wrench size: 20 mm;
- published IP68 / IP69 class; current LAPP data sheet lists IP68 up to 10 bar for 30 min;
- nominal body envelope in the WB05 screen: ~Ø22 x 31 mm class.

Installation:
- screws into the rear of PX1-452;
- seals/supports the **outer cable jacket** and provides bend relief.

Critical rule:
**the SKINTOP gland is not the crawler recovery/towing anchor.**

## 13. Aramid/Kevlar load termination

Project structural parts:
- `PX1-455-ARAMID-CAPSTAN-PIN`, Ø8 mm A4/316L class;
- `PX1-456-ARAMID-TAIL-CLAMP`;
- clamp fasteners: 2 x M3 A4 candidate.

Concept:
1. outer jacket is supported by the M16 gland;
2. aramid strength member is separated from the copper cores inside the plug shell;
3. aramid makes approximately three smooth wraps around the rounded Ø8 capstan pin;
4. the unloaded tail is retained by the clamp plate;
5. the six copper cores form a relaxed service loop before the female crimp contacts.

Hardware-only screening load: 1.0 kN.
At 1 kN the Ø8 pin double-shear screen is only ~9.95 MPa.

This 1 kN number is **not the released tether working load**. Final allowable pull is limited by the selected inspection cable manufacturer data and the physical clamp-slip test.

Acceptance sequence:
- test aramid termination alone with sacrificial cable sample;
- no copper conductor connected during first pull test;
- measure slip at 100/250/500 N and then to the permitted proof load;
- after proof, dissect the cable and inspect aramid fibre damage;
- repeat after wet/dirty cycling.

## 14. Pressure consequence

The connector opening is small relative to the rear wall.

At a 24 mm pressure opening:
- +0.30 bar gauge -> ~13.6 N outward pressure force;
- +0.60 bar proof screen -> ~27.1 N.

The mechanical tether load is therefore much more important to the bulkhead fasteners than pressure thrust.

The structural connector flange is screened around a 1 kN cable-hardware load:
- four screws -> ~250 N nominal per screw before uneven-load factors.

Final rear-wall boss/thread pull-out and flange FEA remain mandatory; the current values are not a substitute for the pressure/tether proof test.

## 15. DN150 / packaging result

Executable CAD:
`mechanical/cadquery/PX1_TailConnector_RevB.py`

Validation:
`mechanical/REV_B_WB05_VALIDATION.json`

Result: `PASS_SCREEN`.

Current result:
- bulkhead flange, barrel, connector nose, cable-plug envelope and M16 gland remain fully inside the ideal DN150 cylinder;
- minimum adjacent contact metal clearance screen: ~4.4 mm;
- HV pin separation: 12 mm center-to-center;
- contact-to-shell insulation screen: ~5.2 mm;
- no need to enlarge the crawler transverse envelope for the tail connector.

The connector increases axial tail length. A complete bend/elbow sweep with the cable boot remains a separate release gate.

## 16. Field retermination sequence

The design is intentionally repairable:
1. HV OFF and verify discharge;
2. unscrew connector coupling;
3. remove M16 gland nut and withdraw cable-end shell;
4. cut damaged tether back to sound jacket;
5. strip outer jacket to the specified service length;
6. separate aramid from the six copper cores;
7. terminate aramid on the capstan/clamp first;
8. leave relaxed conductor loop;
9. crimp six female H-D contacts with the correct LAPP tooling/contact article for measured conductor size;
10. insert contacts according to the keyed pin map;
11. inspect/grease approved O-rings;
12. close plug, perform continuity/insulation test;
13. low-voltage communication test;
14. only then permit HV qualification.

## 17. Errors/corrections recorded

1. A normal cable gland alone is **not** an acceptable tether tensile termination. It is retained only for jacket sealing and bend support.
2. H-D 1.6 contact-family voltage/current ratings cannot be transferred automatically to our custom PEEK insert. The custom insert needs its own dielectric/wet test.
3. Original Proteus contact seal dimensions are source evidence, not an automatic machining drawing. Contact samples are required before gland release.
4. The present Library does not provide a trustworthy conductor cross-section for the original six-core Proteus tether. Therefore exact H-D crimp-barrel article remains tied to physical cable measurement.
5. Motor-service access and tail-connector service are separate problems. WB05 does not pretend the small connector opening is a motor extraction opening.

## 18. WB05 closure gates

Before drawing release:
1. strip and measure the actual initial 40 m six-core tether: OD, six conductor copper areas, insulation diameters, aramid construction;
2. buy sample H-D male/female contacts and verify geometry/crimp/removal tooling;
3. machine one PEEK insert and one six-hole seal coupon;
4. leak/immersion test contact seals;
5. dielectric/insulation test connector standalone at a voltage margin above the released 120 VDC line;
6. build the M16 jacket seal + aramid capstan prototype and pull-test it independently of contacts;
7. contaminate with water/mud, cycle connection/retermination, repeat insulation test;
8. freeze final coupling thread/key/anti-loosening;
9. merge the exact tail into the Rev.B full crawler and run physical DN150/elbow deployment test.

## Change log

### 2026-09-11 — WB05
- recovered the original six-contact Proteus connector architecture from ASS-002-090/364/003-215;
- confirmed modern LAPP EPIC H-D 1.6 contacts remain commercially available;
- created a new PX-1 six-pin pattern instead of copying proprietary insert geometry;
- selected real FKM O-rings for body and mating-shell seals;
- selected the LAPP M16 metal gland for the 6.5-7 mm cable class;
- separated aramid recovery load from the electrical contacts;
- added a 1 kN structural-hardware screen without claiming a cable working load;
- achieved DN150 `PASS_SCREEN` for all tail hard envelopes;
- retained conductor size, contact gland, dielectric qualification and actual tether pull capacity as release HOLD items.
