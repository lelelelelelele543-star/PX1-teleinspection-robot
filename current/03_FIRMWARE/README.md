# 03 FIRMWARE

Rev.A firmware is intentionally minimal.

First required functions:
- forward/reverse;
- differential steering;
- speed command;
- traction stop on lost communications;
- light level command;
- pressure telemetry;
- basic fault/status telemetry.

After the crawler physically drives through the tether, add distance/OSD/operator conveniences. Do not block A0/A1 mechanics waiting for advanced UI features.

Recommended split:
- `crawler/` — STM32 traction/telemetry firmware;
- `console/` — operator controls/protocol;
- `protocol/` — one documented RS-485 packet definition shared by both ends.
