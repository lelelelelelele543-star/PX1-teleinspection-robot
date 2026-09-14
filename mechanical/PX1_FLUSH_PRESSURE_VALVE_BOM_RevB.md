# PX-1 WB24A flush PRESSURE valve — prototype BOM

Date: 2026-09-14
Status: **PROTOTYPE BOM / MACHINING + LEAK QUALIFICATION HOLD**

This BOM is for the small low-profile pressure/fill valve inside the WB23E removable service cover.

## Source-derived items and PX-1 equivalents

| Qty | Function | MiniCam source evidence | PX-1 prototype candidate | State |
|---:|---|---|---|---|
| 1 | Protection/service cap | FSS-001-844 CAMERA VALVE COVER | PX1 machined low-profile cap, M8x1 candidate, OD <=12 mm, exposed height <=1.5 mm target | DRAWING HOLD |
| 1 | Guided push shaft | FSS-001-843 CAMERA VALVE SHAFT | 316L turned shaft, ~3 mm class; exact grooves/stroke from bench prototype | DRAWING HOLD |
| 1 | Check ball | BEA-001-845 4MM BALL BEARING | 4.0 mm AISI 316 precision ball, Grade 100 class candidate | SAMPLE |
| 2 | Small seals | SEA-001-846 3 x 1 O-RING | FKM/FPM 3 x 1 mm, 70–75 Shore A initial prototype | SAMPLE |
| 1 | Source outer/secondary seal reference | SEA-001-848 6 x 1.5 O-RING | FKM/FPM 6 x 1.5 mm if retained by final insert geometry | GEOMETRY HOLD |
| 1 | Valve spring | SPR-001-847 | stainless compression spring, wire 0.5 / OD 3.7 / free L 7.9 mm | SAMPLE |
| 1 | Lower spring/flow retainer | source assembly-specific | PX1 316L perforated retainer/plug | DRAWING HOLD |
| 1 | Seat | source detail not controlled | replaceable FKM soft seat around gas orifice, geometry from leak bench | TEST HOLD |
| 1 | Fill/purge adapter | official Proteus service method uses screw-on adaptor | PX1 M8x1 screw-on service adapter with mechanical opening probe and purge screw | TOOL PROTOTYPE |

## Commercial evidence for prototype parts

### Spring

MiniCam source BOM gives `SPR-001-847` geometry `d0.5 / De3.7 / L0 7.9 mm`.

That exact geometry exists as a standard spring rather than requiring a custom winding. Examples found during the current availability check:

- Febrotec `0X-DF1333` / `D11160` class, OD 3.7 mm, wire 0.5 mm, free length 7.9 mm;
- STAMO `VI4835`, DIN 2098/2098R, stainless steel, 0.5 x 3.7 x 7.9 mm.

Important: these examples prove that the geometry is standard. The project's allowed procurement-source rule still applies; locate the same DIN geometry on an approved marketplace/source before final BOM release if these suppliers are not approved for the build.

Do not freeze the spring rate merely from geometry. Current standard examples around this geometry are quite stiff, so the actual valve opening stroke/preload is set on the bench with the screw-on adaptor mechanically opening the valve.

### 3 x 1 FKM O-rings

Standard FKM/FPM/Viton 3 x 1 mm rings are widely catalogued at 70–80 Shore A. Start with 75 Shore A for dry/wet leak experiments and compare 70 Shore A only if seat friction/sealing requires it.

### 6 x 1.5 FKM O-ring

Standard FKM 6 x 1.5 mm exists as a normal metric size. It is retained only if the final PX1 insert geometry benefits from this source-like secondary/static seal; do not force the source size into a different PX1 gland.

### 4 mm ball

AISI 316 4 mm Grade-100 loose balls are commercially available. AISI 316 is preferred for the first wastewater-corrosion sample; hardened 440 stainless can be A/B tested if seat wear or dimensional finish is better, but 440 corrosion performance must be checked in the actual environment.

## Material / manufacturing candidates

### Shaft and retainer

- 316L stainless first choice;
- polish the O-ring-running area after turning;
- no sharp groove edges on dynamic seals;
- final surface finish and O-ring gland proportions come from the actual selected ring datasheet/ISO 3601 practice, not from guessed CAD.

### Protection cap

Two candidates:

1. 316L stainless — robust, compact, but protect aluminium threads from galling;
2. hard-anodized 6082 aluminium — low galvanic mismatch/weight, but inspect thread wear.

The cap is not allowed to become the primary pressure seal. Valve must pass pressure decay **with cap removed**.

### Seat

Prototype A uses a replaceable FKM soft seat so minor contamination does not rely on perfect metal-to-metal contact. If repeated-cycle testing shows the soft seat extrudes/wears, compare a precision conical metal seat with the same 4 mm ball.

## Quantity for first bench build

Make/buy enough for at least three complete insert sets:

- Set A1: guided-shaft / FKM seat;
- Set A2: duplicate guided-shaft build for repeatability;
- Set B1: simplified ball-check without guided shaft seals.

Recommended consumables for testing:

- >=20 x 3 x 1 FKM rings;
- >=10 x 6 x 1.5 FKM rings if retained;
- >=10 x 4 mm balls;
- >=10 x springs of the selected geometry.

This allows deliberate contamination, damage and repeated rebuilds without treating one successful assembly as proof.

## Release gates

Do not move these parts to production BOM until:

- real dimensions are recorded;
- opening stroke is repeatable;
- primary valve holds +0.25 bar for the qualified decay interval with protection cap removed;
- submerged bubble test passes;
- adaptor mate/unmate >=100 cycles passes;
- grit/dirty-water mouth contamination test passes;
- purge operation reduces crawler pressure to ambient reliably;
- WB24A final cap/adapter/seat drawing is released.
