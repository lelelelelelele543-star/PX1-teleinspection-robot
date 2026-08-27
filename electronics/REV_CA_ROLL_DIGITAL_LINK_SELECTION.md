# PX-1 Rev.CA — digital link across continuous ROLL

Status: architecture decision.

## Finding
Off-the-shelf contactless 100BASE-TX rotary joints exist, but known industrial units are much too large/heavy for the PX-1 Ø52 mm camera head. Conventional Ethernet slip rings are available in compact families, but exact small-size models and long-term packet integrity must be qualified before release.

10BASE-T1L is attractive for the long crawler tether because it carries 10 Mbit/s Ethernet over one balanced pair and is intended for long-reach industrial links. It does NOT automatically mean an arbitrary two-ring collector will preserve the PHY channel through continuous rotation.

## Revised architecture
Do not force the long-line 10BASE-T1L physical layer through the camera ROLL joint.

Preferred topology:
rotating camera + encoder -> short local Ethernet/data interface -> qualified rotary data joint -> fixed head electronics -> 10BASE-T1L bridge -> crawler tether.

This separates two problems:
1. short rotating data transfer inside the head;
2. 100–150 m robust single-pair Ethernet along the crawler tether.

## Candidate paths
A. Compact Ethernet-rated contact slip ring, if a <=30 mm OD part with documented 100M performance and suitable power rings is sourced and bench-qualified.
B. Custom/contactless capacitive data coupler later, only if commercial slip-ring life becomes a limiting factor.
C. Mechanical ROLL limited to +/-180 deg as a fallback only; not the baseline because PX-1 requirement is continuous 360 deg.

## Qualification gate
Any candidate rotary joint must pass:
- continuous ping/packet-loss test while rotating;
- RTSP H.265 stream test at maximum configured bitrate;
- 24 h rotation endurance prototype test;
- electrical-noise test with TILT/ROLL motors switching;
- temperature test in sealed head;
- visual inspection and repeat test after endurance cycling.

## Current decision
Keep 10BASE-T1L for the long tether. Keep continuous ROLL. Do not freeze a rotary-joint part number until exact dimensions, Ethernet rating and power circuits are documented.
