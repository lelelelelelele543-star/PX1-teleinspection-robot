# PX-1 Rev.CB — compact Ethernet ROLL joint and camera-size correction

Status: architecture correction and component candidate selection.

## Key correction
The previously considered 38x38 mm IP camera board is too large for the current Ø52 mm head once the real inner diameter is considered. With a 2.5 mm shell wall, the nominal inner diameter is about 47 mm; a 38x38 mm square has a diagonal of about 53.7 mm and therefore does not fit as a square board inside the cylindrical head.

Do not release CAD based on the 38x38 camera board.

## Preferred ROLL data/power candidate
Primary prototype candidate: JINPAT LPC-12-0602-01E2 class.
- capsule OD: 22 mm;
- 1x 100 Mbps Ethernet channel;
- 6x additional 2 A circuits;
- continuous 360 degree rotation;
- compact enough for the current Ø52 mm camera head architecture.

Alternative candidate: MOFLON ME1221 family.
- OD: 22 mm;
- 1x 100/1000BASE-T Ethernet channel;
- additional mixed power/signal circuits available;
- vendor publishes very low BER target and industrial variants.

For PX-1, 100 Mbps is already far above the H.265 stream bandwidth, so 1 GbE is not required in the rotating joint.

## Revised digital topology
ROTATING PART:
small digital camera/encoder -> 100BASE-TX -> Ethernet-rated slip ring + DC power rings

FIXED HEAD / CRAWLER:
100BASE-TX -> 10BASE-T1L bridge -> one twisted pair through the long tether

CONSOLE:
10BASE-T1L -> standard Ethernet -> display/recording/control computer

This keeps the difficult long-line PHY outside the rotating cartridge and uses the rotary joint only for a short, standard Ethernet link.

## Camera target
The next camera must satisfy ALL of:
- board/body cross-section that genuinely fits inside the Ø47 mm internal head diameter;
- digital output only;
- 1080p minimum;
- H.265 preferred;
- RTSP/ONVIF strongly preferred if the encoder is on the rotating side;
- low-light performance suitable for pipe inspection;
- fixed lens around 90-120 degree DFOV candidate;
- power preferably <=4 W.

A 30x30 mm IP camera class is geometrically plausible because its diagonal is about 42.4 mm, leaving several millimetres for mounting and wiring inside a 47 mm internal bore. Exact selected camera remains HOLD until a suitable H.265 model with documented dimensions is found.

## Mechanical impact
Replacing the previous generic miniature slip ring with a real Ø22 Ethernet capsule changes the ROLL cartridge architecture substantially. The old Ø17 mm central passage concept is no longer valid if the slip ring sits coaxially inside the rotating cartridge. The cartridge and bearing arrangement must be repackaged around the Ø22 device.

Two options remain:
1. increase ROLL support bearing IDs / use larger thin-section bearings around the Ø22 slip ring;
2. place the slip ring behind the main bearing pair and couple the rotor mechanically through a hollow/stepped shaft.

Option 2 is preferred first because it may preserve the current compact front camera geometry.

## Release gates
- exact JINPAT or MOFLON drawing and lead arrangement;
- Ethernet packet-loss test while rotating;
- power-ring voltage drop at camera load;
- selected camera dimensions and power;
- repackaged ROLL bearings and gear geometry;
- thermal test in sealed head;
- DN150 sweep after head geometry update.
