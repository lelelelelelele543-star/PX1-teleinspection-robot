# Console firmware

Minimum Rev.A operator behaviour:
- read 2-axis joystick;
- read crawler enable/stop controls;
- read speed and lighting controls;
- send periodic drive/control command;
- display link state, pressure and basic faults;
- force zero-drive command on local fault or disabled state.

Video is independent CVBS to the monitor and must not depend on firmware to remain visible.

Distance/time/address/advanced OSD are later additions unless they are already available without delaying the A4 demonstration.
