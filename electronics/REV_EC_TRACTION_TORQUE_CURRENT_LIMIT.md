# PX-1 Rev.EC — traction torque/current protection

Status: control requirement derived from the current JGB37-555 + KHK bevel drivetrain. Exact current thresholds remain bench-calibration items.

## Mechanical limit that now matters
Preferred bevel pair is KHK SB1.5-1845H / SB1.5-4518H, ratio 2.5:1.

The small bevel gear is the limiting member. Use **1.50 N*m maximum commanded motor-output torque** as the provisional drivetrain ceiling before full life-factor calculation and physical testing.

This gives approximately:
`1.50 * 2.5 * 0.90 = 3.375 N*m` maximum commanded side torque after the bevel stage.

The normal rated JGB37-555 operating point is expected to remain substantially below this ceiling.

## Current is not torque until calibrated
Do not hard-code a final ampere threshold from internet motor tables.

For each purchased motor lot:
1. record no-load current and rpm at 24.0 V;
2. load the output shaft through several known torque points;
3. record current versus torque in both directions;
4. build a per-motor linear/piecewise torque estimate after subtracting no-load/friction current;
5. set the firmware current threshold corresponding to <=1.50 N*m motor-output torque;
6. use the lower safe value of the two installed motors unless individual calibration is stored.

## Protection layers
1. PWM/current control prevents excessive commanded torque;
2. fast jam detector trips on high current + low wheel speed;
3. driver hardware overcurrent/thermal protection is backup;
4. per-side fuse protects wiring/fire, not gear teeth;
5. hardware E-STOP removes traction power independently of software.

## Initial jam timing concept
Before measured data, use only as firmware development placeholders:
- high-current transient during acceleration allowed for tens of milliseconds;
- sustained current above calibrated torque ceiling -> command reduction immediately;
- high current with near-zero wheel speed for roughly 100–250 ms -> traction fault and disable affected side;
- repeated jam events -> global traction inhibit until operator reset.

Exact times follow real motor inertia and pipe tests.

## Reversal rule
Do not command full forward to full reverse in one PWM step.

Use:
- ramp to zero;
- short zero/decay interval as required by driver behavior;
- ramp into reverse;
- monitor 24 V bus overvoltage and current throughout.

This reduces bevel impact load and regenerative bus spikes.

## Side Z50 margin
KHK SSG1-50 class gears have published torque capability well above the 3.375 N*m side-input ceiling, so the bevel pinion currently governs the mechanical torque policy rather than the Z50 side gears.

## Driver consequence
BTS7960 remains prototype-only. A final driver must:
- support 24 V traction bus;
- tolerate measured motor stall current with margin;
- provide predictable current sensing or allow external current sensing;
- survive repetitive braking/reversal transients;
- have thermal protection and hardware disable.

## Release gate
No final fuse, current limit, driver, contactor or DC/DC peak rating is released until the exact installed JGB37-555 samples are characterized.