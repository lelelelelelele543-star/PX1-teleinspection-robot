#pragma once
/* PX-1 crawler / NUCLEO-F446RE / Rev.B WB09 logical pin map */

/*
 * Main tether RS-485
 * Waveshare TTL TO RS485 (C), SKU 27479, handles half-duplex direction
 * internally and exposes TXD/RXD rather than an external DE input.
 * PC10/PC11 are used so PA2/PA3 can remain on the NUCLEO ST-LINK VCP
 * for bench diagnostics.
 */
#define PX1_RS485_TX "PC10/USART3_TX"
#define PX1_RS485_RX "PC11/USART3_RX"
#define PX1_RS485_AUTO_DIR 1

/* ST-LINK VCP / bench debug */
#define PX1_DEBUG_TX "PA2/USART2_TX"
#define PX1_DEBUG_RX "PA3/USART2_RX"

/* Local crawler <-> camera-node UART; does not use tether cores */
#define PX1_CAMERA_TX "PC12/UART5_TX"
#define PX1_CAMERA_RX "PD2/UART5_RX"

/* Ready current/power sensors */
#define PX1_I2C_SCL "PB8/I2C1_SCL"
#define PX1_I2C_SDA "PB9/I2C1_SDA"

/* Traction */
#define PX1_TRACTION_L_PWM "PA8/TIM1_CH1"
#define PX1_TRACTION_R_PWM "PA9/TIM1_CH2"
#define PX1_WHEEL_L_ADC "PA0/ADC1_IN0"
#define PX1_WHEEL_R_ADC "PA1/ADC1_IN1"

/* Sensors */
#define PX1_PRESSURE_ADC "PC0/ADC1_IN10"
#define PX1_BUS_ADC "PC1/ADC1_IN11"
#define PX1_TEMP_ADC "PC2/ADC1_IN12"

/* Camera / lighting control */
#define PX1_LIGHT_PWM "PB6/TIM4_CH1"
#define PX1_TILT_IN1 "PC6"
#define PX1_TILT_IN2 "PC7"
#define PX1_ROLL_IN1 "PC8"
#define PX1_ROLL_IN2 "PC9"

/* Safety */
#define PX1_ESTOP "PB13"
#define PX1_LEAK "PB14"
