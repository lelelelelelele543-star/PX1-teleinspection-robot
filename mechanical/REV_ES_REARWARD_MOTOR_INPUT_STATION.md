# PX-1 Rev.ES — rearward motor pack and X200 side-drive input

Status: packaging correction; supersedes the Rev.EQ assumption that the longitudinal JGB37 motor bodies occupy X≈104…194 with the bevel stage at X150.

## Problem found
The LOW/DN150 camera envelope is centered near X≈84 mm and is about 72 mm long. Its rear end therefore reaches approximately X≈120 mm. A conservative JGB37 motor envelope starting near X104 creates a real front-body conflict once the camera recess, lift plates and actual pressure-body roof are modeled rather than treated as transparent packaging boxes.

## Correction
Move the traction bevel input to the second idler station at **X=200 mm**.

The five equal m1 Z50 side gears remain:
- wheel X50;
- idler X100;
- wheel X150;
- idler/input X200;
- wheel X250.

Driving the X200 idler still gives the same rotation direction at all three wheel gears. No extra ratio is introduced.

## Motor orientation
Both JGB37 motors remain longitudinal but are reversed so their output shafts point toward the front and the motor/gearbox bodies extend rearward from the bevel stage.

Packaging target:
- bevel intersection plane: X≈200 mm;
- small bevel/pinion immediately forward of X200;
- motor gearbox front face near X202…208;
- conservative motor body reserve extends rearward toward X295;
- paired holder carries both motors and both supported pinion shafts as one removable unit.

This frees the front X≈40…125 region for the folded camera/lift recess.

## Side-drive coupling
The large bevel shaft at X200 crosses the P0/P1 or P0/P2 bulkhead through its dedicated dynamic seal and couples directly to the X200 side-drive idler shaft. The coupling remains serviceable and does not make the wheel shaft itself a P0 boundary.

## Consequences
- front camera pocket no longer competes with a motor body;
- P0 front zone can house control electronics and low-profile power conversion;
- side-drive geometry remains five equal Z50 gears on 50 mm pitch;
- the former assumption that the center wheel X150 is necessarily the powered station is cancelled;
- exact rear clearance still depends on the purchased JGB37 length and rear service-port layout.

## Release gates
1. actual JGB37 overall length measured from output mounting face to rear cap/encoder;
2. actual pinion adapter length measured;
3. complete motor holder solid at X200 checked against rear connector and pressure manifold;
4. full DN150 collision check with camera LOW, screw heads and tether boot;
5. side-drive input idler shaft strength/bearing stack checked for bevel torque.
