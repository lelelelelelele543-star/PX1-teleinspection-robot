# A48 — rear X250 input reach
A47 source branch: feature/px1-a47-staggered-motor-envelope-20261117.
ASSUMED: body x=0..278 mm, rear axle x=250 mm, motor L x=55..120, motor R x=150..215. Not measured Proteus geometry.
DERIVED: motor-end to X250 projected axial gaps 130 mm (L), 35 mm (R). These are **not** shaft lengths or validated gearbox dimensions.
DERIVED IF PARALLEL SPUR GEARS: m=1.5, Z16/Z40 => pitch-center spacing 42 mm. This does not validate the baseline's bevel/right-angle stage.
PASS: arithmetic, coordinate ordering; SKIPPED: FreeCAD solid collisions, physical verification.
Open design issue: staggered motor arrangement needs distinct power transmission paths and bearing supports to X250; 2D lateral clearance alone does not resolve drivetrain.
Next: construct 3D shaft and bevel/input arrangement with motor-axis orientations and test collisions, preserving 10xZ50, six wheels, pressure housing.
