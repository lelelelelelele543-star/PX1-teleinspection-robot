#include "px1_protocol.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

static void test_crc_vector(void) {
    static const uint8_t s[] = "123456789";
    assert(px1_crc16_ccitt_false(s, 9) == 0x29B1u);
}

static void test_cmd_roundtrip(void) {
    uint8_t wire[PX1_MAX_FRAME];
    size_t wire_len = 0;
    px1_cmd_drive_t in = {
        .enable = true,
        .flags = 0,
        .left = -321,
        .right = 777,
        .light = 650
    };
    assert(px1_encode_cmd_drive(65535u, &in, wire, sizeof wire, &wire_len) == PX1_OK);
    assert(wire_len == 17u);

    px1_frame_t frame;
    size_t used = 0;
    assert(px1_decode_frame(wire, wire_len, &frame, &used) == PX1_OK);
    assert(used == wire_len);
    assert(frame.sequence == 65535u);
    assert(frame.type == PX1_CMD_DRIVE_TYPE);

    px1_cmd_drive_t out;
    assert(px1_parse_cmd_drive(&frame, &out) == PX1_OK);
    assert(out.enable);
    assert(out.left == -321);
    assert(out.right == 777);
    assert(out.light == 650);
}

static void test_disable_forces_zero(void) {
    uint8_t wire[PX1_MAX_FRAME];
    size_t wire_len = 0;
    px1_cmd_drive_t in = {.enable=false, .flags=0, .left=900, .right=-900, .light=1000};
    assert(px1_encode_cmd_drive(1, &in, wire, sizeof wire, &wire_len) == PX1_OK);
    px1_frame_t frame;
    size_t used = 0;
    assert(px1_decode_frame(wire, wire_len, &frame, &used) == PX1_OK);
    px1_cmd_drive_t out;
    assert(px1_parse_cmd_drive(&frame, &out) == PX1_OK);
    assert(out.left == 0 && out.right == 0);
}

static void test_clamp(void) {
    assert(px1_clamp_demand(-5000) == -1000);
    assert(px1_clamp_demand(5000) == 1000);
    assert(px1_clamp_light(5000) == 1000u);
}

static void test_crc_reject(void) {
    uint8_t wire[PX1_MAX_FRAME];
    size_t wire_len = 0;
    px1_cmd_drive_t cmd = {.enable=true, .left=1, .right=2, .light=3};
    assert(px1_encode_cmd_drive(7, &cmd, wire, sizeof wire, &wire_len) == PX1_OK);
    wire[10] ^= 0x01u;
    px1_frame_t frame;
    size_t used = 0;
    assert(px1_decode_frame(wire, wire_len, &frame, &used) == PX1_ERR_CRC);
    assert(used == wire_len);
}

static void test_noise_resync_hint(void) {
    uint8_t wire[PX1_MAX_FRAME];
    size_t wire_len = 0;
    px1_cmd_drive_t cmd = {.enable=true, .left=10, .right=20, .light=30};
    assert(px1_encode_cmd_drive(8, &cmd, wire, sizeof wire, &wire_len) == PX1_OK);
    uint8_t noisy[PX1_MAX_FRAME + 3];
    noisy[0]=0x00; noisy[1]=0x12; noisy[2]=0xA5;
    memcpy(&noisy[3], wire, wire_len);
    px1_frame_t frame;
    size_t used = 0;
    assert(px1_decode_frame(noisy, wire_len + 3, &frame, &used) == PX1_ERR_SOF);
    assert(used == 3u);
}

static void test_telemetry_roundtrip(void) {
    px1_telemetry_t in = {
        .status_flags = 0x0055u,
        .fault_flags = 0x0102u,
        .pressure_pa_rel = 25123,
        .bus_mv = 24110,
        .left_ma = 840,
        .right_ma = 910,
        .hottest_c10 = 473
    };
    uint8_t wire[PX1_MAX_FRAME];
    size_t wire_len = 0;
    assert(px1_encode_telemetry(9, &in, wire, sizeof wire, &wire_len) == PX1_OK);
    px1_frame_t frame;
    size_t used = 0;
    assert(px1_decode_frame(wire, wire_len, &frame, &used) == PX1_OK);
    px1_telemetry_t out;
    assert(px1_parse_telemetry(&frame, &out) == PX1_OK);
    assert(memcmp(&in, &out, sizeof in) == 0);
}

int main(void) {
    test_crc_vector();
    test_cmd_roundtrip();
    test_disable_forces_zero();
    test_clamp();
    test_crc_reject();
    test_noise_resync_hint();
    test_telemetry_roundtrip();
    puts("PX1 protocol V1 tests: PASS");
    return 0;
}
