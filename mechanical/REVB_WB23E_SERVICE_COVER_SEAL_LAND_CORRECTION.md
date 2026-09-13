# PX-1 Rev.B — WB23E service-cover seal-land correction

Date: 2026-09-14
Status: **PASS_SEAL_LAND_AND_FULL_INTEGRATION_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD**

## Why WB23E was required

WB23C/D established the correct simple Proteus-style topology, but a detailed fastener/seal review found that the first `78 x 42` cover with `58 x 24` opening placed the M4 clearance-hole centres only 4 mm outside the opening edge. After accounting for a realistic face-seal groove and M4 clearance-hole radius, the remaining web was too small for a sensible prototype.

This is a real design correction, not a cosmetic change.

## Corrected cover screen

WB23E changes only the small service cover/opening package:

- cover centre X: **261 mm**;
- cover: **86 x 44 x 6 mm**;
- cover X span: **218...304 mm**, fully supported by the pressure pod;
- service opening: **48 x 22 mm**;
- opening X span: **237...285 mm**;
- opening Y span: **-11...+11 mm**;
- two M4 centres: **X226 / X296**, Y0;
- pressure-valve screen centre: **X273 / Y0**;
- provisional seal-groove centre offset from opening edge: **4.0 mm**;
- provisional groove width: **2.5 mm**.

WB22A lift geometry, horizontal M12 gland and local harness route are unchanged.

## Seal/fastener geometry result

Using an M4 clearance-hole diameter of 4.5 mm and an 8 mm screw-head envelope:

- minimum clearance-hole edge to provisional groove outer edge: **3.5 mm**;
- minimum screw-head edge to cover outer edge: **4.0 mm**;
- minimum groove outer edge to cover Y edge: **5.75 mm**.

This is significantly more credible than the original WB23C/D land.

The dry JST VH 8-position connector family envelope was also screened at approximately 31.62 x 10.5 mm and fits through the revised 48 x 22 mm service opening.

## Pressure-force screen after smaller opening

Opening area is reduced to 48 x 22 mm:

- +0.25 bar separating force: **26.4 N**;
- +1.0 bar separating force: **105.6 N**;
- ideal equal share at 1 bar: **52.8 N per M4 screw**.

Again, this is only a load-magnitude sanity check, not a plate/thread certification.

## Full integration result retained

The corrected package still passes the complete WB22A integration screen:

- body remains valid after opening cut;
- opening remains inside pressure pod;
- cover remains supported by pressure pod;
- horizontal gland crosses pod front wall as intended;
- fixed package vs ten Z50: 0 mm³;
- fixed package vs six wheel envelopes: 0 mm³;
- fixed package vs lift arms LOW/MID/HIGH: 0 mm³;
- fixed package vs camera outer envelope: 0 mm³;
- lift guard vs package/Z50: 0 mm³.

DN150 fixed clearances:

- corrected cover: **~7.37 mm**;
- pressure-port envelope: **~4.70 mm**;
- horizontal M12 gland: **~13.86 mm**;
- M4 heads: **~7.93 mm**.

The pressure port remains the limiting fixed item.

## Control decision

WB23E supersedes the dimensional cover/opening/screw data in WB23C and WB23D. WB23C remains the functional topology definition and WB23D remains the first full-integration proof, but any prototype cover layout after 2026-09-14 uses WB23E dimensions.

Final groove depth/width is still not released until the purchased seal material and compression target are known.
