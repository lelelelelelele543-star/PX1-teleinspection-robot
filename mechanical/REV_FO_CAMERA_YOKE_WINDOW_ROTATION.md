# PX-1 Rev.FO — camera yoke, front window and internal ROLL architecture

Status: prototype mechanical baseline, not production release.

## Source lessons retained
Uploaded CAM026 documents show several robust ideas that are worth preserving without copying proprietary geometry:
- camera housing and rear cover are separate service parts;
- multiple static O-rings isolate housing interfaces;
- illumination is a separate light-ring assembly;
- camera pan/rotation uses dedicated gears and bearings rather than making the electrical connector structural;
- the rotate connector assembly contains a dedicated slip ring and its own O-ring-sealed metalwork;
- the bearing-housing assembly uses a separate rotate motor, gear, encoder gear and seal flange.

PX-1 keeps these service and sealing principles but uses a fully digital internal camera and its own dimensions.

## External head
Current target envelope:
- fixed outer shell OD 52 mm;
- nominal overall shell length 72 mm before any final connector/latch correction;
- material EN AW-6082 T6 candidate;
- wall 2.5 mm nominal in Rev.FN packaging model;
- whole shell TILT range -105..+105 deg in the lift yoke;
- internal camera cartridge ROLL continuous 360 deg.

## Yoke
Prototype yoke:
- two 5 mm aluminum/stainless cheeks;
- nominal outside half-width 34 mm from centerline;
- Ø8 transverse tilt pivots;
- rear bridge ties both cheeks together;
- cheeks protect the optical front from direct side impact;
- yoke carries all TILT loads; electrical connector carries none.

The LOW-position numeric DN150 check remains acceptable with the current yoke envelope, but real screw heads and cable routing must still be included.

## Front optical stack
Target service stack from front inward:
1. replaceable front retaining ring;
2. sapphire or tempered glass window, approximately Ø28 x 3 mm candidate;
3. static FKM O-ring;
4. machined window shoulder in the fixed outer shell;
5. black optical separator around the lens;
6. separate annular LED MCPCB.

Rules:
- window is mechanically captured, never adhesive-only;
- no LED cavity light path directly into the lens cavity;
- sealing land is metallic and continuous;
- front retainer is removable without disturbing internal ROLL bearings.

Current Rev.FN model uses a Ø30 optical clear aperture as a conservative starting envelope.

## Lighting
Keep the separate-ring philosophy from the source camera:
- annular aluminum MCPCB around the optical aperture;
- current project baseline 6 white high-power LEDs;
- shell is the heat sink;
- LED return is separate from data reference/shield;
- front ring can be serviced independently from camera electronics.

## Internal ROLL cartridge
The rotating cartridge contains:
- digital camera PCB and lens carrier;
- two spaced radial bearings;
- ROLL driven gear;
- home/index magnet or encoder target;
- Ethernet-capable miniature rotary transfer.

The rotary electrical transfer is non-structural. Bearings carry the cartridge, not the slip ring.

Because PX-1 uses digital video, the old CAM026 electrical slip-ring topology is only a mechanical/service reference. Exact digital rotary transfer remains procurement-gated.

## TILT drive
The entire fixed shell turns in the yoke.

Drive baseline:
- compact geared motor in the fixed cradle/yoke region;
- self-holding worm or high-reduction spur/worm combination preferred;
- independent hard stops slightly outside the ±105 deg software range;
- absolute/home reference;
- serviceable gear cover.

## Quick removal
The complete head must be removable without opening P0.

Target:
- keyed cylindrical/spigot mechanical interface;
- retained latch or captive clamp screw;
- static O-ring only if the cradle/head interface itself forms a pressure boundary;
- connector recessed/protected behind the mechanical register;
- latch takes axial retention; connector takes no impact or bending load.

## Pressure strategy
Preferred architecture remains a fully sealed camera head as its own pressure volume rather than sharing crawler P0 directly.

Prototype pressure:
- same normal positive-pressure class as crawler (+0.20..+0.30 bar gauge) if practical;
- independent leak test before fitting to crawler;
- structural proof pressure tested safely on empty shell before electronics installation.

## Release blockers
1. exact 32 mm digital camera PCB outline/component heights;
2. exact lens and optical working distance;
3. exact Ethernet rotary transfer drawing/sample;
4. actual ROLL bearing spacing and gear geometry;
5. front window/O-ring supplier articles;
6. full yoke/screw/cable DN150 sweep;
7. 2 h thermal stream test;
8. tilt/roll endurance and submerged leak test.