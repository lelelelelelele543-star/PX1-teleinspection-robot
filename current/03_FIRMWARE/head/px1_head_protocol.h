#ifndef PX1_HEAD_PROTOCOL_H
#define PX1_HEAD_PROTOCOL_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include "px1_protocol.h"

#define PX1_CMD_HEAD_TYPE 0x02u
#define PX1_HEAD_TELEMETRY_TYPE 0x82u
#define PX1_CMD_HEAD_PAYLOAD_LEN 8u
#define PX1_HEAD_TELEMETRY_PAYLOAD_LEN 14u

typedef struct {
    bool enable;
    uint8_t flags;
    int16_t pan;
    int16_t rotate;
    uint16_t light;
} px1_cmd_head_t;

typedef struct {
    uint16_t status_flags;
    uint16_t fault_flags;
    int16_t pan_cdeg;
    int16_t rotate_cdeg;
    uint16_t pan_ma;
    uint16_t rotate_ma;
    int16_t hottest_c10;
} px1_head_telemetry_t;

px1_result_t px1_encode_cmd_head(uint16_t sequence,
                                 const px1_cmd_head_t *cmd,
                                 uint8_t *out,
                                 size_t out_capacity,
                                 size_t *out_len);
px1_result_t px1_parse_cmd_head(const px1_frame_t *frame,
                                px1_cmd_head_t *cmd);
px1_result_t px1_encode_head_telemetry(uint16_t sequence,
                                       const px1_head_telemetry_t *tm,
                                       uint8_t *out,
                                       size_t out_capacity,
                                       size_t *out_len);
px1_result_t px1_parse_head_telemetry(const px1_frame_t *frame,
                                      px1_head_telemetry_t *tm);

#endif
