# RFQ — PX-1 six-core professional inspection tether

Project: PX-1 teleinspection crawler
Revision: Rev.B / WB06
Date: 2026-09-11
Prototype quantities requested: 10 m sample, then 100 m and 150 m continuous lengths

## 1. Application

Flexible crawler tether for sewer / pipeline inspection robot.

The cable must carry:
- high-voltage DC power;
- one half-duplex RS-485 pair;
- one balanced analog-video pair;
- mechanical recovery load through aramid/Kevlar-class strength reinforcement.

The cable is reeled repeatedly, pulled through wet/abrasive pipes and must be field-reterminable.

## 2. Functional copper-core count — mandatory

Exactly six functional copper cores:
- 2 x power cores;
- 2 x 2-core differential signal pairs.

No coax.
No optical fibre.
No separate external data cable.
No extra drain wire requiring a seventh/eighth connector contact or slip-ring circuit.

Preferred construction:
- power: 2 x 22 AWG, approximately 0.33 mm², tinned fine-stranded copper;
- signal: 2 x (2 x 24 AWG), approximately 0.20 mm² each conductor;
- internal signal pairs twisted as controlled pairs;
- 100 ohm nominal differential impedance preferred;
- >=100 MHz construction class preferred;
- low mutual capacitance suitable for RS-485 and balanced analog video.

If your standard product includes foil/drain shielding, please quote an alternative without separate drain conductors, or explain how the shield is constructed while preserving only six copper termination conductors.

## 3. Electrical ratings

Required:
- nominal operating DC line: 100-120 VDC;
- cable voltage rating: >=300 V preferred;
- conductor insulation and finished cable to pass a supplier-controlled dielectric test appropriate for this voltage class;
- DC resistance per conductor to be stated at 20°C;
- pair impedance/capacitance to be stated;
- insulation resistance to be stated.

Please provide guaranteed maximum conductor resistance, not only nominal AWG.

## 4. Mechanical construction

Required:
- aramid/Kevlar, Dyneema or equivalent strength member integrated in the cable;
- tensile load must be carried by the strength member, not copper cores;
- abrasion/hydrolysis/oil-resistant PUR or TPU outer jacket suitable for sewer inspection;
- flexible trailing/reel service;
- field-strip and field-retermination capability;
- no GFRP push-rod core: cable must remain flexible for powered crawler towing.

Breaking load:
- minimum acceptable: 1.5 kN;
- preferred: >=3.0 kN.

Please state:
- minimum breaking load;
- recommended working load;
- minimum dynamic bend radius;
- minimum static bend radius;
- recommended drum core diameter;
- flex/reel cycle rating if available.

## 5. Size / mass target

Preferred finished cable:
- OD <=8.0 mm;
- absolute prototype gate <=8.5 mm;
- mass <=60 g/m preferred.

If the requested mechanical strength requires a larger diameter, quote the smallest manufacturable OD and provide actual g/m.

A 10.1-11 mm cable is considered electrically acceptable but is not preferred because it increases sewer drag and forces a larger crawler gland/reel geometry.

## 6. Jacket / buoyancy

Preferred outer jacket:
- polyether PUR;
- black, orange or yellow;
- smooth low-friction surface;
- abrasion resistant;
- hydrolysis resistant;
- oil/grease resistant;
- microbial/wastewater environment compatible.

Neutral buoyancy is not mandatory. A slightly negative or near-neutral cable is acceptable if it is mechanically more abrasion-resistant than a heavily foamed jacket.

Please quote:
A. solid/compact crawler PUR jacket;
B. foamed/near-neutral PUR version if available.

## 7. Signal-pair requirement

Pair 1: RS-485 half duplex.
Pair 2: balanced analog CVBS video.

Please state for each pair:
- characteristic impedance;
- capacitance conductor-to-conductor and conductor-to-screen if screened;
- attenuation versus frequency if available;
- twist pitch;
- pair-to-pair crosstalk data if available.

PX-1 will qualification-test the finished cable under motor PWM and LED PWM noise.

## 8. Power-loss design point

Reference load for supplier review:
- source 120 VDC;
- remote cable-input power approximately 111 W;
- target lengths 40 / 100 / 150 m.

For 22 AWG at ~53.5 ohm/km per conductor, the current internal PX-1 screen predicts at 150 m / 20°C:
- loop resistance ~16.05 ohm;
- remote voltage ~102.6 V;
- line current ~1.08 A;
- cable loss ~18.8 W.

Please advise if your guaranteed resistance is materially different.

## 9. Termination compatibility

PX-1 crawler connector uses LAPP EPIC H-D 1.6 machined contacts.

Preferred contact barrel:
- 0.14...0.37 mm²;
- LAPP 13162500 male / 13163500 female;
- 8 mm stripping length.

Therefore conductor copper areas around 0.20...0.33 mm² are intentionally preferred.

Please provide:
- conductor insulation OD;
- strand count / individual strand diameter;
- recommended stripping method;
- any water-blocking yarn/compound that affects field stripping.

## 10. Strength-member termination

PX-1 mechanically terminates the aramid separately using a capstan/clamp before the copper service loop.

Please provide:
- strength-member material;
- yarn/braid construction;
- whether strength member can be separated cleanly from cores;
- recommended knotless clamp/capstan termination method;
- minimum capstan diameter if specified;
- whether cutting the outer jacket releases/loosens the strength braid.

## 11. Requested deliverables with quotation

1. controlled cross-section drawing;
2. exact OD tolerance;
3. mass g/m;
4. conductor resistance max ohm/km @20°C;
5. voltage/test-voltage rating;
6. pair impedance and capacitance;
7. pair shielding structure, if any;
8. jacket material designation;
9. tensile breaking load and working-load recommendation;
10. bend radii;
11. 10 m sample price;
12. 100 m continuous price;
13. 150 m continuous price;
14. MOQ;
15. lead time;
16. reel/spool dimensions;
17. available cable colours;
18. confirmation that there is no coax or fibre;
19. confirmation that only six functional copper cores require termination.

## 12. Candidate supplier references

Primary custom-family reference:
- Shanghai Kabel / ROVConnector `2x22AWG + 2x2x24AWG` ROV tether family.

European robustness benchmark:
- Novacavi `6XM524`: 2x16AWG + 2x(2x24AWG)IS, HDPE/PUR, ~10.1 mm OD, ~320 kg BS.

The supplier may propose another equivalent construction, but deviations must be explicit.
