# PX1 M1 — integrated kinematic architecture audit (2026-11-20)

Source reviewed: `PX1_Integrated_6x6_M1_interface_repair.py` in the same working branch, and governing `AGENTS.md` from main. This is a **source-level audit**, not an executed FreeCAD or physical validation.

## Critical interfaces, not isolated shaft edits

1. **Wheel torque path — FAIL (unimplemented).** Six Z50 wheel-station gears have Ø10 bores and six Ø10 shafts; six wheel hubs also have Ø10 bores. Coaxial contact is not a torque joint. Add a common, manufacturable positive-drive feature (e.g. keyed hub or cross pin) at each wheel gear/shaft and wheel/shaft interface, with tolerances and stress check.
2. **Idler kinematic freedom — FAIL (unimplemented).** Four Z50 idlers have Ø10 bores, and each uses an Ø10 stationary stub and nominal 10×22×7 bearing ring at Y=19..26; the gear occupies Y=27..33. The gear does not mount to the bearing outer race and no idler hub is modeled. Therefore bearing presence alone does not demonstrate an independently rotating idler. Add hub/outer-race engagement and an axial retention scheme without locking the idler to its stub.
3. **Bevel power input — FAIL (unimplemented).** Z16/Z40 are pitch-cylinder proxies, not conjugate bevel gears. Rear Z40 and Z50 are coaxial only; no torque-carrying common hub is modeled. Do not claim powered 6×6 motion until actual bevel geometry, tooth contact, hub fixation and axial thrust support are checked.
4. **Pressure boundary — FAIL (unqualified).** Six 22 mm bearing pockets penetrate the 5 mm side walls. External annular seal cartridges are packaging proxies only; they do not establish a continuous pressure barrier or qualified 0.4–0.7 bar dynamic seal. Define retained seal housing, radial/axial interfaces and a pressure-qualified dynamic element; perform safe physical verification later.
5. **Fastener/lid — PHYSICAL_CHECK.** Eight nominal M3 pilots and a 3 mm flat gasket strip exist. Fastener preload, compression distribution, flange deflection and pressure extrusion are not established. At 0.7 bar and a 170×60 mm opening, force = 714 N (analytical, ignoring other loaded surfaces).

## Reproducible next integrated implementation

In **the existing assembly generator**, model three functional groups together: (A) six positive-drive wheel gear/axle/wheel joints, (B) four freely rotating idler hubs and their retained bearing supports, (C) two real bevel inputs and rear common hubs. Add a kinematic test that each of the two motor rotations propagates to its own three wheels, while idler gears rotate freely. Keep sealing as a separately tracked local blocker; it must not be silently marked PASS. Run FreeCAD and STEP round-trip before claiming the integrated milestone.

**Status:** source inspection PASS; actual 3D interference NOT_RUN; transmission motion FAIL (unimplemented); pressure qualification PHYSICAL_CHECK. No manufacturing release.
