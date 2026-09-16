#ifndef PX1_PROTOCOL_H
#define PX1_PROTOCOL_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define PX1_SOF0 0xA5u
#define PX1_SOF1 0x5Au
#define PX1_PROTOCOL_VERSION 0x01u
#define PX1_MAX_PAYLOAD 32u
#define PX1_MAX_FRAME (2u + 1u + 1u + 2u + 1u + PX1_MAX_PAYLOAD + 2u)
#define PX1_CMD_DRIVE_TYPE 0x01u
#define PX1_TELEMETRY_TYPE 0x81u
#define PX1_CMD_DRIVE_PAYLOAD_LEN 8u
#define PX1_TELEMETRY_PAYLOAD_LEN 16u

#define PX1_DEMAND_MIN (-1000)
#define PX1_DEMAND_MAX (1000)
#define PX1_LIGHT_MAX 1000u

typedef enum {
    PX1_OK = 0,
    PX1_ERR_ARG = -1,
    PX1_ERR_SHORT = -2,
    PX1_ERR_SOF = -3,
    PX1_ERR_VERSION = -4,
    PX1_ERR_LENGTH = -5,
    PX1_ERR_CRC = -6,
    PX1_ERR_TYPE = -7
} px1_result_t;

typedef struct {
    uint8_t type;
    uint16_t sequence;
    uint8_t payload_len;
    uint8_t payload[PX1_MAX_PAYLOAD];
} px1_frame_t;

typedef struct {
    bool enable;
    uint8_t flags;
    int16_t left;
    int16_t right;
    uint16_t light;
} px1_cmd_drive_t;

typedef struct {
    uint16_t status_flags;
    uint16_t fault_flags;
    int32_t pressure_pa_rel;
    uint16_t bus_mv;
    uint16_t left_ma;
    uint16_t right_ma;
    int16_t hottest_c10;
} px1_telemetry_t;

uint16_t px1_crc16_ccitt_false(const uint8_t *data, size_t len);

px1_result_t px1_encode_frame(uint8_t type,
                              uint16_t sequence,
                              const uint8_t *payload,
                              uint8_t payload_len,
                              uint8_t *out,
                              size_t out_capacity,
                              size_t *out_len);

px1_result_t px1_decode_frame(const uint8_t *buf,
                              size_t len,
                              px1_frame_t *out,
                              size_t *consumed);

px1_result_t px1_encode_cmd_drive(uint16_t sequence,
                                  const px1_cmd_drive_t *cmd,
                                  uint8_t *out,
                                  size_t out_capacity,
                                  size_t *out_len);

px1_result_t px1_parse_cmd_drive(const px1_frame_t *frame,
                                 px1_cmd_drive_t *cmd);

px1_result_t px1_encode_telemetry(uint16_t sequence,
                                  const px1_telemetry_t *tm,
                                  uint8_t *out,
                                  size_t out_capacity,
                                  size_t *out_len);

px1_result_t px1_parse_telemetry(const px1_frame_t *frame,
                                 px1_telemetry_t *tm);

int16_t px1_clamp_demand(int32_t value);
uint16_t px1_clamp_light(uint32_t value);

#ifdef __cplusplus
}
#endif

#endif
