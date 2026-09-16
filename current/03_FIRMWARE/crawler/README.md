# Crawler firmware

First firmware target is deliberately small and hardware-test oriented.

Required Rev.A functions:
- receive drive command;
- differential left/right motor command;
- forward/reverse;
- speed limiting/ramp where needed for drivetrain protection;
- communication watchdog: traction output OFF on timeout;
- read pressure sensor;
- report basic status/faults;
- accept lighting command when head electronics are integrated.

Do not add menu systems, logging frameworks or elaborate autonomy before A2 proves stable control through the 40 m tether.

Board-specific GPIO/timer mapping belongs in a separate hardware configuration file after the exact controller board used in the prototype is locked in the BOM.
