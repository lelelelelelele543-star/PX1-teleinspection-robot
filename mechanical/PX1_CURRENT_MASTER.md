# PX1 Current Master

**Date:** 2026-09-14  
**Controlling assembly:** `PX1_Current_Master.step` in the current release pack  
**Status:** `HOLD / NOT_FINAL_MACHINING_OR_FULL_DN150_RELEASE`

Proteus CRP-150 remains the primary mechanical reference. This is the single active PX1 integration state; old WB/Rev files are historical evidence only. A HOLD proxy is never treated as a manufacturing PASS.

## Frozen architecture

- 6 wheels at X50 / X150 / X250, mirrored left/right.
- 5 x Z50 per side at X50 / X100 / X150 / X200 / X250; adjacent centers 50 mm; rear X250 driven.
- Two traction motors total; motor -> supported Z16 -> Z40 -> rear axle -> five-Z50 train.
- Dry positively pressurized body; dynamic wheel sealing by X-rings; Z40 body shafts by 18x30x7 seals.
- Manual one-hand parallelogram-like camera lift; camera is separately sealed and removable.
- Removable PRESSURE/LIFT service cover with compact pressure valve and M12 camera-cable gland.
- Local camera harness exactly six insulated conductors: +12V, GND, TX, RX, CVBS signal, CVBS return.
- Main tether exactly six copper cores: HV+, HV return, RS485_A, RS485_B, VIDEO+, VIDEO-. Aramid/Kevlar is mechanical only.
- No coax in the main tether, no fibre, no custom PCB in the prototype, no cassette/cartridge mechanics, no external pressure-body hinges.

## Corrected drivetrain source content

Current master contains 12 x 61801 in the two side drives (6 per side), plus 2 x 61801 supporting the Z16 input shafts. Also present: 6 x 61903, 6 x X-ring 18.72x2.62, 2 x 61800, 2 x 18x30x7 shaft seals, 10 x Z50, 2 x Z16 and 2 x Z40.

## CAM026 camera evidence incorporated 2026-09-14

User teardown photos/video have been incorporated into the current camera reference. The previous ~Ø52 camera proxy is retired.

Confirmed / directly observed:
- lower/base cylinder outer diameter approximately **62.5 mm** from a caliper photo;
- hollow central wiring path through the rotating output;
- large internal ring-gear output driven by a smaller pinion;
- multi-stage reduction;
- thrust-bearing/race stack carrying axial load.

The current release-pack STEP uses ~62.5 mm as the CAM026-derived camera base-OD integration screen and contains reference solids for the hollow rotor, internal ring gear, thrust-bearing stack and reduction concept. Internal fits, wall thickness, tooth geometry and seal-groove dimensions remain HOLD. No further user teardown measurements are required; those items must be closed by controlled drawings, supplier samples or prototype work rather than invented values.

## Current validation facts

- 6 wheels / 10 Z50 / 12 side-drive 61801 / 6 61903 / 6 X-rings / 2 Z40 / 2 Z16 / 2 Z16-support 61801 / 2 motors / exactly 6 camera conductors.
- No invalid CAD shapes in the current generated assembly.
- Service-vs-Z50, service-vs-lift, service-vs-camera and motor-vs-camera modeled intersections: 0 mm³.
- Electronics pairwise intersections: none in the modeled envelopes.
- Ideal-DN150 non-wheel screen: pressure body about +1.01 mm, service cover +6.42 mm, pressure valve cap +8.28 mm, LAPP gland +13.75 mm, camera LOW +20.80 mm, rear connector panel +44.51 mm.
- **Full DN150 vehicle remains HOLD** pending the actual QRW90SR/150 wheel profile/hub and a real rigid-pipe test.

## Current real/published components represented

- ISL PGM-32P-24-100-60-02: 24 V, Ø32 mm, published length 92 mm, 100:1, 60 rpm no-load.
- NBK MLR-20C-6-6: Ø20 x 24 mm, 6/6 bores.
- LAPP 53112000 SKINTOP MS-M 12x1.5: M12x1.5, clamp 3.5-7 mm, ØA17.6, Cmax26.5, thread 6.5 mm.
- Cincon CQB150W-110S24: 57.9 x 36.8 x 12.7 mm.
- Adafruit MPRLS Product 3965: 17.8 x 16.7 x 7.5 mm, 0-25 PSI absolute.
- Nichicon UCS2D221MHD1TN: 220 uF / 200 V, Ø18 x 25 mm.
- WEIPU SP13 six-way camera connector family; sample/detail gate remains.
- WEIPU SP17 rear connector family; current architecture uses 7 contacts with exactly 6 tether cores and one unused spare.

## Current files

- `mechanical/cadquery/PX1_Current_Master_RevB.py` - earlier GitHub executable source retained for history/reference; the exact generator used for the current binary master is distributed in the release pack as `PX1_Current_Master.py`.
- `mechanical/cadquery/PX1_CURRENT_MASTER_VALIDATION.json` - current validation, synchronized with the current release pack.
- `mechanical/PX1_CURRENT_CRAWLER_BOM_RevB.md` - current BOM mirror.
- `mechanical/PX1_CHANGE_LOG.md` - current change journal.
- `electrical/PX1_Current_Electrical_Pressure_Pinouts.md` - electrical / pressure / pinout specification.
- `mechanical/PX1_Current_Manufacturing_Assembly_Test.md` - manufacturing, assembly and test sequence.

Binary STEP/PDF/STL deliverables and the exact current generator are distributed in the release ZIP. GitHub text specifications and validation are synchronized to this release.