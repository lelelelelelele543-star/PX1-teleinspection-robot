# PX-1 Rev.GO — traction, wheel and ballast architecture

Status: PROTOTYPE ENGINEERING BASELINE; not machining release.

## Completed after Rev.GM
Rev.GN introduced an executable traction/tether model using the active DN150 wheel-contact geometry. Rev.GO converts the result into hardware provisions: interchangeable wheel tread variants, removable low ballast and a physical calibration test.

## Traction result
For the active Ø90 wheel contact at Y≈54 mm in an ideal Ø150 pipe, the wheel-normal vertical support factor is ~0.69397. Therefore total wheel normal force on level ground is ~1.441 times crawler weight.

The current protected drive screen is retained:
- 1.0 N.m motor-output command ceiling per side;
- 2.5:1 bevel ratio;
- Ø90 wheel;
- 0.75 conservative whole-path efficiency screening value.

Motor force ceiling is ~83.3 N total, but the present 6.3–7.7 kg crawler is normally expected to be adhesion-limited first.

Critical 30-degree observation: with the current contact geometry and placeholder Crr=0.02, effective tire friction must exceed roughly μ=0.415 before any positive tether-pull reserve exists. Ballast cannot fix a tire compound below that threshold.

## Wheel architecture
The active Rev.GF external envelope is preserved exactly. No wider Ø90 crown is added because DN150 outer-shoulder clearance is already tight.

Common keyed metal core:
- Ø17 wheel seat;
- 4 mm key interface retained from Rev.GF;
- same external dished/tapered profile for every tread type.

Two prototype traction shells are now executable in CadQuery:
1. SR — smooth/compliant elastomer candidate;
2. HG — same envelope with 18 transverse drainage/edge slots cut inward.

HG geometry can never worsen DN150 clearance because the slots only remove material.

Exact rubber/PU compound and Shore hardness remain test variables. Manufacturer documentation confirms the system-level logic of separate soft-rubber, high-grip and carbide wheel families for Proteus crawlers, but PX-1 does not copy proprietary wheel geometry.

## Removable ballast architecture
Do not gain traction by thickening the pressure body.

Rev.GO adds a smooth belly ballast provision:
- plate planform: 250 x 50 x 5 mm;
- stainless screening density: 7.85 g/cc;
- mass per plate: ~0.49 kg;
- maximum initial stack: 3 plates, ~1.47 kg;
- plate longitudinal center X≈155 mm, close to the current estimated mechanical CG X≈153 mm.

With all three plates:
- nominal 7.0 kg screen becomes ~8.47 kg;
- estimated CG Z falls from ~48 mm to ~40.4 mm;
- maximum ballast cross-section still retains ~10.9 mm ideal-DN150 radial margin;
- current side-cover lower corner remains more limiting at ~6.3 mm.

Therefore ballast is not the new DN150 bottleneck.

## Pressure-boundary attachment rule
No ballast fastener may penetrate P0.

Current prototype attachment concept:
- four M5 screws from below;
- screws terminate in local thickened blind floor bosses;
- boss material remains continuous above the blind thread;
- no through-hole, sealing washer or penetrator is permitted for ballast attachment.

Exact boss placement must be merged into the full pressure-body solid and checked against the internal electronics tray before machining release.

## Physical calibration procedure
`tests/PX1-TP-020_TRACTION_TETHER_RevGO.md` is now the mandatory calibration gate.

It measures:
- actual whole-crawler rolling/seal/gear drag;
- actual stable pull before wheel slip;
- effective wheel/pipe friction;
- ballast benefit;
- incline behaviour;
- actual 40 m tether tension;
- actual tether sliding coefficient.

Initial prototype targets:
- >=40 N stable level pull on normal wet wheel set;
- preferred >=50 N with the best normal/high-grip wheel without exceeding the protected current limit;
- prove the actual 40 m tether before making any 100–150 m range claim.

## Important source-derived architecture sanity checks
Current Minicam Proteus documentation states:
- 90 mm soft black rubber wheel for the 150 mm crawler class;
- high-grip hard-wearing carborundum/deep-bevel wheel for wet/greasy conditions;
- separate carbide wheel option;
- optional 2.5 kg extra weight plate to increase down-force/traction.

These support the PX-1 system decisions of interchangeable traction surfaces and removable ballast, not copied dimensions.

## Current open gates
1. integrate the four blind ballast bosses into the active full pressure body and electronics tray;
2. select/prepare physical SR and HG tread materials;
3. weigh the actual 6-core PX-1 tether sample per metre;
4. measure tether drag and crawler rolling drag;
5. measure actual Ø32 motor torque/current/speed curve;
6. full 3D FEM of the pressure body after ballast bosses and rear fillets are frozen;
7. physical DN150 sweep with maximum ballast;
8. 40 m pull/deployment test.

## Next autonomous block — Rev.GP
- integrate ballast bosses into the full body without P0 penetration;
- correct the internal packaging document to the current rearward Ø32 motor layout;
- freeze a practical prototype traction-ring manufacturing method;
- create the first complete test-build order so one wheel station and one side drive can be proven before machining six copies.
