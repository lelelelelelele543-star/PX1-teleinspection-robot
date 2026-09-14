# PX1 Manufacturing / Assembly / Test - Current

## A. What may be purchased now

Purchase without waiting for unresolved custom dimensions: 61903-2RS (6 + spares), 61801-2RS (14 + spares: 12 side-drive + 2 Z16), 61800-2RS (2 + spares), X-ring 18.72x2.62 samples, 18x30x7 shaft-seal samples, NBK MLR-20C-6-6 (2 + spare), LAPP 53112000 glands, NUCLEO-F446RE, Cincon CQB150W-110S24, Nichicon UCS2D221MHD1TN, Delta TR-1D*P2 and the Molex six-way connector family.

Buy as physical samples before custom metal release: one QRW90SR/150 or original Proteus 90 mm wheel, three ISL PGM-32P-24-100-60-02 motors, two exact BTS7960 modules + spare, one Z16/Z40 matched prototype pair, one ACE GS-12-20-V4A-class 150 N spring with chosen end fittings, the exact WEIPU SP13 pair, local six-core cable samples, rear six-core tether/connector samples, and the pressure-sensor module once selected.

## B. Metalwork list

**HOLD - do not final-machine until the listed measurement gate closes:**
- main pressure body and side-cover interfaces;
- left/right side covers;
- 4 short wheel axles + 2 rear long axles;
- 6 axle flanges;
- 2 Z40 shafts;
- 2 supported Z16 shafts;
- motor holder;
- lift arms/holding plates/pivots;
- camera carrier/housing sealing details;
- PRESSURE/LIFT cover final seal groove;
- rear tether housing/nut/strain relief.

The release package folder `STEP_MACHINING_REFERENCE/` contains HOLD-tagged reference solids only. Their purpose is setup/fit discussion, not an authorization to cut final parts.

### Pre-release fit targets (PX1 engineering targets, not recovered MiniCam dimensions)
- 61903 shaft journal: nominal 17 mm; rotating inner-ring fit target k6, housing target H7.
- 61801 shaft journal: nominal 12 mm; rotating inner-ring fit target k6, housing target H7.
- 61800 Z40 journal: nominal 10 mm; rotating inner-ring fit target k6, housing target H7.
- 18x30x7 seal shaft land: nominal 18 mm; final tolerance/roughness follows the purchased seal datasheet; target polished, no lead/spiral tool marks.
- X-ring running land/groove: final groove and surface finish must follow the selected X-ring supplier data; source size alone is not enough to machine the groove.

## C. 3D-print list - Anycubic Chiron

Current STL files are **fit-check prototypes**, not wet-pressure production parts:
- `STL_PRINT/PX1_Lift_Harness_Guard_PROTOTYPE.stl`;
- `STL_PRINT/PX1_PRESSURE_LIFT_Cover_FitMockup.stl`;
- `STL_PRINT/PX1_Tether_StrainRelief_Mockup_HOLD_OD.stl`.

Print the mockups in PETG/ASA for dry fit only. Do not use printed cover/strain-relief mockups as final pressure boundaries.

## D. Assembly sequence

1. Deburr/clean metal parts; inspect bearing and seal seats.
2. Assemble each side-drive dry on bench: two 61801 per wheel station according to the finally measured axial stack, Z50 train, keys, outer 61903, flange/static seal and X-ring. Set end-float only after the source stack is closed.
3. Install rear long axles and align each X250 Z50 with its transverse Z40 path.
4. Install 61800, 18x30x7 body seals, Z40 shafts/gears.
5. Build both supported Z16 input units with 61801 bearings, matched Z16/Z40 pair and measured backlash/mounting distance.
6. Couple each PGM-32P motor through the NBK coupling; verify free rotation before power.
7. Install the dry electronics and secure all wiring away from rotating parts; keep the pressure-sensor reserved position until its exact article is fitted.
8. Install PRESSURE/LIFT cover, valve and LAPP gland with the final seal/groove.
9. Assemble manual lift, gas spring and camera carrier. Route exactly six camera conductors under the removable guard; connect the six-way camera connector.
10. Install rear tether connector and terminate the aramid/Kevlar strength path mechanically before the electrical cores.
11. Close the body, apply controlled positive pressure and perform leak testing before any wet powered run.
12. Fit wheels last after axle end-float and retention are confirmed.

## E. Test sequence

1. **Static mechanical:** free rotation of each wheel/gear train, no binding, measured backlash, wheel-retention torque witness.
2. **24 V bench:** current-limited supply, one motor at a time, direction check, current logging, stall/jam cut-off calibration.
3. **Electronics:** RS-485 watchdog, loss-of-command stop, voltage rails, thermal soak, pressure telemetry.
4. **Camera branch:** local six-core power/UART/CVBS continuity, lift sweep, cable bend and connector removal/refit.
5. **Pressure dry:** +0.25 bar(g), stabilization, timed decay recording.
6. **Pressure wet:** submerged unpowered bubble test; then low-voltage wet test after dry acceptance.
7. **DN150 fixture:** full crawler through rigid DN150 gauge/pipe with the **real measured wheel solid**, lift LOW and service hardware installed.
8. **40 m tether:** motor load + RS-485 + CVBS simultaneously; record crawler 24 V, current, video noise and faults.
9. **Dirty/wet run:** traction, reversing, obstruction/jam recovery, repeated camera removal and wheel service.
10. Only after 40 m acceptance, repeat voltage/video calculations and test with 100-150 m equivalent.

## F. Physical closures still required

1. ТРЕБУЕТСЯ ЗАМЕР: exact QRW90SR/150 wheel width, tread/profile and hub/recess dimensions; current wheel is a HOLD proxy and DN150 wheel clearance is NOT released.
2. ТРЕБУЕТСЯ ЗАМЕР/чертеж: axial order and Y shoulder dimensions of the six 61801 bearings per side-drive; quantity 6/side is source-confirmed.
3. ТРЕБУЕТСЯ чертеж поставщика: Z16/Z40 pressure angle, face width, tooth system, mounting distances, backlash and heat treatment; only m1/Z16/Z40 topology is frozen.
4. ТРЕБУЕТСЯ ЗАМЕР: ISL PGM-32P purchased sample overall length, shaft length/diameter and flange hole pattern before motor holder release.
5. ТРЕБУЕТСЯ ЗАМЕР: exact purchased BTS7960/IBT-2 PCB dimensions, terminal projection and heatsink height; 50x50x43 is only a conservative module keep-out.
6. ТРЕБУЕТСЯ ВЫБОР/ПОКУПКА: real pressure sensor article; CAD contains only a keep-out marked NOT_PART and makes no fit claim.
7. ТРЕБУЕТСЯ ЗАМЕР: exact WEIPU SP13 chosen variant body/panel/thread dimensions and rear six-contact tether connector/strain-relief geometry.
8. ТРЕБУЕТСЯ ИСПЫТАНИЕ: pressure-cover seal groove/valve stack, +0.25 bar decay/submersion test, and camera housing pressure test.
9. ТРЕБУЕТСЯ ИСПЫТАНИЕ: 6-core camera cable flex + CVBS/UART EMC and 40 m tether voltage/video test before 100-150 m release.
