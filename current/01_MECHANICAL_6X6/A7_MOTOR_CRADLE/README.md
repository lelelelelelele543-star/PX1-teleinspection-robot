# PX1 A7 — two-V motor cradle (preliminary)
Design goal: model a physically reproducible one-piece cradle for one of the two drive motors. Geometry is an original proposal, **not** a Proteus measurement. Do not treat as released manufacturing design.

## Inputs (mm, all ESTIMATED / DESIGN TARGET)
- plate 44×26×3; four through holes Ø3.2 at x=5/39 and y=±9.5
- support x=12–16 and 28–32, across width 26; block extends z=3–12
- V notch from (y=-11,z=12) through (0,5) to (+11,12)
- provisional motor envelope Ø24; no verified motor CAD yet
- coordinates: X length, Y transverse, Z vertical, origin at plate left/center/bottom

## Outputs
- `PX1_A7_Motor_Cradle.FCMacro.py`: FreeCAD Python source for actual solid with through holes and two V cuts; run as macro in FreeCAD Python environment.
- `px1_a7_motor_cradle_preview.svg`: dimensioned **2D diagram** of exactly the same numeric design inputs, **not** a FreeCAD screenshot.
- On successful macro execution, `.FCStd`, `.step`, `.stl` are generated alongside the script (not committed in this stage).

## Verification
- PASS: parameter cross-check of SVG dimensions vs macro text, four mounting positions, two support x positions.
- SKIPPED: FreeCAD macro execution, BREP validation and STEP/STL exports (no FreeCAD in this execution environment).
- NEEDS_PHYSICAL_CHECK: selected motor dimensions and mounting interface, contact stress, fastening and clamp retention, vibration, corrosion, motor-to-X150 axle and Z16/Z40 clearance.
- This is a **cradle**, not yet a complete clamping assembly. Do not install an unrestrained motor.

## Next
Obtain selected motor supplier drawing, build upper retention clamp and fastener pockets, assemble two cradles and Z16/Z40 in FreeCAD, collision-test against X150 and X250. Do not change the frozen 6-wheel drivetrain.
