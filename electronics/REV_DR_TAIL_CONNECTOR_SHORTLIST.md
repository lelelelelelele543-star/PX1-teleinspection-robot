# PX-1 Rev.DR — rugged digital tail connector shortlist

Status: prototype shortlist. The old coax-hybrid connector requirement is superseded by the fully digital tether architecture.

## Requirements
Rear electrical connector must support:
- 48 V tether power;
- at least one balanced data pair for 10BASE-T1L;
- preferably one spare pair/service circuit;
- IP68 when mated;
- wet/gloved field operation;
- compact CRP150-class rear body packaging;
- no tether tensile load on the contacts;
- replaceable panel-side receptacle.

## Leading low-cost industrial candidate — Amphenol LTW X-Lok Standard B, 6-pin mixed-current family
Current manufacturer data for BBD 6-contact variants show:
- push-lock mating;
- IP68 when mated;
- 300 V rating;
- mixed current family marked **10A + 5A**;
- 6 contacts;
- overmolded cable example OD about 9.3 mm;
- operating temperature examples -20…+85 °C;
- 16/26 AWG mixed cable examples.

This contact mix is attractive for PX-1 because it can potentially allocate the higher-current contacts to +48V/0V and the smaller contacts to the differential pair(s).

### Important limitation
The cited X-Lok mixed-power variant is not marketed as an Ethernet connector; manufacturer pages list transmission speed as N/A and plastic examples are non-shielded.

Therefore it is **not yet released for 10BASE-T1L**. It becomes the leading prototype candidate only if a real 150 m tether link test passes with adequate BER/link margin, motor PWM active and the connector wet/dirty cycling completed.

Tether braid/pair shield can terminate to chassis separately from the plastic connector shell if EMC testing supports this arrangement.

## Robust fallback — Bulgin 900 Series Buccaneer
Manufacturer data show:
- IP68 and IP69K class;
- up to 32 A / 600 V family rating;
- 2/3/4/5/7/10-contact variants;
- fast locking ring usable with gloved hand;
- cable acceptance roughly 7–22 mm depending version;
- field screw termination;
- specifically positioned for harsh wet/dust industrial environments.

### Why it is only fallback
The 900 Series is physically large; current 7-contact inline example data show a coupling diameter around 58 mm. That is excessive for the compact CRP150-style tail unless later packaging proves we need this level of field termination and power robustness.

## Premium fallback
LEMO K-series remains an engineering fallback when:
- smaller shell size is essential;
- repeated mating life and environmental sealing justify the price;
- exact multipole contact arrangement is validated for our data pair.

The old 5K.870 coax-hybrid arrangement is no longer preferred because PX-1 no longer needs coaxial video contacts.

## Prototype pin allocation target
Six-contact minimum concept:
- P1: +48 V;
- P2: 0 V;
- P3/P4: 10BASE-T1L pair;
- P5/P6: spare differential/service pair.

If exact mixed-current contact mapping differs, pin numbers are reassigned accordingly. Do not parallel unmatched signal contacts for power.

## Connector qualification
Before production freeze:
1. exact panel receptacle + cable plug pair obtained;
2. 48 V current/temperature-rise test;
3. 150 m tether 10BASE-T1L BER/link-margin test;
4. test with both traction motors PWM/reversing;
5. 100 mate/unmate cycles minimum prototype gate;
6. mud/wash contamination test;
7. submerged mated pressure test;
8. verify contacts remain completely unloaded during 1 kN tether pull test.

## Current decision
Use **Amphenol LTW X-Lok B-size 6-pin 10A+5A family as first connector sample to investigate**, not as a manufacturing release.
Bulgin 900 remains the simple heavy-duty field-service fallback.
