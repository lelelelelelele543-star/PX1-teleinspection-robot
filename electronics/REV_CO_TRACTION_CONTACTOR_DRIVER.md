# PX-1 Rev.CO — traction contactor and hardware driver

Status: engineering candidate. Final current rating remains HOLD until JGB37-520 stall-current measurements are completed.

## Selected engineering reference
Current robust reference: TE Connectivity / KILOVAC LEV100A5ANG, 24 VDC coil, environmentally sealed, SPST-NO DC contactor.

Manufacturer data used for architecture:
- 24 VDC nominal coil;
- coil resistance about 96 ohm;
- nominal coil current about 250 mA;
- nominal coil power about 6 W;
- environmentally sealed construction;
- contactor class is far above PX-1 expected traction current, therefore this is a reliability/reference option, not yet a cost/size optimized production freeze.

## E-STOP chain
24V_AUX -> E-STOP NC contact -> optional service interlock NC -> coil driver -> contactor coil -> return.

The traction contactor switches only the 24 V motor-power bus feeding both BTS7960 channels. Camera, controller, telemetry and communications remain powered when E-STOP is pressed.

A second independent E-STOP contact must force both BTS7960 enable lines LOW. Thus a single firmware fault cannot keep traction enabled after E-STOP.

## Coil driver
Do not drive the contactor coil directly from STM32.

Candidate low-side stage:
- logic-level N-MOSFET rated >=60 V;
- gate series resistor 47–100 ohm;
- gate-source pulldown 47–100 kohm;
- flyback suppression directly across coil;
- prefer diode + TVS/Zener clamp rather than only a slow diode if release time proves excessive;
- local 100 nF + bulk decoupling on 24 V auxiliary branch.

The physical E-STOP must remove coil drive independently of MCU state. MCU may request TRACTION_ENABLE, but cannot override an open E-STOP chain.

## Feedback
Production architecture should include contactor-state feedback. Preferred method: auxiliary contact if selected contactor version provides one. Otherwise verify traction-bus voltage downstream of the contactor using an isolated/divided measurement channel.

Fault examples:
- command OFF but downstream 24 V remains present -> possible welded contactor;
- command ON but downstream bus absent -> contactor/coil/fuse/interlock fault.

## Serviceability
- contactor mounted as a replaceable module;
- ring/fork terminals or robust locking connector, no soldered-in power component;
- coil suppression located with contactor/driver, not meters away;
- label input/output polarity if selected DC contactor has polarity-sensitive arc suppression.

## Freeze gates
1. Measure one JGB37-520 motor no-load, loaded and locked-rotor current at actual 24 V.
2. Repeat cold and warm where practical.
3. Calculate worst-case two-side simultaneous current and fuse coordination.
4. Then decide whether LEV100-class contactor is retained or replaced by a smaller 30–50 A sealed DC-rated unit.
5. Verify E-STOP opening under worst-case motor load and check 24 V bus transient with oscilloscope.

Do not substitute an ordinary automotive relay unless its DC breaking rating, sealing, contact life and measured interruption behavior are verified for the PX-1 traction load.
