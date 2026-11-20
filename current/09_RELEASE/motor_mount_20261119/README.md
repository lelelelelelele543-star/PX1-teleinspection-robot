> Preserved on feature/px1-motor-mount-study-20261120. During push, origin advanced to4a34b8c with GP26/D22 motors and major integrated changes. This study is based on fe8a5f9, NOT validated against the newer master. Do not merge its generated CAD wholesale over the new assembly.

# Integrated motor mounting — 2026-11-19

Engineering prototype, NOT manufacturing release. Continues fe8a5f9 on feature/px1-integrated-cad-20261117; main unchanged.

GA24 motor holder now has an integral L-foot seated on internal floor Z23. Two M3x10 at X194.5,Y±20 attach the foot into blind holes ending Z17, retaining6mm pressure-body floor. Foot9.5x52.8x4mm, vertical plate3mm. Motor faceX188.5 clears the floor-screw heads; shaft endX206 gives3mm nominal pinion-end gap and6.5mm insertion into the split adapter. Eight M2.5x6 fasten motor faces with provisional3mm tapped engagement. All motor mounting dimensions are ESTIMATED until exact bought variant is checked; no purchased motor identity or delivery confirmation.

Geometry: 6mm remaining floor, minimum nominal foot-hole edge ligament1.8mm (X edge), 4.7mm (Y edge). These dimensions are not a strength or leak qualification. Under assumed equal sharing, one0.6865Nm motor requires18.1N tangential force per screw on4xPCD19; both motor reactions1.373Nm correspond to34.3N ideal couple force across40mm floor-screw spacing. This ignores preload/friction, prying, impact, fatigue and jam load; no allowable stress calculation or material release claimed.

All rigid pairs checked, including new holder and fasteners. Only explicit motor screw/motor and floor screw/body major-diameter/tap-pilot contacts are classified THREAD_ENGAGEMENT_HOLD_NO_HELICAL_GEOMETRY. They remain reported, not omitted. See integrated_checks.json for actual results, plus full PX1_Current_Validation.json. Ten D3 driver-bit probes added:80mm vertically for floor screws and29mm rearward for motor screws. Probes check retained geometry after named preceding removals; handles and complete disassembly not certified. Motors remain removable in the conservative envelope screen after required removals.

STEP ../../CAD/PX1_Current_Master.step and parametric source ../../CAD/PX1_Current_Master.py. Images are actual tessellated CAD surfaces, including isometric and drivetrain views; hidden parts recorded in render_manifest.json. All prior release directories refer to their own historical revisions. Older PDFs were not regenerated.

Open: exact motor threads/outline, material/fastener grade/preload, motor leads, shaft torque retention, bevel teeth, pinion support attachment, seals and physical traction/thermal/pressure tests. No A0/A1/A5 physical pass claimed.

Completed and saved2026-11-20:20/20 local CAD checks pass. Zero rigid intersections and Boolean errors. Thirty explicit unqualified seal/thread/bevel contacts remain. STEP reimport checks validity, solid count, volume and bounds. Initial failed validation records two screw-head/holder intersections before correction.
