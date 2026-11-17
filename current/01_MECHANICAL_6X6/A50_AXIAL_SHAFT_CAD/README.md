# A50 — axial shaft and bearing envelope
This stage supplies an executable FreeCAD macro, **not** an executed FreeCAD model.
Assumed Ø8 shafts and 8x22x7 annular bearing envelopes. Two independent longitudinal shafts, left motor end X120 and right motor end X215, both terminating X246. Bearing centre X234.
Geometry-only checks: right coupling ends X227; bearing begins X230.5; **3.5 mm axial gap**. Left coupling ends X132.
The macro exports FCStd and STEP when run in FreeCAD; neither output has been produced or validated in this stage.
PASS: arithmetic and envelope spacing. SKIPPED: FreeCAD execution, STEP validation, 3D clash detection. NEEDS_PHYSICAL_CHECK: bearing SKU, motor dimensions, pressure sealing, gear transition, shaft stress.
Next: model bevel input and shaft support/motor envelopes together and check 3D interference; resolve BLDC driver mismatch issue #15.
