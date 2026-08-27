# FreeCAD workflow for PX-1

## First model
1. Open FreeCAD and create a new document.
2. View -> Panels -> Python console.
3. Run `PX1_Master_Parameters.py`.
4. Run `PX1_Body_Master.py`.
5. Save as `PX1_MASTER.FCStd`.

The model is parameter-driven. Change dimensions on the `PX1_Parameters` object instead of editing geometry directly.

## Frozen prototype baseline
- body 250 x 94 x 76 mm
- wheelbase 160 mm
- wheel diameter 90 mm
- front axle X=45 mm
- rear axle X=205 mm
- axle Z=37 mm
- only two rear rotating body penetrations
- rear carrier bore Ø38 mm
- shaft Ø10 mm
- 6000 bearing: 10 x 26 x 8 mm
- seal: 10 x 22 x 7 mm

## Important
The rear LEMO opening in this model is only the controlled nominal interface envelope. Do not use generated thread geometry as a substitute for the official connector machining requirements.

Next FreeCAD components will be linked to the same master parameter object: rear carrier, output shaft, front stub axle, drivetrain gears, wheel, motor cradle, camera lift and camera head.
