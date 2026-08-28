# PX-1 Rev.GR — FreeCAD / CalculiX FEA load-case specification

Status: SOLVER-READY ANALYSIS PLAN; not a structural release by itself.

## Purpose
Define the exact analysis cases to run when the active Rev.GL/GP pressure-body solid is opened in FreeCAD FEM / CalculiX. This document prevents arbitrary constraints or a single misleading pressure case from being treated as proof.

The prior Rev.GM plate-series calculation remains a screening check only. The 3D model must include at minimum:
- main P0 pressure body;
- P1/P2 4 mm pressure membranes;
- side-bay openings and local wheel/X200 bosses;
- top opening and cover fastener region;
- rear 76x44 mm pressure extension and its transition around X299;
- four blind Rev.GP ballast bosses;
- rear tether structural-anchor load introduction region.

## Material model — provisional until stock certificate
Use isotropic aluminium properties only for the first screening run:
- E = 70 GPa;
- Poisson ratio = 0.33;
- density = 2700 kg/m3.

The current manufacturing concept uses 6082-T6-class aluminium for machined structural parts, but **yield/allowable stress is not frozen here**. Final allowable must use the actual purchased alloy/temper, section thickness and material certificate.

For the screening plots, always report raw von Mises stress and displacement. Do not hide the result behind a single automatically calculated factor of safety.

## Mesh policy
Use quadratic tetrahedra where supported.

Initial global element target: 3-4 mm.

Local refinement target: 1.0-1.5 mm around:
- X200 cartridge/bearing-seat transitions;
- wheel-flange pilot and screw-hole regions;
- P0/P1/P2 membrane-to-body fillets;
- top-opening corners;
- rear extension transition X≈299;
- ballast-boss roots;
- tether-anchor bolt/contact region.

Run at least one mesh-convergence comparison. Peak singular stress exactly at a mathematically sharp fixed edge or point load must not be accepted as a physical result without examining stress one to two element lengths away and improving the real fillet/contact geometry.

## Constraint philosophy
Pressure on a closed body is self-equilibrating; excessive fixed faces create false stress.

For pressure-only cases use a **minimal 3-2-1 rigid-body restraint** or equivalent weak-spring stabilization:
- one remote/noncritical node: UX=UY=UZ=0;
- second remote node: two translations fixed;
- third remote node: one translation fixed.

Choose all three away from the stress-critical X200/rear-transition/top-opening areas.

For tether or wheel-load cases use the physical reaction path described per case rather than reusing the pressure-only minimal constraints.

## Pressure convention
All values below are **differential gauge pressure** applied normal to the relevant wall. CalculiX sign/orientation must be verified with a small test model before the production run.

### LC-P01 — 10 m water / retained positive internal pressure
Purpose: worst normal submerged external-pressure direction used in Rev.GM.

Apply net `0.060 MPa = 0.60 bar` **inward** on all external wetted walls of the closed pressure system that remain internally at about +0.4 bar gauge while outside hydrostatic pressure approaches +1.0 bar gauge.

Use pressure-only minimal 3-2-1 restraints.

Report:
- max displacement;
- membrane stress around P0/P1/P2 walls;
- top-opening corner stress;
- rear-extension transition stress;
- local buckling warning signs/large panel deformation.

### LC-P02 — P1 pressure-loss fault at surface
P0 retained at +0.40 bar gauge, P1 approximately 0 bar gauge.

Apply `0.040 MPa` from P0 toward P1 on the left 4 mm membrane only. P2 remains balanced with P0 for this case.

Purpose: isolate left membrane / X200 / wheel-boss stress.

### LC-P03 — P2 pressure-loss fault
Mirror LC-P02 on the right side.

### LC-P04 — reverse zone differential
P1/P2 retained near +0.40 bar while P0 loses pressure toward 0 bar.

Run left and right separately if the solver model is not perfectly symmetric. This checks the opposite bending direction of the same 4 mm membrane and boss fillets.

### LC-P05 — empty-body proof pressure
For the bare pressure body only, with pressure-sensitive electronics/seals excluded from the certification claim, screen `0.10 MPa = 1.0 bar` internal proof differential.

This is a **structural proof-screen case**, not the intended continuous operating pressure.

Do not combine this with the operational wheel/tether loads unless a later qualification procedure explicitly requires the combination.

## X200 drivetrain local loads
Use the active Rev.GL reaction screen at the provisional 1.0 N.m motor-output ceiling.

Nominal bearing/support resultants per X200 station are approximately:
- support A: 98 N;
- support B: 196 N;
- bevel axial component: 33.8 N.

### LC-D01 — X200 nominal drive
Apply the nominal reaction forces at the actual 61800 bearing-seat contact regions with correct vector directions from the bevel/spur force solution.

### LC-D02 — X200 2x shock screen
Apply:
- 196 N at support A;
- 391 N at support B;
- 67.6 N axial bevel component.

Run left and right drive stations. Combine with P0 normal operating pressure only if needed to identify local seat/fillet interaction.

Do not apply these as point forces to one mesh node; distribute over the bearing-seat surface or use rigid/remote coupling.

## Wheel-station structural cases
The older reliability screen used a deliberately conservative 200 N radial wheel load acting outboard of the nearest support.

### LC-W01 — single-wheel radial obstacle load
Apply 200 N radial load at the wheel-seat/hub load introduction for one station while constraining the corresponding inner structural support realistically.

Repeat at front/middle/rear station if local body geometry differs materially.

### LC-W02 — asymmetric side impact
Apply 200 N radial at one wheel plus a 50 N tangential component at that wheel. Use this only as a screening load until physical obstacle tests give a better transient load.

## Tether / rear-anchor cases
The mechanical tether load path bypasses the electrical connector and enters the structural rear bulkhead/extension.

### LC-T01 — centered 2 kN proof pull
Apply 2000 N along the tether axis into the actual strength-member anchor contact/fastener region.

Reaction boundary for the **local rear-structure model**: constrain the cut plane well forward of the rear-extension transition, preferably through a sufficiently long section of the main body so the X299 fillet/transition remains free to deform.

Do not fix the rear face itself.

### LC-T02 — 2 kN pull with 30 mm eccentricity
Apply 2000 N with load line 30 mm from the rear-extension centroid, equivalent to a 60 N.m bending moment plus axial pull.

### LC-T03 — 2 kN pull with 50 mm eccentricity
Apply 2000 N with 50 mm eccentricity, equivalent to 100 N.m bending moment. This is the more abusive installation/recovery screen.

### LC-T04 — 5 kN gross-section abuse screen
Optional only for the bare structural model: 5000 N at 30 mm eccentricity. This is not a required operational proof load; it checks whether the gross rear section has an unexpectedly weak transition.

## Ballast-boss cases
Rev.GP uses four blind M5 ballast bosses and up to three 225x50x4 mm stainless plates, about 1.06 kg total.

### LC-B01 — static ballast
Apply gravity with the maximum plate mass represented at the actual mounting faces. This is expected to be minor but confirms boss-root stress.

### LC-B02 — ballast shock
Apply a 5g vertical inertial screening load to the maximum ballast mass, equivalent to about 52 N total, distributed over the four bosses.

This is not expected to govern the body but catches thin-root mistakes after the blind bosses were added.

## Combined operational cases
Only after individual cases are debugged:

### LC-C01 — submerged + X200 drive
LC-P01 plus nominal LC-D01 on both sides.

### LC-C02 — submerged + one-wheel obstacle
LC-P01 plus LC-W01 on the most critical wheel station.

### LC-C03 — maximum ballast + operational traction body loads
Gravity for current estimated crawler mass plus maximum ballast, nominal drivetrain reactions, and normal +0.4 bar internal/ambient operational pressure condition.

Do **not** combine proof loads (1 bar body proof or 2 kN tether proof) with every other proof load unless required by the qualification plan; doing so creates a fictitious test case rather than a realistic or specified one.

## Result extraction
For every solved case save:
- solver version;
- mesh element/node count;
- element type;
- material values;
- applied loads and restraint screenshots;
- max displacement and location;
- max von Mises stress and location;
- principal stresses around seals/threads where relevant;
- reaction-force balance check;
- deformed-shape scale factor clearly stated;
- one section plot through the critical region.

## Acceptance philosophy before material freeze
No final MPa PASS limit is declared until actual alloy/temper is frozen.

Before that freeze, Rev.GR uses these engineering gates:
- no gross instability or unrealistic panel deformation;
- pressure-case deflection must not threaten O-ring compression, bearing alignment or gear center locations;
- critical stress must not be dominated by an avoidable sharp CAD corner;
- tether load path must remain in the structural bulkhead/extension and not the electrical connector or thin service cover;
- X200 loads must not ovalize bearing/seal seats enough to threaten alignment;
- ballast bosses must not pierce or materially weaken the P0 pressure floor.

Any geometry modification driven by FEA must be rerun through the full Rev.GL DN150/collision validator before it is accepted.
