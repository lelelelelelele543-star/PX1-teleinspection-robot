# PX-1 Rev.AR — tolerance stack and field tool access

Status: engineering verification, not machining release.

## Rear wheel axial stack
Nominal shaft working length: 62.0 mm.
Controlled stack targets:
- 6000-2RS bearing width: 8.0 mm nominal
- spacer: 3.0 mm target
- rotary seal: 7.0 mm nominal
- labyrinth/grease zone: 4.0 mm target
- external gear/hub zone: 8.0 mm target
- wheel hub: 18.0 mm
- washer + M8 retention allowance: 6.0 mm target

Nominal occupied length = 54.0 mm, leaving 8.0 mm design reserve for shoulders, axial clearance and final purchased-part tolerances.

## Axial-clearance rule
Do not clamp the rotary seal axially with the wheel/gear stack. Bearing location and seal location are controlled by machined shoulders/carrier. External wheel/gear retention must remain independent.

Target assembled free axial clearance for external removable stack: 0.20–0.50 mm before final locking method is frozen.

## Tool envelopes
- M8 retention: reserve cylindrical socket envelope Ø20 mm minimum around fastener axis.
- M4 cover screws: reserve Ø12 mm driver/bit envelope and straight approach.
- No cover screw may be hidden behind a wheel.
- Side cover must be removable before wheel/gear service.
- No service operation may require opening the dry electronics body for ordinary wheel/gear replacement.

## Radial clearances
Prototype minimum moving-to-fixed clearance:
- rotating gear to cover: >=2.0 mm nominal
- rotating wheel/hub to cover: >=2.0 mm nominal
- gear to body/protective wall: >=1.5 mm nominal
- socket/tool to adjacent fixed geometry: >=1.0 mm nominal during service

These are prototype dirt-tolerant targets, not precision gearbox backlash values.

## Fastener decision
Keep M8 external retention for prototype because it is robust and field-serviceable. Exact nut form remains HOLD until the wheel hub and shaft end are finalized. Preferred direction: standard stainless self-locking nut or prevailing-torque all-metal nut; do not release drawing until exact standard and available part are selected.

## Release gate
Wheel hub, side cover and rear shaft may move from PROTOTYPE to DRAWING-CANDIDATE only after:
1. FreeCAD interference check passes at nominal geometry;
2. tolerance stack passes worst-case purchased bearing/seal widths;
3. Ø20 socket envelope is clear;
4. all M4 cover screws have direct tool approach;
5. selected M8 hardware is purchasable and its dimensions are entered into CAD/BOM;
6. physical printed mock-up confirms hand/tool access.
