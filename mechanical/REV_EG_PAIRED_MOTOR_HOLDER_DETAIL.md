# PX-1 Rev.EG — paired traction motor holder

Status: prototype architecture derived from the uploaded CRP150 motor-unit arrangement, with PX-1 motors and catalog bevel gears.

## Source-derived facts
The CRP150 motor-unit drawing contains:
- 1 common Motor Holder;
- 2 motors with gearboxes;
- 2 small bevel gears Z16;
- 2 separate bevel-gear axles;
- 2 bearings 61801-2RS (12x21x5);
- 8 M3 countersunk screws and a central M5 retaining/assembly fastener.

The important system idea is retained: both traction motors and both pinion shafts live on one removable, accurately located holder.

## PX-1 motor holder
Prototype target envelope:
- one-piece Al 6082-T6 or 7075-T6 holder;
- nominal envelope about 100 x 80 x 44 mm before pocketing;
- two JGB37-555 mounting faces machined in one setup;
- motor axes parallel to crawler X-axis;
- nominal motor-axis transverse coordinates Y = +/-19 mm;
- nominal axis height Z = 45 mm;
- motor-body envelope Ø37 mm;
- paired holder locates from two dowels and is clamped to the main housing by four accessible M4/M5 screws.

The body itself does not carry vendor-specific JGB37 hole patterns. A thin replaceable adapter plate/ring may be used between each motor gearbox face and the common holder.

## Small bevel pinion shaft
Current KHK pinion SB1.5-1845H has nominal bore 8 mm. Rather than opening it to 12 mm, PX-1 uses a stepped support shaft:
- gear seat Ø8 h6;
- bearing journal Ø12 h6 for 61801;
- motor-side coupling journal Ø8 or Ø10 depending on the final clamp coupling;
- short shoulder between gear and bearing;
- positive axial retention with shoulder + circlip/nut, not adhesive.

This preserves both the catalog gear bore and the source-proven 61801 bearing class.

## Motor-to-pinion coupling
JGB37 output shafts vary between suppliers, so this interface remains modular.

Preferred prototype:
- split-clamp steel coupling;
- motor side sized after actual shaft measurement (likely D6 class, not frozen);
- pinion-shaft side Ø8;
- coupling length <=20 mm;
- no set-screw-only torque transfer unless a D-flat is positively captured;
- coupling must be removable without removing the large bevel gear/output shaft.

## Bearing support
One 61801 per pinion shaft is retained, matching the source motor-unit architecture.
The JGB37 gearbox output bearing provides the second support across the short coupling/pinion span.

Rules:
- keep bevel pinion as close as practical to the 61801;
- minimize unsupported Ø8 length;
- holder shoulder must locate the bearing outer race positively;
- bevel mesh load must not be reacted through the motor mounting screws alone.

## Adjustment
The holder locates the two motor/pinion axes rigidly. Bevel mesh adjustment occurs at the holder-to-body interface or by defined shim packs, not by loose slotted motor screws.

Initial target:
- shim range +/-0.30 mm;
- repeatability after holder removal <=0.05 mm at the pinion axis;
- verify tooth contact with marking compound before final torque.

## Service sequence
1. remove top/electronic service cover;
2. unplug two motor connectors;
3. remove holder clamping screws;
4. withdraw complete motor/pinion-holder assembly upward/rearward;
5. large bevel/output shafts stay in crawler housing;
6. side-drive pressure zones remain closed unless drivetrain service is also required.

## Thermal path
JGB37 motors and holder sit inside P0. Use the aluminum holder as a heat spreader into the crawler housing:
- broad metal-to-metal mounting land;
- optional thin thermal interface at holder/base interface;
- motor can clamped/supporting saddle allowed but do not distort gearbox nose.

## Electrical service
Each motor gets a separate keyed connector inside P0. Hall encoder wiring, if the selected motor includes it, remains serviceable but is not relied on for final crawler distance; wheel/output sensing remains the preferred measurement architecture.

## Release gates
- buy/measure two exact JGB37-555 samples;
- measure shaft diameter, D-flat, nose boss and screw circle;
- manufacture one holder mock-up;
- verify two motors + both couplings + both 61801 + both KHK pinions fit simultaneously;
- hand-turn bevel pair through 360 degrees with no tight spots;
- run 1000 forward/reverse cycles;
- check bearing and coupling temperature;
- only then release holder drilling and adapter dimensions.