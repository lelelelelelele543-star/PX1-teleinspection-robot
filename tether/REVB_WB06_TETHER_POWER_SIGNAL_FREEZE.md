# PX-1 Rev.B — WB06 six-core tether power/signal freeze

Date: 2026-09-11
Status: ELECTRICAL BASELINE FROZEN / CABLE SAMPLE QUALIFICATION HOLD

## 1. Architecture check

No top-level tether architecture change is made.

PX-1 still uses one professional inspection tether containing exactly six functional copper cores:
1. HV+
2. HV return
3. RS485_A
4. RS485_B
5. VIDEO+
6. VIDEO-

Forbidden:
- coaxial conductor;
- optical fibre;
- Ethernet patch cable substituted for the tether;
- separate external twisted-pair leads;
- copper contacts used as the crawler recovery member.

Two signal pairs may be twisted **inside the single six-core inspection tether**. This does not violate the ban on separate twisted-pair lines; it is the required internal lay for differential RS-485 and balanced video.

## 2. Rev.B two-stage cable plan

### TETHER-A — first 40 m demonstrator
Use the existing professional six-core Proteus-class tether already available to the project.

Before any 100-120 VDC operation, measure and record:
- outer diameter;
- mass per metre;
- each conductor DC resistance over a known sample length;
- copper cross-section by construction/measurement;
- conductor insulation OD;
- pair lay/twist structure;
- tensile member material and construction;
- insulation resistance wet/dry;
- actual 40 m loop resistance of the two selected power conductors.

Do not assume the original Proteus cable equals the replacement-cable AWG values below.

### TETHER-B — replacement / 100-150 m production candidate
Preferred custom construction based on a currently manufactured ROV/sewer tether family:
- 2 x 22 AWG power conductors (~0.33 mm² each), tinned fine-stranded copper;
- 2 x 2 x 24 AWG differential signal pairs (~0.205 mm² each conductor);
- pair characteristic impedance target 100 ohm nominal, controlled;
- pair bandwidth target >=100 MHz class;
- NO coax;
- NO fibre;
- NO separate drain-wire cores in the six-contact pinout;
- preferred unshielded twisted pairs to preserve exactly six copper conductors; if a supplier proposes foil screens, no additional drain conductor may consume a functional core or require an extra slip-ring/contact path;
- aramid/Kevlar or equivalent tensile strength member;
- abrasion/hydrolysis/oil-resistant polyether PUR outer jacket;
- field-strippable and field-reterminable;
- target OD <=8.0 mm preferred, <=8.5 mm absolute prototype gate;
- target mass <=60 g/m preferred;
- minimum documented breaking strength >=1.5 kN;
- preferred breaking strength >=3.0 kN;
- minimum bend radius and reel-cycle life to be supplier-controlled.

A current commercial family exists as `2x22AWG + 2x2x24AWG` ROV tether with foamed PUR, two 24 AWG twisted signal pairs and customizable Kevlar. PX-1 requires a crawler-oriented jacket/buoyancy variant rather than blindly purchasing a generic floating-Rov configuration.

## 3. Why 22 AWG power + 24 AWG signal is the current optimum

A 2x16AWG + 2-pair tether gives excellent power efficiency but grows diameter/weight. A European stock reference with this topology (Novacavi 6XM524) is approximately Ø10.1 mm and 320 kg breaking-strength class. It is electrically excellent but exceeds the current compact M16 gland/low-drag target.

Using six equal 26 AWG cores can achieve ~6.8 mm cable diameter, but one 26 AWG pair used as HV power produces excessive long-run voltage drop at the 100 W-class crawler load.

The 22/24 AWG hybrid is the preferred compromise:
- enough copper for 100-150 m power at ~120 VDC;
- 24 AWG gives materially lower signal-pair resistance than 26 AWG;
- all six copper conductors remain small enough to fit one common H-D 1.6 crimp-contact size;
- expected finished cable can remain close to the desired 7-8 mm crawler-tether class if manufactured without unnecessary extra conductors/layers.

## 4. Power-line calculation basis

Engineering screen only; final release uses measured cable resistance.

Assumptions:
- source: 120 VDC for 100-150 m operation;
- power cores: 22 AWG, conservative nominal R20 = 53.5 ohm/km per conductor;
- two-wire loop;
- crawler HV input power screen: 111.1 W, corresponding to ~100 W useful crawler DC power at a 90% downstream-converter screen;
- copper temperature coefficient: 0.00393/K.

Constant-power load is solved, not treated as a fixed current:

`Vs = Vr + (P/Vr) * Rloop`

### 20°C conductor screen

| Length | Loop R | Crawler HV input | Line current | Drop | Cable loss |
|---:|---:|---:|---:|---:|---:|
| 40 m | 4.28 ohm | 115.9 V | 0.959 A | 4.10 V | 3.93 W |
| 100 m | 10.70 ohm | 109.1 V | 1.018 A | 10.90 V | 11.10 W |
| 150 m | 16.05 ohm | 102.6 V | 1.083 A | 17.38 V | 18.81 W |

### 60°C conductor screen

| Length | Loop R | Crawler HV input | Line current | Drop | Cable loss |
|---:|---:|---:|---:|---:|---:|
| 40 m | 4.95 ohm | 115.2 V | 0.964 A | 4.78 V | 4.60 W |
| 100 m | 12.38 ohm | 107.2 V | 1.037 A | 12.84 V | 13.31 W |
| 150 m | 18.57 ohm | 99.2 V | 1.120 A | 20.80 V | 23.30 W |

Decision:
- 40 m has ample margin;
- 100 m is practical at 120 V;
- 150 m is still practical but must be treated as a thermal/efficiency qualification case, not assumed from the 40 m demo;
- a crawler HV->24 V converter intended for 150 m should tolerate at least ~90-125 VDC operating input with transient margin, because ~99 V can occur at the crawler in the hot 150 m screen before adding connector/slip-ring tolerance;
- 100 V source operation is acceptable only for short/demo lengths unless the final converter and cable measurements prove otherwise. At 150 m it causes unnecessarily large line loss.

## 5. Signal-pair electrical screen

For 24 AWG, use nominal R20 ~84.2 ohm/km per conductor only as a first resistance screen.

Loop resistance:
- 40 m: ~6.74 ohm;
- 100 m: ~16.84 ohm;
- 150 m: ~25.26 ohm.

This is acceptable for low/medium-rate differential control but the final decision is based on actual pair impedance/capacitance and end-to-end tests.

### RS-485
Required:
- one dedicated 24 AWG internal pair;
- 100-120 ohm controlled differential impedance preferred;
- isolated transceiver architecture strongly preferred because there is no seventh common/reference core;
- termination/bias only after measured line impedance;
- CRC/watchdog retained;
- test with traction reversal and lighting PWM.

### Balanced CVBS
Required:
- second dedicated 24 AWG internal pair;
- balanced active transmitter/receiver or transformer/active hybrid designed for ~100 ohm pair;
- no coax conductor added;
- verify amplitude, frequency response, sync stability and motor-noise immunity at 40 m first, then 100/150 m.

A supplier's statement of `100 MHz / Cat5e-grade per pair` is useful construction evidence but does not by itself prove PX-1 analog-video performance through the reel, connector and slip ring.

## 6. Exact contact freeze for TETHER-B

Both 22 AWG (~0.33 mm²) power cores and 24 AWG (~0.205 mm²) signal conductors fit the same LAPP EPIC H-D 1.6 machined-contact range 0.14...0.37 mm².

Preferred gold-plated contacts:
- crawler male: LAPP `13162500`, H-D SCEM AU 0.14-0.37, pin;
- cable female: LAPP `13163500`, H-D BCEM AU 0.14-0.37, socket;
- stripping length: 8.0 mm;
- H-D 1.6 system current class: 8-10 A depending insert/system rating, far above the ~1.1 A tether-power screen.

Quantity for one crawler/tether mating pair:
- 6 male working + spares;
- 6 female working + spares.

LAPP packages the machined contacts in larger quantities; because one contact size serves every PX-1 core, buying a full service pack is acceptable and simplifies field repair.

Important:
- these part numbers are frozen only for the 22/24 AWG replacement tether;
- the existing Proteus cable must be measured before using the same barrel size.

## 7. Connector pin map

Retain WB05 circular insert allocation:
- pin 1: HV+ / 22 AWG;
- pin 2: RS485_A / 24 AWG;
- pin 3: RS485_B / 24 AWG;
- pin 4: HV- / 22 AWG;
- pin 5: VIDEO- / 24 AWG;
- pin 6: VIDEO+ / 24 AWG.

HV cores remain opposite each other in the insert. Each differential pair remains adjacent.

## 8. Mechanical tether requirement

Professional crawler references demonstrate that six-conductor Kevlar tethers can carry very high recovery loads; the PX-1 need is much lower because the crawler is in the ~single-digit-kilogram class.

PX-1 controlled limits for first prototype:
- normal operating tether tension target: <100 N;
- warning/investigation region: >150 N sustained;
- crawler recovery operational limit: 500 N until cable and tail termination are qualified;
- tail hardware proof target: 1.0 kN;
- production replacement cable minimum breaking load: 1.5 kN;
- preferred replacement cable breaking load: >=3.0 kN.

The existing WB05 Ø8 capstan-pin hardware remains structurally comfortable at the 1 kN proof screen, but clamp slip/fibre damage, not pin shear, is expected to govern.

Do not increase the recovery load merely because a supplier advertises a higher cable breaking strength. Side-cover, tail body, reel, lowering hardware and stuck-crawler extraction loads must all be qualified as one system.

## 9. Reel consequence

Cable OD and mass affect:
- drum capacity;
- levelwind pitch;
- measuring-wheel preload;
- bend radius;
- crawler drag.

Therefore the custom cable RFQ must return:
- guaranteed OD tolerance;
- actual mass g/m;
- minimum dynamic bend radius;
- minimum static bend radius;
- recommended drum core diameter;
- flex-cycle rating if available.

The existing 40 m demo may run without the final reel. The 100/150 m release may not.

## 10. Alternative / benchmark cables

### ROVConnector 2x22AWG + 2x2x24AWG family
Strongest topology match.
- 2 x 22 AWG power;
- 2 shielded 24 AWG twisted pairs in the standard product;
- foamed PUR;
- pair bandwidth claimed 100 MHz;
- Kevlar and shielding are customizable.

PX-1 requests a six-functional-conductor crawler variant with controlled strength and preferably no extra drain-wire cores.

### ROVConnector 2x16AWG + 2x2x26AWG family
Excellent power margin but likely heavier/larger. Keep as alternate if 22 AWG hot 150 m loss proves unacceptable.

### Novacavi 6XM524
European stock/reference cable:
- 2 x 16 AWG + 2 x (2 x 24 AWG) individually screened;
- HDPE/PUR;
- OD ~10.1 mm;
- breaking strength ~320 kg.

Technically robust but too large for the current low-drag/M16-tail target without redesign. It is a fallback, not the Rev.B first choice.

## 11. Errors/corrections recorded

1. `6x0.5 mm²` is not automatically a better inspection tether. Equal cores waste diameter on signals and do not solve the controlled-pair requirement efficiently.
2. A 6x26 AWG ~6.8 mm cable is attractive mechanically but under-sized for the active 100 W / 150 m HV power pair if only two conductors can be allocated to power.
3. The previously provisional H-D 1.6 contact article can now be frozen for the production candidate because both 22 and 24 AWG fit 0.14-0.37 mm².
4. Pair shields/drain wires must not silently create extra electrical paths beyond the agreed six functional copper cores.
5. 100 V and 120 V source settings are not equivalent at 150 m. The long-cable design should use the top of the existing 100-120 V class unless final measurements justify otherwise.

## 12. WB06 release gates

WB06 becomes fully released only after:
1. characterize the actual existing 40 m Proteus cable;
2. run 40 m resistance, insulation and wet test;
3. request/receive controlled custom-cable drawing for TETHER-B;
4. confirm OD <=8.5 mm, conductor build, 100 ohm signal pairs, jacket, aramid construction and documented breaking load;
5. obtain a 5-10 m sample before ordering 100-150 m;
6. crimp LAPP 13162500/13163500 onto the sample and perform pull/crimp inspection;
7. run RS-485 and balanced-CVBS noise test with traction/lighting switching;
8. run 120 V protected dummy-load test at 40 m-equivalent resistance before live crawler HV;
9. perform tail capstan proof separately from contacts;
10. only after these pass, order/qualify 100 m then 150 m.

## Change log

### 2026-09-11 — WB06
- preserved the exact six-core tether architecture;
- selected the 2x22AWG + 2x2x24AWG topology as the preferred long-run replacement construction;
- rejected equal-26AWG cable for HV-power duty despite its attractive 6.8 mm diameter;
- established constant-power voltage-drop screens for 40/100/150 m;
- established 120 V as the preferred long-run source setting inside the existing 100-120 V architecture;
- froze one common gold H-D 1.6 contact size for all six replacement-cable conductors;
- separated existing 40 m Proteus-cable demo qualification from replacement-cable procurement;
- retained cable OD, mass, breaking load and pair electrical parameters as supplier/sample qualification items rather than invented values.
