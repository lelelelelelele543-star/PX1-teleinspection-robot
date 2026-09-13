# PX-1 Rev.B — WB23D full pressure-service integration screen

Date: 2026-09-14
Status: **PASS_FULL_INTEGRATION_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**

## Purpose

WB23C proved the pressure/service concept using a local pressure-roof reference. WB23D reinserts the same package into the exact corrected WB22A body geometry and checks it against the hard six-wheel crawler, all ten Z50 gears, lift arms and camera envelope.

No WB22A hard geometry is changed.

## Body integration

The service opening is cut through the WB22A pressure pod at:

- X = 228...286 mm;
- Y = -12...+12 mm;
- opening size = 58 x 24 mm.

Checks:

- opening lies inside the pressure-pod plan envelope: PASS;
- corrected WB22A body remains a valid solid after opening cut: PASS;
- M12 gland axis crosses the pressure-pod front wall as intended: PASS.

## Architecture lock

Executable model explicitly contains:

- 6 wheels;
- X50 / X150 / X250 wheel stations;
- 10 Z50 side gears;
- body lift pivot X200.

No four-wheel/two-axle interpretation is introduced.

## Fixed package DN150 screen

- cover: ~7.688 mm;
- pressure port hard envelope: ~4.699 mm;
- horizontal M12 gland: ~13.855 mm;
- M4 head 1: ~7.929 mm;
- M4 head 2: ~7.929 mm.

The fill/pressure port remains the limiting fixed feature.

## Full collision result

Across LOW / MID / HIGH checked lift states:

- fixed service package vs all ten Z50: 0 mm³;
- fixed package vs all six wheel envelopes: 0 mm³;
- fixed package vs four lift arms: 0 mm³;
- fixed package vs conservative camera outer envelope: 0 mm³;
- protected local harness guard vs fixed service package: 0 mm³;
- guard vs all Z50: 0 mm³.

LOW guard ideal-DN150 clearance remains ~29.234 mm.

MID and HIGH are not DN150-required positions; HIGH leaving DN150 is expected and is not a failure.

## Pressure-load sanity screen

For the 58 x 24 mm opening:

- +0.25 bar: ~34.8 N separating force;
- +1.0 bar: ~139.2 N total;
- ideal equal share on two screws at 1 bar: ~69.6 N each.

This is not a cover-stress or thread-certification calculation. It only confirms that pressure force magnitude itself does not justify a bulky multi-bolt cover. Sealing, plate stiffness, impact, gasket compression and thread engagement remain physical gates.

## Result

WB23D confirms that the simple Proteus-style service topology is compatible with the corrected WB22A crawler geometry. The project should **not** return to the abandoned dual-flex-chamber solution unless physical tests prove the simple topology inadequate.

## Remaining release gates

- real LAPP gland sample;
- real <=5 mm cable sample;
- real low-profile pressure valve;
- final body boss and O-ring groove design;
- +0.25 bar pressure decay and submersion;
- lift endurance and wet/grit cycling;
- physical DN150 jig with final hardware;
- full manufacturing tolerance review.

Controlled files:

- `cadquery/PX1_WB23D_FullServiceIntegration_RevB.py`;
- `cadquery/REV_B_WB23D_VALIDATION.json`;
- WB23C remains the functional/service definition.
