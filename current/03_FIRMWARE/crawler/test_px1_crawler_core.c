#include <assert.h>
#include <stdio.h>
#include "px1_crawler_core.h"

static px1_cmd_drive_t make_cmd(int left, int right, int enable)
{
    px1_cmd_drive_t c = {0};
    c.enable = enable ? true : false;
    c.left = left;
    c.right = right;
    c.light = 350;
    return c;
}

int main(void)
{
    px1_crawler_core_t s;
    px1_crawler_init(&s);

    px1_crawler_outputs_t o = px1_crawler_tick(&s, 0, 10);
    assert(!o.traction_enabled && o.left == 0 && o.right == 0);

    px1_cmd_drive_t c = make_cmd(1000, 500, 1);
    assert(px1_crawler_accept_command(&s, 10, &c, 100));
    assert(!px1_crawler_accept_command(&s, 10, &c, 101));
    o = px1_crawler_tick(&s, 110, 10);
    assert(o.traction_enabled && o.left == 40 && o.right == 40 && o.light == 350);
    o = px1_crawler_tick(&s, 210, 100);
    assert(o.left == 440 && o.right == 440);
    o = px1_crawler_tick(&s, 260, 50);
    assert(o.left == 640 && o.right == 500);

    /* Watchdog expiry is an immediate stop, not a ramp-down. */
    o = px1_crawler_tick(&s, 351, 10);
    assert(!o.traction_enabled && o.left == 0 && o.right == 0);

    c = make_cmd(-600, 600, 1);
    assert(px1_crawler_accept_command(&s, 11, &c, 400));
    assert(!px1_crawler_accept_command(&s, 9, &c, 401));
    o = px1_crawler_tick(&s, 410, 10);
    assert(o.left == -40 && o.right == 40);

    px1_crawler_set_faults(&s, PX1_FAULT_DRIVER_LEFT);
    o = px1_crawler_tick(&s, 420, 10);
    assert(!o.traction_enabled && o.left == 0 && o.right == 0);

    px1_crawler_set_faults(&s, 0);
    px1_crawler_set_estop(&s, true);
    o = px1_crawler_tick(&s, 430, 10);
    assert(!o.traction_enabled && o.left == 0 && o.right == 0);

    px1_crawler_set_estop(&s, false);
    c = make_cmd(1200, -1200, 1);
    assert(px1_crawler_accept_command(&s, 12, &c, 500));
    o = px1_crawler_tick(&s, 510, 10);
    assert(o.left == 40 && o.right == -40);

    px1_crawler_measurements_t m = {12345, 24100, 850, 900, 423};
    px1_crawler_set_measurements(&s, &m);
    px1_telemetry_t t;
    px1_crawler_make_telemetry(&s, 510, &t);
    assert((t.status_flags & PX1_CRAWLER_STATUS_LINK_OK) != 0);
    assert(t.pressure_pa_rel == 12345);
    assert(t.bus_mv == 24100);
    assert(t.left_ma == 850);
    assert(t.hottest_c10 == 423);

    /* 16-bit command sequence wrap is intentionally accepted. */
    px1_crawler_init(&s);
    c = make_cmd(1, 1, 1);
    assert(px1_crawler_accept_command(&s, 65535, &c, 1));
    assert(px1_crawler_accept_command(&s, 0, &c, 2));

    puts("PX1 crawler core tests: PASS");
    return 0;
}
