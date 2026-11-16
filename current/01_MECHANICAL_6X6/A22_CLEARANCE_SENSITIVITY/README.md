# A22 — clearance sensitivity
All inputs **ASSUMED** from A21 PR #39, not measured Proteus dimensions. Relief radius min 13.15 mm; motor radius max 12.75 mm; plate temperature delta -30 C, alpha 23e-6/K; motor +60 C, alpha 12e-6/K; eccentricity 0.2 mm.

PASS: independent JS arithmetic and Python assertions (Python runtime execution SKIPPED). Baseline gap 0.1817465 mm; zero gap at e=0.3817465 mm; e=0.4 gives -0.0182535 mm, interference. 3D/FreeCAD SKIPPED; physical envelope, thermal, assembly and wall stress NEEDS_PHYSICAL_CHECK.

|Assumption|Why|Verification|
|---|---|---|
|Motor max radius 12.75 mm|A21 tolerance|Manufacturer drawing / gauge|
|Relief min radius 13.15 mm|A21 tolerance|Machining inspection|
|Eccentricity 0.20 mm|Assembly allowance|Datum stack and runout|
|Thermal coefficients 12e-6/23e-6|Indicative steel/aluminium|Material certificate|

Next: real 3D collision check against X150, Z50 and motor, then plate stress. No manufacture release.