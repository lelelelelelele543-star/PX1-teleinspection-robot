#include <stdint.h>
#include <stdbool.h>

#include "traction_bts7960.h"
#include "../common/px1_protocol.h"

extern void board_pwm_left(uint16_t duty);
extern void board_pwm_right(uint16_t duty);
extern void board_left_dir(bool forward);
extern void board_right_dir(bool forward);
extern void board_left_enable(bool en);
extern void board_right_enable(bool en);

typedef enum {
    SIDE_DRIVE = 0,
    SIDE_RAMP_TO_ZERO,
    SIDE_COAST_FOR_REVERSE
} side_state_t;

typedef struct {
    int16_t requested;
    int16_t output;
    int8_t last_motion_sign;
    int8_t pending_sign;
    side_state_t state;
    uint32_t coast_since_ms;
    uint32_t jam_since_ms;
    bool jam_timer_active;
} traction_side_t;

static traction_side_t g_left;
static traction_side_t g_right;
static uint32_t g_last_update_ms;
static uint32_t g_fault_bits;
static uint16_t g_left_jam_ma;
static uint16_t g_right_jam_ma;
static uint16_t g_jam_delay_ms;
static uint16_t g_zero_current_ma = PX1_TRACTION_ZERO_CURRENT_MA;
static bool g_outputs_enabled;

static int8_t command_sign(int16_t v)
{
    if (v > PX1_TRACTION_DEADBAND) return 1;
    if (v < -PX1_TRACTION_DEADBAND) return -1;
    return 0;
}

static uint16_t abs_i16_u16(int16_t v)
{
    int32_t x = v;
    if (x < 0) x = -x;
    if (x > 65535) x = 65535;
    return (uint16_t)x;
}

static int16_t approach_with_step(int16_t current, int16_t target, uint16_t step)
{
    int32_t c = current;
    int32_t t = target;

    if (t > c + step) return (int16_t)(c + step);
    if (t < c - step) return (int16_t)(c - step);
    return target;
}

static uint16_t slew_step_from_dt(uint32_t dt_ms)
{
    /* Prevent a delayed scheduler call from producing one large command jump. */
    if (dt_ms == 0u) dt_ms = 1u;
    if (dt_ms > 50u) dt_ms = 50u;

    uint32_t step = (PX1_TRACTION_SLEW_PER_SECOND * dt_ms + 999u) / 1000u;
    if (step < 1u) step = 1u;
    if (step > PX1_TRACTION_CMD_MAX) step = PX1_TRACTION_CMD_MAX;
    return (uint16_t)step;
}

static void apply_left(int16_t cmd)
{
    if (command_sign(cmd) == 0) {
        board_pwm_left(0u);
        board_left_enable(false);
        return;
    }

    /* Opposite polarity is reached only after a disabled COAST state. */
    board_left_dir(cmd > 0);
    board_pwm_left(abs_i16_u16(cmd));
    board_left_enable(true);
}

static void apply_right(int16_t cmd)
{
    if (command_sign(cmd) == 0) {
        board_pwm_right(0u);
        board_right_enable(false);
        return;
    }

    board_right_dir(cmd > 0);
    board_pwm_right(abs_i16_u16(cmd));
    board_right_enable(true);
}

static void disable_outputs_now(void)
{
    board_pwm_left(0u);
    board_pwm_right(0u);
    board_left_enable(false);
    board_right_enable(false);
    g_outputs_enabled = false;
}

static void reset_side_state(traction_side_t *s, uint32_t now_ms)
{
    s->requested = 0;
    s->output = 0;
    s->last_motion_sign = 0;
    s->pending_sign = 0;
    s->state = SIDE_DRIVE;
    s->coast_since_ms = now_ms;
    s->jam_since_ms = now_ms;
    s->jam_timer_active = false;
}

static void force_side_coast(traction_side_t *s, uint32_t now_ms)
{
    s->requested = 0;
    s->output = 0;
    s->pending_sign = 0;
    s->state = SIDE_COAST_FOR_REVERSE;
    s->coast_since_ms = now_ms;
    s->jam_timer_active = false;
}

void traction_init(uint32_t now_ms)
{
    reset_side_state(&g_left, now_ms);
    reset_side_state(&g_right, now_ms);
    g_last_update_ms = now_ms;
    g_fault_bits = 0u;
    g_left_jam_ma = 0u;
    g_right_jam_ma = 0u;
    g_jam_delay_ms = 0u;
    g_zero_current_ma = PX1_TRACTION_ZERO_CURRENT_MA;
    disable_outputs_now();
}

void traction_set_target(int16_t left, int16_t right)
{
    g_left.requested = px1_clamp1000(left);
    g_right.requested = px1_clamp1000(right);
}

void traction_configure_jam_limits(uint16_t left_jam_ma,
                                   uint16_t right_jam_ma,
                                   uint16_t jam_delay_ms,
                                   uint16_t zero_current_ma)
{
    g_left_jam_ma = left_jam_ma;
    g_right_jam_ma = right_jam_ma;
    g_jam_delay_ms = jam_delay_ms;
    g_zero_current_ma = zero_current_ma ? zero_current_ma : PX1_TRACTION_ZERO_CURRENT_MA;
}

static bool update_jam_detector(traction_side_t *s,
                                bool drive_active,
                                uint16_t abs_current_ma,
                                uint16_t limit_ma,
                                uint32_t now_ms)
{
    if (!drive_active || limit_ma == 0u || g_jam_delay_ms == 0u) {
        s->jam_timer_active = false;
        return false;
    }

    if (abs_current_ma < limit_ma) {
        s->jam_timer_active = false;
        return false;
    }

    if (!s->jam_timer_active) {
        s->jam_timer_active = true;
        s->jam_since_ms = now_ms;
        return false;
    }

    return (uint32_t)(now_ms - s->jam_since_ms) >= g_jam_delay_ms;
}

static int16_t side_update(traction_side_t *s,
                           int16_t requested,
                           int16_t measured_ma,
                           uint16_t slew_step,
                           uint32_t now_ms)
{
    int8_t req_sign = command_sign(requested);
    uint16_t abs_current = abs_i16_u16(measured_ma);

    switch (s->state) {
    case SIDE_DRIVE:
        if (req_sign == 0) {
            s->output = approach_with_step(s->output, 0, slew_step);
            if (command_sign(s->output) == 0) {
                s->output = 0;
            }
            return s->output;
        }

        if (s->last_motion_sign == 0) {
            s->last_motion_sign = req_sign;
        }

        if (req_sign != s->last_motion_sign) {
            s->pending_sign = req_sign;
            s->state = SIDE_RAMP_TO_ZERO;
            s->output = approach_with_step(s->output, 0, slew_step);
            if (command_sign(s->output) == 0) {
                s->output = 0;
                s->state = SIDE_COAST_FOR_REVERSE;
                s->coast_since_ms = now_ms;
            }
            return s->output;
        }

        s->output = approach_with_step(s->output, requested, slew_step);
        return s->output;

    case SIDE_RAMP_TO_ZERO:
        /* If operator returns to the old direction before zero, resume normally. */
        if (req_sign == s->last_motion_sign) {
            s->pending_sign = 0;
            s->state = SIDE_DRIVE;
            s->output = approach_with_step(s->output, requested, slew_step);
            return s->output;
        }

        s->pending_sign = req_sign;
        s->output = approach_with_step(s->output, 0, slew_step);
        if (command_sign(s->output) == 0) {
            s->output = 0;
            s->state = SIDE_COAST_FOR_REVERSE;
            s->coast_since_ms = now_ms;
        }
        return s->output;

    case SIDE_COAST_FOR_REVERSE:
    default:
        s->output = 0;

        if (req_sign == 0) {
            s->pending_sign = 0;
            return 0;
        }

        /* Same-direction restart is not a polarity reversal. */
        if (req_sign == s->last_motion_sign) {
            s->pending_sign = 0;
            s->state = SIDE_DRIVE;
            return 0;
        }

        s->pending_sign = req_sign;

        if ((uint32_t)(now_ms - s->coast_since_ms) < PX1_TRACTION_REVERSE_COAST_MS) {
            return 0;
        }

        if (abs_current > g_zero_current_ma) {
            return 0;
        }

        /* Only now is the opposite direction allowed on a later apply. */
        s->last_motion_sign = req_sign;
        s->pending_sign = 0;
        s->state = SIDE_DRIVE;
        return 0;
    }
}

void traction_update(uint16_t bus_mv,
                     int16_t left_ma,
                     int16_t right_ma,
                     bool current_valid,
                     uint32_t now_ms)
{
    uint32_t dt_ms = (uint32_t)(now_ms - g_last_update_ms);
    g_last_update_ms = now_ms;
    uint16_t slew_step = slew_step_from_dt(dt_ms);

    if (bus_mv >= PX1_TRACTION_BUS_TRIP_MV) {
        g_fault_bits |= PX1_FAULT_BUS_OVERVOLT;
    }

    if (!current_valid) {
        g_fault_bits |= PX1_FAULT_CURRENT_SENSOR;
    }

    if (current_valid) {
        if (update_jam_detector(&g_left,
                                command_sign(g_left.output) != 0,
                                abs_i16_u16(left_ma),
                                g_left_jam_ma,
                                now_ms)) {
            g_fault_bits |= PX1_FAULT_LEFT_OVERCURRENT;
        }
        if (update_jam_detector(&g_right,
                                command_sign(g_right.output) != 0,
                                abs_i16_u16(right_ma),
                                g_right_jam_ma,
                                now_ms)) {
            g_fault_bits |= PX1_FAULT_RIGHT_OVERCURRENT;
        }
    }

    if (g_fault_bits != 0u) {
        g_left.output = 0;
        g_right.output = 0;
        disable_outputs_now();
        return;
    }

    /* WB08 warning threshold: stop generating torque before BTS7960 OV lockout. */
    int16_t left_request = g_left.requested;
    int16_t right_request = g_right.requested;
    if (bus_mv > PX1_TRACTION_BUS_WARN_MV) {
        left_request = 0;
        right_request = 0;
    }

    int16_t left_out = side_update(&g_left, left_request, left_ma, slew_step, now_ms);
    int16_t right_out = side_update(&g_right, right_request, right_ma, slew_step, now_ms);

    apply_left(left_out);
    apply_right(right_out);
    g_outputs_enabled = (command_sign(left_out) != 0) || (command_sign(right_out) != 0);
}

void traction_stop(void)
{
    g_left.requested = 0;
    g_right.requested = 0;
}

void traction_estop(uint32_t now_ms)
{
    g_fault_bits |= PX1_FAULT_ESTOP;
    force_side_coast(&g_left, now_ms);
    force_side_coast(&g_right, now_ms);
    disable_outputs_now();
}

void traction_hard_disable(uint32_t now_ms)
{
    force_side_coast(&g_left, now_ms);
    force_side_coast(&g_right, now_ms);
    disable_outputs_now();
}

bool traction_clear_faults(bool deliberate_reset,
                           uint16_t bus_mv,
                           bool current_valid,
                           bool estop_released,
                           uint32_t now_ms)
{
    if (!deliberate_reset) return false;
    if (bus_mv >= PX1_TRACTION_BUS_REENABLE_MV) return false;
    if (!current_valid) return false;
    if (!estop_released) return false;

    g_fault_bits = 0u;
    force_side_coast(&g_left, now_ms);
    force_side_coast(&g_right, now_ms);
    return true;
}

uint32_t traction_fault_bits(void)
{
    return g_fault_bits;
}

bool traction_outputs_enabled(void)
{
    return g_outputs_enabled;
}
