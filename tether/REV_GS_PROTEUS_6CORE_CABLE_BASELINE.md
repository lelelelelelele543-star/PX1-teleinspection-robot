# PX-1 Rev.GS — Proteus-style single 6-core copper tether baseline

Status: ACTIVE PHYSICAL-CABLE ARCHITECTURE; exact vendor cable still OPEN.

This document supersedes the physical cable construction proposed in Rev.CH.

## Non-negotiable architecture
PX-1 tether is one professional lightweight reinforced inspection cable, in the same design class as the Mini-Cam Proteus cable:
- one overall cable;
- **6 copper conductors total**;
- tensile reinforcement integrated into the cable, preferably aramid/Kevlar class;
- abrasion/water/mud-resistant outer jacket;
- field-repairable/re-terminable;
- no coaxial core;
- no optical fiber;
- no bundle of ordinary separate twisted-pair cables substituted for this architecture.

Two conductors may be electrically used as a balanced differential data channel, but they remain conductors of the single six-core inspection cable; PX-1 is not to be redesigned around Ethernet patch cable or multiple sub-cables.

## Public Proteus mechanical reference
Current Mini-Cam public information gives a strong physical target for the cable class:
- reinforced lightweight 6-core copper cable is retained even for Proteus HD;
- long mainline versions operate to 350-500 m class;
- published reel cable diameter is approximately 6.5 mm;
- Proteus Lite literature gives approximately 6.8 mm in another reel generation;
- cable mass: approximately 5.5 kg per 100 m = 55 g/m;
- breaking strength: approximately 500 kgf = 4.9 kN class;
- Kevlar reinforcement;
- copper construction is explicitly promoted as easily repairable.

These values are reference targets, not permission to claim that a third-party cable is identical to Mini-Cam cable.

## PX-1 mechanical procurement target
Preferred first sample:
- OD target: 6.5-7.0 mm;
- mass target: <=60 g/m preferred;
- six stranded copper conductors;
- integrated aramid/Kevlar tensile member;
- minimum breaking load target: >=4.9 kN preferred if achievable in this size class;
- minimum PX-1 qualification proof load at termination: 2 kN;
- flexible PUR/TPU or equivalent hydrolysis/abrasion-resistant jacket;
- repeated reel bending and crawler deployment service;
- continuous wet/mud use;
- 40 m prototype cut length, same cable family scalable to 100-150 m;
- field strip/retermination possible with ordinary service tooling.

The cable strength member, not the copper conductors or connector contacts, takes towing/recovery load.

## Preliminary six-conductor allocation
Until link and power tests prove otherwise:
1. POWER +V tether bus;
2. POWER 0V return;
3. DATA+ primary long differential channel;
4. DATA- primary long differential channel;
5. SERVICE A;
6. SERVICE B.

Current preferred use of 3/4 is the long digital link class previously studied with 10BASE-T1L. Conductors 5/6 remain available for RS-485 service/redundancy or another differential service channel.

This allocation does **not** require physically separate pair sub-cables. The exact cable sample must be measured to determine whether a chosen pair of cores has acceptable impedance, insertion loss, crosstalk and EMC for the selected PHY.

If the six-core sample fails 10BASE-T1L over 150 m, the answer is to change the PHY/modulation/conditioning while preserving the six-core inspection-cable architecture where possible — not to silently replace the tether with coax, fiber or Ethernet patch cable.

## Cable mass reference for traction planning
At the public Proteus reference mass of 55 g/m:
- 40 m cable mass ≈2.2 kg;
- 100 m ≈5.5 kg;
- 150 m ≈8.25 kg.

Only a portion of that full mass becomes longitudinal crawler drag in a horizontal pipe; actual drag depends strongly on bends, water, surface, payout geometry and reel synchronization. Therefore traction qualification uses measured pull force, not cable mass alone.

## Electrical power-conductor requirement
Conductor cross-sections are **not publicly established** by the Proteus data above and must not be guessed from OD.

For each candidate six-core sample measure:
- resistance of each power core in mOhm/m at known temperature;
- round-trip resistance at 40/100/150 m equivalent;
- insulation resistance between all cores and strength member/wet exterior as applicable;
- conductor DC current temperature rise;
- actual voltage at crawler under dynamic motor load.

A practical first target is to find a six-core construction whose two power conductors are at least roughly 0.75-1.0 mm2 copper class while the four signal/service conductors occupy the remaining cable volume. This is a search target only; measured resistance is the real acceptance variable.

## Tether-bus voltage is no longer hard-frozen at 48 V
Rev.GS explicitly removes the assumption that a 48 V bus must serve every future cable length.

Reason: on a very light ~6.5-7 mm cable, 150 m round-trip copper resistance may make 48 V inefficient or incapable of delivering the required constant power during traction peaks.

Architecture rule:
- 48 V remains acceptable for bench and short prototype testing where measured drop permits;
- 60 V nominal is a candidate for long-cable operation because the currently studied 18-75 V class crawler converter can potentially accept it with useful margin;
- any move above the qualified converter/connector/cable voltage rating requires a new protection and safety release, not an informal voltage increase.

The final tether source voltage is chosen from the **measured cable loop resistance + measured crawler power**, using the Rev.GS power-drop calculator.

## Constant-power feasibility examples — planning only
Using 0.0175 ohm*mm2/m copper resistivity for planning:

For two 1.0 mm2 power cores at 150 m:
- loop resistance ≈5.25 ohm;
- 48 V can deliver 70 W at the crawler with ~38.4 V remaining, but 100 W leaves only ~31.1 V and high line loss;
- 60 V delivers 100 W with ~49.4 V remaining and markedly better efficiency.

For two 0.75 mm2 power cores at 150 m:
- loop resistance ≈7.0 ohm;
- 48 V cannot sustain a 100 W constant-power load at all;
- 60 V can sustain 100 W but with significant line loss.

These are planning examples only. The actual cable resistance measurement overrides copper-area assumptions.

## Rear termination requirements
The Rev.EO/FP mechanical philosophy remains:
`outer jacket/bend support -> exposed tensile reinforcement -> dedicated structural wedge/clamp -> rear bulkhead/body`

Then, after the structural anchor:
- six copper conductors form a relaxed service loop;
- conductors terminate electrically without towing preload;
- electrical connector is not the mechanical recovery element;
- cable can be shortened and reterminated in the field without opening wheel-drive bays.

## First-sample acceptance tests
Before tail collet/connector machining is frozen:
1. measure OD at 10 locations along a sample;
2. measure mass per metre over >=5 m;
3. document six-core conductor construction and strand count;
4. measure one-way resistance of all six cores;
5. identify/verify tensile reinforcement material and termination behaviour;
6. 2 kN termination proof pull on a sacrificial sample;
7. minimum bend-radius/repeated-bend test on the reel-size candidate;
8. wet abrasion/slurry test;
9. jacket cut/strip/retermination trial;
10. 40 m full-power voltage-drop test;
11. 150 m equivalent loop-resistance emulator or actual-length test;
12. primary digital-link BER/packet-loss test while motors reverse and lighting PWM operates;
13. RS-485/service-channel test on cores 5/6 if retained;
14. pressure/water-ingress test of the completed crawler tail.

## Decision
Rev.CH is stale for physical tether construction.

The active PX-1 tether is now a **single reinforced lightweight six-core copper inspection cable**. Exact conductor gauges, signal pairing and bus voltage remain measurement-driven release items, but coax/fiber/separate ordinary twisted-pair substitutions are outside the active architecture.
