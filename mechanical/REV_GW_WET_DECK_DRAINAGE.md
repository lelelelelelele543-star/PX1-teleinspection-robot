# PX-1 Rev.GW — wet-deck drainage correction with sealed scuppers

Status: CAD-SCREENED DESIGN CORRECTION; integrates on top of Rev.GV.

## Why the Rev.GV forward slope alone is not enough
The Rev.GV front wet-deck roof runs approximately:
- X0 Z38
- X120 Z42

That is a 3.33% body-frame slope, about 1.91 degrees.

On a level crawler it drains cleanly to the open nose. However, if the crawler points nose-up by more than about 1.91 degrees, gravity can reverse the flow direction on this shallow front section and water can collect around the transition near X120.

A camera deck described as self-draining should not depend only on the crawler being level.

## Added sealed wet scuppers
Two drain passages are added at the transition/local-low region:
- X = 120 mm
- Y = -26 / +26 mm
- wet passage bore = Ø6 mm
- structural tube OD = Ø10 mm
- top opening flush with the wet-deck roof around Z42
- bottom opening flush to the crawler underside

These are NOT simple holes opening P0.

CAD construction rule:
1. fuse a solid Ø10 tube from the belly structure to the wet-deck roof AFTER the dry P0 cavity has been created;
2. cut only the central Ø6 wet passage through that fused tube;
3. therefore the annular tube wall is continuous pressure-boundary material and the water passage never communicates with P0.

Starting radial wall = 2.0 mm. This is a prototype value and requires pressure FEA/proof testing before release.

## Drainage behaviour
- level / nose-down: the open nose remains the primary drain;
- small/moderate nose-up: water moving rearward on the shallow front deck reaches the X120 scuppers rather than forming a cup;
- the following roof ramp from X120 Z42 to X200 Z77 is about 43.75% (about 23.63 degrees), so for nose-up angles below roughly 23.6 degrees X120 remains a gravitational local-low region in the longitudinal section;
- more extreme attitudes and roll still require physical water/sludge qualification and are not claimed solved by calculation alone.

## Packaging correction
To clear the two scupper tubes, Rev.GW moves the low dry-zone modules without changing the pressure body:
- 48->24 V converter reserve: X20..90, centered Y0, Z15..33;
- AVD video TX reserve: X95..150, centered Y0, around Z19..31;
- TB6612, input-protection reserve, compact dual traction driver, NUCLEO top saddle, pressure sensor and both Ø32x92 motors retain the Rev.GV zones.

CadQuery screen PASS:
- pressure body valid;
- zero body volume outside ideal DN150;
- zero LOW camera/body intersection;
- zero four lift-arm/body intersections;
- zero scupper/component intersections with the revised module placement.

## Manufacturing requirements
- scupper entrances/exits require generous radii/chamfers, no sharp sludge-catching lips;
- internal wet bore finish must be cleanable with a small brush/wire;
- do not use a pressed loose tube as the production pressure boundary unless it has an independently qualified seal/weld/braze;
- preferred final implementation is integral-machined/fused body geometry or a permanently joined qualified metal tube;
- both passages must be included in the pressure proof and dye/immersion test.

## Remaining gates
1. integrate the scuppers into the next full Rev.G* pressure-body CAD source, not only the incremental screen;
2. smooth the deck roof transitions with manufacturing radii and repeat LOW/MID/HIGH lift sweep;
3. bench test water + representative sludge with crawler pitch/roll fixtures;
4. verify that external belly flow cannot pack debris upward into the scuppers;
5. if clogging is observed, enlarge/re-shape the wet passages rather than adding a water-retaining recess.
