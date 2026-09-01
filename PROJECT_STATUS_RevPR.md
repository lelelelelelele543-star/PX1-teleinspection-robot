# PX-1 PROJECT STATUS — Rev.PR

Date: 2026-09-01
Status: ACTIVE CORRECTED CRAWLER MASTER

## Purpose
Rev.PR converts the current Proteus reverse-engineering result into a corrected buildable crawler master and removes an old geometry conflict that survived in Rev.GL/GX.

The verified CRP-150 side-drive architecture uses the **rear wheel long axle as the driven input station**. Therefore the active input station is X250, not the old X200 placeholder.

## 1. Active side-drive skeleton
Per side:
- X50 = front wheel Z50;
- X100 = idler Z50;
- X150 = centre wheel Z50;
- X200 = idler Z50;
- X250 = rear wheel Z50 + driven long axle.

All five spur gears remain:
- module 1;
- Z50;
- pitch diameter 50 mm;
- adjacent pitch centres 50 mm.

Wheel centres remain X50 / X150 / X250, therefore wheel pitch is 100 mm and front-to-rear wheelbase is 200 mm.

The rear X250 shaft carries the handoff from the Z16 -> Z40 bevel stage. There is no separate fourth side-input shaft.

## 2. Motor envelope
Rev.PR preserves two motors total, one per side.

Packaging envelope accepted by the current body model:
- maximum screening diameter: Ø35 mm;
- maximum screening length: 100 mm;
- longitudinal motor axes;
- rearward arrangement from the X250 bevel handoff.

This envelope contains the currently documented Ø32 x ~92 mm industrial reference family with useful installation margin.

Exact motor bolt pattern, shaft geometry and final holder remain HOLD until a physical sample is selected/measured.

## 3. Bevel drive
Frozen functional data:
- small bevel: Z16;
- large bevel: Z40;
- ratio: 2.5:1;
- one pair per side.

The temporary module-1.25 geometry used in older screening studies is **not a machining release**. Rev.PR carries it only as a collision envelope until the actual reproducible bevel geometry is frozen.

## 4. Pressure body and lift
Rev.PR retains the useful Rev.GX pressure-body/wet-deck work:
- DN150-class body cross-section;
- open wet deck in front of the camera;
- two sealed wet scuppers;
- streamlined top controller saddle;
- dry central pressure volume;
- dry side gear bays under removable covers;
- rear pressure extension for the two longitudinal motors.

The manual lift remains structurally referenced to the main housing. Rev.PR intentionally does not create a full-width pressure-penetrating lift tube; the source-style local holding plates/bosses are to be detailed as conventional serviceable body features.

## 5. Internal electronics reserve
The corrected body was screened with non-purchased reserve volumes for:
- 100-120 V-class tether input -> local 24 V DC/DC;
- data/video interface;
- two traction driver channels;
- input protection;
- NUCLEO-F446RE;
- pressure sensor.

These are packaging reserves only. Exact commercial modules still require procurement/thermal validation.

## 6. Executed CAD validation
Active source:
`mechanical/cadquery/PX1_CRP150_Master_RevPR.py`

Executed with CadQuery 2.8.0.

PASS results:
- valid pressure-body solid;
- body volume outside ideal DN150 = 0 mm3;
- rear driven station = X250;
- all five Z50 pitch spacings = 50 mm;
- spur train spacing error = 0 mm;
- both Ø35 x 100 motor envelopes have zero body intersection;
- all current electronics reserve volumes fit inside the modeled dry cavity;
- no reserve-volume intersections.

Recorded result:
`mechanical/cadquery/REV_PR_VALIDATION.json`

## 7. Supersession
Where older CAD/status files conflict with the verified rear-wheel-input source architecture:
- Rev.GL X200 driven input is historical;
- Rev.GX X200 drive opening is historical;
- Rev.PR X250 rear-wheel long-axle input is active.

Rev.GX wet-deck, drainage and streamlined saddle concepts remain valid where they do not conflict with this correction.

## 8. Next engineering block
1. Move the detailed axle flange/bearing/seal stack to X250 and rebuild the driven rear wheel station as a manufacturable assembly.
2. Re-integrate the verified Rev.GF tapered wheel profile instead of simple wheel envelopes.
3. Freeze one real traction motor article and replace the Ø35 x 100 screening cylinders with measured geometry.
4. Freeze the reproducible Z16/Z40 bevel pair and its supported pinion shaft.
5. Run complete LOW/MID/HIGH lift sweep on the corrected body.
6. Run pressure/structural FEA on the rear extension, X250 drive station, scuppers and lift holding points.
7. Build and bench-test **one complete side drive first** before duplicating the opposite side.

Rev.PR is the active crawler mechanical master for subsequent PX-1 work.
