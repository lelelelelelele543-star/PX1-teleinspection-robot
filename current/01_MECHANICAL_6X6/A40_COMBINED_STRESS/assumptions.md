# PX1 A40 — combined bending and torsion (sensitivity only)
- Input assumptions: groove root Ø11 mm; bending moments 0/5/10/20 Nm; torques 5/10/20 Nm; theoretical concentration multipliers Kt_b=Kt_t=2.0. These are NOT measured Proteus data or DIN values.
- Formula: sigma=Kt_b*32*M*1000/(pi*d^3), tau=Kt_t*16*T*1000/(pi*d^3), sigma_VM=sqrt(sigma^2+3*tau^2), MPa.
- Example M=10 Nm, T=10 Nm: sigma=153.057 MPa, tau=76.528 MPa, VM=202.475 MPa. No safety factor or material allowable asserted.
- PASS: local Python execution, assertions and 12-row CSV generation; SVG preview generated from the same parameters.
- SKIPPED: FreeCAD/FEA and real geometry Boolean; NEEDS_PHYSICAL_CHECK: motor stall torque, wheel traction, bending reactions, notch radius, material and fatigue.
- Verification plan: obtain confirmed ring groove drawing and motor/gear torque; solve bearing reactions with shaft geometry; calculate fatigue with material data; validate by CAD/FEA and bench.
- This A40 study does not alter frozen six-wheel architecture or claim manufacturing release.
