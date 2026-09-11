#include <assert.h>
#include <stdbool.h>
#include <stdint.h>

#include "../crawler/traction_bts7960.h"
#include "../common/px1_protocol.h"

static uint32_t g_now;
static uint16_t g_pwm_l, g_pwm_r;
static bool g_dir_l = true, g_dir_r = true;
static bool g_en_l, g_en_r;
static uint32_t g_left_disable_ms;
static uint32_t g_first_left_reverse_dir_ms;

void board_pwm_left(uint16_t duty) { g_pwm_l = duty; }
void board_pwm_right(uint16_t duty) { g_pwm_r = duty; }
void board_left_dir(bool forward)
{
    if (!forward && g_first_left_reverse_dir_ms == 0u) {
        g_first_left_reverse_dir_ms = g_now;
    }
    g_dir_l = forward;
}
void board_right_dir(bool forward) { g_dir_r = forward; }
void board_left_enable(bool en)
{
    if (!en) g_left_disable_ms = g_now;
    g_en_l = en;
}
void board_right_enable(bool en) { g_en_r = en; }

static void tick(uint16_t bus_mv, int16_t left_ma, int16_t right_ma, bool current_valid)
{
    g_now += 20u;
    traction_update(bus_mv, left_ma, right_ma, current_valid, g_now);
}

static void reset_hw(void)
{
    g_pwm_l = g_pwm_r = 0u;
    g_dir_l = g_dir_r = true;
    g_en_l = g_en_r = false;
    g_left_disable_ms = 0u;
    g_first_left_reverse_dir_ms = 0u;
}

static void test_reverse_coast_gate(void)
{
    g_now = 0u;
    reset_hw();
    traction_init(g_now);
    traction_configure_jam_limits(0u, 0u, 0u, 150u);

    traction_set_target(500, 0);
    for (unsigned i = 0; i < 20u; ++i) tick(24000u, 100, 0, true);
    assert(g_en_l);
    assert(g_dir_l);
    assert(g_pwm_l > 0u);

    traction_set_target(-500, 0);

    /* Wait until the bridge has ramped down and disabled. */
    for (unsigned i = 0; i < 30u && g_en_l; ++i) tick(24000u, 50, 0, true);
    assert(!g_en_l);
    assert(g_pwm_l == 0u);
    assert(g_first_left_reverse_dir_ms == 0u);

    uint32_t disabled_at = g_left_disable_ms;

    /* Before 150 ms coast, opposite direction is forbidden. */
    for (unsigned i = 0; i < 7u; ++i) tick(24000u, 50, 0, true); /* 140 ms */
    assert(g_first_left_reverse_dir_ms == 0u);
    assert(!g_en_l);

    /* State releases after dwell + low-current confirmation; drive follows later. */
    tick(24000u, 50, 0, true);
    tick(24000u, 50, 0, true);
    assert(g_first_left_reverse_dir_ms >= disabled_at + PX1_TRACTION_REVERSE_COAST_MS);
    assert(!g_dir_l);
    assert(g_en_l);
}

static void test_bus_fault_latch(void)
{
    g_now = 0u;
    reset_hw();
    traction_init(g_now);
    traction_set_target(500, 500);
    tick(24000u, 100, 100, true);
    assert(traction_fault_bits() == 0u);

    tick(PX1_TRACTION_BUS_TRIP_MV, 100, 100, true);
    assert((traction_fault_bits() & PX1_FAULT_BUS_OVERVOLT) != 0u);
    assert(!traction_outputs_enabled());
    assert(!g_en_l && !g_en_r);

    assert(!traction_clear_faults(true, 26000u, true, true, g_now));
    assert(traction_clear_faults(true, 24000u, true, true, g_now));
    assert(traction_fault_bits() == 0u);
    assert(!traction_outputs_enabled());
}

static void test_estop_reset_gate(void)
{
    g_now = 1000u;
    reset_hw();
    traction_init(g_now);
    traction_set_target(400, 400);
    tick(24000u, 100, 100, true);

    traction_estop(g_now);
    assert((traction_fault_bits() & PX1_FAULT_ESTOP) != 0u);
    assert(!g_en_l && !g_en_r);
    assert(!traction_clear_faults(true, 24000u, true, false, g_now));
    assert(traction_clear_faults(true, 24000u, true, true, g_now));
    assert(traction_fault_bits() == 0u);
}

static void test_jam_timer(void)
{
    g_now = 0u;
    reset_hw();
    traction_init(g_now);
    traction_configure_jam_limits(500u, 500u, 40u, 150u);
    traction_set_target(600, 0);

    /* First ticks build output; then sustained >500 mA starts the jam timer. */
    for (unsigned i = 0; i < 4u; ++i) tick(24000u, 100, 0, true);
    assert(traction_fault_bits() == 0u);

    tick(24000u, 700, 0, true);
    tick(24000u, 700, 0, true);
    assert((traction_fault_bits() & PX1_FAULT_LEFT_OVERCURRENT) == 0u);
    tick(24000u, 700, 0, true);
    assert((traction_fault_bits() & PX1_FAULT_LEFT_OVERCURRENT) != 0u);
    assert(!g_en_l && !g_en_r);
}

int main(void)
{
    test_reverse_coast_gate();
    test_bus_fault_latch();
    test_estop_reset_gate();
    test_jam_timer();
    return 0;
}
