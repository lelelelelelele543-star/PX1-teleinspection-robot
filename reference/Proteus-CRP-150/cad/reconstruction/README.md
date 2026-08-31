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
| `PX1_X200_RevGK_PROVISIONAL.step.gz` | Gzip-compressed whole-crawler STEP checkpoint | PROVISIONAL - not for machining |
| `PX1_SIDE_DRIVE_RevGN_PROVISIONAL.step.gz` | Gzip-compressed left side-drive STEP checkpoint | PROVISIONAL - not for machining |

These checkpoints preserve the current engineering work. Their presence does not promote reconstructed dimensions to factory-confirmed dimensions.

Decompress with `gzip -dk FILE.step.gz` before opening in FreeCAD.

## SHA-256 of decompressed STEP files

```text
PX1_X200_RevGK_PROVISIONAL.step       07676f664a2336969910af4db3567c713c65d9119e724d497f7242439d73a5a5
PX1_SIDE_DRIVE_RevGN_PROVISIONAL.step 271cc81fafdf9d0d644d882b8472e06d1f29f3cda11964e28a31bb8631739148
```
