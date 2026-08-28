# ME-PX1-610 — first traction build order — Rev.GQ

Status: prototype manufacturing sequence; supersedes stale dimensional details in Rev.FZ while preserving its one-station-first philosophy.

## Objective
Do not machine six wheel stations and both complete side drives before the active Rev.GF/GL seal, bearing and gear stack has been physically proven.

The first build is deliberately split into three gates.

# Gate A — purchased-part metrology before cutting metal
Obtain and measure one sample minimum of every fit-controlled part used in the first wheel/X200 station:
- 6701-2RS 12x18x4;
- 61801-class 12x21x5;
- 61903-class 17x30x7;
- selected 18.72x2.62 X-ring or final replacement article;
- selected static axle-flange O-ring;
- 61800 10x19x5 for X200;
- selected 18x30x7 X200 shaft seal;
- actual Z50 gear blank/finished gear;
- actual bevel pair or prototype custom bevel sample;
- one exact Ø32 traction motor sample.

Record actual:
- ID/OD/width;
- seal lip/interference dimensions where measurable;
- bearing radial/axial play class if supplied;
- motor shaft D-profile, protrusion and mounting face dimensions;
- gear hub/bore/key dimensions.

No final bearing pocket or seal gland is released from catalog nominal dimensions alone.

# Gate B — one complete wheel station WS-01
Machine/build only one current Rev.GF wheel station:
- 1 wheel shaft;
- 1 axle flange;
- 1 local inner 6701 support feature/fixture;
- 1 61801;
- 1 61903;
- 1 X-ring and static flange seal candidate;
- 1 keyed Ø90 wheel core;
- 1 SR tread prototype;
- one recessed M8 axial wheel-retaining fastener arrangement.

Use a simple rigid test plate/fixture reproducing the real side-cover and P1 membrane datums. Do not require the full pressure body for this gate.

## WS-01 checks
1. bearing fits can be assembled without brinelling or loose rocking;
2. shaft spins freely by hand before seal insertion;
3. seal insertion does not damage lip or X-ring;
4. measure breakaway and running drag after seal installation;
5. wheel core/key assembles without forcing;
6. M8 axial retention does not clamp the rotating stack incorrectly;
7. shaft runout at wheel seat and seal land;
8. 2 h wet rotation test;
9. pressure decay test of the local sealed fixture;
10. remove/refit wheel 20 times and inspect key/seat/fastener.

Only after WS-01 passes are the remaining five wheel shafts/flanges duplicated.

# Gate C — one complete LEFT side-drive bench module
Build one full side, not the whole crawler:
- 3 proven wheel stations;
- five equal m1 Z50 gears on 50 mm pitch centers;
- wheel axes X50 / X150 / X250;
- intermediate gear center X100;
- X200 input Z50;
- active Rev.GL internal-supported X200 shaft architecture;
- one Ø32 motor;
- supported small bevel shaft;
- compact 2.5:1 bevel candidate;
- real side cover / datum plate geometry.

A rigid bench plate may substitute for the complete P0 body only if all bearing and gear center datums exactly match the active CAD.

## LEFT side checks
1. hand-rotate motor/input with no wheel load: no tight spot through 20 revolutions;
2. record no-load drive current at several speeds;
3. verify all three wheel outputs rotate in the same direction;
4. blue/contact-pattern check on bevel if applicable;
5. inspect five-Z50 contact/backlash along the entire train;
6. run 30 min unloaded and 30 min representative loaded;
7. block each wheel individually for a short current-limited test;
8. verify no gear walks axially into cover or membrane;
9. record bearing/gear temperatures;
10. perform controlled forward/reverse cycles.

Only after this side passes should the RIGHT side hardware be duplicated.

# Gate D — pressure body / ballast / integrated prototype
After Gates A-C:
- machine the Rev.GP body with four blind ballast bosses;
- machine both side covers from the proven station datums;
- install both completed side drives;
- install front control tray and rear motor/power layout;
- add camera lift/head and structural tether tail;
- perform full DN150 sweep before electronics power-up;
- then run PX1-TP-020 traction/tether tests.

## Printed parts allowed before metal
Use Anycubic Chiron prints for:
- wheel/tread fit-check models;
- split elastomer casting molds;
- bearing/seal assembly gauges that do not contact final seal lips aggressively;
- gear-center alignment jig;
- side-drive transparent/open service mock-up;
- DN150 clearance gauges;
- electronics tray mock-up.

Do not use printed polymer as a substitute for the final pressure body, wheel shafts or pressure-critical bearing/seal flanges.

## Stop conditions
Stop duplication and correct the design if any first article shows:
- bearing seat looseness or excessive press fit;
- seal damage or high drag;
- visible shaft runout at the seal land;
- uneven Z50 contact pattern;
- bevel overheating/noise;
- motor current asymmetry not explained by measurement error;
- wheel key fretting;
- pressure decay outside the test limit;
- DN150 hard interference.

## Release principle
A failed first article is useful information. Six identically failed machined articles are waste. Therefore no quantity multiplication occurs until the relevant first-article gate has passed.
