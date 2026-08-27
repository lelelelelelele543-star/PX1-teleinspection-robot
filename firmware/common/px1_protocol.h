#pragma once
#include <stdint.h>
#include <stdbool.h>
#define PX1_SOF1 0xAAu
#define PX1_SOF2 0x55u
#define PX1_PROTO_VER 1u
#define PX1_MAX_PAYLOAD 64u
#define PX1_CONTROL_TIMEOUT_MS 300u
enum { PX1_CMD_CONTROL=0x01, PX1_CMD_HOME=0x02, PX1_CMD_ZERO_DISTANCE=0x03, PX1_CMD_ARM=0x04, PX1_CMD_DISARM=0x05, PX1_TELEMETRY=0x10, PX1_FAULT=0x11, PX1_ACK=0x12 };
typedef struct __attribute__((packed)) { int16_t drive,steer,tilt,roll; uint16_t light,flags; } px1_control_t;
typedef struct __attribute__((packed)) { uint8_t state; uint16_t fault_code,pressure_mbar,bus_mV; int16_t left_rpm_x10,right_rpm_x10; int32_t distance_mm; int16_t tilt_deg_x10,roll_deg_x10; uint16_t light_permille; int16_t temp_c_x10; uint16_t flags; } px1_telemetry_t;
uint16_t px1_crc16(const uint8_t *data,uint16_t len);
int16_t px1_clamp1000(int32_t v);
void px1_mix(int16_t drive,int16_t steer,int16_t *left,int16_t *right);
