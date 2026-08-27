# PX-1 Rev.BY — modern digital video architecture

Status: architecture decision. This revision supersedes all CVBS/NTSC/PAL/coax video-path assumptions in earlier revisions.

## Decision
PX-1 moves to a fully digital camera path. No CVBS, NTSC, PAL or coaxial video conductor is used in the final architecture.

Preferred long-tether transport:
- camera sensor -> digital video encoder -> Ethernet packets;
- 10BASE-T1L Single-Pair Ethernet for the crawler-to-console long tether;
- one twisted pair for data, separate conductors for 24 V power;
- target H.265 stream 1080p25/30 at approximately 2-6 Mbit/s;
- ONVIF/RTSP-compatible stream preferred at console side.

## Why 10BASE-T1L
10BASE-T1L is IEEE 802.3cg long-reach single-pair Ethernet. It is appropriate for 100-150 m tether operation and gives substantial distance margin compared with ordinary 100BASE-TX. A suitable PHY/MAC-PHY family is Analog Devices ADIN1100/ADIN1110.

ADIN1110 class capability:
- 10 Mbit/s full Ethernet over one balanced pair;
- up to approximately 1700 m depending on implementation/cable/voltage mode;
- cable diagnostics;
- 1.0 Vpp / 2.4 Vpp modes;
- compact 6x6 mm IC class.

## Camera-side implementation
Because the project avoids custom PCBs wherever possible, the practical prototype path is:
1. compact digital IP-camera/encoder module with MIPI sensor and H.264/H.265 hardware encoder;
2. ready-made 10BASE-T1L media-converter/evaluation module where available;
3. later integrate a smaller industrial module only if packaging requires it.

The camera head shall not depend on analog video standards.

## Continuous ROLL interface
The continuous ROLL axis no longer needs a controlled-impedance 75-ohm coax channel.

Preferred rotating interface:
- Ethernet-capable digital slip ring / rotary transformer supporting at least 10 Mbit/s differential data;
- plus 2 power contacts for camera electronics;
- alternatively place the encoder and 10BASE-T1L PHY on the rotating cartridge and pass only the single balanced T1L pair plus power across the rotary interface.

The second option is preferred if a compact encoder/T1L module fits because it minimizes the number of high-speed rotating contacts.

## Tether allocation target
Final tether electrical minimum:
- conductor pair A/B: 10BASE-T1L differential data;
- +24 V;
- 0 V;
- RS-485 A/B only if retained for independent crawler safety/control bus;
- spare conductors for service/lighting/sensor redundancy.

No coax is required.

## Console side
Console converts 10BASE-T1L back to ordinary Ethernet and feeds:
- embedded Linux controller / mini PC;
- 7-inch display GUI;
- RTSP/ONVIF viewer;
- recording to SSD/SD;
- OSD generated digitally in software (distance, pressure, time, address, robot state).

## Key design benefit
Video, telemetry and future software features become packet-based. The system can support recording, snapshots, digital zoom, software overlays, remote diagnostics and future AI processing without redesigning the tether video conductor.

## Holds
1. select exact compact H.265 IP camera module that fits the Ø52 mm head architecture;
2. select ready-made 10BASE-T1L converter/module compatible with no-custom-PCB rule;
3. select Ethernet-capable rotary transfer for continuous ROLL;
4. verify end-to-end latency target;
5. verify 100-150 m tether BER/link margin on actual cable;
6. update LEMO pin allocation after digital transport is frozen.
