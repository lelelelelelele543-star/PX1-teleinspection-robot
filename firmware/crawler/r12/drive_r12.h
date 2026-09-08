#pragma once
#include <stdbool.h>
#include <stdint.h>
/* Host-testable control only. HAL must atomically apply each IN1/IN2 pair. */
typedef void (*px1_r12_write)(unsigned motor, uint16_t in1, uint16_t in2);
typedef struct {
  bool armed, fault;
  int16_t target[2], output[2];
  uint32_t last_command, zero_since[2];
  bool reversal_wait[2];
  px1_r12_write write;
} px1_r12_drive;
void px1_r12_init(px1_r12_drive*, px1_r12_write);
bool px1_r12_arm(px1_r12_drive*, uint32_t now, bool interlocks_ok);
bool px1_r12_command(px1_r12_drive*, uint32_t now, int left, int right);
void px1_r12_stop(px1_r12_drive*);
void px1_r12_tick(px1_r12_drive*, uint32_t now, bool interlocks_ok);

