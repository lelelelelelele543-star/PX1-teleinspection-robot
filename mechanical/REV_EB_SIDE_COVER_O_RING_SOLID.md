# PX-1 Rev.EB — side cover / pressure cavity / perimeter O-ring

Status: detailed prototype geometry; supersedes the earlier external wavy-cover concept.

## External cover form
The visible side cover is now a CRP150-style rectangular plate with softened corners, not a scalloped external plate.

Candidate envelope per side:
- X start: 15.5 mm;
- length: 276 mm;
- Z start: 5 mm;
- height: 81 mm;
- basic thickness: 5 mm;
- material: Al 6082-T6;
- hard anodize after machining preferred;
- outer Y plane: ±51 mm with 92 mm central body and 5 mm cover.

At the current corrected DN150 pipe-axis model this gives about 5.6 mm nominal minimum clearance at the lowest outer cover corner before manufacturing/tube tolerance.

All external cover screws must therefore be flush/countersunk or otherwise remain inside the cover clearance envelope.

## Internal five-gear cavity
The cavity contains five m1 Z50 gear envelopes with centers:
X = 50, 100, 150, 200, 250 mm; Z = 45 mm.

Gear OD nominal = 52 mm.

Provide at least 1.5–2.0 mm local radial running clearance around the rotating teeth, plus additional local clearance at grease pockets and manufacturing transitions.

The internal pocket may follow a five-lobed/scalloped form similar in functional principle to the uploaded CRP150 drawing. This reduces dead volume and leaves material around fasteners while the outside remains rectangular.

## Perimeter O-ring
Preferred prototype seal:
- FKM 75A;
- nominal 190x2.5 mm standard O-ring candidate.

Use a racetrack centerline rather than a hand-glued cord.

For a 190 mm ID / 2.5 mm cross-section O-ring, approximate neutral centerline circumference is:
`pi * (190 + 2.5) = 604.76 mm`.

With 200 mm straight length between the semicircular ends, matching racetrack end radius is approximately:
`R = (604.76 - 400)/(2*pi) = 32.59 mm`.

Resulting seal-centerline bounds:
- X ≈ 17.41…282.59 mm;
- Z ≈ 12.41…77.59 mm.

These bounds fit inside the candidate 276x81 cover with useful external land.

## Groove start dimensions
For 2.5 mm FKM axial static seal:
- groove depth: 2.00 mm starting value;
- groove width: 3.20 mm starting value;
- axial squeeze: 20%;
- nominal groove fill: about 77% by cross-sectional area.

These are engineering starting dimensions only. Final release follows the purchased O-ring compound and supplier gland tables.

## Fastener strategy
- M4 A4/A2 Torx/cap or countersunk screws preferred around the outer perimeter;
- target pitch 30–38 mm;
- screws outside the O-ring path;
- add local fasteners near the end semicircles and near each axle-flange region where cover stiffness is interrupted;
- precision location by body pilot + two dowels, not by screw clearance holes.

Do not place a fastener hole through the O-ring groove or into the pressure cavity.

## Three axle-flange openings
At X=50/150/250, Z=45:
- precision pilot for each Ø48-class axle flange;
- local land thick enough for flange O-ring and M3 screws;
- local counterbore/recess can allow the wheel hub to overlap the flange without increasing the outer traction width;
- all three flange interfaces remain serviceable without opening P0 electronics body.

## Pressure
Each complete side cover closes one isolated zone:
- left: P1;
- right: P2.

Normal pressure +0.20…+0.30 bar gauge.
Structural target remains 1.0 bar differential proof capability before release.

The cover is not intentionally vented or drained in operation.

## Cover stiffness
5 mm Al 6082 remains the starting floor. The combination of:
- perimeter screws;
- internal scalloped pocket ribs/lands;
- three flange bosses;
- relatively low service pressure
makes this plausible, but final release still requires FEA or conservative plate verification and physical proof testing.

## DN150 rules
- no screw head may protrude beyond the modeled Y envelope;
- no sharp lower corner below Z=5 at |Y|=51 unless the pipe clearance is recalculated;
- flange bosses may protrude locally because they sit near wheel-center height where radial pipe clearance is much larger;
- wheel tread, not the side cover, is the intentional pipe-contact surface.

## Release gates
1. cut full cover and pocket solid in CAD;
2. verify minimum wall between cavity and O-ring groove >=2.5 mm everywhere;
3. verify minimum wall between groove and cover outside edge >=2.5 mm everywhere;
4. verify M4 head geometry against DN150 envelope;
5. FEA or conservative deformation check at 1 bar differential;
6. machine one cover/body mockup and perform pressure test;
7. repeat pressure test after 20 cover service cycles.