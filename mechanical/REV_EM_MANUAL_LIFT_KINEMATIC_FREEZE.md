# PX-1 Rev.EM — CRP150-style manual lift kinematic freeze

Status: prototype geometry freeze for integration; exact gas-spring article remains a physical-sample gate.

## Basis
This revision keeps the architecture already extracted from the uploaded Proteus/CRP150 lift drawings: paired side arms, manual M8 clamp, disc-spring preload, serviceable pins/bushings and a 150 N-class gas spring. The geometry below is PX-1-specific.

## Frozen functional architecture
- one-hand manual camera lift;
- true parallelogram: two equal links per side keep the camera cradle approximately level while height changes;
- no lift motor;
- M8 adjustable clamp carries the static holding function;
- gas spring only counterbalances weight and must not be the sole position lock;
- hard LOW/DN150 stop is mechanical;
- HIGH travel is physically blocked when the DN150 stop pin is installed.

## Current datum geometry
Crawler coordinates remain those of the current six-wheel master:
- body top nominal Z = 90 mm;
- wheel axis Z = 45 mm;
- ideal DN150 pipe-axis datum approximately Z = 52.05 mm;
- camera head design envelope Ø52 x 72 mm.

Lift baseline:
- lower/main pivot axis: X = 200 mm, Z = 94 mm;
- link effective length: 120 mm;
- paired arm thickness: 4 mm stainless or 5 mm Al 7075/6082 after stiffness test;
- main pivot pins: Ø8 mm;
- replaceable POM/iglidur/bronze bushings;
- camera-axis offset above moving upper pivot: +10 mm nominal.

The arms extend toward the crawler front. This allows the camera head to fold forward and low rather than forcing it above the body roof.

## Indexed positions
Using the current idealized parallelogram:

### LOW / DN150 SAFE
- camera axis Z = 75 mm;
- arm angle ≈ -14.0° relative to horizontal;
- moving upper pivot X ≈ 83.6 mm;
- this is the only released DN150 lift position until a real-pipe sweep proves otherwise.

### MID
- camera axis Z = 130 mm;
- arm angle ≈ +12.5°;
- moving upper pivot X ≈ 82.9 mm;
- intended for larger pipe only.

### HIGH
- camera axis Z = 205 mm;
- arm angle ≈ +57.3°;
- moving upper pivot X ≈ 135.2 mm;
- final maximum is still subject to rollover/stability and tether-pull tests.

The moving X coordinate is intentionally not constant; a CRP-style manual lift trades some fore/aft movement for compact folded height.

## DN150 safety rule
The previous Rev.DE target of Z≈95–105 mm for DN150 SAFE is superseded. The current combined crawler/camera clearance work supports a conservative DN150 camera-axis target around Z=75 mm, not 100 mm.

Mechanical implementation:
- captive Ø6 stop pin or shoulder stop blocks the linkage above LOW/DN150;
- stop feature acts on a steel insert/shoulder, not directly on a soft aluminum edge;
- operator cannot accidentally lift into the DN150 crown while the stop is installed.

## Clamp stack
Baseline:
- M8 adjustable clamping lever;
- hardened stainless clamp axle;
- Belleville stack sized to preserve clamp load after wet/dirty cycles;
- stainless thrust washers;
- replaceable friction washer/disc if testing shows metal-on-metal clamp drift.

Acceptance requirement: full camera head held for 10 min at worst lift angle with no measurable creep and with all electrical power removed.

## Gas spring
Retain 150 N class from the source architecture as the starting force class.

Do not freeze stroke or extended length yet. The current geometry shows that gas-spring mount location must be solved jointly with the link arc; a poor anchor location can produce almost no useful stroke or strongly varying moment.

Selection window for the physical prototype:
- 120–180 N;
- corrosion-resistant body/rod or protective boot;
- spherical/clevis serviceable ends;
- temperature at least -20…+70 °C, preferably wider;
- no gas spring geometry may create a dead-center lock that traps the lift.

## Service / fabrication
- all four main pivots removable with normal hand tools;
- no welded permanent axle;
- axial shims available for play correction;
- replaceable bushings;
- clamp and stop pin accessible with wheels installed;
- lift base bolts into reinforced bosses of the structural body, not the removable electronics cover.

## Release gates
1. full-solid arm/cradle model;
2. exact camera head solid, not Ø52 cylinder only;
3. DN150 sweep with TILT -105…+105° at LOW;
4. gas-spring line-of-action optimization;
5. 500 wet lift cycles;
6. clamp creep test;
7. HIGH-position rollover/tether-pull stability test.
