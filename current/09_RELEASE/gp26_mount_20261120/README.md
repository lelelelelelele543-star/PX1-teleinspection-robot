# GP26 mounting integrated with current F25 — 2026-11-20

Engineering CAD study, NOT manufacturing release. Based on remote980c82a, on branch feature/px1-gp26-mount-integration-20261120. Archived GA24 outputs were not merged. Current GP26/D22 envelope, toothed bevel gears, steel ballast, wheel locks, F25 lift/cover/harness and corrected power/traction documentation are preserved.

## Mounting

Motor face staysX189.5. A3mm plate and9.2x52.8x4 integral foot sit atZ32..36 on two integral body bossesR3.2, centresX195.5,Y±20. Existing1mm floor over weight plate is not tapped through. Cosmetic M3 holes endZ25,2mm above the plate recess roofZ23. Low-head M3x6 screws sit atZ33.5, with4.5mm nominal engagement and2.5mm tap allowance; headtopZ35.5. Foot counterboresD5.7 leave1.5mm under heads. X clearance-hole edge ligament1.5mm, head/upright nominal gap0.25mm. Lower motor-head reliefsR2.6 avoid the original near-zero gap above foot.

Eight provisional M2.5x6 attach motor faces,3mm engagement plus2.5mm modelled tap allowance. Exact supplied GP26 threads/diameter/depth are ESTIMATED. Major-diameter cosmetic threaded holes omit helical flanks; zero CAD overlap is not proof of thread strength. Material, screw grade/preload, bosses/foot strength and motor case internals require qualification. The archived GA24 floor-hole design was rejected here because only1mm Al remains above ballast.

At0.83Nm/motor, equal four-screw load-sharing onPCD19 gives21.8N tangential load per face screw. Worst summed reaction1.66Nm across40mm boss spacing gives41.5N ideal couple force. These are load estimates, not allowable-load proof: prying, friction/preload, jam transients, vibration and fatigue excluded. Power/thermal limits remain governed by corrected F19/F20 documentation.

## Evidence

See integrated_checks.json for final whole-assembly, STEP reimport and motor-tool results; drawing_check.json and lift_kinematics.json for current drawing/kinematic checks. Tool screen uses D3 bit cylinders80mm above floor heads and29mm behind motor heads, after explicit named removals (including motor face screws before accessing foot screws). Full handles, preceding removals and real wiring remain unqualified. No new physical test is claimed.

STEP: ../../CAD/PX1_Current_Master.step.gz (gzip, verify decoded SHA against integrated_checks.json). Source: ../../CAD/PX1_Current_Master.py. Images: images/px1_isometric.png and images/px1_drivetrain.png, actual CAD tessellation with hidden parts listed in render_manifest.json. Earlier historical release evidence applies to its own commits, not this model. F25 mesh removed per repository retention policy; recover it from980c82a.

Unresolved inherited issues include exact motor purchase/delivery, input shaft retention and pinion-support attachment, body/cover/seal strength, camera cable height, thermal and physical traction/pressure/endurance tests. Mounting does not close those issues.

Verified: 295 components, zero invalid solids and zero pair intersections (no excluded pairs). Integrated CAD/STEP checks20/20, drawing checks161/161, lift checks21/21. All ten nominal bit approaches clear. STEP reimport matches solid count, validity, volume and bounds.
