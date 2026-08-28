# PX-1 — Proteus CRP-150 replacement baseline

Status: ACTIVE PROJECT MASTER BASELINE.

## Mission
Build a teleinspection system that behaves and is serviced as close as practical to MiniCam Proteus CRP-150 / CAM026 / RMP300, while replacing unavailable or unnecessarily expensive proprietary parts with common, field-serviceable components.

The target is NOT to reinvent the crawler, reel or camera mechanism. The target is to preserve what already works well in Proteus:
- crawler form and six-wheel layout;
- five-gear side drive architecture;
- two-motor bevel input;
- manual camera lift concept;
- sealed pan/rotate camera concept;
- lightweight manual reel with level wind, meter counter and slip ring;
- simple operator workflow.

## What is preserved as closely as practical
### Crawler mechanics
Source assemblies:
- DRW-002-375 / ASS-002-375 Housing - CRAWLER
- DRW-002-374 side drive
- DRW-002-386 / ASS-002-386 Motor Unit - Crawler
- DRW-002-744 Crawler Lift Parts
- DRW-002-745 Crawler Cover Parts
- DRW-002-752 Lift Housing

Baseline architecture:
- one central machined crawler housing;
- two removable side-drive covers;
- five Z50 gears per side;
- three wheel shafts and two intermediate/input positions per side;
- two drive motors total, one per side;
- Z16 small bevel gears driving Z40 large bevel gears;
- 61800/61801/61903-class bearing architecture where it remains practical;
- standard replaceable O-rings / X-rings / shaft seals;
- wheel retention by a simple center fastener, not a proprietary cartridge.

### Camera/lift
Source assemblies:
- ASS-001-801 CAMERA HOUSING ASSY - CAM026
- ASS-001-802 SIDE FRAME HOUSING ASSY
- ASS-001-803 BEARING HOUSING ASSY - CAM026
- ASS-001-917 PAN MOTOR ASSY
- ASS-001-919 ROTATE AXLE ASSY
- ASS-001-998 ROTATE SPUR GEAR ASSY
- DRW-002-744 Crawler Lift Parts

Preserve:
- compact centered camera head;
- front light ring around the lens;
- side-frame pan axis with worm/self-holding principle;
- rotate axis around the camera assembly;
- manual lift assisted by 150 N gas spring and clamping/indexing mechanism;
- useful image in the lowest/folded position;
- open wet area around the folded camera so water/sludge does not remain trapped.

### Reel
Source assemblies:
- ASS-004-097 CABLE REEL ASSY (RMP300)
- ASS-004-093 KERN ASSY
- ASS-004-094 CABLE REEL ASSY LEFT
- ASS-004-095 CABLE REEL ASSY RIGHT
- ASS-004-096 CABLE REEL CHAIN ASSY
- ASS-002-696 Measure Unit - ASSY
- ASS-004-092 METER COUNTER ASSY
- ASS-002-710 LAYERING SPINDLE ASSY
- ASS-002-711 MAIN SHAFT ASSY
- ASS-002-712 Reel Handle ASSY

Preserve:
- lightweight open manual frame;
- hand crank;
- mechanical brake;
- level-wind spindle;
- measuring wheel/counter;
- slip ring in drum shaft;
- serviceable bearings and chain transmission.

## What is deliberately replaced
- MiniCam crawler main PCB and proprietary high-voltage/power electronics;
- proprietary camera control PCBs;
- proprietary motor control boards;
- proprietary meter-counter electronics;
- proprietary cable connectors where sourcing is poor;
- unavailable proprietary motors/gearheads where a dimensional/performance equivalent can be fitted.

Replacement principle:
- ready-made replaceable modules only for the prototype;
- no custom multilayer main PCB required;
- 24 V-class low-voltage internal architecture where practical;
- simple RS-485 control;
- simple balanced analog video over the reinforced 6-core inspection tether;
- external operator unit with 7-inch monitor, joystick, light/speed controls and OSD.

## Tether
Preserve the Proteus philosophy:
- one reinforced lightweight 6-core copper inspection cable;
- no coax in the main tether;
- no optical fiber;
- no bundle of unrelated loose cables;
- tensile load carried by the cable strength member / tail clamp, not electrical contacts;
- field retermination must be possible.

## Design rule
Before inventing a new mechanism, first check the corresponding Proteus source drawing.
If the original mechanism is simple, reliable and serviceable, reproduce its architecture and change only the part that is unavailable, too expensive, electrically proprietary or unsuitable for current sourcing.

Recent experimental PX1 branches with additional pressure pods, controller saddles, unusual X200 supports or other non-Proteus structures are NOT the master geometry. They remain engineering experiments only.

## Immediate rebuild order
1. Reconstruct the CRP-150 crawler mechanical skeleton from the source assemblies.
2. Fit available traction motors into the original two-motor/Z16-Z40 concept.
3. Reconstruct the three-wheel/five-Z50 side-drive architecture.
4. Reconstruct the manual lift from DRW-002-744.
5. Reconstruct a CAM026-like mechanical camera using modern camera/video/motor modules.
6. Reconstruct the RMP300 reel architecture using standard bearings, chain, slip ring and a modern distance sensor.
7. Build the simple console around the existing 7-inch CVBS display and RS-485 control.

No machining release until one complete side drive, one camera axis and one reel counter mechanism are physically proven.