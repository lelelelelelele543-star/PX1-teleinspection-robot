# Verification register

Revision 0.1, 2026-08-31.

| ID | Item | Current conclusion | Evidence state | Next proof action |
|---|---|---|---|---|
| CRP-DRV-001 | Motor count and assignment | Two motors total, one per crawler side | CONFIRMED-DRAWING + CONFIRMED-PHOTO | Close after full assembly cross-section check |
| CRP-DRV-002 | FAULHABER gear ratio | Original observed gearhead marked 66:1 | CONFIRMED-PHOTO | Identify the attached motor and measure free speed/current |
| CRP-DRV-003 | Bevel pair | Z16 drives Z40, module 1.0, reduction 2.5:1 | CONFIRMED-DRAWING + RECONSTRUCTED scale | Verify face width, pressure angle, mounting distance and backlash |
| CRP-DRV-004 | Side gears | Five Z50 m1 B4 gears per side; 50 mm adjacent centers, 100 mm wheel spacing, 200 mm wheelbase | CONFIRMED-DRAWING + RECONSTRUCTED scale | Confirm with one physical center measurement |
| CRP-DRV-005 | Driven side station | Rear wheel long axle FSS-002-064 is the input; no fourth side input shaft | CONFIRMED-DRAWING | Confirm axial coupling stack with physical assembly |
| CRP-DRV-006 | Body seal | 18x30x7 dynamic shaft seal, two per crawler | CONFIRMED-DRAWING | Verify orientation, material and pressure direction |
| CRP-DRV-007 | Motor-unit bearing | 61801-2RS, 12x21x5, two per crawler | CONFIRMED-DRAWING | Verify fit class and retention |
| CRP-DRV-008 | Body bearing | 61800-2RS, 10x19x5, two per crawler | CONFIRMED-DRAWING | Verify fit class and axial retention |
| CRP-DRV-009 | Replacement motor | JGB37-520 24 V family is a packaging/performance candidate | PROVISIONAL | Purchase exact ratio, bench test and design adapter only after measurements |
| CRP-CAD-001 | Current STEP reconstruction | Suitable as engineering hypothesis, not a manufacturing master | PROVISIONAL | Compare every interface with confirmed source dimensions |
| CRP-CAD-002 | RevGK/RevGN drive skeleton | Contains module 1.25 gears, center-wheel input and 170x1.5 side O-ring; conflicts with source | REJECTED-ARCHITECTURE | Rebuild with m1 gears, rear input and 190x1.5 O-ring |

## Promotion rule

A part or dimension may be released for machining only when:

1. its source and evidence state are recorded;
2. mating dimensions form a closed tolerance chain;
3. standard components have exact catalogue identities;
4. seals have verified shaft, gland, finish and pressure orientation;
5. the assembly has been checked for tool access and service removal;
6. any reconstructed geometry has been validated against the physical CRP-150/X200 part or a readable factory dimension.
