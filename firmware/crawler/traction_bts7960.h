#pragma once

#include <stdint.h>
#include <stdbool.h>

/* Rev.B traction safety defaults. Exact current limits remain bench-calibrated. */
#define PX1_TRACTION_CMD_MAX            1000
#define PX1_TRACTION_DEADBAND           25
#define PX1_TRACTION_BUS_WARN_MV        26500u
#define PX1_TRACTION_BUS_TRIP_MV        27000u
#define PX1_TRACTION_BUS_REENABLE_MV    25500u
#define PX1_TRACTION_REVERSE_COAST_MS   150u
#define PX1_TRACTION_ZERO_CURRENT_MA    150u
#define PX1_TRACTION_SLEW_PER_SECOND    1750u

/* Initialize software state. Hardware outputs are forced disabled. */
void traction_init(uint32_t now_ms);

/*
 * Store desired LEFT/RIGHT commands (-1000..+1000).
 * This function does not bypass the safety state machine.
 */
void traction_set_target(int16_t left, int16_t right);

/*
 * Configure measured-current jam protection after bench calibration.
 * A jam limit of 0 disables that side's jam detector; this is intended only
 * for early bench calibration, not released field operation.
 */
void traction_configure_jam_limits(uint16_t left_jam_ma,
                                   uint16_t right_jam_ma,
                                   uint16_t jam_delay_ms,
                                   uint16_t zero_current_ma);

/*
 * Run from a periodic task (recommended 10..20 ms).
 * current_valid must represent calibrated/credible LEFT and RIGHT sensors.
 */
void traction_update(uint16_t bus_mv,
                     int16_t left_ma,
                     int16_t right_ma,
                     bool current_valid,
                     uint32_t now_ms);

/* Normal commanded stop: target zero, ramp then coast through update(). */
void traction_stop(void);

/* Immediate hardware-style disable and latched E-STOP software state. */
void traction_estop(uint32_t now_ms);

/* Immediate disable without adding a new fault bit (watchdog/supervisor use). */
void traction_hard_disable(uint32_t now_ms);

/*
 * Clear traction-local latched faults only after deliberate operator action
 * and after the measured conditions are healthy. This never arms traction.
 * estop_released must represent the real hardware E-STOP chain state.
 */
bool traction_clear_faults(bool deliberate_reset,
                           uint16_t bus_mv,
                           bool current_valid,
                           bool estop_released,
                           uint32_t now_ms);

uint32_t traction_fault_bits(void);
bool traction_outputs_enabled(void);
