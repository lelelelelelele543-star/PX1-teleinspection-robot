# PX-1 Rev.CI — tether power voltage-drop study

Status: design calculation for 40/100/150 m tether. Not final production rating.

## Assumptions
Copper conductor resistivity at ~20 C: 0.0175 ohm*mm2/m.
Round-trip loop resistance R = 2*rho*L/A.

### Loop resistance
- 1.0 mm2: 40 m = 1.40 ohm; 100 m = 3.50 ohm; 150 m = 5.25 ohm
- 1.5 mm2: 40 m = 0.933 ohm; 100 m = 2.333 ohm; 150 m = 3.50 ohm

Actual hot-cable resistance will be higher; add temperature/contact margin in final design.

## Key consequence
Power should not be transmitted at 24 V over 100-150 m if crawler peak power is substantial. Cable current and I^2R loss become too high.

Example at 150 m using 1.5 mm2 pair:
- 100 W load at 24 V -> ideal current 4.17 A; cable loss ~60.8 W before converter losses: unacceptable.
- 100 W load at 48 V -> ideal current 2.08 A; cable loss ~15.2 W: still significant but practical with local conversion and power budgeting.

For 1.0 mm2 at 150 m the same 48 V / 100 W case would lose ~22.8 W, therefore 1.5 mm2 is strongly preferred for the long tether.

## Baseline recommendation
- Tether DC bus: nominal 48 V.
- Power pair: 2x1.5 mm2 finely stranded copper minimum candidate.
- Robot local conversion: isolated/protected 48->24 V DC/DC for traction and 48->12/5 V branches as required.
- Main motor bus remains 24 V locally; do not redesign every actuator for 48 V.
- Use soft-start/inrush limiting and input TVS/reverse-polarity protection at crawler.
- Measure tether voltage at the robot and expose it in telemetry.

## Cable architecture candidate
- 2x1.5 mm2 power;
- 1 shielded twisted pair for 10BASE-T1L;
- optional second shielded pair for service/fallback;
- aramid/Dyneema strength member independent of copper;
- hydrolysis-resistant PUR/TPU outer jacket.

## Why 48 V
Relative to 24 V, delivering the same power at 48 V approximately halves current and quarters cable I^2R loss. 36 V is usable but gives less margin and is less convenient for standard industrial DC/DC modules. 48 V therefore becomes the PX-1 long-tether baseline unless later safety/regulatory constraints require otherwise.

## Release gates
1. measure real peak and continuous crawler power;
2. obtain actual candidate cable conductor resistance per km;
3. include +temperature conductor resistance;
4. verify connector current/contact resistance;
5. size fuse/breaker and DC/DC input range for worst-case remote voltage;
6. bench-test at equivalent 150 m loop resistance before field deployment.
