# Reconstruction CAD

Only original engineering reconstruction files may be stored here. Factory PDFs, copied drawing sheets and unmodified proprietary CAD are excluded from the public repository.

Every model must include:

- revision and date;
- source identifiers used;
- confirmed versus reconstructed dimensions;
- unresolved interfaces;
- manufacturing-release state.

Current generated STEP models remain provisional until the shaft, bevel-gear and side-drive tolerance chains are verified.

## Current models

| File | Purpose | Release state |
|---|---|---|
| `PX1_X200_RevGK_PROVISIONAL.step.gz` | Gzip-compressed whole-crawler STEP checkpoint | REJECTED-ARCHITECTURE - historical only |
| `PX1_SIDE_DRIVE_RevGN_PROVISIONAL.step.gz` | Gzip-compressed left side-drive STEP checkpoint | REJECTED-ARCHITECTURE - historical only |

These checkpoints preserve historical engineering work. They must not be used for machining or as a base for a released revision. Audit against DRW-002-374/375/386 found four source conflicts: module-1.25 gears instead of module 1.0, center-wheel input instead of the rear long axle, and a 170x1.5 side-cover O-ring instead of SEA-002-102 190x1.5. See [`../../crawler/GEAR_AND_SHAFT_AUDIT.md`](../../crawler/GEAR_AND_SHAFT_AUDIT.md).

Decompress with `gzip -dk FILE.step.gz` before opening in FreeCAD.

## SHA-256 of decompressed STEP files

```text
PX1_X200_RevGK_PROVISIONAL.step       07676f664a2336969910af4db3567c713c65d9119e724d497f7242439d73a5a5
PX1_SIDE_DRIVE_RevGN_PROVISIONAL.step 271cc81fafdf9d0d644d882b8472e06d1f29f3cda11964e28a31bb8631739148
```
