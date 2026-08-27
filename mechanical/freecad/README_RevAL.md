# PX-1 FreeCAD Rev.AL

Added:

- analytical involute spur-gear generator for z18, z30 and z40;
- standard geometry: module 1.0, pressure angle 20°, addendum 1.0m, dedendum 1.25m;
- exact involute flanks generated from the base circle;
- drivetrain center-distance checker;
- checks for 160 mm wheelbase, 4×40 mm side-gear chain and 24 mm z18/z30 motor-reduction center.

## Important manufacturing note

The involute **flanks** are analytical. The current root transition is simplified and is not a cutter-generated trochoid. Therefore these gears are suitable for prototype printing/machining and interference testing, but a final production gear drawing must either:

1. specify the actual hob/cutter and root form, or
2. import the finished gear geometry from the selected gear supplier.

This distinction is intentional: PX-1 must not release approximate root geometry as serial-production tooth data.
