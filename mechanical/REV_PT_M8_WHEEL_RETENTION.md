# PX-1 Rev.PT — internal M8 quick-wheel retention

Status: active first-article baseline; prototype proof/endurance required.

## Decision

Use an **internal M8x1.25 blind thread** in the Ø17 wheel end. Do not reduce the load-carrying wheel seat to an external M8 threaded neck.

The wheel service operation remains one-tool:

1. remove the protective cap;
2. remove one central M8 socket screw and retaining disk;
3. slide the keyed wheel off the Ø17 seat;
4. refit and tighten with controlled torque.

Radial wheel load is carried by the Ø17 shaft shoulder and 61903 bearing. Drive torque is carried by the 5x5 key. The M8 screw provides axial retention only.

## Screening calculation

Inputs:

- conservative wheel radial load: 200 N;
- load overhang: 25 mm;
- bending moment: 5 N·m;
- simultaneous side torque: 3.375 N·m;
- shaft: Ø17;
- M8 internal minor diameter: 6.647 mm basic value;
- local stress-concentration screen: 2.5;
- additional impact screen: 5x.

Results:

| Result | Value |
|---|---:|
| Solid Ø17 nominal von Mises | 12.01 MPa |
| Ø17 with axial M8 hole nominal von Mises | 12.29 MPa |
| Second-moment loss from axial hole | 2.34% |
| Local screen with Kt=2.5 | 30.74 MPa |
| Local screen with Kt=2.5 and 5x impact | 153.69 MPa |
| A4-80 M8 nominal proof-load calculation | 21.96 kN |

The internal axial hole has little effect on the Ø17 bending section. A pessimistic external-M8-root comparison exceeds 200 MPa nominal under the same full bending load, so an external threaded neck is rejected for the baseline.

## Prototype dimensions

- shaft wheel seat: Ø17, fit frozen after actual wheel hub sample;
- key: 5x5 candidate, effective length at least 12 mm;
- blind thread: M8x1.25-6H;
- minimum full thread engagement: 10 mm;
- target drilled/threaded depth: 12–14 mm, with bottom clearance;
- retaining disk: Ø24 x 3 mm stainless candidate;
- screw: A4-80 M8 socket-head, length selected after real disk/washer stack;
- lock: stainless wedge-lock pair or positive captive locking method;
- cap: Ø27 polymer snap/thread cap with drainable dirt labyrinth.

The blind hole must end within the wheel-seat region and must not reach the Ø18 polished seal land, 61903 journal, keyway termination or shaft shoulder fillet.

## Material and assembly

- shaft: 17-4PH/1.4542 preferred, final heat-treatment state after fatigue/corrosion review;
- screw and disk: A4 stainless;
- prevent stainless galling with compatible anti-seize and controlled torque;
- do not use threadlocker as the only locking mechanism in a wet service joint;
- replace damaged screws, washers and caps rather than dressing them in place.

## Release gates

1. First-article dimensional inspection and thread gauge.
2. Static 1 kN radial wheel proof at the design overhang.
3. Rated-torque forward/reverse cycling.
4. Twenty wheel removal/refit cycles with recorded screw torque.
5. Mud/grit operation with cap installed.
6. Dye-penetrant inspection around the blind-hole end, keyway and shoulder.
7. Final fatigue decision after actual shaft material certificate and geometry are frozen.

Calculation source: `mechanical/analysis/PX1_M8_WheelRetention_RevPT.py`  
Recorded result: `mechanical/analysis/REV_PT_M8_WHEEL_RETENTION.json`

