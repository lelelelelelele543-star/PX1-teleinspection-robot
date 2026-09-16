# Crawler firmware

Rev.A firmware is deliberately small and hardware-test oriented.

## Implemented hardware-independent core
`px1_crawler_core.c/.h` now provides:
- left/right traction demand handling;
- demand clamp to ±1000;
- command sequence rejection for duplicate/out-of-order packets;
- 250 ms communication watchdog;
- immediate fail-safe traction stop on watchdog, E-stop or fault;
- normal-command acceleration/deceleration ramp;
- lighting demand storage;
- pressure / bus voltage / motor current / temperature telemetry packing;
- explicit fault/status flags;
- 16-bit sequence wrap handling.

The core contains no STM32 HAL calls and no motor-driver-specific code. This is intentional: the same safety logic survives whether A0 freezes a brushed H-bridge package or a Hall-BLDC package.

## Next board layer
The future `stm32f446/` hardware layer only has to provide:
- millisecond timebase;
- RS-485 receive/transmit;
- selected motor-driver adapter;
- pressure ADC/I2C acquisition;
- bus/current/temperature measurements where present;
- light PWM;
- hardware E-stop input.

Then its main loop is essentially:
1. parse protocol frame;
2. call `px1_crawler_accept_command()`;
3. update faults/measurements;
4. call `px1_crawler_tick()` at a fixed interval;
5. send returned left/right/light values to the hardware adapter;
6. build telemetry with `px1_crawler_make_telemetry()`.

Do not add menu systems, logging frameworks or autonomy before A2 proves stable control through the 40 m tether.

Board-specific GPIO/timer mapping remains separate until the exact controller/traction driver combination is locked.
