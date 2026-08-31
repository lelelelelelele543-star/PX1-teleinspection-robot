# Replacement-parts strategy

Revision 0.1, 2026-08-31.

## Decision rule

Keep a Proteus part when it is a standard available component or can be manufactured economically. Replace it only when it is proprietary, unavailable, excessively expensive, a known recurring failure point, or incompatible with the 24 V modular prototype.

## First replacement matrix

| Function | Original architecture | Replacement direction | Status |
|---|---|---|---|
| Traction gearmotor | FAULHABER 26/1S 66:1 plus unidentified motor | Available 24 V metal gearmotor, nominal 60-120 rpm at bevel input, adapted to the original supported Z16 shaft | Candidate selection required |
| Z16/Z40 bevel pair | Proprietary part codes GEA-002-531 / GEA-002-530 | Manufacture from verified geometry or source a matched standard pair only if center distance and packaging remain compatible | Geometry incomplete |
| Motor-unit pinion bearing | 61801-2RS 12x21x5 | Keep standard bearing | Available standard |
| Body bearing | 61800-2RS 10x19x5 | Keep standard bearing | Available standard |
| Body shaft seal | 18x30x7 | Keep standard seal; select lip material after lubricant and pressure validation | Available standard |
| Wheel bearing | 61903 class | Keep standard bearing after load check | Available standard |
| Wheel dynamic seal | X-ring 18.72x2.62 | Keep standard size where sourcing is stable; validate compound and gland | Specification check required |
| Main controller | Proprietary Mini-Cam PCB | STM32 NUCLEO-F446RE | Project baseline |
| Traction drivers | Proprietary Mini-Cam power stage | Two replaceable BTS7960 modules for prototype testing | Project baseline; current margin must be tested |
| Command link | Proprietary system | RS-485 module over the six-core tether | Project baseline |
| Main tether | Reinforced Proteus inspection cable | Reinforced field-repairable six-core copper inspection cable | Architecture fixed; conductor sizing pending |

## Candidate motor family

The previously selected accessible prototype family is JGB37-520, 24 V, purchased through Ozon or an equivalent marketplace. It is only a candidate family, not an approved exact motor. The accepted variant must meet all of the following on a bench:

- measured no-load output near 60-120 rpm;
- acceptable continuous current at realistic crawler load;
- stall current compatible with wiring, connector and driver protection;
- sufficient starting torque after the 2.5:1 bevel reduction;
- manageable backlash;
- shaft and flange that can couple to a separately supported Z16 shaft;
- repeatable availability from more than one seller.

No seller listing alone is sufficient for approval. Record voltage, no-load speed, no-load current, loaded speed, loaded current, stall current and gearbox backlash for the exact received unit.

## Sourcing constraints

- electronics and ordinary modules: ChipDip where practical;
- traction motors: Ozon or another verifiable available source;
- use standard metric bearings, seals and fasteners;
- avoid custom PCBs in the prototype;
- retain service access with ordinary workshop tools;
- record manufacturer, exact part number, seller URL, purchase date, measured data and replacement alternates.

