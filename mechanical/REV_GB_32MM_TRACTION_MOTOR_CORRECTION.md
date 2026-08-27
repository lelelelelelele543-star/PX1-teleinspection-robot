# PX-1 Rev.GB — traction motor package correction

Status: prototype architecture correction; exact purchased motor remains HOLD.

## Why the Ø37 JGB37 envelope is superseded
The separated P0/P1/P2 architecture requires enough side-wall thickness to contain the 8 mm side-gear bay plus a pressure membrane between the central electronics cavity and each side drive. Two Ø37 mm motors side-by-side require approximately 75 mm internal width before wiring/clearance, forcing the P0 wall too thin or pushing the side covers outward into the DN150 envelope.

Therefore Ø37 JGB37-555 remains an obsolete packaging candidate for the current CRP150-like separated-side-bay geometry.

## New packaging class
Use a 24 V planetary gearmotor in the 32 mm diameter class:
- body/gearbox diameter: <=32 mm target;
- complete motor length: <=95 mm target;
- output speed: 45–65 rpm target;
- rated output torque: >=1.1 N*m target, >=1.2 N*m preferred;
- metal planetary gearbox;
- output shaft suitable for supported coupling to the bevel pinion shaft;
- quadrature Hall encoder preferred;
- motor output shaft still does NOT carry bevel-mesh radial load.

Current CAD envelope:
- centerlines Y = +/-16.5 mm;
- envelope outer half-width = 32.5 mm;
- P0 clear internal half-width = 34.0 mm;
- nominal side clearance = 1.5 mm each side.

## External performance references — not procurement release
Current web research shows the 32 mm class is physically capable of the required torque/speed. Examples include:
- 32 mm planetary families with 24 V versions and encoder options;
- ratios around 1:139 producing roughly 50–60 rpm and about 12 kgf*cm class rated torque in manufacturer tables;
- other 32 mm encoder gearmotors around 75 rpm / 8 kgf*cm.

These are feasibility references only. Final motor article must be sourced and bench-tested before machining the motor holder/shaft adapter.

## Drivetrain consequence
For a reference motor at 51 rpm and 12 kgf*cm (~1.177 N*m), with the current 2.5:1 bevel stage and assumed 0.90 stage efficiency:
- wheel train input torque per side ~2.65 N*m;
- wheel speed ~20.4 rpm;
- Ø90 theoretical linear speed ~5.77 m/min;
- ideal tangential force per side ~58.9 N before tire/gear losses.

The reference motor torque is below the current ~1.5 N*m bevel-pinion protection ceiling.

## Release gates
- exact 32 mm motor sample and drawing;
- shaft diameter/flat/key dimensions;
- no-load current and rpm;
- rated-load current/temperature;
- short controlled stall current;
- 30 min crawler duty test;
- encoder signal under PWM;
- final motor-holder drilling only after measurement.
