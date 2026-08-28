# PX-1 Rev.GP — ballast-body and current internal-packaging integration

Status: PROTOTYPE ENGINEERING BASELINE; not machining release.

## Completed
Rev.GP integrates the traction/ballast decisions from Rev.GN/GO into the active pressure-body and current rearward Ø32 motor arrangement.

Two executable CadQuery checks now pass:
- `mechanical/cadquery/PX1_Internal_Packaging_RevGP.py`
- `mechanical/cadquery/PX1_Ballast_Body_RevGP.py`

## Ballast refinement
Rev.GO used 5 mm screening plates. Rev.GP supersedes that thickness with **4 mm plates** for a practical fastener reason.

Active first-prototype ballast:
- plate: 225 x 50 x 4 mm stainless screening geometry;
- X≈55...280 mm;
- one plate ~0.353 kg;
- three plates ~1.06 kg;
- maximum initial stack thickness 12 mm;
- maximum stack bottom Z=-4 mm;
- ideal DN150 radial margin at the ballast lower corner ~13.6 mm.

The ballast therefore remains comfortably inside the DN150 envelope; the side cover/wheel region remains more critical.

## Ballast fasteners
Four local pressure-body bosses:
- X105, Y+/-18;
- X245, Y+/-18;
- boss OD 13 mm;
- boss rises 5 mm into P0 from the normal inner floor;
- M5 tap drill candidate Ø4.2;
- blind hole depth 9 mm from the external belly face;
- 2 mm solid metal remains above the blind hole.

No ballast hole penetrates P0.

Standard screw lengths can now maintain constant nominal 8 mm thread engagement:
- 1 plate: M5x12;
- 2 plates: M5x16;
- 3 plates: M5x20.

Exact screw head/countersink and aluminium thread qualification remain drawing gates.

## Ballast effect
For the current nominal 7.0 kg / CG Z≈48 mm screening model, the maximum three-plate stack gives approximately:
- total mass ~8.06 kg;
- CG X≈154.9 mm;
- CG Z≈42.0 mm.

This is enough to produce a useful traction/CG test delta without turning ballast into a permanent structural mass penalty.

## Internal packaging correction
The old Rev.EP motor zoning is superseded.

Current validated envelope arrangement:
- NUCLEO-F446RE X≈15...97.5, mounted diagonally 45° about X inside the 68 x 71 mm P0 cross-section;
- TB6612 front corner reserve;
- compact data/PHY/service front corner reserve;
- BTS7960-L X≈105...155;
- BTS7960-R X≈160...210;
- input protection/current-sense reserve X≈212...234;
- two Ø32 x 92 motors X≈237...329;
- compact 48→24 half-brick X≈220...290 above the motor fronts.

Bounding-envelope validation reports zero component intersection and zero part volume outside the active P0/rear-extension cavity.

Important clearances:
- BTS pair axial gap ~5 mm;
- BTS2 to protection reserve ~2 mm;
- protection reserve to motor front ~3 mm;
- motor top to half-brick bottom ~4 mm;
- front ballast boss pair to NUCLEO X envelope ~7.5 mm;
- rear ballast bosses remain ~10 mm below motor envelope in the final 5 mm boss concept.

These are envelope clearances only. Exact plugs, wires and heat spreaders remain to be inserted.

## Wheel/tread state
Rev.GO executable geometry retains the current Rev.GF DN150 outer profile and introduces:
- SR compliant/smooth traction shell;
- HG shell with 18 inward-cut transverse slots;
- common keyed metal core.

The HG cuts do not increase the external wheel envelope.

Exact elastomer compound remains intentionally unfrozen until PX1-TP-020 traction testing.

## Test state
`tests/PX1-TP-020_TRACTION_TETHER_RevGO.md` is the active traction calibration plan.

The analysis must be recalibrated with:
- actual crawler rolling drag;
- actual wheel slip pull;
- actual tether mass per metre;
- actual tether sliding drag;
- actual motor current/torque data.

## Next block — Rev.GQ
1. create a first-build sequence that proves one wheel station, then one complete side drive, before duplicating all six stations;
2. define prototype wheel-core + cast/printed tread manufacturing route;
3. insert exact purchased bearing/seal/motor dimensions as soon as samples are selected;
4. model real harness plug bodies and extraction paths;
5. prepare the pressure body for true FreeCAD/CalculiX FEA with ballast bosses and rear fillets included.
