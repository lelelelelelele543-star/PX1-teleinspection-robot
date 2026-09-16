# A2 — 40 m six-core tether: power architecture

Status: ARCHITECTURE SELECTED FOR BENCH QUALIFICATION / CABLE VOLTAGE RATING STILL HOLD.

## Decision
Do **not** distribute the crawler's 24 V bus directly over the 40 m tether.

For A2, the preferred power path is:

`touch-safe current-limited HV DC source at console -> POWER+ / POWER- tether cores -> crawler input protection + precharge/filter -> isolated wide-input DC/DC -> local 24 V crawler bus`.

Working source voltage for calculation: **110 VDC nominal**. This value is a design point, not permission to energize an unidentified cable. The final source voltage is released only after the tether insulation and every connector/contact voltage rating are known.

## Why 24 V direct feed is rejected
A long two-wire feeder has the resistance of the outbound and return conductors. Using 40 m tether length and hot-copper planning resistance:

`Rloop = 0.0175 Ω·mm²/m × 80 m / conductor_area × 1.20`.

For a 0.75 mm² power pair, `Rloop ≈ 2.24 Ω` in the hot-copper planning case.

A constant-power calculation then gives:
- 24 V / 48 W: only about 18.0 V reaches the crawler and about 15.9 W is lost in the cable;
- 24 V / 96 W: there is no stable constant-power operating point in this simple model;
- 24 V / 150 W: likewise not feasible.

So a 24 V tether makes crawler performance depend strongly on cable length and load. Raising the transmission voltage and converting locally is the robust architecture.

## 110 V planning cases
Candidate onboard converter: `Cincon CQB150W-110S24`.

Published values used by the A2 model:
- input 43…160 VDC, nominal 110 VDC;
- output 24 VDC / 6.3 A;
- 150 W class;
- full-load efficiency about 89%;
- full-load input current about 1.54 A at nominal input;
- isolated input/output;
- remote on/off and protection functions.

With the same 40 m, 0.75 mm² hot-copper planning loop:
- 96 W crawler output -> converter input ≈107.8 V, line current ≈1.00 A, cable loss ≈2.24 W;
- 150 W crawler output -> converter input ≈106.5 V, line current ≈1.58 A, cable loss ≈5.61 W.

A 0.50 mm² pair at 150 W still screens at about 104.6 V converter input and about 8.73 W cable loss. This is only an electrical-loss screen; it does not release 0.50 mm² cable for service.

## Six-core assignment
Frozen PX1 assignment:
1. `POWER+`
2. `POWER-`
3. `RS485_A`
4. `RS485_B`
5. `CVBS_SIGNAL`
6. `CVBS_RETURN`

No shield/braid may be used as normal power return. Any overall shield is EMC/chassis treatment only.

## Useful source analogue from the user's service archive
The iPEK six-wire cable repair instruction is useful as a construction reference, not as a claim about the PX1/Proteus cable. It specifies:
- black GND and violet VCC+ conductors: 0.75 mm²;
- four thin conductors: 0.14 mm²;
- green/white video pair;
- brown/yellow CAN pair;
- Kevlar reinforcement in the cable termination.

This confirms that a professional inspection cable can place the two heavier power conductors and four lighter signal conductors in one reinforced six-core tether. PX1 substitutes RS-485 for CAN and keeps its own CVBS interface. Exact PX1 tether construction remains H07 until its cable is identified.

## Crawler input block
A2 crawler-side order:
1. rear connector / strain relief;
2. service fuse or resettable protection appropriate to the selected cable/source;
3. polarity protection / reverse-energy strategy;
4. surge/transient clamp sized for the final source;
5. controlled precharge/inrush path;
6. input capacitor per DC/DC application requirements;
7. `CQB150W-110S24` or released equivalent;
8. protected local 24 V bus;
9. 24->12 V and 24->5 V local rails as required.

The converter manufacturer recommends external input capacitance. Therefore directly connecting an uncharged input capacitor to 110 V through a long cable is not accepted as the final design: A2 must use a current-limited source and qualify inrush/precharge.

## Console-side safety block
110 VDC is hazardous. A2 HV testing is allowed only with an enclosed, touch-safe, current-limited source and correctly voltage-rated connectors/test leads.

Required functions before a field/demo release:
- mains-side fuse and protective earth for the console power supply where applicable;
- DC output current limit;
- DC-rated isolation/switching device or power-supply remote enable;
- latched E-stop that removes traction/tether power independently of software;
- visible HV-present indication;
- discharge path so the tether does not remain charged after shutdown;
- connector arrangement that prevents exposed live pins;
- no reliance on an AC-only switch/relay rating for interrupting the DC tether.

Exact fuse, contactor/precharge resistor and discharge resistor values remain tied to the selected console supply and cable capacitance; they are not guessed in this revision.

## A2 physical qualification sequence
Before applying HV:
1. identify tether conductor construction, insulation rating and connector/contact ratings;
2. continuity + conductor-to-conductor short test;
3. insulation test appropriate to the cable's documented rating;
4. record end-to-end resistance of both power cores;
5. compare actual loop resistance with the calculator.

Powered tests:
1. energize with crawler electronics only, traction disabled;
2. verify DC/DC input and local 24 V;
3. run RS-485 traffic continuously;
4. verify CVBS image simultaneously;
5. enable one traction side, then both;
6. step load toward the A1/A0 measured maximum;
7. test forward/reverse transitions and lighting changes while watching video/link errors;
8. record source voltage/current, crawler DC/DC input, local 24 V, motor currents and temperatures;
9. E-stop and command-timeout tests;
10. repeat with all 40 m deployed, not coiled tightly under high load.

## PASS gate
A2 passes only when, over the real 40 m tether:
- the converter input remains inside its qualified range under worst tested load;
- the 24 V local bus stays in the accepted operating band;
- no unintended resets occur;
- RS-485 has no motion-producing corrupt-frame failure;
- video remains usable during motor/lighting switching;
- cable/connector temperatures remain acceptable;
- E-stop removes traction/tether energy as designed;
- cable and connector voltage ratings are documented.

`A2_TETHER_POWER.md` does not release 110 V field operation by itself. It selects the architecture and the tests needed to release it.
