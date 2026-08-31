# CRP-150 / X200 crawler drive architecture

Revision 0.1, 2026-08-31.

## Confirmed topology

The crawler uses two traction motors total, one for each side. Both motors are installed longitudinally in a removable motor holder. Each motor drives a supported small bevel pinion. The bevel pair turns the drive through 90 degrees into a transverse side-drive input.

Per crawler:

| Element | Quantity | Confirmed specification |
|---|---:|---|
| Motor and gear unit | 2 | Original observed gearhead: FAULHABER 26/1S, 66:1 |
| Small bevel gear | 2 | GEA-002-531, Z16 |
| Small-gear shaft | 2 | FSS-002-083 |
| Small-gear support bearing | 2 | 61801-2RS, 12x21x5 mm |
| Large bevel gear | 2 | GEA-002-530, Z40 |
| Large-gear / body shaft | 2 | FSS-002-066 |
| Body bearing | 2 | 61800-2RS, 10x19x5 mm |
| Dynamic body shaft seal | 2 | 18x30x7 mm |

The motor gearhead does not directly carry a wheel. The Z16/FSS-002-083 assembly is supported in the motor holder by the 61801 bearing. FSS-002-083 lies concentrically between the supported bevel assembly and the FAULHABER output shaft. The exact coupling fit is unresolved, but the bevel radial load is reacted through the 61801 into the motor holder rather than only through the gearhead output bearing. The large bevel gear transfers torque into the side-drive input path.

## Ratios

Bevel reduction:

```text
i_bevel = Z_large / Z_small = 40 / 16 = 2.5
```

Using the marked nominal FAULHABER ratio:

```text
i_to_side_input = 66 x 2.5 = 165:1
```

The five side gears are all Z50. Therefore they distribute motion to the three wheel stations without changing speed ratio. Two idlers make all three wheels on one side rotate in the same direction.

Calibrated DRW-002-374 geometry gives:

- spur and bevel module: 1.0 mm;
- adjacent Z50 center distance: 50 mm;
- wheel-axle spacing: 100 mm;
- front-to-rear wheelbase: 200 mm;
- Z50 face width: 4 mm (`B4`).

See [`GEAR_AND_SHAFT_AUDIT.md`](GEAR_AND_SHAFT_AUDIT.md) for the derivation and evidence limits.

Nominal wheel speed before losses:

```text
n_wheel = n_motor / 165
```

Examples for a 90 mm nominal wheel:

| Motor speed | Wheel speed | Theoretical crawler speed |
|---:|---:|---:|
| 4,000 rpm | 24.2 rpm | 0.114 m/s |
| 6,000 rpm | 36.4 rpm | 0.171 m/s |
| 8,000 rpm | 48.5 rpm | 0.228 m/s |

These values exclude load, gear efficiency, tire deformation and slip. They are selection targets, not acceptance-test results.

## Side-drive sequence

Each side uses the following five equal spur gears:

1. front wheel Z50;
2. front-middle idler Z50;
3. middle wheel Z50;
4. middle-rear idler Z50;
5. rear driven wheel / long-axle input Z50.

The rear station is the driven input. There is no separate fourth input shaft. This point controls the replacement CAD: the Z40 bevel input, long axle and rear Z50 wheel gear must be treated as one aligned torque path.

## Confirmed side sealing and support family

Per side, the established source architecture includes:

- one 61801-class bearing on the long-axle/input path;
- three 61903-class wheel bearings;
- three X-rings 18.72x2.62 mm on wheel shaft paths;
- three static axle-flange O-rings 32x1.5 mm;
- one side-cover O-ring 190x1.5 mm;
- two idler bushings 10x12x4 mm.

The detailed axial stack, shoulder positions and retaining hardware remain subject to drawing-by-drawing verification before manufacturing release.

## Motor-interface requirements for the replacement

The available motor must preserve the functional interface, even if its flange is different:

- 24 V class motor;
- approximately 60 to 120 rpm at the motor-unit bevel input under no load, giving about 24 to 48 wheel rpm after the Z16/Z40 pair;
- separate bearing support for the bevel pinion shaft;
- motor coupled to the supported shaft rather than using the motor gearbox shaft as a cantilevered wheel axle;
- independently replaceable left and right motor units;
- current and stall torque measured before driver selection;
- no belt drive and no cartridge/cassette motor module.

## Unresolved measurements

- exact motor can dimensions and flange pattern behind the 26/1S gearhead;
- coupling between the FAULHABER output and FSS-002-083;
- Z16 and Z40 pressure angle, face width, tooth system and mounting-distance tolerances;
- exact location of the bevel pitch-cone intersection;
- preload/end-float adjustment method for both bevel shafts;
- material and heat treatment of the bevel gears;
- complete long-axle shoulder and seal journal dimensions;
- exact FSS-002-083 coupling bore, fit and axial retention.
