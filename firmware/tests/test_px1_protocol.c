#include <assert.h>
#include <stdint.h>
#include <string.h>

#include "../common/px1_protocol.h"

int main(void)
{
    static const uint8_t check[] = "123456789";
    assert(px1_crc16(check, (uint16_t)strlen((const char *)check)) == 0x29B1u);

    assert(sizeof(px1_frame_header_t) == 6u);
    assert(sizeof(px1_control_t) == 12u);
    assert(sizeof(px1_telemetry_t) == 36u);
    assert(px1_frame_wire_size(0u) == 10u);
    assert(px1_frame_wire_size(64u) == 74u);
    assert(px1_frame_wire_size(65u) == 0u);

    px1_frame_header_t h = {
        .ver = PX1_PROTO_VER,
        .dst = PX1_ADDR_CRAWLER,
        .src = PX1_ADDR_CCU,
        .type = PX1_CMD_CONTROL,
        .seq = 1u,
        .len = (uint8_t)sizeof(px1_control_t)
    };
    assert(px1_header_valid(&h));

    h.ver = 1u;
    assert(!px1_header_valid(&h));
    h.ver = PX1_PROTO_VER;

    h.len = 65u;
    assert(!px1_header_valid(&h));
    h.len = (uint8_t)sizeof(px1_control_t);

    h.src = 0u;
    assert(!px1_header_valid(&h));
    h.src = PX1_ADDR_CCU;

    int16_t left = 0;
    int16_t right = 0;
    px1_mix(800, 400, &left, &right);
    assert(left == 1000);
    assert(right == 400);

    px1_mix(-900, -300, &left, &right);
    assert(left == -1000);
    assert(right == -600);

    return 0;
}
