# PX-1 Rev.CU — sealed pressurized side gear covers

Status: architecture update. Supersedes the open/draining gear-guard concept from Rev.CT.

## User requirement
The side gear trains must be covered by removable sealed covers. Covers use replaceable gaskets/O-rings, and the enclosed drive volume is maintained at slight positive pressure relative to ambient.

## Architecture
Each side of the crawler has a rigid removable cover over the complete external spur-gear train:
- cover is bolted directly to a machined sealing land on the main side structure;
- continuous elastomer gasket or O-ring sits in a dedicated groove;
- no intentional drain holes through the sealed cavity;
- wheel shafts pass through dedicated radial shaft seals;
- cover has no structural wheel load; it is only a protective pressure boundary;
- service access is by removing the bolted cover with ordinary hand tools.

## Pressurization philosophy
The side gear cavities shall be connected to the crawler dry pressure volume through a small protected equalization passage so the complete sealed system can be pressurized from one service fill point.

Initial design target for prototype testing:
- slight positive gauge pressure only;
- nominal working target around +0.2 to +0.3 bar;
- pressure relief / maximum permitted pressure must be defined before RELEASE;
- exact pressure must be validated against all shaft seals, window, connectors and covers.

Positive pressure is a secondary barrier against water/mud ingress. It does NOT replace correct shaft seals, O-rings or gasket compression.

## Cover sealing
Preferred final solution:
- machined aluminium cover;
- continuous O-ring in a captured groove rather than flat-cut sheet gasket where geometry permits;
- NBR for general prototype use; FKM considered where oil/chemical/temperature resistance justifies cost;
- cover screw spacing sized so gasket compression remains uniform around the full perimeter;
- locating dowels or machined register take shear/alignment; cover screws provide clamp load only.

Exact O-ring cross-section and groove dimensions are HOLD until cover geometry and pressure proof target are frozen.

## Gear cavity
Because the cavity is sealed, do not intentionally fill it with heavy grease that can churn and trap contamination. Initial prototype preference is lightly lubricated metal gears inside a clean sealed cavity. Lubricant type/quantity must be tested for low-temperature drag and long-duration wear.

## Pressure monitoring
The internal pressure sensor already planned for PX-1 shall monitor the common pressurized volume. The console should alarm on pressure loss. A pressure-decay test becomes part of pre-use inspection.

Recommended workflow:
1. pressurize crawler before deployment;
2. verify pressure stabilizes;
3. monitor pressure during operation;
4. if pressure falls outside allowed band, flag possible leakage and recover robot.

## Serviceability
- both side covers are individually removable;
- O-ring/gasket is replaceable and should be stocked as a service item;
- gear train is accessible without removing the electronics tray where possible;
- sealing surfaces must be inspectable and cleanable in the field;
- captive cover screws preferred.

## Mandatory tests before RELEASE
- static pressure proof test;
- pressure decay/leak test;
- immersion test under representative external water head;
- shaft rotation while pressurized and immersed;
- thermal cycling low/high temperature followed by leak test;
- grit/mud exposure outside the cover;
- repeated cover removal/reassembly to validate seal robustness.

## Release gates
- final working and proof pressure;
- cover wall thickness and screw pattern;
- exact O-ring/gasket material and groove;
- shaft seal type and shaft surface specification;
- pressure equalization passage details;
- pressure relief method;
- validated leakage rate and acceptance criterion.
