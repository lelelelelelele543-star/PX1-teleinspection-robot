# PX-1 — Rev.A engineering audit

Date: 2026-09-11
Status: CONTROLLED AUDIT / NO ARCHITECTURE CHANGE

## 0. Revision-control rule

This document introduces the user-requested top-level release stages without deleting the repository's historical engineering revision labels.

- **Rev.A** = current audited prototype design basis. The active controlled repository documents remain `PROJECT_STATUS_RevPO.md`, `PROJECT_SUPERSESSION_RevPP.md`, `PROJECT_STATUS_RevPR.md` and their controlled subsystem notes.
- **Rev.B** = corrected prototype after the mechanical/procurement/clearance gates in this audit are closed.
- **Rev.C** = manufacturing-release candidate after first-article build, pressure/immersion tests, service-cycle tests and complete drawing/BOM freeze.

Historical Rev.* files remain evidence and calculation records. They do not override the active master documents.

## 1. Frozen constraints checked

PX-1 shall retain unless an explicit change request is approved:
- Proteus-derived serviceable mechanical architecture;
- no coaxial conductor in the main tether;
- no cartridge/cassette mechanical modules;
- no external hinge penetrating the dry pressure volume;
- dry pressurized crawler volume with dynamic shaft seals and replaceable static seals;
- gear drive, no belt traction drive;
- commercially obtainable/service-replaceable prototype electronics and motors;
- CAD must include tolerances, seals and service access before release.

## 2. Active crawler architecture

The current controlled GitHub baseline is the six-wheel CRP-150-derived crawler:
- three wheel stations per side;
- five equal Z50, module-1 side gears per side;
- X50 front wheel, X100 idler, X150 centre wheel, X200 idler, X250 rear wheel/input;
- 100 mm wheel pitch, 200 mm front-to-rear wheelbase;
- two traction motors total, one per side;
- rear X250 long axle is the side-drive input;
- Z16 -> Z40 bevel reduction, 2.5:1.

Any older 4WD/independent-wheel or centre-input study is historical unless the user explicitly issues a new architecture change request. Do not silently mix it into the active master.

## 3. Source identity correction

Files `ASS-002-885`, `ASS-002-886`, `ASS-002-887`, `ASS-002-889` and `ASS-003-121` currently available in the Library are marked **CRP300**, not CRP-150.

Decision:
- use them only as secondary evidence for MiniCam service philosophy, sealing, bearing/flange arrangement and lift construction;
- do **not** copy their Z80 gears, bearing sizes, seal sizes or housing dimensions into PX-1 as CRP-150 dimensions;
- CRP-150-specific geometry must come from the controlled CRP-150 reference set (`DRW-002-374`, `DRW-002-375`, `DRW-002-386`, source register) or physical measurement.

This corrects an earlier project tendency to treat some CRP300 assembly sheets as direct CRP150 dimensional evidence.

## 4. DN150 clearance status — important correction

`PX1_CRP150_Master_RevPR.py` validates the **pressure body** against the ideal DN150 cylinder, but it intentionally does not use the simple Ø90 cylindrical wheel placeholders as the final wheel-clearance proof.

Therefore the repository statement `body outside ideal DN150 = 0` must not be interpreted as a complete crawler DN150 PASS.

The Rev.GF tapered/dished Ø90-class wheel profile is the current clearance candidate. Its documented minimum analytical ideal-DN150 margin is only about **0.12 mm**. This is near-contact geometry and provides no real allowance for pipe ovality, welds, scale, debris, tread manufacturing tolerance or elastic growth.

Rev.A disposition: **HOLD — full crawler DN150 fit is not manufacturing-released.**

Rev.B gate:
1. integrate the real tapered wheel solid into the active X250 master;
2. include all screw heads, axle flanges, cover edges and folded camera/lift solids;
3. run full static and swept ideal-DN150 CAD check;
4. define a practical clearance allowance rather than relying on 0.12 mm nominal analytical margin;
5. perform a physical DN150 tube sweep with the real tread compound.

## 5. Side-drive / wheel-station sealing

Preserve the CRP-150-derived service principle:
- removable side cover;
- removable axle flange at each wheel station;
- outboard 61903-2RS-class wheel-load bearing;
- dynamic X-ring architecture on a dedicated polished shaft land;
- static axle-flange O-ring;
- static perimeter side-cover O-ring;
- wheel torque transmitted by a key/positive drive, not by the retaining screw;
- no keyway/thread/circlip groove through the dynamic seal track.

Current PX-1 candidate values remain prototype data, not production dimensions:
- X-ring: 18.72 x 2.62, FKM preferred;
- seal land: approximately Ø19 mm, Ra <= 0.4 um target;
- axle-flange O-ring class: 32 x 1.5;
- side-cover O-ring class: 190 x 1.5;
- normal positive pressure study: approximately +0.20...+0.30 bar gauge.

Positive pressure is only an additional barrier and never substitutes for the dynamic/static seals.

### Bearing-stack HOLD
Historical PX-1 notes contain different interpretations of the exact 61801 distribution around the wheel stations. Do not release the shaft/flange machining chain solely from a historical note. Before Rev.B, reconcile the active X250 long-axle stack directly against the CRP-150 source drawing and selected physical bearings, then freeze fits and shoulders from actual manufacturer tolerances.

## 6. Bevel gear correction

CRP-150 evidence supports:
- Z16 / Z40;
- 90-degree straight-bevel pair;
- ratio 2.5:1;
- module approximately 1.0 from the calibrated source geometry.

The `BEVEL_MODULE_SCREEN = 1.25` value in the active Rev.PR CadQuery model is explicitly a collision/screening envelope only. It must never appear on a machining drawing or purchase specification as the released module.

Rev.B gate:
- select one reproducible, commercially obtainable Z16/Z40-compatible bevel solution or freeze a machinable gear specification;
- confirm module, pressure angle/tooth system, face width, mounting distance, backlash and bore/retention;
- retain separate bearing support for the Z16 input shaft so motor/gearhead bearings do not carry bevel-mesh radial load alone.

## 7. Traction motor procurement gate

Do not freeze JGB37-520 as the primary crawler traction motor merely because it is inexpensive and available.

Current required motor envelope:
- 24 V nominal;
- geared output approximately 45-65 rpm class;
- documented/verified rated output torque >= 1.0 N.m, >= 1.3 N.m preferred;
- preferred body <= Ø35 mm;
- preferred overall length <= 100 mm;
- shaft interface compatible with a separately supported Z16 shaft;
- two identical realistically obtainable units.

The ISL PGM-32P / MOT-IG32PGM 100 family remains a performance/dimensional reference, not yet the released purchased part.

No final motor holder, coupler, hole PCD or shaft bore may be released until the exact purchased motor or manufacturer-controlled drawing is available.

## 8. Camera lift and wet deck

Retain:
- manual lift;
- integrated body mounting, no external pressure-penetrating hinge;
- 150 N gas-spring class as the current balance reference;
- open wet deck in front of the folded camera;
- sealed structural pressure roof under the wet deck;
- useful forward picture in LOW position;
- drainage without a cup/pocket under the camera.

The old geometry where an upper `nose` subtraction opened the pressure cavity is rejected. Rev.B must retain the later sealed wet-deck architecture and rerun LOW/MID/HIGH lift sweep on the corrected X250 master.

## 9. Rev.A errors formally recorded

1. Some CRP300 assembly drawings were previously at risk of being interpreted as direct CRP150 dimensional evidence. Corrected: secondary-reference only.
2. `Rev.PR PASS` can be misread as complete DN150 crawler clearance. Corrected: it proves the body screen and packaging checks, not the final wheels/lift/camera in a real DN150 tube.
3. Module-1.25 bevel geometry exists in historical/current screening CAD. Corrected: packaging-only; source-correct design direction is module-1-class until exact gear geometry is frozen.
4. A motor envelope is not a motor selection. Corrected: exact traction motor remains a procurement/test gate.
5. Historical bearing-stack notes are not sufficient to release the X250 axle. Corrected: direct source reconciliation + purchased-bearing tolerances are mandatory.

## 10. Rev.B work order

Priority order:
1. rebuild/freeze the complete X250 driven rear-wheel station including shaft, bearing stack, dynamic seal, static flange seal, Z50 gear and Z40 handoff;
2. integrate the detailed tapered wheel profile into the active master and rerun full DN150 checks;
3. select and source the exact traction motor;
4. select/freeze the exact Z16/Z40 bevel solution;
5. reconcile all seal glands against exact selected FKM supplier data;
6. run complete LOW/MID/HIGH camera-lift collision/visibility/drainage sweep;
7. pressure/structural check the rear extension, axle flange zones, side cover, scuppers and lift bosses;
8. build and bench-test one complete side drive before duplicating the opposite side.

## 11. Rev.C release conditions

Rev.C is prohibited until all of the following are closed:
- exact purchasable BOM with manufacturer part number/source/quantity/dimensions;
- first-article dimensional inspection;
- shaft-seal submerged rotating test;
- pressure leak-decay/proof test;
- side-cover/flange service-cycle test;
- motor current/thermal/stall-current characterization;
- full physical DN150 fit/sweep;
- drawing tolerances, surface finishes, seal glands and assembly/service sequence frozen;
- only validated files promoted to the repository `release/` area.

## Change log

### 2026-09-11 — Rev.A audit
- no active architecture changed;
- established Rev.A -> Rev.B -> Rev.C top-level release control;
- corrected CRP300/CRP150 evidence classification;
- downgraded full-crawler DN150 status from implied PASS to HOLD pending complete solid/physical sweep;
- protected module-1.25 bevel screening geometry from accidental manufacturing use;
- retained traction motor as procurement gate;
- placed X250 detailed bearing/seal stack under direct-source verification before machining release.
