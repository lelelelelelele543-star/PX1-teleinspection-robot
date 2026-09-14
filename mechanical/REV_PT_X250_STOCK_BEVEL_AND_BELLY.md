# PX-1 Rev.PT — X250 stock bevel and pressure-belly correction

Date: 2026-09-02  
Status: validated packaging candidate; first-article and pressure-test HOLD.

## Decision

The source Proteus Z16/Z40 pair is retained as historical evidence, but it is not a reproducible purchasing specification. PX-1 changes the replacement pair to:

- pinion: **KHK SB1.5-1845H**, m1.5, Z18, bore Ø8, OD 30.86, face 11;
- large gear: **KHK SB1.5-4518H**, m1.5, Z45, bore Ø10, OD 68.18, face 11;
- ratio: 45/18 = **2.5:1**, unchanged;
- material family: S45C, hardened-plus `H` version;
- one pair per side, two pairs per crawler.

The pair is a catalog geometry that can be ordered and replaced by article number. Generic marketplace gears may be used only when they match the complete KHK interface and pass hardness, backlash, contact-pattern and loaded-endurance checks.

Manufacturer references:

- https://khkgears.net/new/bevel_gears.html
- https://khkgears.net/pdf/2025/bevel-gears.pdf

## Why m1 cannot be used

The compact m1 SB1-1845H/SB1-4518H pair fits easily, but the small gear is limited to about 0.61 N·m by the hardened surface-durability rating. That is below the 1.37 N·m published rated torque of the current Ø32 motor reference.

For the selected m1.5 H pair:

| Check | Applied | Catalog allowable | Margin |
|---|---:|---:|---:|
| Pinion surface durability | 1.50 N·m | 2.16 N·m | 1.44 |
| Large gear surface durability | 3.375 N·m | 5.39 N·m | 1.60 |

The 3.375 N·m side value includes 2.5:1 reduction and 90% screening efficiency. Stall/jam protection remains mandatory because the motor can exceed the catalog gear limit during a locked-rotor event.

## X250 placement

Rev.PT keeps the corrected source topology:

- rear driven station X250;
- all five side spur gears remain m1 Z50 at 50 mm pitch;
- wheel stations remain X50/X150/X250;
- there is no X200 input shaft and no extra fourth input station.

The large bevel diameter requires a local change to the pressure body:

- outer belly datum changes from Z8 to Z5;
- local dry pocket: X234...266, Y-31...+31, bottom Z10.5;
- nominal remaining belly floor: **5.5 mm**;
- wheel bottom remains Z0, so the body keeps 5 mm nominal ground clearance;
- calculated body volume outside the ideal DN150 cylinder remains **0 mm³**.

The local pocket is preferable to weakening the whole floor. It still requires structural FEA and a safe empty-body hydrostatic proof at 1 bar differential before release.

## Shaft/support architecture

Preserve the Proteus load path:

1. the motor couples to a separate Ø8 pinion shaft;
2. the bevel pinion is supported in the holder by its own bearing close to the tooth load;
3. the motor gearbox bearing is not the only bevel support;
4. the Ø10 large-gear shaft uses a 61800-class support near the mesh;
5. the transverse handoff connects at X250 to the rear long-axle side gear;
6. the 61903 wheel bearing carries external wheel bending close to the wheel;
7. wheel load does not pass through the motor gearbox.

Exact KHK mounting distances and the motor-to-pinion coupling are intentionally not machining-released from cone envelopes. The real KHK pair or manufacturer STEP must set the holder datums.

## Executed validation

Source: `mechanical/cadquery/PX1_X250_StockBevel_Master_RevPT.py`  
Result: `mechanical/cadquery/REV_PT_VALIDATION.json`

PASS:

- valid body solid;
- zero body volume outside ideal DN150;
- X250 input retained;
- Z50 spacing error 0 mm;
- both KHK gear envelopes fully inside dry volume;
- 5.5 mm nominal floor under the local pocket;
- motor envelopes do not intersect body;
- electronics reserve volumes still fit;
- catalog torque margins meet the current 1.40 screening floor.

## Release gates

1. Buy one exact H-suffix pair and obtain its current drawing/STEP.
2. Measure bore, hub, total length and mounting-distance datums.
3. Add shims and check contact pattern at four shaft angles.
4. Calibrate motor current to pinion torque; limit to 1.50 N·m maximum.
5. Run repeated stall/reversal protection tests.
6. Complete pressure FEA of the Z5 belly and pocket transitions.
7. Hydrostatic proof-test the empty body before electronics or motors are installed.

