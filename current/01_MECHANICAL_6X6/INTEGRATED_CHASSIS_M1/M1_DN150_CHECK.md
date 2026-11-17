# M1 DN150 integrated clearance correction

Previous M1 wheel envelope: Ø105 x 18, wheel Y=60..78, Z=-5. Conservative pipe radial bound sqrt(78²+57.5²)=96.903 mm, exceeding DN150 radius 75 mm by 21.903 mm (FAIL). Previous analytical test checked only adjacent wheel spacing and missed pipe clearance.

Revised design assumptions: body 307x80x70 mm, wheel Ø78x18 mm, wheel Y=40..58 mm, Z=-5 mm; six wheels, two motors, ten Z50, X stations unchanged. New conservative wheel bounding radial extent sqrt(58²+44²)=72.801 mm; DN150 nominal radial margin 2.199 mm (PASS analytical). Body corner sqrt(40²+35²)=53.151 mm. Wheel spacing 110-78=32 mm. No claim of factory Proteus geometry.

The CAD script updates wheel envelopes, axle lengths, bearing positions and asserts DN150 envelope. Bearings, wheel hubs, pressure shaft seals, motor-to-bevel gear mesh, lid sealing and 3D Boolean collisions remain NOT_RUN/PHYSICAL_CHECK. A 2.2 mm theoretical margin is NOT adequate evidence of operating clearance with tolerances, debris or pipe ovality. No manufacturing release.

Next: run FreeCADCmd on integrated M1, export STEP and evaluate all rigid-solid intersections with explicit allowed mating pairs; verify hub/bearing/wall interfaces and replace gear proxy solids.