# PX-1 MASTER DESIGN BASIS — Proteus CRP-150 replacement system

Status: ACTIVE MASTER DIRECTIVE.

## Mission
Build a serviceable, lower-cost teleinspection system that preserves the proven MiniCam Proteus CRP-150 / CAM026 / RMP300 user experience and mechanical logic while replacing proprietary, obsolete, expensive or hard-to-source parts with readily available equivalents.

This document supersedes earlier experimental PX1 concepts where they conflict with the Proteus-reference architecture.

## System-level rule
Preserve where possible:
- crawler external form and DN150-class packaging;
- six-wheel crawler layout;
- three driven wheel stations per side;
- five equal side gears per side;
- rear wheel long-axle input architecture;
- Z16 -> Z40 bevel input with two motors total;
- manual camera lift with 150 N gas spring and M8 clamp;
- CAM026-like 360-degree ROTATE and +/-135-degree PAN envelope/function;
- lightweight manual RMP300-style reel with level-wind, brake, measuring wheel and slip-ring path;
- simple portable control console workflow.

Change where needed:
- motors;
- controller electronics;
- motor drivers;
- video electronics;
- pressure sensor electronics;
- connectors;
- slip ring;
- distance encoder;
- bearings/seals only when original sizes are unavailable or a direct standard replacement is preferable;
- camera imaging module and focus system.

## Crawler baseline
Source references: DRW-002-374, DRW-002-375, DRW-002-386.

Active side-drive topology, each side:
- wheel Z50;
- idler Z50;
- wheel Z50;
- idler Z50;
- driven rear wheel Z50 on long axle.

The rear wheel is the driven input station. There is no separate fourth input shaft.

Source bearing/seal architecture per side:
- 1x 61801-class bearing on long-axle/input path;
- 3x 61903-class wheel bearings;
- 3x X-ring 18.72x2.62;
- 3x static axle-flange O-rings 32x1.5;
- side-cover O-ring 190x1.5;
- two small idler bushings 10-12-4.

Main crawler body source architecture:
- 2x Z40 large bevel gears;
- 2x 18x30x7 shaft seals;
- 2x 61800 10x19x5 bearings;
- lift holding/axle parts integrated into body.

Motor unit source architecture:
- 2 motors total;
- 2x Z16 small bevel gears;
- 2x supported bevel pinion shafts;
- 2x 61801 bearings.

Official CRP-150 control envelope used as target reference: about 307 x 133 x 110 mm.

## Manual lift baseline
Source: DRW-002-744.

Retain:
- 1x gas spring 150 N;
- 2 side levers;
- lever sheet plate;
- M8 clamping lever;
- Belleville spring stack;
- source-style axle/washer/circlip arrangement.

Do not invent new powered lift mechanisms unless the manual source architecture proves impossible to reproduce.

## Camera baseline
Source family: CAM026 assembly drawings.

Target reference function/envelope:
- CAM026-like external form;
- continuous 360-degree ROTATE;
- PAN +/-135 degrees;
- roughly 75-degree forward FOV class;
- two clusters of 3 white LEDs around the lens;
- separately sealed camera module.

Simplification:
- delete proprietary motor-control PCBs;
- delete proprietary focus motor/gear/PCB;
- use a fixed-focus modern camera module/lens where practical;
- use standard replaceable motor driver modules;
- use an off-the-shelf slip ring sized for the required circuits;
- retain mechanical sealing/axis logic where practical.

## RMP300 reel baseline
Source family: ASS-004-097 and child assemblies.

Retain:
- manual drum;
- 160 mm crank handle;
- mechanical brake;
- 272 mm level-wind spindle;
- main reel shaft/slip-ring path;
- measuring roller assembly;
- mechanical level-wind driven from drum motion;
- lightweight portable frame concept.

Simplify:
- no reel drive motor;
- delete proprietary meter-counter PCB;
- replace distance pickup with a standard magnetic or optical encoder module;
- replace proprietary 12-pole slip-ring/PCB arrangement with a readily available serviceable slip ring matched to PX1 tether current/voltage/circuit needs.

## Tether
Use one professional reinforced six-core copper inspection cable, Proteus-like in principle:
- no coax;
- no optical fiber;
- no bundle of ordinary loose twisted pairs;
- aramid/Kevlar strength path separate from electrical contacts;
- field-repairable/reterminable.

Initial length: 40 m. Longer 100-150 m versions are accepted only after real conductor-resistance and cable-loss measurement.

## Electronics philosophy
No custom main PCB for the prototype.
Use standard, replaceable modules and simple wiring:
- MCU/controller module;
- two traction H-bridge channels;
- camera PAN/ROTATE driver channels;
- RS-485;
- pressure sensor;
- video interface;
- simple DC/DC conversion as required;
- encoder inputs for distance/odometry.

The electronics must be cheaper and easier to replace than original Proteus P01/CAM/reel boards.

## Release rule
No feature is added merely because it is technically interesting. A deviation from Proteus must have a clear benefit in at least one of:
- availability;
- cost;
- field repairability;
- manufacturing simplicity;
- reliability.

If the original Proteus mechanical solution already works well and can be reproduced economically, keep it.
