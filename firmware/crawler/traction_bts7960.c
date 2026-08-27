#include <stdint.h>
#include <stdbool.h>
#define PX1_CMD_MAX 1000
#define PX1_DEADBAND 25
#define PX1_SLEW_STEP 35
extern void board_pwm_left(uint16_t duty); extern void board_pwm_right(uint16_t duty);
extern void board_left_dir(bool forward); extern void board_right_dir(bool forward);
extern void board_left_enable(bool en); extern void board_right_enable(bool en);
static int16_t l_out=0,r_out=0;
static int16_t approach(int16_t cur,int16_t target){ if(target>cur+PX1_SLEW_STEP)return cur+PX1_SLEW_STEP; if(target<cur-PX1_SLEW_STEP)return cur-PX1_SLEW_STEP; return target; }
static void apply(int16_t cmd,void(*pwm)(uint16_t),void(*dir)(bool),void(*en)(bool)){ if(cmd>-PX1_DEADBAND&&cmd<PX1_DEADBAND){pwm(0);en(false);return;} en(true);dir(cmd>=0);uint16_t d=(uint16_t)(cmd>=0?cmd:-cmd);if(d>PX1_CMD_MAX)d=PX1_CMD_MAX;pwm(d); }
void traction_set_target(int16_t left,int16_t right){l_out=approach(l_out,left);r_out=approach(r_out,right);apply(l_out,board_pwm_left,board_left_dir,board_left_enable);apply(r_out,board_pwm_right,board_right_dir,board_right_enable);}
void traction_stop(void){l_out=r_out=0;board_pwm_left(0);board_pwm_right(0);board_left_enable(false);board_right_enable(false);}
