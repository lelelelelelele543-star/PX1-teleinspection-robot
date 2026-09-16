#include "px1_crawler_core.h"
#include <string.h>

static bool sequence_is_newer(uint16_t a, uint16_t b)
{
    return (int16_t)(a - b) > 0;
}

static int16_t ramp_i16(int16_t current, int16_t target, uint32_t elapsed_ms)
{
    uint32_t step32 = elapsed_ms * PX1_CRAWLER_RAMP_PER_MS;
    if (step32 > 2000u) step32 = 2000u;
    int32_t step = (int32_t)step32;
    int32_t c = current;
    int32_t t = target;

    if (c < t) {
        c += step;
        if (c > t) c = t;
    } else if (c > t) {
        c -= step;
        if (c < t) c = t;
    }
    return (int16_t)c;
}

void px1_crawler_init(px1_crawler_core_t *s)
{
    if (!s) return;
    memset(s, 0, sizeof(*s));
}

bool px1_crawler_accept_command(px1_crawler_core_t *s,
                                uint16_t sequence,
                                const px1_cmd_drive_t *cmd,
                                uint32_t now_ms)
{
    if (!s || !cmd) return false;
    if (s->have_command && !sequence_is_newer(sequence, s->last_sequence)) return false;

    s->command = *cmd;
    s->command.left = px1_clamp_demand(s->command.left);
    s->command.right = px1_clamp_demand(s->command.right);
    s->command.light = px1_clamp_light(s->command.light);
    s->last_sequence = sequence;
    s->last_command_ms = now_ms;
    s->have_command = true;
    return true;
}

void px1_crawler_set_faults(px1_crawler_core_t *s, uint16_t faults)
{
    if (!s) return;
    s->faults = faults;
}

void px1_crawler_set_estop(px1_crawler_core_t *s, bool active)
{
    if (!s) return;
    s->estop_active = active;
    if (active) {
        s->applied_left = 0;
        s->applied_right = 0;
    }
}

void px1_crawler_set_measurements(px1_crawler_core_t *s,
                                  const px1_crawler_measurements_t *m)
{
    if (!s || !m) return;
    s->measurements = *m;
}

px1_crawler_outputs_t px1_crawler_tick(px1_crawler_core_t *s,
                                       uint32_t now_ms,
                                       uint32_t elapsed_ms)
{
    px1_crawler_outputs_t o = {0};
    if (!s) return o;

    bool fresh = s->have_command &&
                 ((uint32_t)(now_ms - s->last_command_ms) <= PX1_CRAWLER_WATCHDOG_MS);
    bool safe = fresh && s->command.enable && !s->estop_active && (s->faults == 0u);
    int16_t target_l = safe ? s->command.left : 0;
    int16_t target_r = safe ? s->command.right : 0;

    if (!safe && (!fresh || s->estop_active || s->faults)) {
        /* Fail-safe conditions stop immediately; normal operator changes are ramped. */
        s->applied_left = 0;
        s->applied_right = 0;
    } else {
        s->applied_left = ramp_i16(s->applied_left, target_l, elapsed_ms);
        s->applied_right = ramp_i16(s->applied_right, target_r, elapsed_ms);
    }

    s->applied_light = s->have_command ? s->command.light : 0u;
    o.left = s->applied_left;
    o.right = s->applied_right;
    o.light = s->applied_light;
    o.traction_enabled = safe;
    return o;
}

void px1_crawler_make_telemetry(const px1_crawler_core_t *s,
                                uint32_t now_ms,
                                px1_telemetry_t *tm)
{
    if (!s || !tm) return;
    memset(tm, 0, sizeof(*tm));

    bool fresh = s->have_command &&
                 ((uint32_t)(now_ms - s->last_command_ms) <= PX1_CRAWLER_WATCHDOG_MS);

    if (fresh) tm->status_flags |= PX1_CRAWLER_STATUS_LINK_OK;
    if (fresh && s->command.enable && !s->estop_active && s->faults == 0u)
        tm->status_flags |= PX1_CRAWLER_STATUS_DRIVE_ENABLE;
    if (!fresh) tm->status_flags |= PX1_CRAWLER_STATUS_WATCHDOG_STOP;
    if (s->faults) tm->status_flags |= PX1_CRAWLER_STATUS_FAULT_STOP;
    if (s->estop_active) tm->status_flags |= PX1_CRAWLER_STATUS_ESTOP;

    tm->fault_flags = s->faults |
                      (s->estop_active ? PX1_FAULT_EXTERNAL_ESTOP : 0u);
    tm->pressure_pa_rel = s->measurements.pressure_pa_rel;
    tm->bus_mv = s->measurements.bus_mv;
    tm->left_ma = s->measurements.left_ma;
    tm->right_ma = s->measurements.right_ma;
    tm->hottest_c10 = s->measurements.hottest_c10;
}
