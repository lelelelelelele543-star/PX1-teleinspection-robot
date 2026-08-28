# PX-1 Rev.GI — X200 bevel gear trade study

Status: engineering trade study; not machining release.

## Input architecture retained
The CRP150 source drawings show a supported small bevel shaft (Z16 + 61801) and a housing-side large bevel / output seal architecture. PX-1 retains that *system architecture* but not the source geometry.

Current PX-1 constraints:
- two independent 24 V traction motors;
- motor envelope Ø32 x <=92 mm candidate;
- motor axes at Y +/-16.5, Z45;
- side bay Y38..46;
- P0 inner wall Y +/-34 and 4 mm membrane to the side bay;
- X200 spur handoff uses m1 Z50 in the side bay;
- no side-cover recess is allowed to break the main side-cover seal path.

## Stock bevel pair check
A readily catalogued hardened KHK pair was investigated as a way to avoid a custom bevel set:
- SB1.25-2040H, m1.25, Z20, ratio 2 pair member, bore 8, mounting distance 36 mm;
- SB1.25-4020H, m1.25, Z40, bore 10, mounting distance 27 mm.

The pair has useful strength and commercial availability, but is **not a drop-in** for the current side-by-side motor architecture. With the large-gear shaft intersection at Y=+/-16.5, its 27 mm mounting distance places the large-gear back face around |Y|=43.5, crossing the P0/P1/P2 membrane and consuming the side-bay space needed for the 18x30x7 seal and the X200 Z50 handoff.

Using this stock pair would therefore require a major motor/shaft architecture change, not just a gear substitution.

## Compact PX-1 bevel candidate
Continue the compact source-inspired layout with an independently specified bevel pair:
- straight bevel, 90 degree shafts;
- module 1.25;
- Z16 / Z40;
- ratio 2.5:1;
- 20 degree pressure angle target;
- face width 8 mm;
- pitch diameters 20 / 50 mm;
- cone distance ~26.926 mm;
- pinion pitch angle ~21.80 deg;
- gear pitch angle ~68.20 deg;
- pinion outer pitch-plane axial distance ~25 mm;
- large-gear outer pitch-plane axial distance ~10 mm;
- compact hubs controlled by PX-1 packaging rather than a generic catalog hub.

The 8 mm face width is below one-third of cone distance (~8.98 mm), satisfying the usual preliminary face-width packaging rule.

## Torque protection rule
The current Ø32 motor candidate can exceed what is needed for available crawler traction. Until the actual motor and bevel supplier are validated, firmware/current sensing shall impose a **1.0 N.m motor-output torque-equivalent ceiling** for the bevel design basis.

At 1.0 N.m:
- pinion tangential force at 10 mm pitch radius: ~100 N;
- preliminary Lewis screen with conservative Y=0.30: ~33 MPa nominal, ~67 MPa with 2x screening factor;
- after 2.5:1 and 0.85 bevel efficiency: ~2.125 N.m delivered to one side gear chain;
- with Ø90 wheels, theoretical torque-limited tractive force is still well above the expected adhesion-limited force.

This is a screening calculation only. Supplier AGMA/ISO rating, contact stress, material/heat treatment, actual tooth geometry and measured motor torque-current data remain release gates.

## Decision
For the current prototype geometry:
1. retain compact m1.25 Z16/Z40 as the active X200 bevel candidate;
2. do not redesign the whole crawler around the stock KHK pair merely to avoid a custom bevel;
3. use printed gears only for low-load kinematic bench work;
4. final metal gears require a gear supplier drawing/rating and controlled heat treatment;
5. current limiting is part of mechanical protection, not only electronics protection.
