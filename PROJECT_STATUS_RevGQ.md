# PX-1 Rev.GQ — first-article traction build plan

Status: PROTOTYPE BUILD STRATEGY BASELINE; not machining release.

## Completed in Rev.GQ
Two manufacturing documents now convert the active engineering model into a controlled first-build sequence:
- `manufacturing/ME-PX1-610_FIRST_TRACTION_BUILD_RevGQ.md`
- `mechanical/REV_GQ_WHEEL_PROTOTYPE_PROCESS.md`

## First-article strategy
Do not machine six wheel stations at once.

Gate A — buy/measure one sample of each fit-controlled bearing, seal, gear and exact Ø32 motor.

Gate B — build one wheel station WS-01 and prove:
- bearing fits;
- seal drag/leak behaviour;
- shaft runout;
- keyed wheel fit;
- M8 axial retention;
- wet rotation and repeated wheel service.

Gate C — build one complete LEFT side drive and prove:
- five-Z50 train;
- X200 bevel input;
- all three wheels same direction;
- no tight spot/backlash error;
- current/temperature under load;
- controlled reversal and blocked-wheel behaviour.

Only then duplicate the right side and remaining wheel stations.

## Wheel prototype process
Common metal core remains keyed and retained by the active Rev.GF interface.

SR and HG wheels are complete swappable wheel assemblies, not a field-change tire cartridge.

Prototype route:
- machine one common metal core;
- verify core/key/retainer before elastomer;
- 3D print split molds on Anycubic Chiron;
- cast/overmold SR or HG elastomer onto prepared core;
- use mechanical bond grooves plus a compatible primer/adhesive system;
- use TPU only for fit/mold/low-load checks, not as proof of final wet traction.

Exact Shore hardness is held until PX1-TP-020 pull testing.

## FEM tool state
The current execution environment has CadQuery/OpenCascade/SciPy but no installed CalculiX, Gmsh or FreeCAD solver binary. Rev.GM therefore remains a pre-FEA analytical screen.

The pressure body is not released for machining until a true 3D FreeCAD/CalculiX run is completed with:
- Rev.GP ballast bosses;
- rear motor extension transition;
- X200 cartridge loads;
- 0.6 bar differential pressure cases;
- 2 kN tether proof load/off-axis moment.

## Current highest-value physical information still missing
1. exact Ø32 motor sample/drawing and torque-current-speed data;
2. actual selected 6701/61801/61903/61800 bearings;
3. actual X-ring and 18x30x7 seal articles;
4. actual 6-core tether mass per metre and OD;
5. measured wet traction of first SR/HG wheel samples.

These measurements now matter more than further cosmetic CAD refinement.

## Next autonomous engineering block — Rev.GR
- generate first-article inspection sheets for WS-01 and LEFT side drive;
- formalise datum/measurement points so shop measurements feed directly back into CAD;
- prepare CalculiX/FreeCAD load cases and boundary-condition specification;
- continue exact motor/tether procurement search without changing geometry until a sample is justified.
