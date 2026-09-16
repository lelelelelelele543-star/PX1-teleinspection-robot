#ifndef PX1_CRAWLER_CORE_H
#define PX1_CRAWLER_CORE_H

#include <stdbool.h>
#include <stdint.h>
#include "px1_protocol.h"

#define PX1_CRAWLER_WATCHDOG_MS 250u
#define PX1_CRAWLER_RAMP_PER_MS 4u

#define PX1_CRAWLER_STATUS_LINK_OK       0x0001u
#define PX1_CRAWLER_STATUS_DRIVE_ENABLE  0x0002u
#define PX1_CRAWLER_STATUS_WATCHDOG_STOP 0x0004u
#define PX1_CRAWLER_STATUS_FAULT_STOP    0x0008u
#define PX1_CRAWLER_STATUS_ESTOP         0x0010u

#define PX1_FAULT_EXTERNAL_ESTOP 0x0001u
#define PX1_FAULT_DRIVER_LEFT    0x0002u
#define PX1_FAULT_DRIVER_RIGHT   0x0004u
#define PX1_FAULT_OVERTEMP       0x0008u
#define PX1_FAULT_UNDERVOLT      0x0010u
#define PX1_FAULT_OVERVOLT       0x0020u
#define PX1_FAULT_PRESSURE       0x0040u

typedef struct {
    int16_t left;
    int16_t right;
    uint16_t light;
    bool traction_enabled;
} px1_crawler_outputs_t;

typedef struct {
    int32_t pressure_pa_rel;
    uint16_t bus_mv;
    uint16_t left_ma;
    uint16_t right_ma;
    int16_t hottest_c10;
} px1_crawler_measurements_t;

typedef struct {
    bool have_command;
    uint16_t last_sequence;
    uint32_t last_command_ms;
    px1_cmd_drive_t command;
    int16_t applied_left;
    int16_t applied_right;
    uint16_t applied_light;
    uint16_t faults;
    bool estop_active;
    px1_crawler_measurements_t measurements;
} px1_crawler_core_t;

void px1_crawler_init(px1_crawler_core_t *s);
bool px1_crawler_accept_command(px1_crawler_core_t *s,
                                uint16_t sequence,
                                const px1_cmd_drive_t *cmd,
                                uint32_t now_ms);
void px1_crawler_set_faults(px1_crawler_core_t *s, uint16_t faults);
void px1_crawler_set_estop(px1_crawler_core_t *s, bool active);
void px1_crawler_set_measurements(px1_crawler_core_t *s,
                                  const px1_crawler_measurements_t *m);
px1_crawler_outputs_t px1_crawler_tick(px1_crawler_core_t *s,
                                       uint32_t now_ms,
                                       uint32_t elapsed_ms);
void px1_crawler_make_telemetry(const px1_crawler_core_t *s,
                                uint32_t now_ms,
                                px1_telemetry_t *tm);

#endif
