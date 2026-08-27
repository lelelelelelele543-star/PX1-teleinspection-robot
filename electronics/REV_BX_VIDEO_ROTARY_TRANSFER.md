# PX-1 Rev.BX — video rotary transfer candidate

Status: engineering candidate, not production release.

## Selected candidate
JINPAT LPMS-05D-0201-SD1 class miniature SDI slip ring.

Manufacturer-listed key data:
- 1x SDI / 75-ohm controlled-impedance video channel;
- 2x 1 A electrical circuits;
- operating voltage up to 48 V;
- outer diameter approximately 5.5 mm;
- body length approximately 9.6 mm.

This is a much better fit than a generic 12.5 mm capsule slip ring because the video path is designed as a controlled 75-ohm channel.

## PX-1 allocation
- 75-ohm rotary channel: CVBS video from rotating camera;
- power circuit 1: camera +V;
- power circuit 2: camera 0 V.

The LED ring remains on the fixed outer head wherever practical, so lighting current does not cross the ROLL interface.

## Important qualification
The manufacturer describes the channel for SDI. PX-1 uses analog CVBS. Electrically, a properly implemented 75-ohm broadband SDI path is expected to pass CVBS, but this must be proven on the actual part before RELEASE.

Mandatory bench test:
1. feed PAL/NTSC CVBS through 75-ohm source/termination;
2. observe picture while stationary and while rotating continuously;
3. check for level loss, ringing, hum bars, intermittent noise and colour loss;
4. repeat with camera powered through the two 1 A channels;
5. verify no visible interference when ROLL motor is driven in both directions;
6. run at least 10,000 revolutions for prototype endurance screening.

## Packaging impact
The listed ~Ø5.5 x 9.6 mm body is comfortably inside the existing Ø17 mm cartridge passage and removes the previous Ø12.5 mm keep-out constraint.

## Release holds
- obtain exact current manufacturer drawing for the ordered suffix;
- confirm lead/cable geometry and minimum bend radius;
- bench-prove analog CVBS compatibility;
- verify power-channel voltage drop at camera current;
- verify electrical noise with N20 ROLL motor running;
- then replace the generic rotary-transfer keep-out in CAD with the purchased-part envelope.
