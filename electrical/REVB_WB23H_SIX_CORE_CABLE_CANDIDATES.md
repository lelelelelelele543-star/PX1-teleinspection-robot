# PX-1 Rev.B WB23H — real six-core local cable candidates

Date: 2026-09-14
Status: **PRIMARY SAMPLE CANDIDATE SELECTED / EMC + FLEX QUALIFICATION HOLD**

## Hard requirement

The local lift/camera harness is exactly six insulated conductors:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

No seventh/eighth spare core is added merely because a vendor has a convenient cable. Overall braid/shield, if present, is not counted as a signal/power core.

Mechanical interface limits from WB23G:

- target core section: 0.25 mm² class;
- preferred OD: 5.5...6.0 mm;
- absolute current package limit: 6.5 mm because WEIPU SP1310/S6I-N accepts 4.0...6.5 mm and the selected M12 gland accepts 3.5...7 mm;
- cable must tolerate repeated lift movement and wet/grit exposure.

## Candidate A — PRIMARY MECHANICAL/FLEX SAMPLE

### LAPP UNITRONIC FD P plus A 6x0.25

- manufacturer article: `0028679`;
- exactly 6 x 0.25 mm²;
- nominal OD: 5.4 mm in current LAPP data;
- extra-fine stranded copper;
- PUR outer jacket;
- intended for highly flexible / continuously flexing drag-chain service;
- current LAPP minimum bend radius during flexing: 5 x OD, approximately 27 mm nominal for this size;
- max conductor resistance at 20 C: 79 ohm/km in current product data;
- **unshielded**.

Why it is the primary sample:

- correct core count;
- correct conductor section;
- excellent OD for M12 gland and SP13 S6I;
- substantially better dynamic bend requirement than the shielded industrial cordset alternatives found so far;
- PUR jacket and continuous-flex application match the mechanical duty better than ordinary LiYCY.

Main HOLD:

Because it is unshielded, raw CVBS/UART must be tested with traction motors, camera motors and LED PWM active. Do not promote it to production before video/noise qualification.

Availability note (2026-09-14 search): current Czech/EU sellers list article 0028679 in 100 m / 500 m / 1000 m package variants with EU availability. A small cut-length source is still preferable for prototype procurement; do not buy 100 m until a short sample is proven.

## Candidate B — SHIELDED SIZE BENCHMARK / LOW-DUTY SAMPLE

### LAPP UNITRONIC LiYCY 6x0.25

- article used in current study: `0034406`;
- exactly 6 x 0.25 mm²;
- shielded;
- nominal OD about 6.0 mm;
- mechanically fits M12 gland and SP13 S6I;
- but standard application is fixed/occasional flexing rather than a strong continuous-flex lift claim.

Use only as:

- EMC comparison sample;
- bench/video reference;
- short-term prototype if flex cycling proves acceptable.

Do not assume production flex life from the cable name.

## Candidate C — SHIELDED DRAG-CHAIN CORDSET CABLE REFERENCE

### Pepperl+Fuchs V19-G-25M-PUR-A5S-WCS cable construction

Current manufacturer data for this cable/cordset reports:

- 6 x 0.25 mm²;
- PUR jacket;
- OD 6.0 mm;
- foil + tinned-copper braid shield;
- fine-stranded conductor, 19 x 0.13 mm;
- drag-chain suitability;
- minimum 2,000,000 chain cycles;
- moving bend radius >10 x OD (~60 mm).

Advantages:

- exact six-core count;
- shielded;
- proven high-cycle drag-chain duty;
- OD fits current SP13/M12 package.

Disadvantages:

- moving bend-radius requirement is much larger than LAPP 0028679;
- currently surfaced mainly as long pre-terminated M12 cordsets, not convenient short bare cable by the metre;
- therefore this is a material/construction reference and secondary sample path, not current procurement baseline.

## Candidate D — igus chainflex CF9.UL.02.06

- exact 6 x 0.25 mm²;
- TPE chainflex control cable;
- current max OD about 6.5 mm;
- strong high-flex / chain application;
- **unshielded**;
- Czech HENNLICH/TME listings confirm exact article, but current local stock found in search was zero/request-based.

It fits the hard 6.5 mm package only at the upper limit, leaving less connector/gland tolerance than LAPP 0028679. Keep as second unshielded continuous-flex candidate.

## Rejected / not baseline

### HELUKABEL S-PAAR-TRONIC-C-PUR 19103

- 6 x 0.25 mm²;
- shielded and suitable for energy chains;
- OD about 7.2 mm;
- **REJECT for current SP13 S6I package: exceeds 6.5 mm**.

### HELUKABEL SUPER-PAAR-TRONIC 340-C-PUR 49835

- 6 x 0.25 mm²;
- shielded drag-chain cable;
- OD about 8.8 mm;
- **REJECT: much too large for current lift/connector package**.

### SAB Bröckskes SD 90 C

Excellent continuously flexible PUR shielded family, but current standard table for 0.25 mm² contains 2, 3, 4, 5, 7, 12, 18, 25 cores — **no standard 6 x 0.25 article**. Do not substitute the 7-core version; user/project architecture is six-core. A custom six-core build would destroy the current availability/repairability advantage unless later justified.

### LAPP UNITRONIC LiYD11Y 0033306

- 6 x 0.25 mm² and shielded/PUR;
- OD around 6.8 mm in surfaced dimensional data;
- **REJECT for current S6I package unless connector backshell is deliberately reopened**.

## Current engineering decision

For the first physical lift harness, procure short samples in this order:

1. LAPP `0028679` — primary flex/mechanical candidate;
2. one shielded 6 x 0.25 / ~6 mm LiYCY sample such as `0034406` for EMC/video A/B comparison;
3. if obtainable economically, a piece of the Pepperl+Fuchs 6 x 0.25 PUR shielded high-cycle construction as a high-flex shielded comparison.

Do not change SP13 or enlarge the lift merely to accommodate a thicker shielded cable before the unshielded primary candidate is actually shown to fail EMC/video testing.

## Acceptance test for Candidate A

Build one complete prototype harness with the real M12 gland, six-way Micro-Fit and SP13:

- measure all six core resistances;
- run maximum head current and measure camera-terminal voltage;
- run raw CVBS and UART continuously;
- operate traction motors forward/reverse and PWM through full range;
- operate TILT/ROLL and LED PWM simultaneously;
- inspect picture for sync loss/banding/noise;
- run >=500 lift cycles, target 1000;
- repeat video/electrical checks wet and after grit exposure;
- repeat pressure test at the gland after flex cycling.

If Candidate A passes these tests, an overall shield is not mandatory merely because it looks preferable on paper. If it fails EMC, reopen shielded cable/connector packaging with test evidence rather than adding cores.
