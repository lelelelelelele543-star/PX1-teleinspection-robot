#include "px1_protocol.h"

uint16_t px1_crc16(const uint8_t *d, uint16_t n)
{
    uint16_t crc = 0xFFFFu;

    while (n--) {
        crc ^= (uint16_t)(*d++) << 8;
        for (uint8_t i = 0; i < 8u; i++) {
            crc = (crc & 0x8000u)
                ? (uint16_t)((crc << 1) ^ 0x1021u)
                : (uint16_t)(crc << 1);
        }
    }

    return crc;
}

int16_t px1_clamp1000(int32_t v)
{
    if (v > 1000) return 1000;
    if (v < -1000) return -1000;
    return (int16_t)v;
}

void px1_mix(int16_t drive, int16_t steer, int16_t *left, int16_t *right)
{
    if (!left || !right) return;
    *left = px1_clamp1000((int32_t)drive + steer);
    *right = px1_clamp1000((int32_t)drive - steer);
}

bool px1_header_valid(const px1_frame_header_t *h)
{
    if (!h) return false;
    if (h->ver != PX1_PROTO_VER) return false;
    if (h->len > PX1_MAX_PAYLOAD) return false;

    /* Never accept a zero/undefined endpoint as a normal addressed frame. */
    if (h->src == 0u || h->dst == 0u) return false;

    return true;
}

uint16_t px1_frame_wire_size(uint8_t payload_len)
{
    if (payload_len > PX1_MAX_PAYLOAD) return 0u;
    return (uint16_t)payload_len + PX1_FRAME_OVERHEAD_BYTES;
}
