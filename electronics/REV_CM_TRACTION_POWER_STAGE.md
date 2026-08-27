# PX-1 Rev.CM — traction motor power stage

Status: engineering candidate, not final release.

## Architecture
- 48 V tether input remains isolated from traction motors by the main 48→24 V DC/DC.
- Traction rail: 24 V nominal.
- Two independent BTS7960 H-bridge modules: LEFT and RIGHT drive sides.
- Each H-bridge feeds the motors of one side only. No shared motor output between bridges.
- MCU control is logic-side only; traction current never passes through controller PCB traces.

## Protection per traction channel
Each LEFT/RIGHT motor-driver branch shall include:
1. dedicated branch fuse upstream of BTS7960;
2. local bulk capacitance directly at driver supply terminals;
3. local high-frequency ceramic decoupling;
4. bidirectional current measurement on branch or motor return;
5. temperature monitoring on/near BTS7960 heatsink;
6. short, twisted motor leads routed away from camera/data pair.

Fuse values remain HOLD until actual JGB37-520 stall current is measured. Do not size fuses from nominal running current only.

## Emergency stop philosophy
Emergency stop must remove traction energy independently of firmware.
Preferred prototype architecture:
- hardware-controlled high-side disconnect/contactor on the 24 V traction rail;
- MCU may request shutdown, but cannot prevent hardware E-stop from removing traction power;
- camera, communications and pressure telemetry may remain powered during traction E-stop so the operator retains visibility and diagnostics.

## Braking / reverse energy
BTS7960 can return motor energy to its DC supply during active braking/reversal. The 24 V rail must therefore be treated as bidirectional/transient rather than as a purely consuming load.

Rules:
- avoid instant full-forward to full-reverse commands in firmware;
- command controlled deceleration ramp before direction reversal;
- provide local electrolytic energy storage at traction bus;
- measure 24 V bus overshoot at worst-case wheel speed and load;
- if the selected 48→24 converter cannot absorb reverse energy, add a dedicated clamp/dump path on the 24 V rail.

Final TVS/clamp voltage and dump resistor are HOLD until bus overshoot is measured with the actual motors and converter.

## Current sensing
Preferred: one current sensor per LEFT/RIGHT traction branch so the controller can detect:
- jammed wheel/gear;
- stalled motor;
- asymmetric mechanical load;
- sudden debris blockage;
- damaged gearbox.

Sensor technology can be Hall-based or low-ohmic shunt with isolated/current-sense amplifier. Final part selection follows measured peak current.

## Software limits
Firmware shall implement:
- acceleration/deceleration ramp;
- configurable continuous-current warning threshold;
- configurable hard-current trip threshold with short delay for startup surge;
- left/right current comparison diagnostics;
- motor-output inhibit on communication loss;
- neutral output at boot until valid command received.

Software limits supplement hardware protection and do not replace fuses/E-stop.

## Bench tests before release
1. measure no-load current per motor;
2. measure loaded running current;
3. measure locked-rotor current with a current-limited bench setup and very short duration;
4. scope 24 V rail during acceleration, coast, brake and reversal;
5. test one wheel mechanically blocked;
6. verify fuse coordination and hardware E-stop;
7. verify driver/heatsink temperature during 30 min representative operation;
8. verify camera/data link remains stable during repeated motor starts/stops.

## Current release blockers
- exact JGB37-520 motor SKU and measured stall current;
- actual BTS7960 module thermal performance;
- 48→24 converter reverse-energy behavior;
- chosen current sensor;
- final fuse values;
- final 24 V clamp/dump network.
