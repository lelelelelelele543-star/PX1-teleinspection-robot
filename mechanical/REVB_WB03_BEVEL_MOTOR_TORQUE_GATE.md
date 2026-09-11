# PX-1 Rev.B — WB03 bevel gear / traction motor torque gate

Date: 2026-09-11
Status: ACTIVE ENGINEERING GATE — architecture retained, machining release blocked

## 1. Frozen architecture preserved

No architecture change is made in this work block.

Retained drivetrain per crawler side:
- one longitudinal 24 V traction motor;
- separately supported bevel-pinion shaft;
- 90 degree straight-bevel pair;
- Z16 -> Z40 ratio 2.5:1;
- rear long-axle side-drive input;
- five m1 Z50 side gears with 1:1 distribution to three wheel stations;
- no belt drive;
- no independent wheel motors;
- no cartridge/cassette mechanical module.

CRP-150 assembly evidence confirms GEA-002-531 Z16, GEA-002-530 Z40, 61801 support at the pinion unit, 61800 support and 18x30x7 dynamic seal at the large-bevel shaft. The available assembly drawings do NOT state the bevel-gear material or heat treatment. Therefore material/hardness must not be invented from the assembly sheets.

## 2. Tractive-force-derived motor torque requirement

Current prototype acceptance targets from PX1-TP-020:
- normal wet pull target: >=40 N total crawler pull;
- preferred result: >=50 N total crawler pull.

Screen assumptions already used by the Rev.GO traction model:
- wheel effective radius: 45 mm (Ø90 class);
- two drive sides;
- bevel reduction: 2.5:1;
- conservative whole mechanical path efficiency: 0.75.

Motor-output torque required per side:

`T_motor = F_total * r_wheel / (2 * i_bevel * eta_path)`

Results:
- 40 N target -> 0.480 N.m per motor;
- 50 N target -> 0.600 N.m per motor;
- 60 N -> 0.720 N.m;
- 66.7 N -> 0.800 N.m;
- 83.3 N -> ~1.000 N.m.

Therefore the crawler does NOT need 1.7+ N.m continuously to meet the present 40-50 N prototype pull target. The higher-torque motor is useful as reserve, but it must be current/torque limited so it does not become a gear-destroying source during stall or skid-turn events.

## 3. ISL PGM-32P-24-100-60-02 status

Manufacturer-controlled 2023 datasheet for `MOT-IG32PGM 100 / PGM-32P-24-100-60-02` gives:
- 24 V DC;
- Ø32 mm class;
- ~92 mm overall length;
- reduction 100:1;
- no-load speed 60 rpm;
- rated speed 49 rpm;
- rated torque 18 kg.cm = ~1.765 N.m;
- rated current 1.06 A;
- stall torque 98 kg.cm = ~9.61 N.m motor/gear output theoretical;
- stall current 5.5 A;
- explicit gearbox limitation: 40 kg.cm = ~3.923 N.m; operation above this may cause premature gearbox failure.

The manufacturer's current online shop lists this exact part as in stock (22 units at the time of this audit), but its marketing table shows slightly different performance values than the downloadable technical datasheet. For engineering release, the technical datasheet controls until a newer signed datasheet is obtained.

With the 2.5:1 bevel stage and Ø90 wheel:
- 49 rpm rated motor output -> 19.6 rpm wheel -> ~0.092 m/s theoretical crawler speed;
- 60 rpm no-load motor output -> 24 rpm wheel -> ~0.113 m/s theoretical no-load crawler speed.

Decision: `PGM-32P-24-100-60-02` is now the leading purchasable Rev.B traction-motor candidate for the slower/stronger prototype, but final holder holes/coupler remain sample-driven.

## 4. Soft stock m1 Z16/Z40 pairs are rejected for traction release

### Mädler 36056400 / 36056500
Exact geometry class:
- straight bevel;
- m1;
- Z16 / Z40;
- ratio 2.5:1;
- OD approximately 18.6 / 40.5 mm;
- face width 6.5 mm.

But the published allowable torque is only:
- Z16: 0.09 N.m;
- Z40: 0.225 N.m.

Material up to module 2 is 11SMn30+SH / 1.0715, not hardened.

Result: REJECTED for PX-1 traction. The Z16 rating is only 15% of the ~0.60 N.m motor torque required for the 50 N crawler target.

### TYMA OKS M1 Z16/40 B
Commercially available geometry is attractive:
- m1;
- Z16 / Z40;
- ratio 2.5:1;
- straight Gleason type B;
- 20 degree pressure angle;
- C45 steel;
- teeth explicitly NOT hardened;
- pilot bores for finish machining.

TYMA does not publish an allowable torque on the product page used in this audit.

A comparable KHK soft S45C m1 18/45, 2.5:1 pair publishes for the pinion:
- bending strength ~1.33 N.m;
- surface durability only ~0.14 N.m.

This does not prove the TYMA pair has the same rating, but it shows why tooth-surface durability, not simple root bending, is the governing risk for an unhardened m1 bevel pair at our duty.

Result: TYMA pair may be bought only as a low-cost dimensional/backlash/alignment prototype. It is NOT approved as the released traction pair unless TYMA/manufacturer provides a verified load rating meeting the gate below or a controlled hardening process is qualified.

## 5. Hardened stock alternatives checked

Commercial hardened 2.5:1 bevel sets exist and demonstrate that the torque requirement is practical, but the compact ones found do not preserve the CRP-150 envelope.

Examples:

### Mädler 38557200
- spiral bevel set;
- module 1;
- 20/50 teeth;
- ratio 2.5:1;
- 42CrMo4;
- tooth flanks induction hardened;
- allowable torque published ~9.9 N.m pinion / 24.8 N.m gear;
- large gear OD ~75.7 mm.

This is much larger than the reconstructed ~40.7 mm CRP-150 Z40 envelope. REJECTED geometrically.

### Mädler 38566600
- spiral bevel set;
- module 1.3;
- 14/35 teeth;
- ratio 2.5:1;
- 42CrMo4;
- induction-hardened flanks;
- allowable torque ~11.3 N.m pinion / 28.2 N.m gear;
- large gear OD ~70.9 mm.

Also REJECTED geometrically.

Conclusion: the market proves hardened small bevel gears can exceed PX-1 torque by a wide margin, but no currently verified stock hardened pair found in this work block simultaneously preserves m1-class compactness, 2.5:1 ratio and the ~41 mm large-gear envelope.

## 6. Rev.B bevel-pair requirement

Preferred final direction: custom or supplier-special hardened straight-bevel pair preserving the Proteus envelope.

Target specification to request from gear manufacturers:
- shaft angle: 90 degrees;
- straight bevel, Gleason-compatible system preferred;
- pressure angle: 20 degrees;
- module: 1.0 nominal;
- teeth: 16 / 40;
- ratio: 2.5:1;
- pitch diameters: ~16 / 40 mm;
- large-gear outside envelope target: <=41 mm class unless CAD proves otherwise;
- face width target: ~6.5 mm minimum; modest increase allowed only if axial packaging remains valid;
- material candidate: 42CrMo4 with induction-hardened flanks OR 16MnCr5/SCM415-class carburized design as agreed with gear manufacturer;
- hubs/bores to remain machinable or be finish-machined before heat treatment as appropriate;
- backlash and mounting distance to be supplied as controlled pair data;
- pair supplied/matched as one set.

### Torque gates
Normal operating command target:
- ~0.60 N.m pinion torque for 50 N total crawler pull;
- initial software torque/current ceiling to be tuned around the 0.65-0.80 N.m pinion range on the physical bench, not inferred from current alone.

Minimum Rev.B pair acceptance:
- verified continuous pinion torque >=1.0 N.m;
- verified short-duration pinion overload >=2.0 N.m.

Preferred Rev.C robustness target:
- continuous capability >=1.8 N.m pinion if practical;
- short transient capability approaching the selected motor gearbox's ~3.9 N.m mechanical limit, or another documented fail-safe torque boundary.

Do not command the full motor stall torque. The motor gearbox itself has a lower published limit.

## 7. Tooth force / bearing-load screen

For m1 Z16/Z40, 90 degree shafts:
- pinion pitch angle ~21.801 degrees;
- gear pitch angle ~68.199 degrees;
- cone distance ~21.541 mm.

Using a 6.5 mm face-width screen, mean pinion pitch diameter is ~13.586 mm.

Approximate pinion tooth forces at 20 degree pressure angle:

| Pinion torque | Ft tangential | Fr radial | Fa axial |
|---:|---:|---:|---:|
| 0.60 N.m | ~88 N | ~30 N | ~12 N |
| 0.80 N.m | ~118 N | ~40 N | ~16 N |
| 1.00 N.m | ~147 N | ~50 N | ~20 N |
| 2.00 N.m | ~294 N | ~99 N | ~40 N |

These values indicate that the tooth surface/strength problem is more critical than the nominal rolling-bearing load. Exact bearing life is still checked from the selected 61801/61800 manufacturers and the final shaft reactions/mounting distances.

At 2.0 N.m pinion input, ideal Z40 output torque is 5.0 N.m. A solid Ø10 mm shaft would see only ~25.5 MPa nominal torsional shear before keyway/stress-concentration factors, so the shaft diameter itself is not the current governing element.

## 8. Procurement decision

### Buy/use now for prototype fit
1. `ISL PGM-32P-24-100-60-02` — leading motor candidate; buy two identical units plus one spare if budget allows.
2. `TYMA OKS M1 Z16/40 B` — optional one pair only as an alignment/backlash/packaging mule. Do not use it for full-load endurance qualification.

### Do not buy for traction release
- Mädler 36056400/36056500 soft pair: published torque rating is inadequate.

### Request quotation/drawing
- exact hardened m1 Z16/Z40 matched pair to the requirement above.

## 9. Release gates before WB03 closes

1. Obtain exact technical drawing of purchased ISL motor and physically measure two samples.
2. Bench record speed/current/torque curve of both motors at 24 V.
3. Obtain supplier-controlled drawing and torque rating for final hardened Z16/Z40 pair.
4. Freeze mounting distance, backlash, bores, keys/retention and heat-treatment state.
5. Update CadQuery master with exact bevel solids, not module-1.25 screening cones.
6. Check LOW/MID/HIGH camera, motor holder, rear connector and DN150 hard-part clearance with final bevel/motor geometry.
7. Run one-side load test to >=50 N crawler-equivalent pull before duplicating the second side.

## Change log

### 2026-09-11
- derived real motor torque from the existing 40/50 N pull targets;
- confirmed the in-stock ISL 100:1 motor has more torque than the crawler presently needs;
- rejected soft Mädler m1 Z16/Z40 on published torque capacity;
- limited TYMA C45 pair to alignment/prototype duty pending verified capacity;
- rejected available hardened stock alternatives that violate the compact CRP-150 envelope;
- froze the direction toward a matched hardened m1 Z16/Z40 pair without changing the drivetrain architecture.
