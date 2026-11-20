# PX1 motor selection — 2026-11-19

> **2026-11-20 (correction):** this file is history. The current CAD no longer uses the JGA25 fit study: since F16 the master carries the ZHAOWEI ZWSMD026026 i=62 + MP2238 (24 V winding) candidate — see MOTOR_F12_PROTEUS_CLASS_20261119.md and HOLD H05.

Status: no purchase-qualified Ozon/Wildberries motor established. User now requires Ozon or Wildberries; FAULHABER excluded. No motors purchased. Current verified CAD/STEP remains the JGA25 fit study, not a traction-qualified design.

## Technical reserve outside requested marketplaces

Z22DP2410-60S / 22PM105, two units, is a conditional technical candidate, not an approved purchase. Supplier catalogue lists 24 V brushed drive and output 0.8 Nm at 57 rpm. Sources:
- https://sirius-drive.ru/Z22DP-10W.html
- https://sirius-drive.ru/pdf/Z22DP-10W.pdf
- https://sirius-drive.ru/Planetarnye_motor-reduktory.html
- https://sirius-drive.ru/price.html

Catalogue S1 does not qualify operation inside the sealed robot. Price and actual availability require supplier confirmation. No enquiry sent. PDF contradicts itself: tabulated shaft 4 mm versus drawing 5 mm; motor torque 1.6 Nm versus website 0.016 Nm (10 W at 6000 rpm implies 0.0159 Nm). Verify selected variant and permissible continuous gearbox torque before ordering. K bearing suffix unconfirmed.

Derived at downstream efficiency 0.75, bevel ratio 2.5 and wheel radius 45 mm: 0.60 Nm per motor for total 50 N; catalogue 0.8 Nm yields 66.7 N and 6.45 m/min. These are calculations, not measured drawbar pull; traction and tether drag remain unqualified. Minimum downstream efficiency for 50 N at 0.8 Nm is 0.5625.

Drawing-derived envelope: OD22, body85+40.6=125.6 mm. At existing face X195.5 rear is X69.9; body pair width49 in cavity53. Existing lid opening begins X128, so previous vertical removal proof does not apply. Bounds screen flags body, old motors and forward electronics/video balun. Bounds are not exact intersections. New holder, shaft adapter, wiring, electronics relocation and full service/collision verification required; no replacement committed to master CAD.

Reproduce preliminary package screen:
`python scripts/cloud/check_z22_candidate.py`
Output: `Z22_PACKAGE_SCREEN_20261119.json`.

## Ozon / Wildberries search outcome

Search engines and indexed Ozon product/category pages inspected. Prices/stock/delivery shown by cached pages are not a live quote for the user's region.

- https://www.ozon.ru/category/reduktor-24v/ lists JGA25-370B 24V 77rpm with contradictory 1:226 marking. Existing manufacturer-family analysis in RF_MOTOR_CANDIDATES_20261117.md rejects the 77rpm winding for target traction. Marketplace title does not resolve variant identity.
- https://www.ozon.ru/product/planetarnyy-motor-reduktor-3064926340/ is a concrete planetary listing, but accessible text does not establish voltage, rated torque, speed or dimensions. Not recommended from title/price alone.
- https://www.ozon.ru/product/775-dvigatel-dc-geared-motor-24v-vysokiy-krutyashchiy-moment-planetarnoy-peredachi-1632586117/ is a larger 775 family listing; no evidence of compatibility with current motor envelope. Not a drop-in selection.
- Targeted Wildberries searches did not establish a traceable compact 24V motor with required continuous output. This does not prove none are sold there.

Decision: do not substitute an unverified marketplace motor or lower the 50 N target silently. No Ozon/WB product is currently recommended for purchase. Preserve reserve research and actual unresolved constraints for next step.
