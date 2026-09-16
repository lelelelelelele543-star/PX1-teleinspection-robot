#include "px1_protocol.h"
#include <string.h>

static void put_u16_le(uint8_t *p, uint16_t v) {
    p[0] = (uint8_t)(v & 0xFFu);
    p[1] = (uint8_t)((v >> 8) & 0xFFu);
}

static void put_i16_le(uint8_t *p, int16_t v) {
    put_u16_le(p, (uint16_t)v);
}

static void put_i32_le(uint8_t *p, int32_t v) {
    uint32_t u = (uint32_t)v;
    p[0] = (uint8_t)(u & 0xFFu);
    p[1] = (uint8_t)((u >> 8) & 0xFFu);
    p[2] = (uint8_t)((u >> 16) & 0xFFu);
    p[3] = (uint8_t)((u >> 24) & 0xFFu);
}

static uint16_t get_u16_le(const uint8_t *p) {
    return (uint16_t)p[0] | ((uint16_t)p[1] << 8);
}

static int16_t get_i16_le(const uint8_t *p) {
    return (int16_t)get_u16_le(p);
}

static int32_t get_i32_le(const uint8_t *p) {
    uint32_t u = (uint32_t)p[0] |
                 ((uint32_t)p[1] << 8) |
                 ((uint32_t)p[2] << 16) |
                 ((uint32_t)p[3] << 24);
    return (int32_t)u;
}

uint16_t px1_crc16_ccitt_false(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFFu;
    if (data == NULL && len != 0u) return 0u;
    for (size_t i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        for (unsigned b = 0; b < 8u; ++b) {
            crc = (crc & 0x8000u) ? (uint16_t)((crc << 1) ^ 0x1021u)
                                  : (uint16_t)(crc << 1);
        }
    }
    return crc;
}

int16_t px1_clamp_demand(int32_t value) {
    if (value < PX1_DEMAND_MIN) return PX1_DEMAND_MIN;
    if (value > PX1_DEMAND_MAX) return PX1_DEMAND_MAX;
    return (int16_t)value;
}

uint16_t px1_clamp_light(uint32_t value) {
    return (uint16_t)(value > PX1_LIGHT_MAX ? PX1_LIGHT_MAX : value);
}

px1_result_t px1_encode_frame(uint8_t type,
                              uint16_t sequence,
                              const uint8_t *payload,
                              uint8_t payload_len,
                              uint8_t *out,
                              size_t out_capacity,
                              size_t *out_len) {
    if (out == NULL || out_len == NULL) return PX1_ERR_ARG;
    if (payload_len > PX1_MAX_PAYLOAD) return PX1_ERR_LENGTH;
    if (payload_len != 0u && payload == NULL) return PX1_ERR_ARG;

    const size_t needed = 9u + (size_t)payload_len;
    if (out_capacity < needed) return PX1_ERR_SHORT;

    out[0] = PX1_SOF0;
    out[1] = PX1_SOF1;
    out[2] = PX1_PROTOCOL_VERSION;
    out[3] = type;
    put_u16_le(&out[4], sequence);
    out[6] = payload_len;
    if (payload_len != 0u) memcpy(&out[7], payload, payload_len);

    const uint16_t crc = px1_crc16_ccitt_false(&out[2], 5u + payload_len);
    put_u16_le(&out[7u + payload_len], crc);
    *out_len = needed;
    return PX1_OK;
}

px1_result_t px1_decode_frame(const uint8_t *buf,
                              size_t len,
                              px1_frame_t *out,
                              size_t *consumed) {
    if (buf == NULL || out == NULL || consumed == NULL) return PX1_ERR_ARG;
    *consumed = 0u;
    if (len < 2u) return PX1_ERR_SHORT;

    size_t start = 0u;
    while (start + 1u < len && !(buf[start] == PX1_SOF0 && buf[start + 1u] == PX1_SOF1)) {
        ++start;
    }
    if (start != 0u) {
        *consumed = start;
        return PX1_ERR_SOF;
    }
    if (len < 7u) return PX1_ERR_SHORT;
    if (buf[2] != PX1_PROTOCOL_VERSION) {
        *consumed = 2u;
        return PX1_ERR_VERSION;
    }

    const uint8_t payload_len = buf[6];
    if (payload_len > PX1_MAX_PAYLOAD) {
        *consumed = 2u;
        return PX1_ERR_LENGTH;
    }
    const size_t frame_len = 9u + (size_t)payload_len;
    if (len < frame_len) return PX1_ERR_SHORT;

    const uint16_t got_crc = get_u16_le(&buf[7u + payload_len]);
    const uint16_t calc_crc = px1_crc16_ccitt_false(&buf[2], 5u + payload_len);
    if (got_crc != calc_crc) {
        *consumed = frame_len;
        return PX1_ERR_CRC;
    }

    out->type = buf[3];
    out->sequence = get_u16_le(&buf[4]);
    out->payload_len = payload_len;
    if (payload_len != 0u) memcpy(out->payload, &buf[7], payload_len);
    *consumed = frame_len;
    return PX1_OK;
}

px1_result_t px1_encode_cmd_drive(uint16_t sequence,
                                  const px1_cmd_drive_t *cmd,
                                  uint8_t *out,
                                  size_t out_capacity,
                                  size_t *out_len) {
    if (cmd == NULL) return PX1_ERR_ARG;
    uint8_t p[PX1_CMD_DRIVE_PAYLOAD_LEN];
    p[0] = cmd->enable ? 1u : 0u;
    p[1] = cmd->flags;
    put_i16_le(&p[2], px1_clamp_demand(cmd->left));
    put_i16_le(&p[4], px1_clamp_demand(cmd->right));
    put_u16_le(&p[6], px1_clamp_light(cmd->light));
    return px1_encode_frame(PX1_CMD_DRIVE_TYPE, sequence, p, sizeof p,
                            out, out_capacity, out_len);
}

px1_result_t px1_parse_cmd_drive(const px1_frame_t *frame,
                                 px1_cmd_drive_t *cmd) {
    if (frame == NULL || cmd == NULL) return PX1_ERR_ARG;
    if (frame->type != PX1_CMD_DRIVE_TYPE) return PX1_ERR_TYPE;
    if (frame->payload_len != PX1_CMD_DRIVE_PAYLOAD_LEN) return PX1_ERR_LENGTH;
    cmd->enable = frame->payload[0] == 1u;
    cmd->flags = frame->payload[1];
    cmd->left = px1_clamp_demand(get_i16_le(&frame->payload[2]));
    cmd->right = px1_clamp_demand(get_i16_le(&frame->payload[4]));
    cmd->light = px1_clamp_light(get_u16_le(&frame->payload[6]));
    if (!cmd->enable) {
        cmd->left = 0;
        cmd->right = 0;
    }
    return PX1_OK;
}

px1_result_t px1_encode_telemetry(uint16_t sequence,
                                  const px1_telemetry_t *tm,
                                  uint8_t *out,
                                  size_t out_capacity,
                                  size_t *out_len) {
    if (tm == NULL) return PX1_ERR_ARG;
    uint8_t p[PX1_TELEMETRY_PAYLOAD_LEN];
    put_u16_le(&p[0], tm->status_flags);
    put_u16_le(&p[2], tm->fault_flags);
    put_i32_le(&p[4], tm->pressure_pa_rel);
    put_u16_le(&p[8], tm->bus_mv);
    put_u16_le(&p[10], tm->left_ma);
    put_u16_le(&p[12], tm->right_ma);
    put_i16_le(&p[14], tm->hottest_c10);
    return px1_encode_frame(PX1_TELEMETRY_TYPE, sequence, p, sizeof p,
                            out, out_capacity, out_len);
}

px1_result_t px1_parse_telemetry(const px1_frame_t *frame,
                                 px1_telemetry_t *tm) {
    if (frame == NULL || tm == NULL) return PX1_ERR_ARG;
    if (frame->type != PX1_TELEMETRY_TYPE) return PX1_ERR_TYPE;
    if (frame->payload_len != PX1_TELEMETRY_PAYLOAD_LEN) return PX1_ERR_LENGTH;
    tm->status_flags = get_u16_le(&frame->payload[0]);
    tm->fault_flags = get_u16_le(&frame->payload[2]);
    tm->pressure_pa_rel = get_i32_le(&frame->payload[4]);
    tm->bus_mv = get_u16_le(&frame->payload[8]);
    tm->left_ma = get_u16_le(&frame->payload[10]);
    tm->right_ma = get_u16_le(&frame->payload[12]);
    tm->hottest_c10 = get_i16_le(&frame->payload[14]);
    return PX1_OK;
}
