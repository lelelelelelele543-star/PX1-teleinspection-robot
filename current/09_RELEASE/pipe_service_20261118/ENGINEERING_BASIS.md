# PX1 pipe/contact and service-window revision — 2026-11-18

Engineering candidate, not an OEM reconstruction or manufacturing release.
Frozen architecture unchanged: six D90 wheels at X50/150/250, five m1 Z50 per
side, two motors, Z16→Z40 rear X250 input, sealed dry body/manual lift/6-core tether.

## Wheel and pipe contact

The inherited outer shoulder r42 at global |Y|62.5 has radial distance
sqrt(62.5²+42²)=75.3011 mm even when pipe and wheel centres have equal Z.
Thus no vertical adjustment alone fits that rigid level profile into ID150.

The proposed local (radius,Y) vertices retain the inner profile, crown r45 at
localY0, and ±12 width. Only the OUTER shoulder changes from (42,8) to (34.5,8)
and outer edge from (32,12) to (27.5,12). The contour mirrors on the other side.
Overall wheel D90 and crawler width133 stay fixed. These two contour dimensions
are ESTIMATED; they are not claimed to be the real MiniCam QRW90 tyre.

Paired crown contacts lie at Y=±54.5, Z=0. R75 pipe support then fixes
pipe centre Z=sqrt(75²−54.5²)=51.524266 mm. This is the lowest gravity-supported
level chassis pose in the nominal circular pipe, not a visually chosen offset.
Each contact normal has upward component 51.524266/75; paired horizontal
reactions cancel. Contact pressure, friction and tyre deformation are unknown.

For each meridian vertex (r,y), the maximum radial coordinate of its full
revolution is hypot(54.5+y,r+abs(45−pipeZ)). This norm is convex along each
straight meridian segment, so its maximum is at an endpoint. The analytic
checker therefore bounds the ENTIRE proposed tyre surface, not just sampled
mesh vertices. Full assembled mesh/BRep checks remain separate.

The grounded crown has zero nominal radial clearance by definition. Shoulder
clearances are positive but small. Pipe tolerances/ovality, grit, joins, bends,
wheel compliance, loaded pose and traction remain unqualified. No real DN150
passage test is claimed.

## Service-window and pressure-boundary implications

Old opening X138…278, Y±18.5 blocked two Ø25 motors spanning Y±26 and starting
X130.5. New opening X128…278, Y±26.5 gives .5 mm outer lateral clearance and
2.5 mm leading clearance for the active candidate's rigid cylindrical envelope.

The pressure cover changes from158×53×7 to167×68×7, X120…287. Four M3 clearance
holes Ø3.4 are at X123/284, Y±30.5; matching Ø2.5 pilot bores run Z67…75 in
body rails. Bolt/thread solids, preload and thread strength are not released.
The screws are outside the continuous seal path; no new tether penetration.

A rounded-rectangle groove is cut into the cover underside, centre (203,0),
centreline dimensions156×58, corner radius3, width1.9, depth1.2. A nominal1.5
closed elastomer section would give20% squeeze and77.5% nominal section fill.
It requires a specified closed seal/material; spliced cord is NOT approved.
Minimum straight inner sealing land to opening is1.55mm at the sides and2.05mm
at ends; outer cover land is4.05mm at sides. Closest nominal screw-hole edge to
groove edge is about1.08mm at front corners. These are geometric screens only.
Remaining cover thickness under groove5.8mm; pressure bending, gasket loading,
thermal cycling, material, machining tolerances and leak tests remain open.

This revision preserves the dry pressure-body concept but replaces a previously
unresolved cover interface. It does NOT inherit the old110×1.5 O-ring callout;
that unverified ring cannot simply be stretched to this perimeter.

## Motor service-screen scope

Before the screened motion: detach head/lift/harness as applicable, remove the
electronics for access, remove the cover WITH its boss/gland/valve, disconnect
and remove couplings/adapters and the motor holder. Then lift both motors80mm.
The JSON lists every removed component explicitly. Prior dismantling steps,
lead disconnection, retaining screws, tools and manual access are not certified.

The motor is a union of four coaxial X cylinders. Sweeping each along Z80 gives
exact lower/upper cylinders plus a connecting rectangular prism; their union
is the continuous translated volume of this candidate. It is tested against
all retained solids without excluded pairs. The separate32-pose check is kept
as a diagnostic. Passing these screens establishes only the proposed candidate
motor's geometric exit path after the stated disassembly.
