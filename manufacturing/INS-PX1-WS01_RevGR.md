# INS-PX1-WS01 — wheel station WS-01 first-article inspection — Rev.GR

Status: FIRST-ARTICLE INSPECTION BASELINE; prototype only, not machining release.

## Purpose
This sheet converts Rev.GF/Rev.GQ wheel-station geometry into measurable first-article data. The intent is to machine/build **one** wheel station, record real purchased-part dimensions and actual assembled behaviour, then feed those values back into CAD before duplicating five more stations.

## Active architecture being inspected
- inner support: 6701-2RS, nominal 12x18x4;
- wheel gear: m1 Z50, finished face nominal 3.75 mm;
- intermediate/outboard support: 61801-class 12x21x5 + 61903-class 17x30x7;
- dynamic wheel seal: selected X-ring around the active 18.72x2.62 / Ø19-land concept;
- wheel seat: Ø17 keyed seat;
- wheel retention: recessed M8 axial screw; screw carries axial retention only;
- wheel OD class: Ø90 tapered/dished DN150 profile.

## Datum scheme
Use the same datum philosophy for the shaft, flange and test fixture so measurement results can be transferred directly into CAD.

**Datum A — wheel-shaft rotational axis.** Established by the bearing journals, not by the threaded end.

**Datum B — axle-flange inboard locating face.** This is the axial reference that seats against the side-cover datum.

**Datum C — axle-flange pilot / locating diameter.** Used with Datum B to locate the flange radially. Bolt clearance holes are clamping features, not primary datums.

**Datum D — fixture membrane / side-bay inner datum plane.** Reproduces the active P1/P2 membrane plane used in Rev.GF.

## Gate A — purchased-part metrology before cutting final fits
Record actual values for the exact samples that will be used in WS-01.

| Item | Nominal/catalog | Actual sample | Instrument | Notes |
|---|---:|---:|---|---|
| 6701 ID | 12 mm | ___ | bore gauge/micrometer as applicable | record brand/clearance code |
| 6701 OD | 18 mm | ___ | micrometer | |
| 6701 width | 4 mm | ___ | micrometer | |
| 61801 ID/OD/W | 12/21/5 mm | ___/___/___ | micrometer | |
| 61903 ID/OD/W | 17/30/7 mm | ___/___/___ | micrometer | |
| X-ring ID / section | 18.72/2.62 mm concept | ___/___ | optical/caliper, low force | do not distort elastomer |
| static flange O-ring | selected article | ___ | low-force method | record material/hardness if known |
| Z50 bore | supplier value | ___ | bore gauge | no final shaft fit from nominal only |
| Z50 face width | 3.75 mm target | ___ | micrometer | |
| wheel key | 4x4x7 concept | ___ | micrometer | |

**STOP:** do not finish-machine bearing pockets, shaft journal fits or X-ring gland from catalog nominal dimensions alone.

## Shaft inspection before assembly
Record every value even when the acceptance limit is still provisional.

| Feature | Rev.GF target | Measured | Acceptance state |
|---|---:|---:|---|
| inner bearing journal | Ø12 functional seat | ___ | FIT TO ACTUAL 6701/61801 — freeze after sample |
| 61903 journal | Ø17 functional seat | ___ | FIT TO ACTUAL 61903 — freeze after sample |
| X-ring running land | Ø19 nominal | ___ | sample/gland validation required |
| wheel seat | Ø17 keyed | ___ | wheel core must slide/seat without rocking |
| wheel key dimensions | 4x4x7 | ___ | no forcing/fretting |
| thread | internal M8 | ___ | GO/NO-GO thread gauge preferred |
| wheel-seat radial runout to Datum A | target <=0.03 mm | ___ | STOP if >0.03 mm before functional test |
| seal-land radial runout to Datum A | target <=0.03 mm | ___ | STOP if >0.03 mm |
| seal-land surface finish | target Ra <=0.4 µm class | ___ | polish longitudinally; no helical marks |
| keyway location | outboard of seal land | PASS/FAIL | FAIL if it enters dynamic seal track |

The <=0.03 mm runout/coaxiality values are prototype manufacturing targets, not yet production capability limits.

## Axle-flange inspection

| Feature | Target/intent | Measured | Acceptance |
|---|---|---:|---|
| inboard locating face flatness | visibly full contact; quantify | ___ | no rocking on datum fixture |
| pilot concentricity to bearing bores | target <=0.03 mm | ___ | STOP if obvious misalignment |
| 61801 pocket | fit to actual bearing | ___ | no brinelling, no loose rocking |
| 61903 pocket | fit to actual bearing | ___ | no brinelling, no loose rocking |
| dynamic gland | per selected X-ring data | ___ | HOLD until exact seal is frozen |
| static groove | per selected O-ring data | ___ | HOLD until exact seal is frozen |
| flange-to-cover bolt pattern | active CAD | ___ | bolts must clamp; not used to force alignment |

## Dry assembly sequence / measurements
1. Assemble shaft + 6701 + Z50 + 61801 + 61903 **without X-ring**.
2. Measure shaft endplay: `___ mm`.
3. Measure breakaway torque without dynamic seal: `___ N·mm`.
4. Rotate by hand through 20 revolutions; record tight spots: `NONE / location ___`.
5. Install X-ring using assembly lubricant compatible with selected elastomer.
6. Measure breakaway torque with X-ring: `___ N·mm`.
7. Measure running torque at low speed with X-ring: `___ N·mm`.
8. Install keyed wheel core and M8 retainer to the defined prototype torque; verify the retainer does **not** clamp the rotating bearing stack.
9. Measure wheel radial runout at traction crown: `___ mm`.
10. Measure wheel axial wobble at outer profile: `___ mm`.

## Functional acceptance gates
WS-01 passes only if all are true:
- no bearing damage during installation;
- no detectable loose rocking in bearing pockets/journals;
- shaft rotates freely before seal installation;
- dynamic seal adds smooth drag without stick-slip or lip damage;
- M8 retention does not alter bearing endplay unexpectedly;
- key transmits torque without visible fretting after test;
- no shaft/seal-land runout above the provisional 0.03 mm target;
- two-hour wet rotation completes without abnormal temperature/noise;
- local pressure-decay test passes the final test limit once the fixture volume and sensor resolution are defined;
- 20 wheel remove/refit cycles produce no key-seat or thread damage;
- no hard interference in the DN150 gauge/fixture.

## Test record
- bearing brands / lot: ___
- seal brand/material/hardness: ___
- lubricant: ___
- fixture ID: ___
- wet-test speed: ___ rpm
- wet-test duration: ___
- initial pressure: ___
- final pressure: ___
- water temperature: ___ °C
- bearing/flange temperature after run: ___ °C
- operator/date: ___

## CAD feedback fields
After WS-01, update the master model with **measured**, not catalog, values for:
- bearing widths and actual fit decisions;
- shaft journal diameters;
- flange pocket diameters/depths;
- X-ring gland geometry;
- axial spacer/shoulder dimensions;
- measured endplay;
- measured seal drag;
- wheel core/key fit;
- any DN150 interference witness marks.

No remaining five wheel stations are duplicated until this sheet is reviewed and WS-01 is marked PASS.
