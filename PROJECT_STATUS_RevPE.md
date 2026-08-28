# PX-1 Rev.PE — CRP150 manual lift + RMP300 reel source-faithful baselines

Status: ACTIVE PROTEUS-REFERENCE MASTER DEVELOPMENT. Not machining release.

## Design rule
PX1 follows the MiniCam Proteus CRP-150/RMP300 mechanical architecture as closely as practical. Deviate only where a proprietary/obsolete/expensive part must be replaced by a readily available serviceable alternative.

## Rev.PD — manual camera lift
Source: `DRW-002-744`.

Source-supported topology retained:
- 1x `SPR-002-524` gas spring, 150 N;
- 2x `FSS-002-068` lever side;
- 1x `FSS-002-073` lever sheet plate;
- 1x M8 clamping lever;
- 3x DIN2093 20x10.2x1.1 Belleville washers;
- 2x 15x2.5 O-rings;
- 4x 8x0.8 circlips;
- M6x18 pin and source axle/washer arrangement.

The available assembly PDF does not dimension the lever-arm lengths, pivot spacing, exact gas-spring closed/open lengths or detailed housing profile. Those are deliberately left parametric/HOLD rather than guessed from the drawing image.

CadQuery source:
`mechanical/cadquery/PX1_CRP150_Lift_RevPD.py`

Validation:
- all modeled solids valid;
- topology matches DRW-002-744;
- dimension status remains HOLD where the source does not provide numbers.

## Rev.PE — RMP300 manual reel
Source stack:
- `ASS-004-097` complete RMP300 reel;
- `ASS-002-710` layering spindle;
- `ASS-002-711` main shaft;
- `ASS-002-712` crank handle;
- `ASS-002-696` / `ASS-004-092` measure unit;
- `ASS-004-093` drum/kern;
- `ASS-004-094` left side/slip-ring side;
- `ASS-004-095` right side/chain+brake side.

Source-supported hard dimensions already carried into CAD:
- layering spindle: 272 mm;
- crank handle: 160 mm;
- frame bar: 362 mm;
- reel axle source designation: 292.

Source architecture retained:
- fully manual drum;
- mechanical crank;
- mechanical brake;
- chain-driven level-wind/layering system;
- measuring roller unit;
- main shaft/slip-ring path;
- no reel drive motor.

Electrical simplification:
- original `PCB Meterzähler` is deleted from PX1;
- replace distance pickup with a standard magnetic or optical encoder module on the measuring wheel;
- original 12-pole proprietary slip-ring/PCB arrangement is not copied; use an off-the-shelf 6–12 circuit slip ring matched to the PX1 six-conductor tether and required current/voltage;
- reel remains mechanically useful even if the counter electronics are unplugged.

CadQuery source:
`mechanical/cadquery/PX1_RMP300_Reel_RevPE.py`

Validation:
- all modeled solids valid;
- known source dimensions are explicit;
- frame height/depth, drum dimensions, brake-disk diameter, chain sprockets and exact measuring-wheel diameter remain HOLD because they are not dimensioned in the currently retrieved assembly files.

## Immediate next block
1. search the project source set for detail drawings of lift parts `FSS-002-068`, `FSS-002-073`, `FAL-002-067`, `ASS-002-723`;
2. search for detail drawings of RMP300 drum, chain drive, measuring wheel and brake parts;
3. replace each HOLD geometry with source dimensions as found;
4. integrate Rev.PD lift onto Rev.PB crawler and run folded-camera / DN150 checks;
5. integrate Rev.PE reel with the actual six-core tether bend radius and 40 m starting cable capacity;
6. only then choose replacement bought parts.
