# A3 — rear shaft + real involute Z50 / initial 2-bearing carrier

14 November 2026. **Independent prototype geometry**; no OEM dimensional attribution.

## Deliverable
- Parametric CadQuery script: `CAD/px1_a3_rear_drive.py`
- Regenerates 3D assembly STEP and separate m1/Z50 STEP. Uses an actual sampled 20-degree involute with 50 teeth, not pitch-circle disks.
- Rear wheel shaft Ø12 mm, shaft-bearing carrier, two spaced 6001 bearing envelopes (12×28×8 mm), 12×22×7 seal envelope, spur wheel Ø52 mm, pitch Ø50 mm, face width 6 mm, replaceable Ø70×12 tire and hub.
- Independently chosen axial stack (positive Y, right rear shaft): bearing 1 Y14…22, bearing 2 Y27…35, seal Y36…43, spur gear Y44…50, tire Y53…65 mm. This is a **design proposal**.
- Rear shaft center X250 mm; adjacent idler X200 mm. Right wheel outer side Y65 mm. DN150 ideal circular section screen touches at R75 mm.
- Existing A2 motors end near X212.4 mm; new rear housing starts X228 mm, nominal motor-to-carrier clearance 15.6 mm.
- Nominal involute polygon interference at 50 mm pitch centre distance: 0 mm² with chosen half-tooth phase. **Not** a loaded FEA/backlash/contact proof.

## Verified vendor envelope sources
- [NSK 6001 bearing](https://www.nsk.com/engineering/products/bearings/ball-bearings/deep-groove-ball-bearings/single-row-deep-groove-ball-bearings/6001-dgbb-sr.html) 12×28×8 mm.
- [KHK SSY1-50](https://www.rarodriguez.co.uk/wp-content/uploads/2023/10/KHK-2023-Final.pdf) reference module1/Z50/20°/pitch Ø50/outer Ø52; **catalog bore is 8mm**, whereas PX1 A3 proposes a **custom 12mm bored gear**. Do not claim KHK stock gear can directly mount!
- [SKF radial shaft seal catalog](https://www.skf.com/skf/campaign/newindustrialoffers/upload/products/Radial%20Shaft%20Seals%20for%20catalogue%20gearboxes/Maximizing%20bearing%20performance.pdf): standard 12×22×7 exists BUT max operating pressure for the cited standard HMS5/HMSA10 family is 0.03 MPa (0.3 bar), **below PX1 dry cavity 0.4–0.7 bar**. A3 uses it as **packaging envelope only**.
- Candidate pressure-capable family: Parker [TDN3 / NTC4](https://www.mfcp.com/hubfs/MFCP/Catalogs/Catalog%20PDFs/parker-rotary-seal-design-guide-catalog-eps-5350.pdf). Specific 12mm shaft OD/housing OD/width **not yet matched**. Do not substitute sight-unseen.

## Safety/engineering status
- **PASS (geometric screen)**: two 50-tooth involute flanks have no positive planar interference at nominal centre spacing; rear module does not nominally hit the A2 motor bounding envelope; crude circular DN150 envelope.
- **NOT PROVEN**: true shaft/bearing and gear loads; gear contact and backlash across tolerance stack; keyway geometry/fits; circlip and thrust retention; mounting bolts; pressure sealing/underwater contaminants; wheel drive coupling and rubber retention; functional bevel input from motor.
- This assembly represents **one rear driven module**, not a complete six-wheel production-ready system. Continue engineering rather than freezing the project.

## Next mechanical task
Design a pressure-rated rotating shaft seal or a pressure-isolating intermediate chamber, then re-layout the **centre wheel** bearing pair at X150 to avoid A2 motor envelopes (rear axle X250 is clear but centre wheel X150 is not). Produce a direct CAD screenshot after the change and validate collisions.
