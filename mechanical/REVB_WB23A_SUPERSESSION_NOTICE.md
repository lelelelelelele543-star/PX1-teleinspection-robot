# Rev.B WB23A routing supersession notice

Date: 2026-09-14

WB23A remains useful evidence that a thin local harness and guard can fit the lower lift arm. It is **not** the controlling camera-lift routing release after WB23C.

Two reasons:

1. WB23A's one-sided `Workplane('XZ')` helper introduced a Y-direction/sign ambiguity for asymmetric cover geometry. Symmetric lift-arm checks were not materially affected, but absolute one-sided Y placement must not be used as manufacturing data.
2. WB23B then overextended the study into dedicated radius-controlled flex chambers. Repair photographs and MiniCam source drawings support a simpler removable pressure-cover + M12 gland + protected short harness topology.

Controlling interpretation after this notice:

- hard lift/camera geometry: **WB22A**;
- pressure/service cover and local harness topology: **WB23C**;
- camera quick connector: **WB15**;
- WB23A: historical static-packaging study only.

Do not use WB23A clamp coordinates, its sign-sensitive absolute Y construction, or the abandoned WB23B flex-fan concept in machining drawings.
