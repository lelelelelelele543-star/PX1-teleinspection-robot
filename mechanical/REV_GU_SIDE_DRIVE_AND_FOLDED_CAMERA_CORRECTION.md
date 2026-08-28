# PX-1 Rev.GU — side-drive direction check and folded-camera wet-deck correction

Status: ACTIVE DESIGN CORRECTION. This note supersedes any interpretation that the current X200 input reverses the rear wheel, and it rejects the old open `nose` subtraction as a valid pressure-body solution.

## 1. Side Z50 direction check

Active left/right side train positions are:
- X50 = wheel gear;
- X100 = idler;
- X150 = wheel gear;
- X200 = driven input gear from the bevel stage;
- X250 = wheel gear.

For an arbitrary clockwise X200 input:
- X200 CW;
- X150 CCW;
- X100 CW;
- X50 CCW;
- X250 CCW.

Therefore all three wheel gears X50 / X150 / X250 rotate in the same direction. There is no rear-wheel reversal in the active five-gear topology.

### Input-position trade
Mesh count from input to wheel stations:
- X200 input -> X50/X150/X250 = 3 / 1 / 1 meshes;
- X250 input -> X50/X150/X250 = 4 / 2 / 0 meshes;
- X150 input -> X50/X150/X250 = 2 / 0 / 2 meshes.

X250 is therefore not an improvement in mesh-path symmetry. X150 is kinematically the most symmetric input, but it would combine the bevel input with the middle wheel station and significantly complicate the shaft, bearing, seal and axial stack. X200 remains the preferred packaging compromise until an X150 packaging study proves otherwise.

## 2. Folded-camera forward view requirement

User requirement added:
- the camera must provide a useful forward picture while fully folded in DN150 LOW mode;
- the volume directly in front of the lens must be open, not a closed body wall or pocket;
- no cup-shaped recess may retain water/sludge in front of or under the camera.

## 3. Important correction to the old body model

The earlier Rev.FS/Rev.GC body created the folded-camera region by subtracting an upper `nose` volume from the hollow P0 shell. Because the central P0 cavity already extends below that subtraction, this operation by itself opens the pressure volume to the outside. It is acceptable only as an envelope study and is NOT a valid pressure-boundary geometry.

This old nose/recess treatment is superseded.

## 4. New architecture: external wet deck over a sealed pressure roof

The folded camera and its lift mechanism will sit in an OPEN WET DECK, separated from P0 by its own sealed structural roof/floor.

Requirements for the new deck:
- open to the front;
- open upward;
- no front cross-wall in the camera optical cone;
- pressure boundary below the camera, not around it;
- longitudinal drainage slope toward the robot nose;
- smooth radii/chamfers, no horizontal pockets;
- minimum practical free gap under the Ø52 camera in LOW position targeted at >=5 mm before debris qualification;
- side clearance around the camera targeted at >=8 mm per side where possible;
- all lift links/pivots remain in the wet zone unless a dedicated sealed pass-through is deliberately designed.

A rear vertical bulkhead through the current linkage path is prohibited because the Rev.FN parallelogram links cross that region.

## 5. First-order optical/drainage screen

Using the active Rev.FN LOW camera geometry:
- camera axis X ~= 83.56 mm;
- camera axis Z = 75 mm;
- front retainer/lens reference X ~= 42.56 mm;
- camera OD = 52 mm.

A central front opening of approximately Y = +/-34 mm gives a theoretical unobstructed horizontal cone of about 77 degrees at the front plane before lens/FOV specifics.

A pressure-roof top kept below the camera bottom (camera geometric bottom ~= Z49 mm) and sloped forward provides both low-mode visibility and gravity drainage. Exact roof profile remains HOLD until the electronics are repacked below/behind the wet deck and the complete DN150 solid sweep is rerun.

## 6. Consequence for electronics packaging

Rev.GP placed the NUCLEO in the front P0 volume. That packaging is now superseded in the wet-deck region. The controller/drivers must be repacked so no electronics occupy the volume reserved for the external folded-camera wet deck.

The next packaging revision must therefore solve both:
1. camera LOW-mode forward visibility/drainage;
2. sealed P0 volume and serviceable electronics layout.

## Release gates
- rebuild P0 with a real sealed wet-deck pressure roof;
- verify zero camera/body/lift collisions in LOW;
- verify forward optical cone with the actual selected camera lens/FOV;
- verify drain path at level and representative pipe inclines;
- verify no trapped-volume pocket larger than the agreed service limit;
- repack electronics and rerun thermal/service extraction checks;
- rerun complete ideal-DN150 solid validation;
- pressure proof the revised P0 before machining release.
