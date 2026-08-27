# PX-1 Rev.DO — rugged tether / tail mechanical interface

Status: architecture freeze for the cable mechanical path. Exact connector manufacturer remains HOLD.

## Design rule
The PX-1 tether is **not an Ethernet patch cable**.

It is a purpose-built robotic inspection tether. Ethernet/SPE is only the electrical protocol carried by one protected balanced pair inside the tether.

## Tether construction target
Prototype/final family target:
- hydrolysis-resistant PUR/TPU outer jacket;
- abrasion, oil, water, sewer-contaminant and repeated-flex resistance;
- dedicated aramid/Kevlar or UHMWPE/Dyneema tensile member;
- 2 x 1.5 mm² power conductors baseline for 48 V distribution;
- 2 shielded twisted pairs preferred: one active data pair and one spare/service pair;
- overall diameter target roughly 8–12 mm after real cable selection;
- temperature target at least -30…+70 °C class;
- tensile member carries crawler pull load, copper conductors do not.

## Electrical allocation concept
Long tether:
- +48V power;
- 0V power;
- shielded balanced pair A: 10BASE-T1L digital video + packet telemetry/control;
- shielded balanced pair B: spare / independent safety-service bus / future use.

No CVBS, NTSC, PAL or coaxial video conductor is required.

## Tail load path
The rear tail is split into two independent functions:

### 1. Mechanical towing termination
Tether strength member terminates in a dedicated metal clamp/anchor integrated into the rear structural tail.

Required sequence:
`tether jacket -> long bend/strain relief -> outer compression/grip -> exposed/terminated tensile member -> structural anchor`.

The anchor transfers pull directly into the crawler body.

### 2. Electrical connector
After the mechanical anchor, power/data conductors have a relaxed service loop to the sealed electrical connector.

Electrical contacts must never carry tether tensile load.

## Reference lesson from uploaded Proteus cable drawings
The original cable-end architecture uses multiple mechanical layers including connector housing, spring/strain element, cable housing/nut, O-rings, cable gland, PU tubing, hose crimp and adhesive-lined heat shrink.

PX-1 keeps this robust layered philosophy while using its own cable and modern digital connector allocation.

## Field-retermination requirement
The tail must be repairable without replacing 100–150 m of tether.

Target field procedure:
1. cut damaged last section of tether cleanly;
2. strip outer jacket to a fixed gauge length;
3. expose and mechanically terminate the aramid/UHMWPE strength member;
4. fit gland/strain-relief parts;
5. terminate crimp contacts for power/data;
6. assemble connector and rear boot;
7. electrically test pair continuity/insulation;
8. pressure/leak-test the tail before deployment.

No potting compound is the only means of mechanical retention.

## Connector requirements
Exact model remains HOLD, but the production connector must be:
- genuinely waterproof when mated;
- keyed and fast to connect with wet/gloved hands;
- panel receptacle mechanically fixed to the rear body;
- replaceable separately from the tether;
- minimum 2 high-current power contacts plus at least 4 signal contacts, or equivalent mixed-contact arrangement;
- signal contacts/pair geometry verified for the selected differential link;
- corrosion-resistant shell and contacts.

The earlier hybrid connector concept with dedicated coax contacts is no longer a design requirement because the video path is digital.

## Bend protection
Rear boot/strain relief must control the minimum bend radius rather than simply making the cable locally rigid.

Target:
- gradual 80–120 mm long flexible tail support depending on selected cable OD;
- no sharp clamp edge against PUR jacket;
- replaceable sacrificial outer anti-abrasion sleeve at the crawler tail.

## Pull test gates
Before release:
- static tether pull test with connector electrically disconnected from load path;
- target working pull class >=1 kN until real cable spec is frozen;
- proof pull set from selected tether manufacturer data, not guessed;
- repeated bend/pull cycles;
- mud/wash test;
- pressure leak test after retermination;
- data BER/link-margin test at 150 m equivalent.

## Rear service layout
Keep the rear architecture simple:
- one tether mechanical anchor;
- one sealed quick electrical connector;
- one protected pressure-fill/service port;
- one lowering/recovery eye connected to structure.

No antennas and no operator E-stop button are mounted on the crawler itself.
