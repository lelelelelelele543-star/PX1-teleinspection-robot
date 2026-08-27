# PX-1 Rev.EV — manual lift plate solids and hard-stop baseline

Status: prototype mechanical detail; supersedes rod-only lift envelopes.

## Architecture retained
Manual CRP-style parallelogram lift with:
- two side arm plates;
- one-hand M8 adjustable clamp lever;
- 150 N-class gas spring candidate;
- replaceable pivot bushings;
- mechanical DN150 hard stop;
- camera head carried in a rigid front yoke.

## Current kinematic datums
- lower main pivot: X200 / Z94;
- nominal arm effective length: 120 mm;
- LOW/DN150 camera axis: Z75;
- MID camera axis: Z130;
- HIGH camera axis: Z205.

Rev.ES rearward motor pack frees the front region required by the folded lift.

## Arm plates
Prototype arm plate candidate:
- material: 4 mm 1.4301/304 stainless or 5 mm EN AW-7075/6082 after stiffness comparison;
- width around pivot line: 20–24 mm;
- pivot holes: Ø8 mm class with replaceable flanged bushings;
- generous radii at transitions, no sharp internal corners;
- left/right arms connected at the camera yoke so they cannot rack independently.

Preferred first prototype: 4 mm stainless arms because thin sections tolerate impact and wet service well without bulky ribs.

## Pivot support
Lower pivots are carried by structural bosses integral with the main body/rail, not by the top service cover.

Each pivot stack:
- Ø8 stainless shoulder pin or machined axle;
- polymer composite or oil-impregnated bronze bushing;
- stainless thrust washers;
- circlip/retained screw for axial location;
- shim capability to remove side play.

## Manual clamp
One pivot becomes the friction clamp station.

Baseline stack:
- M8 adjustable clamping lever;
- hardened thrust washer;
- Belleville spring pair/stack;
- replaceable friction washer;
- arm plate;
- body boss;
- opposite thrust washer/retainer.

The clamp must hold position with the robot unpowered.

## Mechanical DN150 stop
DN150 safety is hardware, not firmware.

Use a captive stop pin or removable shoulder screw that physically prevents the linkage from passing above the LOW/DN150 range when the robot is configured for DN150.

The stop is positioned so that even with clamp released the camera/yoke cannot enter the pipe wall envelope.

## Gas spring
150 N remains only a force-class candidate. Exact article is blocked until the actual linkage mounting points are fixed.

Requirements:
- corrosion-resistant construction or protective boot;
- stroke sufficient for LOW-to-HIGH motion;
- no singular/over-center force spike;
- gas-spring line of action must not obstruct top-cover removal;
- replaceable with standard ball-joint/clevis hardware.

## Camera yoke
The yoke is a separate rigid part:
- supports TILT bearings/pivots;
- carries no pressure boundary if the camera head has its own sealed shell;
- accommodates quick head removal;
- includes cable bend control into the continuous-ROLL head interface.

## Qualification
- static 3x camera-head mass load at HIGH;
- 500 raise/lower cycles;
- wet/mud clamp test;
- side play measurement before/after cycling;
- drop/impact handling test with lift LOW;
- DN150 full physical sweep with hard stop installed;
- verify no lift fastener can enter the wheel envelope.
