# PX-1 Rev.CH — rugged tether cable selection

Status: architecture candidate; exact vendor cable still OPEN.

## Requirement correction
PX-1 must not use an office/patch Ethernet cable as the tether. The tether is a mechanical umbilical first and a data cable second.

## Baseline construction
Preferred cable construction for PX-1:
- hydrolysis-resistant PUR/TPU outer jacket;
- stranded tinned-copper conductors;
- at least one individually shielded twisted pair for the long digital link;
- 2 dedicated power conductors;
- aramid/Kevlar or Dyneema tensile strength member/braid;
- dynamic-flex construction intended for ROV/robot tether service;
- water, oil, mud, abrasion and UV resistance;
- replaceable field termination at the crawler tail;
- electrical connector isolated from towing load by a separate strength-member termination.

## Preferred electrical core layout
For the current 10BASE-T1L architecture, the minimum useful core set is:
- 2 x power conductors, target 1.0–1.5 mm² each for the first 100–150 m study;
- 1 x shielded twisted pair, target 0.2–0.5 mm² conductors, for 10BASE-T1L;
- optional second shielded pair for service/RS-485/redundancy.

A 2x16AWG + 2x2x26AWG ROV-style tether is a good reference class: 2 x 16AWG power conductors plus two shielded twisted pairs inside a foamed PUR jacket. It is electrically more than sufficient for PX-1 and leaves one spare differential pair.

## Mechanical target values for vendor request
These are purchase targets, not yet released specifications:
- nominal OD: preferably 8–12 mm;
- dynamic minimum bend radius: <= 8x cable OD preferred;
- working temperature: at least -30..+70 °C;
- tensile working load: >=1 kN preferred;
- minimum breaking load: >=2 kN preferred;
- jacket: high-abrasion hydrolysis-resistant PUR;
- strength element: Kevlar/aramid or UHMWPE/Dyneema;
- repeated bending: vendor must state dynamic-flex capability;
- water ingress: continuous wet use, not merely splash-rated;
- length: 40 m prototype, scalable to 100–150 m without changing cable family.

## Current market references
1. ROV-style 2 power + 1 twisted pair, foamed PUR, tinned copper, optional Kevlar/Dyneema reinforcement.
2. ROV-style 2x16AWG + 2x2x26AWG, foamed PUR, individually shielded pairs; good PX-1 electrical reference.
3. Underwater hybrid 16x24AWG + 4x2x26AWG, PUR, braid strength member, optional Kevlar, OD about 11.1 mm — mechanically relevant but electrically excessive for PX-1.

## Important design rule
The outer cable jacket and electrical conductors must never be the primary towing member. The aramid/UHMWPE strength element is terminated into a dedicated clamp/eye in the rear tail. Electrical cores receive a service loop after that clamp and enter the waterproof connector without tensile preload.

## Current recommendation
For prototype sourcing, search first for a custom ROV tether in the class:
**2 x 1.0–1.5 mm² power + 1 or 2 shielded twisted pairs + Kevlar/aramid strength member + hydrolysis-resistant PUR jacket, OD <=12 mm.**

Neutral buoyancy is not a hard PX-1 requirement because sewer-pipe crawling benefits from a cable that stays low and does not float into the camera/lift. A slightly negative-buoyant cable is acceptable and may be preferable.

## Release gates
- exact DC voltage drop at 40/100/150 m using real crawler current;
- exact tensile working load and breaking load from vendor datasheet;
- dynamic bend-cycle specification;
- jacket cut/abrasion test;
- cold-flex test;
- measured OD and compatibility with the selected tail connector/collet;
- proof pull of the rear strength-member termination.
