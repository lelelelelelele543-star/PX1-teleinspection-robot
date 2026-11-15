# PX1 A16 — local motor relief in internal support plates

**DESIGN CANDIDATE, not a manufacturing release.** A15 on main documents rigid collision of old 25 mm motors with internal plates. This proposal avoids moving the six wheel stations and five Z50 stations per side.

Given A15 reference geometry: motor center |Y|=13.5 mm, motor diameter 25 mm, plate center |Y|=25.5 mm, plate thickness 6 mm. Inner plate face is |Y|=22.5 mm. Existing interference = 13.5+12.5-22.5 = **3.5 mm**.

Assume nominal assembly clearance 0.5 mm. Local inner-face relief = **4.0 mm**, leaving **2.0 mm** plate web. The pocket must be limited to the motor's verified X envelope; never cut the pressure shell or bearing seats. This is a candidate, not an approved solution.

**PASS:** arithmetic and Python assertions. **NEEDS_PHYSICAL_CHECK:** bending stiffness, fastener support, bearing seat continuity, actual motor and tolerance stack. **SKIPPED:** FreeCAD/STEP/3D Boolean. For a 26 mm motor, required pocket grows to 4.5 mm and remaining web drops to 1.5 mm; that variant is not approved.

Next: generate a real 3D pocketed support plate and test Boolean collisions against motor, middle X150 shaft, bearing seats and Z50 gears. If web strength is inadequate, reinforce locally without moving wheel positions.
