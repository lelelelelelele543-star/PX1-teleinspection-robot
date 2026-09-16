# A3.1 — pan / rotate architecture

Status: SOURCE TOPOLOGY FROZEN / MOTOR AND GEAR RATIOS NOT RELEASED.

## What the CAM026 source proves
The recovered source gives a clear mechanical split:
- camera housing assembly contains a dedicated **camera PAN gear** (`GEA-001-824`);
- a separate PAN motor assembly uses `MOT-001-759`, a PAN motor gear and a bracket;
- the bearing/rotate housing also uses `MOT-001-759` and a rotate motor gear;
- the rotate train includes two separate idle gears (`ASS-001-998`);
- the rotate housing includes a separate angle-encoder axle gear;
- multiple O-rings and a rotate seal-flange cover isolate the rotating assembly.

So the PX1 head will use two independently controlled axes, not one combined servo mechanism:
1. PAN/tilt of the optical camera module inside the side frame;
2. ROTATE/roll of the camera-frame assembly about the crawler/head axis.

## Rev.A simplification
The original CAM026 focus motor is not reproduced. The RunCam M12 lens is focused during assembly and locked. This leaves only two motorized head axes: PAN and ROTATE.

## Motor selection rule
Do not select motors by outside diameter alone. Each axis must meet all of:
- 12 V preferred local supply;
- brushed gearmotor for simple DRV8871-class control unless a clearly superior ready-made solution is found;
- continuous output speed appropriate to inspection viewing, not high-speed motion;
- measured stall current within the selected driver and local head power budget;
- backlash low enough that the picture does not jump after direction reversal;
- a shaft/gear interface that can be manufactured and serviced;
- physical fit inside the source-like camera envelope.

Current `12V N20` entries remain placeholders until an exact purchasable article is frozen.

## Control strategy
Each axis uses closed-loop **position supervision** even if the first motor driver itself is simple PWM H-bridge.

Rev.A target functions:
- joystick/head command produces desired angular velocity while held;
- releasing the command stops the motor;
- soft angular limits prevent cable or mechanism damage;
- an absolute angle sensor/reference allows return-to-center and repeatable limits;
- current/time fault logic stops a jammed axis.

AS5600 ready-made modules remain candidates for non-contact angle sensing where the mechanical magnet/shaft geometry allows it. They are not yet frozen into the pressure head.

## Axis safety
A local head command watchdog is mandatory:
- stale UART command -> PAN=0 and ROTATE=0 immediately;
- head MCU reset -> both H-bridges disabled;
- sensor angle outside allowed range -> motion further toward the limit inhibited;
- overcurrent/time fault -> affected axis disabled and fault returned to crawler controller.

Light output also returns to a conservative state after a local head-controller reset.

## Mechanical development sequence
1. A3.0 passes camera + lighting + local harness tests.
2. Build one open PAN axis outside a sealed housing and determine motor/gear ratio/current/backlash.
3. Build one open ROTATE axis and repeat.
4. Combine both axes on the A3 fixture.
5. Cycle the six-core harness through all PAN/ROTATE/manual-lift positions.
6. Only then design the sealed shafts, bearings, O-ring/seal grooves and final metal camera body.

## Release gate
Final sealed PAN/ROTATE CAD is blocked only by data that genuinely affects machining:
- exact motors;
- exact gear tooth counts/modules or selected purchased gear set;
- bearing/shaft diameters;
- angle-sensor magnet geometry;
- dynamic seal selection and groove dimensions;
- verified cable bend/twist envelope.

This prevents the project from machining a beautiful sealed head around an untested drive train.
