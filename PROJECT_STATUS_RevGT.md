# PX-1 Rev.GT — common drivetrain dynamic-seal baseline

Status: CAD-VALIDATED PROTOTYPE BASELINE; not machining release.

## Major decision
All eight drivetrain dynamic seal locations are standardized around one rotary/internal Quad-Ring geometry:
- 6 wheel shafts;
- 2 X200 input shafts.

Active prototype seal size:
- Trelleborg Quad-Ring family `QRAR04116`;
- 18.72 x 2.62 mm;
- common dynamic shaft land **Ø18 mm**;
- rotary table geometry: d5 18 f7, d6 22.8 H8, b1 2.8+0.2, r1 0.30 mm, radial gap screening max 0.08 mm;
- first material candidate: V7002 FKM 70; N7004 NBR retained as comparison/test fallback.

## Superseded concepts
- X200 `18x30x7` directional lip seal is no longer the active PX-1 design, although it remains documented as part of the CRP150 source architecture.
- wheel dynamic land Ø19 is superseded by Ø18 so the exact current rotary gland table can be used rather than stretching the source-inspired geometry.
- the earlier 17.13x2.62 X-ring idea for an Ø18 rotating shaft is rejected; the natural-ID relationship is wrong for the preferred rotary/internal installation approach.

## CAD validation
`mechanical/cadquery/PX1_Dynamic_Seals_RevGT.py` executes successfully under CadQuery 2.8.0.

PASS results:
- all local solids valid;
- X200 Quad-Ring housing remains inside the previous Ø30 x 7 seal envelope;
- X200 groove Y36.6...39.4 leaves ~2.1 mm axial shoulder on both sides;
- X200 groove retains ~2.6 mm axial separation to the side Z50 at Y42.0;
- zero X200 seal-housing/Z50 collision;
- wheel Ø18 seal land Y58.35...62.15 gives 3.8 mm total axial land;
- wheel groove Y58.85...61.65 leaves 0.50 mm shoulder on both sides;
- Ø17 keyed wheel seat begins exactly at Y62.15;
- radial ligament between dynamic groove-root Ø22.8 and the nominal Ø32 static flange O-ring ID is ~4.6 mm;
- surface speed at 21.6 rpm / Ø18 is only ~0.0204 m/s;
- external wheel/cover/DN150 envelope is unchanged.

## Bearing prototype baseline
Preferred first-article samples are now documented in `bom/REV_GT_BEARING_SEAL_SELECTION.md`:
- JTEKT/Koyo 6701 2RS, 12x18x4, inner wheel support;
- SKF W 61801-2RS1 stainless preferred, 12x21x5, wheel-flange intermediate support;
- SKF W 61903-2RS1 stainless preferred, 17x30x7, wheel main outboard support;
- SKF W 61800-2RS1 stainless preferred, 10x19x5, two per X200 side shaft.

Standard bearing-steel equivalents remain dry-zone prototype fallbacks if stainless supply is poor.

## Fits remain measurement gates
Rev.GT deliberately does not freeze a universal h6/H7 bearing-fit rule. Rotating-inner-ring load, exact manufacturer guidance, internal clearance and thin-section sensitivity all matter.

Final fits are frozen only after:
1. exact samples are purchased;
2. actual dimensions/internal-clearance code are recorded;
3. one WS-01 shaft/flange is machined;
4. installed running torque/endplay/temperature are measured.

## Source alignment
The uploaded CRP150 side-drive drawing confirms the proven architectural use of:
- 61801 12x21x5;
- 61903 17x30x7;
- 18.72x2.62 X-Ring;
- 32x1.5 axle-flange O-ring;
- 190x1.5 side-cover O-ring;
- keyed wheel shafts.

PX-1 keeps that architecture reference but uses its own modernized Ø18 rotary gland and current bearing packaging.

## Next autonomous block — Rev.GU
- freeze the **static** axle-flange 32x1.5 and side-cover 190x1.5 gland geometry from current supplier tables;
- CAD-check groove land against the Rev.GT dynamic groove, flange screws and side-cover perimeter;
- select prototype material strategy for static seals;
- update WS-01 inspection fields for the new Ø18 common dynamic gland;
- then return to complete full-crawler Rev.GL collision/DN150 rerun with the internal Rev.GT changes included.
