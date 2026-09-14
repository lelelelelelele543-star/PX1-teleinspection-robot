# PX-1 Rev.B WB24A — flush PRESSURE valve / fill interface

Date: 2026-09-14
Status: **SOURCE TOPOLOGY CONFIRMED / PX1 PROTOTYPE ARCHITECTURE SELECTED / LEAK TEST HOLD / MACHINING HOLD**

## 1. Reason for this block

WB23F showed that a conventional exposed pressure valve is the limiting fixed item for LOW / ideal DN150. A Ø14 x 6 mm exposed valve leaves only about 4.70 mm ideal clearance; taller parts quickly consume the margin.

MiniCam source evidence shows that Proteus/CAM026 does not require a permanently tall external Schrader stem. The source architecture uses a compact protected valve with a removable protection cap and a separate screw-on pressure adaptor.

PX-1 will therefore use the same **functional idea**, with independently designed metric parts.

## 2. Confirmed MiniCam source evidence

Repeated source parts across CAM026 / crawler cover assemblies:

- `FSS-001-843` — CAMERA VALVE SHAFT;
- `FSS-001-844` — CAMERA VALVE COVER;
- `BEA-001-845` — 4MM BALL BEARING;
- `SEA-001-846` — 3 x 1 O-RING, quantity 2 in the valve source assembly;
- `SPR-001-847` — VALVE SPRING;
- `SEA-001-848` — 6 x 1.5 O-RING.

A separate MiniCam source BOM identifies `SPR-001-847` as:

- wire diameter `d = 0.5 mm`;
- outside diameter `De = 3.7 mm`;
- free length `L0 = 7.9 mm`.

The individual shaft/cover manufacturing drawings have not been found in the current source set, so **no unshown MiniCam dimension is copied or invented**.

Official Proteus operating instructions independently confirm the service topology:

1. unscrew pressure-valve protection cap;
2. screw on the pressure-valve connection adaptor;
3. fill with regulated CO2/Nitrogen;
4. remove adaptor;
5. refit protection cap.

The Ex instruction also shows a purge screw on the pressure adaptor for controlled depressurisation.

## 3. PX-1 functional architecture

Controlled concept:

`WB23E service cover -> recessed metric service port -> spring/pressure-assisted check element -> removable low-profile protection cap`

Service tool:

`threaded pressure adaptor -> centre opening probe + gas passage -> regulator/hose -> compressor/CO2/N2 source`.

The adapter is present only during servicing and is **not part of the DN150 driving envelope**.

The protection cap is debris protection and a secondary seal. The internal check element is the primary gas-retention device.

## 4. PX-1 prototype geometry — screen values

These are independent PX-1 prototype values, not claimed as original MiniCam dimensions.

### Top service interface

- location retained from WB23E/F: nominal `X273 / Y0`;
- service thread candidate: **M8 x 1** internal/female thread;
- protection-cap outside diameter: **<=12 mm**;
- protection-cap exposed height in driving condition: **<=1.5 mm target**, hard screen <=2.0 mm;
- cap head should be flat/rounded and snag-resistant;
- cap may contain a small dirt/water O-ring but must not be the sole pressure-retaining element.

M8 x 1 is chosen provisionally because it is compact, metrically machinable and leaves room inside the WB23E 86 x 44 x 6 cover. Final thread may reopen after prototype adapter testing.

### Internal valve envelope

Reserve below the top port:

- valve/check envelope OD <=10 mm;
- depth below service-cover top <=18 mm nominal;
- lower retainer/service features remain inside the dry service cavity;
- no part of the internal valve is allowed to reduce the main electronics service opening below practical connector access.

A separate dry six-way Micro-Fit connector is kept toward the opposite side of the 48 x 22 service opening.

## 5. Prototype A — source-inspired guided check valve

This is the preferred first machined experiment because it follows the proven source topology without pretending to know proprietary dimensions.

Elements:

- 1 x stainless 4.0 mm precision ball;
- 1 x replaceable soft FKM seat around the gas orifice;
- 1 x short guided valve/push shaft, approximately 3 mm class;
- 2 x 3 x 1 mm FKM O-rings on/around the guided shaft as secondary sealing/guiding elements;
- 1 x small compression spring, source envelope near `d0.5 / De3.7 / L0 7.9` as a starting geometry only;
- 1 x lower perforated spring retainer;
- M8 x 1 top service thread;
- low-profile protection cap;
- screw-on fill/purge adaptor.

Primary closing action:

- spring closes the check element when unpressurised;
- positive internal crawler pressure assists closing/seating;
- the pressure adaptor mechanically pushes the guided element open while screwed in, so opening does not depend on a narrow differential-pressure window;
- after adaptor removal the valve closes before the protection cap is refitted.

This is deliberately simple and avoids a permanently projecting valve stem.

## 6. Prototype B — simplified ball check

Build one comparison insert without the guided shaft/dynamic shaft O-rings:

- 4 mm ball;
- replaceable soft seat;
- small spring;
- lower retainer;
- same M8 x 1 cap/adaptor interface.

The adaptor probe acts directly on the ball/check element.

Purpose of B:

- determine whether the guided shaft is actually necessary;
- reduce moving seals and manufactured parts if the simpler insert leaks less and survives contamination better.

Do not choose A merely because MiniCam used a shaft; choose the simpler design if testing proves it equal or better.

## 7. Protection cap and pressure adaptor

### Driving cap

Target:

- OD <=12 mm;
- exposed height <=1.5 mm preferred;
- M8 x 1 male thread matching service port;
- broad shallow slot / 2-hole pin-spanner / internal hex only if it remains mud-cleanable;
- no tall knurling;
- tethering is optional only if it does not create a snag hazard.

### Fill/purge adaptor

Bench/field tool, not carried in pipe:

- M8 x 1 male nose;
- centre probe opens valve mechanically;
- radial/axial gas passage around probe;
- opposite end accepts standard regulated hose/compressor connection;
- integrated small purge screw preferred so crawler pressure can be deliberately reduced before the service cover is opened;
- adapter must never be used without a pressure regulator.

The user's existing compressor gun can be connected through the tool-side adaptor rather than forcing a tire valve stem into the crawler roof.

## 8. Pressure and force design rule

Crawler normal prototype pressure remains approximately +0.25 bar gauge. Direct pneumatic force on a 3–4 mm class valve element is very small. The spring is therefore selected for reliable seating and contamination tolerance, not for resisting a large pressure load.

Do **not** select spring rate from the source spring dimensions alone. Coil count/material/preload of the original are not controlled. Start with low preload and tune on the bench so the screw-in adaptor opens the valve positively while the released adaptor always leaves a leak-free seat.

## 9. DN150 improvement

Replacing the WB23F Ø14 x 6 exposed-envelope screen with a cap <=Ø12 x 1.5...2.0 mm moves the pressure-port external envelope below the current WB23E cover as the limiting top feature.

Expected consequence:

- pressure valve is no longer the ~4.70 mm DN150 bottleneck;
- top package becomes limited by the service-cover/screw geometry, currently ~7 mm class ideal clearance;
- exact result is checked in the WB24A executable CAD screen before release.

## 10. Contamination/service rules

- valve mouth receives a removable protection cap whenever crawler is in service;
- first internal passage must be drain/cleanable after cap removal;
- seat is replaceable from the underside when service cover is removed;
- no threadlocker is allowed where it could enter the valve passage;
- do not use the protection cap to force a leaking internal valve shut;
- if the primary check leaks, replace/repair valve before wet operation.

## 11. Prototype materials

Candidate starting set:

- ball: AISI 316/440C precision 4 mm, corrosion test decides final grade;
- shaft/retainer: 316L stainless or equivalent corrosion-resistant material;
- seat/seals: FKM first wastewater/chemical candidate;
- service cover: existing EN AW-6082-T6 WB23E cover;
- spring: stainless spring wire; source size is only a geometry starting point;
- adaptor: stainless or nickel-plated brass; final material chosen to avoid galling/corrosion with cover thread.

## 12. Qualification sequence

1. machine/print transparent or open bench mock-up first to observe opening stroke;
2. make Prototype A and B inserts;
3. test dry at 0 / +0.25 / +0.5 bar;
4. connect/disconnect pressure adaptor 100 cycles;
5. perform 30 min decay at +0.25 bar without protection cap — primary valve itself must hold;
6. repeat with cap installed;
7. submerged bubble test;
8. contaminate external mouth with water/fine grit, clean normally, retest;
9. verify purge adaptor can reduce pressure to ambient before cover opening;
10. install winning insert in WB23E cover and run physical DN150 jig;
11. only then release thread/seat/groove dimensions.

## 13. Release state

WB24A freezes the **functional architecture**, not final machining dimensions.

The current pressure-valve procurement search for tall commercial Schrader-style bodies is stopped as baseline. A standard recessed commercial valve core may still be kept as a fallback comparison, but the crawler exterior will retain a Proteus-like low-profile capped service port.
