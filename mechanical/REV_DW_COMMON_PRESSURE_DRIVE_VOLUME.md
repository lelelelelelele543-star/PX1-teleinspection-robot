# PX-1 Rev.DW — common pressurized body + side-drive volume

Status: packaging-driven architecture decision. Supersedes Rev.DH/Rev.DS three independently sealed pressure zones for the first DN150 prototype.

## Reason for change
The CRP150-style six-wheel drivetrain now uses:
- m1.5 Z18/Z45 bevel stages;
- five equal m1 Z50 side gears per side;
- compact wheel-bearing/seal bosses;
- DN150 overall-width constraint.

Keeping an additional rotary pressure boundary between the large bevel gear and each side gear consumes too much axial width and forces the wheel/cover outward. That reduces DN150 clearance and adds two more dynamic seals.

The user-required function is retained: rigid side covers with real seals and the crawler operated under positive internal pressure.

## Prototype pressure architecture
For the first build, use one common dry pressure volume encompassing:
- central traction/electronics body;
- left side gear bay;
- right side gear bay.

Normal operating target remains +0.20…+0.30 bar gauge.

Primary boundaries to sewer are:
- six wheel-shaft rotary seals;
- left side-cover continuous O-ring;
- right side-cover continuous O-ring;
- main electronics/service cover O-ring;
- camera/tail/fill-port seals.

No internal dynamic shaft seal is used between bevel stage and side gear bay in this prototype.

## Reliability compensation
Because a wheel-seal leak can now depressurize the common volume:
- pressure decay is continuously monitored;
- add at least one water/leak sensor at the lowest internal point;
- electronics sit on a raised removable tray, not on the body floor;
- critical PCB assemblies receive conformal coating where compatible with connectors/sensors;
- no automatic compressor masks a leak during operation;
- rapid pressure loss produces STOP/RETURN fault.

## Fill/test
- one service fill valve;
- surface fill target ~+0.25 bar;
- temperature-compensated 30 min leak test before deployment;
- submerged static test;
- submerged six-wheel rotating test;
- routine pneumatic operation remains low pressure;
- structural proof of covers/body remains a separate controlled qualification test.

## Why this is acceptable for prototype
This removes two dynamic seals, several carriers and axial spacers, reduces width, and makes the mechanical drivetrain much closer to the compact CRP150 packaging class.

If prototype leak/endurance testing shows that independent side-bay isolation is necessary, Rev.DH remains an upgrade path for a larger-body/DN200+ variant or a redesigned smaller bevel stage.

## Release gates
- complete CAD of common volume and side covers;
- pressure sensor selected;
- leak detector selected/located;
- empty-body pressure-decay test;
- 2 h submerged rotating-wheel test;
- deliberate single-seal leak simulation to verify alarm time;
- electronics splash-path review.
