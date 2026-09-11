# PX-1 Rev.B — WB13 camera/reel rotary electrical interfaces

Date: 2026-09-11
Status: REAL PART FAMILY SELECTED / SIGNAL QUALIFICATION HOLD

## 1. Scope

WB13 selects real rotary-interface hardware for:
1. continuously rotating camera electrical functions;
2. manual RMP300-style reel tether functions.

It does not change:
- six functional conductors in the main tether;
- 120 VDC-class tether power;
- balanced VIDEO+/VIDEO- in the main tether;
- RS485_A/B allocation;
- CAM026-inspired camera mechanics;
- manual reel architecture.

## 2. Original MiniCam comparison

CAM026 source `ASS-001-920 / ASM011` contains:
- `COM-001-800 SLIP RING 6 WAY`;
- camera-side connection PCB;
- sealed metalwork/O-rings around the rotary connector assembly.

RMP300 source `ASS-004-094` contains:
- a 12-pole `A6023-12` slip ring;
- separate slip-ring PCB;
- slip-ring bearing/flange/cover architecture.

Therefore PX-1 preserves two distinct rotary interfaces and keeps each inside a protected mechanical housing. Neither replacement slip ring is itself a pressure boundary.

## 3. Problem with the earlier reel candidate

Earlier `PX1_RMP300_Reel_RevPG.md` proposed SenRing `M220-0605`:
- 6 circuits;
- 5 A per circuit;
- Ø22 x ~40 mm.

This is electrically strong but treats all six circuits as power-class channels. It does not explicitly separate the two 120 V power functions from the four low-current signal functions.

Rev.B correction: prefer a mixed power/signal construction so HV current is carried on dedicated AWG22-class circuits while RS-485/video use dedicated signal-class circuits.

## 4. Preferred common rotary family — SenRing M220

Manufacturer-controlled M220 series data:
- outside diameter: 22 mm;
- speed class: 250 rpm;
- temperature: -30...+80 C;
- contact system: precious-metal / gold-gold;
- electrical noise: <0.01 ohm manufacturer figure;
- voltage range: up to 240 VAC/VDC class;
- insulation resistance: >=200 Mohm / 300 VDC;
- dielectric strength: 300 VAC, 50 Hz, 60 s;
- IP51 only — must remain in protected dry housings;
- standard lead length ~150 mm unless ordered otherwise.

Manufacturer explicitly states M-series is intended for mixed power/control/data/video applications. This still does not provide a controlled 100-ohm differential path; RS-485 and video remain physical qualification items.

## 5. Preferred mixed model — M220-0205-12S

Part:
- manufacturer: SenRing;
- model: `M220-0205-12S`;
- outside diameter: 22 mm;
- length: 40 mm;
- two power circuits: 5 A each, AWG22 silver-plated PTFE leads;
- twelve signal circuits: 2 A class, AWG26 silver-plated PTFE leads;
- total physical circuits: 14.

Why a 14-contact device is acceptable:
- PX-1 still has only six **functional** tether/camera circuits;
- unused physical slip-ring contacts do not add tether cores or system functions;
- the extra rings remain insulated/spare;
- no external cassette/module architecture is introduced.

Procurement status:
- model exists in current SenRing controlled catalog;
- manufacturer M220 family is a standard stocked/current product family;
- an active SenRing/Alibaba marketplace route exists for M220 configurations, with MOQ 1 on some current listings;
- some regional SenRing listings mark the exact mixed model as `order`, so delivery time must be confirmed before final BOM freeze.

This is therefore a real orderable engineering candidate, not yet a bought/qualified production part.

## 6. RMP300 reel allocation

Use `M220-0205-12S` as the preferred Rev.B reel candidate.

Power circuits:
- P1: HV+
- P2: HV-

Selected signal circuits:
- S1/S2: RS485_A / RS485_B
- S3/S4: VIDEO+ / VIDEO-

Remaining S5...S12:
- individually insulated;
- not paralleled in Rev.B;
- not used as hidden grounds/drains;
- may be retained as service spares only after continuity labelling.

### Why not parallel spare signal circuits

Paralleling rings without manufacturer guidance can create unequal contact sharing and unexpected signal stubs. Rev.B leaves unused rings open/insulated.

### Reel electrical margin

120 V tether power is below the manufacturer's 240 V class.

WB06 normal long-line current is around 1.0...1.2 A class; a 5 A dedicated power channel therefore has large current margin.

Signal channel current rating is irrelevant to impedance quality. RS-485/video still need waveform testing while the reel rotates.

## 7. Camera rotating-load correction

A miniature six-circuit 1.5 A slip ring such as `M125-06` initially looks attractive because it is only Ø12.5 x 13.5 mm.

It is **not frozen** for PX-1 because one rotating +12 V/GND pair has to supply more than just logic:
- PAN motor stall screen: <=1.1 A;
- camera electronics reserve: ~0.3 A class until exact camera is measured;
- rotating MCU/buck/sensors: reserve ~0.1...0.2 A referred to 12 V;
- full LED lighting reservation can approach ~1 A at 12 V system level depending final light topology.

Conservative simultaneous fault/transition screen is therefore approximately 2.5 A or more.

Conclusion:
- `M125-06` 1.5 A/circuit is REJECTED as the current camera power interface unless later measurements and hard current limits prove the total rotating load stays below its rating with margin.

## 8. Camera preferred candidate

The same mixed `M220-0205-12S` family is the preferred **engineering** candidate for the camera because it gives:
- dedicated 5 A +12 V circuit;
- dedicated 5 A GND circuit;
- dedicated signal-class contacts for UART and CVBS;
- 22 mm OD within the current Ø60-class rear camera envelope;
- 40 mm body length within the current rear-envelope study class;
- common spare family with the reel.

Camera allocation:
- P1: +12V_ROT;
- P2: GND_ROT;
- S1/S2: CAM_UART_TX / CAM_UART_RX;
- S3/S4: CVBS_SIGNAL / CVBS_RETURN;
- remaining S circuits insulated spare.

This preserves six functional camera circuits established in WB12.

### Packaging HOLD

Although Ø22 x 40 mm fits the current gross rear-camera envelope, exact flange/lead exit/wire bend and surrounding bearing/seal geometry must be included in camera CAD before machining release.

Do not replace COM-001-800 mounting metalwork by eyeballing the catalog cylinder.

## 9. Alternative smaller high-current six-way device

SenRing catalogs a configuration example `M155C-0605`:
- OD 15.5 mm class;
- six circuits;
- 5 A per circuit.

This is mechanically very attractive for the camera, but Rev.B has not yet verified a normal marketplace stock listing for this exact article. It remains a **procurement fallback**, not the active frozen purchase.

If an exact marketplace listing/manufacturer quotation with controlled drawing is obtained, it may replace M220 in the camera only after video/UART tests. Reel selection remains independent.

## 10. Signal integrity limitations

SenRing's `<0.01 ohm electrical noise` is a contact-resistance/noise statement. It is not equivalent to:
- 100-ohm characteristic impedance;
- Cat5e pair geometry;
- guaranteed RS-485 common-mode margin;
- guaranteed CVBS frequency response.

Therefore the rotary interfaces are treated as short discontinuities in the transmission line and must be tested as part of the complete system.

For reel and camera:
- keep each selected differential/video signal pair together in the harness;
- twist the external pigtail pair immediately after the slip-ring leads;
- minimize untwisted length;
- keep signal leads physically away from HV/power loops;
- do not bond spare contacts to chassis/ground as an improvised shield.

## 11. Ring-order HOLD

Current public model tables do not define the internal axial ring order for the mixed `M220-0205-12S` sufficiently for PX-1 crosstalk optimization.

Before purchase/release obtain from supplier:
- exact pin/ring sequence;
- lead color map for this mixed article;
- which physical rings are P1/P2 versus S1...S12;
- whether paired adjacent signal rings can be specified;
- whether any pair is characterized for video/data;
- exact flange version/drawing;
- standard lead length and allowable lead shortening.

Do not assume generic M220 color numbering is identical to a mixed-current build until continuity is measured.

## 12. Incoming inspection

For every purchased slip ring:
1. photograph label and lead colors;
2. map every stator lead to rotor lead with an ohmmeter;
3. record static contact resistance;
4. rotate slowly and log resistance/noise for every used circuit;
5. insulation test power-to-signal and used-to-unused circuits at a safe qualified test voltage;
6. run current heat test on power contacts;
7. only then connect electronics.

## 13. Reel qualification

Test sequence:
- 120 V supply disabled: RS-485/video first;
- rotate reel at normal hand-winding speed;
- then apply protected low-energy HV/dummy load;
- then 40 m crawler test;
- finally 100/150 m equivalent.

Record:
- HV contact drop under ~1.2 A line current;
- contact-temperature rise;
- RS-485 error/CRC count;
- RS-485 common-mode behavior;
- CVBS amplitude/sync/chroma;
- video dropouts while rotating.

## 14. Camera qualification

Before connecting camera electronics:
- load P1/P2 to 3 A class for short thermal/contact test;
- verify no unacceptable voltage modulation while rotating;
- then test UART through S1/S2;
- then raw CVBS through S3/S4 into WB12 balun;
- run PAN motor and LED PWM simultaneously;
- repeat continuous camera rotation and direction changes.

A slip ring that passes DC resistance but produces visible video bands or UART errors is rejected.

## 15. Sealing/serviceability

Neither M220 unit is IP-rated for direct sewer immersion; IP51 is insufficient.

Camera:
- slip ring stays inside the separately sealed camera/rotate housing;
- original CAM026-style O-ring boundaries remain outside it;
- slip ring replacement must not require disturbing lens-window seals.

Reel:
- slip ring stays inside the protected left-side reel enclosure;
- it is not a water-pressure boundary;
- replacement is by opening the service cover, not dismantling the drum bearings unnecessarily.

## 16. WB13 decisions

- **Reel:** replace earlier M220-0605 preference with `M220-0205-12S` mixed power/signal candidate.
- **Camera:** reject M125-06 as default because 1.5 A per power circuit is too close to the rotating-load fault envelope.
- **Camera preferred engineering candidate:** `M220-0205-12S`, subject to exact camera CAD.
- **Smaller fallback:** M155C-0605 only if exact source/drawing is obtained.
- Main six-core tether architecture remains unchanged.

## 17. WB13 closure gates

1. obtain controlled drawing/ring order for exact M220-0205-12S;
2. confirm marketplace order route and lead time;
3. buy at least two samples plus one spare/test unit if budget permits;
4. CAD-fit camera unit with flange/leads/service access;
5. incoming resistance/insulation/current test;
6. complete WB09 RS-485 tests through reel ring;
7. complete WB12 video tests through both ring locations;
8. camera 3 A-class power-contact short test and measured normal load;
9. reel 120 V / 1.2 A-class loaded rotation test;
10. only then release mounting metalwork and harness drawings.

## Change log

### 2026-09-11 — WB13
- compared original CAM026 6-way and RMP300 12-pole rotary architecture;
- corrected the old all-5A reel-ring preference to a mixed power/signal design;
- rejected a tempting 1.5 A miniature camera ring before it became a hidden current bottleneck;
- selected one common M220 mixed family as the leading reel/camera engineering candidate;
- retained signal integrity and exact ring order as physical/supplier release gates.
