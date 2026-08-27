# PX-1 Rev.EN — digital camera head integration

Status: integration freeze candidate; exact camera PCB and slip-ring drawings remain procurement gates.

## Architecture retained
- fully digital video; no CVBS/NTSC/PAL/coax;
- camera head target envelope Ø52 x 72 mm;
- TILT -105…+105°;
- continuous ROLL 360°;
- static outer aluminum shell with internal rotating cartridge preferred;
- digital rotary transfer through compact Ethernet-capable slip ring;
- camera head mechanically quick-removable from the lift cradle.

## Internal stack
Front to rear baseline:
1. mechanically retained optical window;
2. annular LED board / light baffle;
3. lens and sensor;
4. 32 x 32 mm digital encoder/camera board class;
5. aluminum thermal carrier bonded by thermal pad to the fixed shell;
6. roll cartridge bearings and drive gear;
7. compact Ethernet-capable rotary transfer;
8. rear sealed service closure / quick-release spigot.

## Optical front
- window nominal candidate Ø28 x 3 mm;
- separate static O-ring seal;
- front retaining ring, not adhesive-only retention;
- matte-black internal baffle around lens;
- LED optical path isolated from lens as far as practical to suppress internal reflections.

## ROLL mechanical rule
ROLL bearings do not provide a pressure seal. Preferred arrangement:
- fixed outer pressure shell remains stationary relative to tilt yoke;
- rotating camera/LED cartridge is fully inside the dry head volume;
- only electrical signals cross rotation through the rotary transfer;
- no dynamic external water seal is required for continuous ROLL.

This is now preferred over rotating the complete pressure shell.

## Bearings / cartridge
Current reserved bearing family remains compact thin deep-groove bearings in the 25–37 mm class from prior camera work, but exact bearing numbers are HOLD until the final PCB/lens carrier diameter is known.

Design rules:
- two spaced bearings support the rotating cartridge;
- slip ring carries no radial/axial structural load;
- roll gear and bearings are on the same rigid cartridge carrier;
- cartridge can be removed from the rear without disturbing the optical-window seal where possible.

## Digital rotary transfer
Current project candidate remains JINPAT LPMS-12 Ethernet-integrated family, with CAD reserve approximately Ø7.6 x 20 mm plus lead keep-outs.

It is not released until:
- exact manufacturer drawing is obtained;
- 100 Mbps link is demonstrated through the actual selected unit;
- BER/stream test passes while ROLL rotates continuously;
- motor PWM and LED PWM are active during the test.

## Thermal path
The camera/encoder PCB is not mounted thermally isolated on plastic standoffs.

Required path:
`SoC/encoder -> thermal pad -> aluminum camera carrier -> fixed aluminum shell -> surrounding air/water`.

At least one temperature sensor or readable SoC temperature must be logged during qualification.

## Lighting
Keep 6 x high-efficiency white LED class around the optical window as the starting geometry. Final LED current is thermally limited, not chosen from LED maximum rating.

Required:
- constant-current driver;
- PWM dimming outside the sensitive video sampling path as far as practical;
- local ceramic decoupling;
- separate high-current LED return path from digital data reference;
- thermal contact from LED MCPCB/ring to aluminum structure.

## Quick release to lift
Mechanical quick release remains independent from the electrical connector:
- rear spigot approximately Ø36 mm class;
- anti-rotation key;
- retained latch/locking collar;
- static O-ring at the mechanical interface only if the cradle interface itself forms part of the pressure boundary;
- connector never carries bending load.

Because the whole camera head is itself sealed, the preferred cradle interface is mechanically rugged but not relied upon as the camera pressure boundary.

## Cabling through TILT
From crawler body to head:
- flexible power pair;
- one protected differential digital pair / Ethernet interface as required by the selected head electronics;
- service/control conductors only if they cannot be carried in the packet link.

Use a hollow tilt pivot or protected flex loop with controlled bend radius. No cable may be repeatedly pinched by the lift arms.

## Current DN150 rule
At DN150 the head axis remains around Z=75 mm in the LOW lift position until a full-solid sweep is passed. The simple Ø52 x 72 cylinder is only an envelope; final front ring, yoke ears, latch and cable loop must all be included before release.

## Release gates
1. exact camera-board STEP/drawing;
2. exact rotary-transfer drawing and test sample;
3. final lens/window/LED geometry;
4. full sealed-head pressure test;
5. 2 h maximum-stream thermal test;
6. continuous ROLL endurance with live video;
7. full DN150 solid sweep with actual yoke and cable loop.
