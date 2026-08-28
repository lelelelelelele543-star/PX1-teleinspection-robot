# PX-1 Rev.GS — corrected two-motor power / tether-voltage budget

Status: ACTIVE POWER ARCHITECTURE STUDY; exact current limits and tether voltage remain measurement-driven.

This document supersedes the stale **four traction motor** assumptions in Rev.CJ and the old JGB37 references in Rev.DJ/CM where they conflict with the current Rev.GB/GL two-motor architecture.

## Active traction architecture
PX-1 has:
- two traction motors total, LEFT and RIGHT;
- one motor drives all three wheels of its side through the supported Z16/Z40 -> X200 -> five-Z50 train;
- two independent H-bridge channels;
- 24 V traction rail inside the crawler;
- current limiting must protect the compact bevel stage before motor stall torque is reached.

Current exact commercial reference candidate: ISL PGM-32P-24-100-60-02 / MOT-IG32PGM 100 class, Ø32 x 92 mm, 24 V, roughly 49-54 rpm rated depending source revision.

## Traction electrical envelope
Published motor data conflict, so Rev.GS does not pretend to know the final rated current.

Use for converter/cable study until bench measurement:
- normal traction electrical budget: **60 W total** for both motors;
- short controlled traction envelope: **100 W total** for both motors;
- uncontrolled two-motor stall is explicitly outside normal operation and must be interrupted by current/jam protection.

The older/current motor references indicate individual stall currents in roughly the 4.7-5.5 A class. Two unrestricted stalls could therefore demand >225 W at 24 V and would also exceed the provisional bevel torque ceiling. The design response is current limiting and fast jam shutdown, not making the tether continuously carry uncontrolled stall power.

## Auxiliary loads
Retain conservative prototype reservations:
- TILT motor: up to ~13 W short/stall-class electrical envelope;
- ROLL/PAN motor: up to ~13 W short/stall-class envelope;
- digital camera/encoder: 4 W reserve;
- lighting: 12 W reserve;
- controller + long-line PHY + sensors: 6 W reserve;
- local conversion/control margin: 5-10 W class.

Both camera-axis motors are not expected to sit at stall continuously.

## System budget used for tether study
Representative **normal** crawler input target after local-conversion losses: about **90-100 W**.

Representative **short controlled peak** target: about **120-145 W**.

These are sizing cases, not measured consumption.

The exact first prototype must log real 24 V motor branch power and tether input power simultaneously.

## Main traction converter
The previously studied Cincon CHB200W-48S24 class remains physically/electrically useful:
- input 18-75 VDC;
- output 24 V / 8.3 A;
- ~199-200 W class;
- ~88% full-load efficiency class;
- half-brick roughly 61 x 58 x 13 mm.

It is intentionally larger than the expected two-motor continuous demand because it provides transient/thermal margin and already fits the current Rev.GP packaging envelope.

The converter is **not yet procurement-frozen**. Reverse motor energy, input filter, thermal interface and actual availability still require qualification.

## Tether source voltage decision
Do not hard-code one source voltage before measuring cable loop resistance.

### 48 V mode
Good for:
- bench work;
- short 40 m prototype runs;
- longer runs only if measured power-core resistance is low enough.

At 150 m, 48 V can become marginal on a lightweight six-core cable because constant-power load causes current to rise as crawler voltage falls.

### 60 V nominal study mode
60 V is now the preferred **long-cable study point** because:
- it materially reduces current/drop versus 48 V;
- it remains inside the 18-75 V input range of the CHB200W-48S24 class;
- it avoids redesigning immediately for a much higher-voltage converter.

This is not a safety/procurement release. Console supply, cable insulation, connector creepage/voltage rating, transient clamp and wet-environment safety must all be designed for the final voltage.

## 150 m planning examples
Using the planning copper value 0.0175 ohm*mm2/m and two equal power conductors:

### 1.0 mm2 each
150 m round-trip R ~5.25 ohm.

At 48 V:
- 70 W crawler input -> ~38.4 V at crawler;
- 100 W -> ~31.1 V and very high line loss;
- ~145 W is physically impossible as a constant-power load at this loop resistance/source voltage.

At 60 V:
- 90 W -> ~50.7 V at crawler;
- 100 W -> ~49.4 V;
- 120 W -> ~46.4 V;
- 145 W -> ~41.8 V, but line loss becomes substantial.

### 0.75 mm2 each
150 m loop R ~7.0 ohm.

At 48 V:
- 70 W already falls to ~33.3 V;
- 100 W is beyond the constant-power transfer limit.

At 60 V:
- 90 W -> ~46.4 V;
- 100 W -> ~44.1 V;
- 120 W -> ~37.8 V;
- ~145 W is beyond the transfer limit.

Therefore the long-cable architecture must be driven by **measured power-core resistance and measured real load**, not merely conductor nominal area.

## Current-limit policy consequence
The compact bevel stage and tether both benefit from the same protection strategy.

Current control should implement at least:
- low-rate continuous current limit based on measured motor thermal capability;
- hard/fast jam threshold;
- acceleration ramp;
- reversal ramp;
- per-side current sensing;
- watchdog/communications-loss traction disable.

The provisional mechanical ceiling remains equivalent to about 1.0 N.m motor output until the actual bevel rating and motor torque-current map are measured.

A catalog-linear estimate suggests this may occur roughly in the 0.6-0.8 A/motor region for the two conflicting published ISL motor data sets, but **that is not a firmware limit**. Bench calibration is mandatory.

## Required first-article measurements
1. exact motor no-load current/rpm at 24 V;
2. motor current at several measured output torques;
3. current corresponding to 1.0 N.m gearbox output;
4. 30 min representative thermal current;
5. LEFT/RIGHT full-side drive current after gears/seals are installed;
6. auxiliary camera/light/control power;
7. total crawler input power at rest, cruise, turn, acceleration and jam-limited event;
8. actual six-core cable loop resistance at known temperature;
9. crawler-end tether voltage at 40 m;
10. 100/150 m equivalent test through real cable or resistance emulator;
11. CHB200W input current/case temperature and 24 V bus ripple;
12. 24 V bus overshoot under deceleration/reversal.

## Decision
- active traction motor count = **2**, not 4;
- 24 V internal traction rail retained;
- 200 W half-brick class retained as a robust prototype converter envelope;
- 48 V tether is no longer treated as an immutable 150 m requirement;
- 60 V nominal is the leading long-cable study point pending real six-core cable resistance and safety qualification;
- no higher tether voltage is introduced without a deliberate converter/protection/connector/safety redesign.
