# PX-1 Rev.B — WB19 camera / lift / body / harness integration

Date: 2026-09-11  
Status: **PASS_SCREEN / MANUFACTURING HOLD**

## 1. Scope

WB19 closes the integration gap left by WB16 and WB18 between:
- the active Rev.PR six-wheel crawler body;
- the Rev.FN manual-lift kinematic datums used by the current camera work blocks;
- the WB18 fixed yoke + SP13 service connector;
- the WB16 LAPP 0027429 external lift harness and its `R_route >= 55 mm` rule.

This work block is an engineering screen, not machining release. It does not cancel the Rev.PF physical-measurement gate for the exact CRP150 lift geometry.

## 2. Hard architecture retained

No architecture change is made:
- 3 wheel stations per side / 6 wheels total;
- X50 / X150 / X250;
- rear X250 long axle remains the drive input;
- five Z50 module-1 side gears per side;
- manual lift;
- separately sealed camera;
- no cartridge/cassette mechanics;
- SP13 remains fixed to the non-TILT portion of the removable head;
- LAPP 0027429 remains the selected prototype external head harness;
- cable dynamic design bend radius remains 55 mm minimum.

## 3. WB16 correction — actual cable exit, not camera axis

WB16 used the camera-axis/head-pivot movement as a proxy for harness movement and therefore reported only about 2.16 mm change in straight anchor distance.

That is not a valid manufacturing assumption after WB18, because the actual SP1310 cable exit is offset from the camera axis.

For the current WB18 connector placement the actual cable-exit offset is approximately:
- `+120.5 mm` in X;
- `+20.0 mm` in Z.

Therefore the actual current WB18 cable exits are:
- LOW: `X204.057 / Z95.0 mm`;
- MID: `X203.351 / Z150.0 mm`;
- HIGH: `X255.700 / Z225.0 mm`.

The actual LOW-to-HIGH cable-exit displacement is about **139.88 mm**, not a ~2 mm harness-motion problem.

WB16 remains useful for the selected cable article, electrical drop screen and R55 rule, but its simple head-pivot routing conclusion is superseded by WB19.

## 4. Why the current WB18 connector location fails full body integration

The active Rev.PR controller saddle starts at `X218` and reaches approximately `Z110` on the crawler centre plane.

With the current WB18 SP13 placement:
- cable exit at LOW = `X204.057 / Z95.0`;
- forward space before the saddle = only **13.943 mm**;
- an R55 cable can deflect only about **1.797 mm** in that forward distance.

Even for only 3 mm cable-to-body design clearance, a Ø6.7 mm cable centre must reach about `Z116.35` over the saddle. From `Z95` that requires about **21.35 mm** rise; an R55 bend needs roughly **43.50 mm** forward run to create that rise.

Therefore the current WB18 SP13 position is **not routable around/over the Rev.PR saddle while respecting R55**. This is a real integration failure and is the reason WB18 must not be treated as manufacturing-released.

## 5. WB19 candidate connector datum

The structural WB18 rear bridge itself stays at its existing low datum (`DX +58 / DZ +20` from the camera axis).

The SP13 panel connector is moved on a new integrated fixed-yoke support to:
- panel plane: `X = camera axis +45.3 mm`;
- connector axis: `Z = camera axis +37.25 mm`;
- connector direction remains `+X` toward the crawler;
- SP13 still does not move with TILT.

At LOW (`camera axis X83.557 / Z75`):
- panel plane X = **128.857 mm**;
- connector axis Z = **112.25 mm**;
- cable exit X/Z = **187.357 / 112.25 mm**.

Executed CadQuery 2.8.0 screen results:
- fixed yoke + candidate SP13 ideal DN150 clearance: **5.048 mm**;
- moving WB18 camera minimum ideal DN150 clearance: **3.0405 mm** at approximately `TILT -61°`;
- moving camera vs candidate fixed package collision: **0.0 mm³** over `-105…+105°`, sampled every 1°.

The connector-position window is narrow. Positions farther forward collided with the TILT sweep; positions farther rearward did not leave enough run for R55 before the body saddle. Therefore `+45.3 / +37.25` is a **screen datum**, not a tolerance-free manufacturing coordinate.

## 6. R55 harness screen

Cable:
- LAPP `0027429`;
- UNITRONIC FD CY `7X0.25`;
- nominal OD 6.7 mm;
- WB16 design bend radius: `R >= 55 mm`.

### LOW / DN150 screen

A two-arc S-route is used so the cable leaves SP1310 along +X and becomes horizontal before the controller saddle.

Screen values:
- starting cable exit: `X187.357 / Z112.25`;
- route height over saddle: `Z116.35`;
- S-curve horizontal run: **29.752 mm**;
- S-curve arc length: **30.127 mm**;
- fixed strain-relief/interface screen datum: `X280 / Z116.35`;
- screened path length to that datum: **93.02 mm**;
- ideal DN150 cable clearance: **7.348 mm**;
- minimum central body clearance: **3.0 mm**.

The 3.0 mm body clearance is **not production-frozen** for wastewater service. It is only enough to prove geometric routability. Mud, grit, jacket swell, guide wear and assembly tolerances still require a physical jig/tube gate and may force a local body-guide redesign.

### MID / HIGH screen

Using the same candidate SP13 datum and fixed strain-relief screen point:
- MID cable exit: `X186.651 / Z167.25`; shortest R55 free-route screen ≈ **107.74 mm**;
- HIGH cable exit: `X239.000 / Z242.25`; shortest R55 free-route screen ≈ **158.74 mm**.

MID/HIGH are not DN150 operating positions. The calculations only prove that R55 geometry can connect the moving head to the fixed interface without requiring a sub-R55 bend.

A real cable has constant cut length, so these shortest-path values must **not** be used as the final cut length. The final cable length, slack shape, guide and clamp coordinates remain a LOW/MID/HIGH physical-jig gate.

## 7. What is now frozen vs still HOLD

Frozen at screen level:
- actual SP13 cable-exit motion must be used for harness calculations;
- WB16 ~2.16 mm head-pivot span is not a harness-travel release value;
- current WB18 connector datum fails R55/full-body integration;
- candidate SP13 direction stays +X and fixed relative to the yoke;
- screen datum `DX +45.3 / DZ +37.25` is the current integration candidate;
- R55 and Ø6.7 mm remain mandatory for the LAPP 0027429 prototype harness;
- six-wheel X50/X150/X250 architecture remains hard-locked.

Still HOLD:
1. exact CRP150 lift dimensions per Rev.PF physical/detail measurement gate;
2. final SP13 support-bracket solid, fasteners and stiffness;
3. body-side strain relief / sealed feedthrough article and mounting boss;
4. LOW cable guide/saddle material and wear geometry;
5. constant final harness cut length and controlled slack shape;
6. measured LAPP 0027429 OD and real bend behaviour;
7. measured SP13 body/backshell dimensions;
8. real fastener heads and camera home/stop hardware;
9. complete real wheel profile rather than Ø90 cylinder placeholders;
10. physical DN150 pipe sweep including ovality, debris and mud allowance;
11. all WB18 camera physical-sample qualification gates.

## 8. Next controlled work block

**WB20 should detail the fixed SP13 support + body-side harness guide/strain-relief/feedthrough as real serviceable hardware.**

Do not change the six-wheel drivetrain, TILT architecture, camera pressure shell, or main tether architecture to solve this local harness problem.

## Change log

### 2026-09-11 — WB19
- integrated WB18 camera/yoke with Rev.PR body obstacle and WB16 R55 cable rule;
- corrected WB16 harness-motion proxy to use the actual SP13 cable exit;
- proved current WB18 connector placement cannot route past the controller saddle at R55;
- searched a collision-free/routable connector window;
- selected screen candidate `DX +45.3 / DZ +37.25`;
- executed full 1° TILT collision sweep for candidate fixed package;
- added LOW R55 S-route plus MID/HIGH free-route screens;
- retained manufacturing HOLD because the 3 mm body margin and physical lift dimensions are not release-ready.
