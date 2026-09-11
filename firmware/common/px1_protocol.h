#pragma once

#include <stdint.h>
#include <stdbool.h>

#define PX1_SOF1 0xAAu
#define PX1_SOF2 0x55u
#define PX1_PROTO_VER 2u
#define PX1_MAX_PAYLOAD 64u
#define PX1_FRAME_HEADER_BYTES 6u
#define PX1_FRAME_OVERHEAD_BYTES 10u /* SOF(2) + header(6) + CRC16(2) */
#define PX1_MAX_FRAME_BYTES (PX1_MAX_PAYLOAD + PX1_FRAME_OVERHEAD_BYTES)
#define PX1_CONTROL_TIMEOUT_MS 300u

/* Node addresses */
#define PX1_ADDR_CCU     0x01u
#define PX1_ADDR_CRAWLER 0x10u
#define PX1_ADDR_REEL    0x20u
#define PX1_ADDR_CAMERA  0x30u
#define PX1_ADDR_BCAST   0xFFu

/* Message types */
enum {
    PX1_CMD_CONTROL      = 0x01,
    PX1_CMD_HOME         = 0x02,
    PX1_CMD_ZERO_DISTANCE= 0x03,
    PX1_CMD_ARM          = 0x04,
    PX1_CMD_DISARM       = 0x05,
    PX1_CMD_CLEAR_FAULTS = 0x06,
    PX1_TELEMETRY        = 0x10,
    PX1_FAULT_EVENT      = 0x11,
    PX1_ACK              = 0x12,
    PX1_PING             = 0x13,
    PX1_PONG             = 0x14
};

/* Crawler operating states */
typedef enum {
    PX1_STATE_SAFE_OFF      = 0,
    PX1_STATE_BOOT          = 1,
    PX1_STATE_DISARMED      = 2,
    PX1_STATE_ARMED_IDLE    = 3,
    PX1_STATE_ACTIVE        = 4,
    PX1_STATE_FAULT_LATCHED = 5,
    PX1_STATE_SERVICE       = 6
} px1_state_t;

/* Simultaneous fault bits */
#define PX1_FAULT_COMM_TIMEOUT        (1UL << 0)
#define PX1_FAULT_BUS_OVERVOLT        (1UL << 1)
#define PX1_FAULT_LEFT_OVERCURRENT    (1UL << 2)
#define PX1_FAULT_RIGHT_OVERCURRENT   (1UL << 3)
#define PX1_FAULT_P0_PRESSURE         (1UL << 4)
#define PX1_FAULT_P1_PRESSURE         (1UL << 5)
#define PX1_FAULT_P2_PRESSURE         (1UL << 6)
#define PX1_FAULT_PRESS_SENSOR        (1UL << 7)
#define PX1_FAULT_P0_LEAK             (1UL << 8)
#define PX1_FAULT_POWER_OVERTEMP      (1UL << 9)
#define PX1_FAULT_CAMERA_COMM         (1UL << 10)
#define PX1_FAULT_CAMERA_TILT         (1UL << 11)
#define PX1_FAULT_CAMERA_ROLL         (1UL << 12)
#define PX1_FAULT_ESTOP               (1UL << 13)
#define PX1_FAULT_CURRENT_SENSOR      (1UL << 14)
#define PX1_FAULT_BUS_UNDERVOLT       (1UL << 15)

/* Frame bytes after SOF1/SOF2 and before payload. CRC covers this header + payload. */
typedef struct __attribute__((packed)) {
    uint8_t ver;
    uint8_t dst;
    uint8_t src;
    uint8_t type;
    uint8_t seq;
    uint8_t len;
} px1_frame_header_t;

/* Operator controls. Manual camera lift is intentionally absent. */
typedef struct __attribute__((packed)) {
    int16_t drive;          /* -1000..+1000 */
    int16_t steer;          /* -1000..+1000 */
    int16_t tilt;           /* -1000..+1000 */
    int16_t roll;           /* -1000..+1000 */
    uint16_t light;         /* 0..1000 */
    uint16_t flags;
} px1_control_t;

/*
 * Rev.B crawler telemetry v2, 36 bytes.
 * Pressure is ABSOLUTE at 0.1 hPa/count. Gauge pressure is calculated in
 * the CCU by subtracting its own local ambient LPS28 reading.
 * Reel distance is intentionally not present: the reel/CCU owns that value.
 */
typedef struct __attribute__((packed)) {
    uint8_t state;
    uint8_t reserved0;
    uint32_t fault_bits;

    uint16_t p0_abs_hpa_x10;
    uint16_t p1_abs_hpa_x10;
    uint16_t p2_abs_hpa_x10;

    int16_t p0_temp_c_x10;
    int16_t p1_temp_c_x10;
    int16_t p2_temp_c_x10;

    uint16_t bus_mV;
    int16_t left_mA;
    int16_t right_mA;
    int16_t power_temp_c_x10;
    uint16_t leak_adc;

    int16_t tilt_deg_x10;
    int16_t roll_deg_x10;
    uint16_t light_permille;
    uint16_t flags;
} px1_telemetry_t;

/* Immediate critical-fault snapshot; periodic telemetry remains authoritative. */
typedef struct __attribute__((packed)) {
    uint32_t fault_bits;
    uint16_t bus_mV;
    int16_t left_mA;
    int16_t right_mA;
    uint16_t p0_abs_hpa_x10;
    uint16_t p1_abs_hpa_x10;
    uint16_t p2_abs_hpa_x10;
    uint32_t uptime_ms;
} px1_fault_event_t;

typedef struct __attribute__((packed)) {
    uint8_t acked_type;
    uint8_t acked_seq;
    uint8_t status;
} px1_ack_t;

uint16_t px1_crc16(const uint8_t *data, uint16_t len);
int16_t px1_clamp1000(int32_t v);
void px1_mix(int16_t drive, int16_t steer, int16_t *left, int16_t *right);
bool px1_header_valid(const px1_frame_header_t *h);
uint16_t px1_frame_wire_size(uint8_t payload_len);

#if defined(__STDC_VERSION__) && (__STDC_VERSION__ >= 201112L)
_Static_assert(sizeof(px1_frame_header_t) == 6u, "PX1 frame header size changed");
_Static_assert(sizeof(px1_control_t) == 12u, "PX1 control payload size changed");
_Static_assert(sizeof(px1_telemetry_t) == 36u, "PX1 telemetry payload size changed");
#endif
