#include "drive_r12.h"
#include <string.h>
#define COMMAND_TIMEOUT 250u
#define REVERSE_DWELL 50u
#define SLEW_STEP 35
static void emit(px1_r12_drive* d) {
  for (unsigned i=0;i<2;i++) {
    int x=d->output[i];
    if(d->write)d->write(i,x>0?(uint16_t)x:0,x<0?(uint16_t)-x:0);
  }
}
void px1_r12_stop(px1_r12_drive* d) {
  d->armed=false;d->fault=true;
  for(unsigned i=0;i<2;i++){d->target[i]=d->output[i]=0;d->reversal_wait[i]=false;}
  emit(d);
}
void px1_r12_init(px1_r12_drive* d,px1_r12_write write) {
  memset(d,0,sizeof(*d));d->write=write;emit(d);
}
bool px1_r12_arm(px1_r12_drive* d,uint32_t now,bool ok) {
  if(!ok||d->armed||d->output[0]||d->output[1])return false;
  d->fault=false;d->armed=true;d->last_command=now;
  d->target[0]=d->target[1]=0;return true;
}
bool px1_r12_command(px1_r12_drive* d,uint32_t now,int left,int right) {
  /* Call only after complete protocol, CRC, source and range validation. */
  if(!d->armed||d->fault||left < -1000||left > 1000||right < -1000||right > 1000)return false;
  d->target[0]=(int16_t)left;d->target[1]=(int16_t)right;d->last_command=now;return true;
}
void px1_r12_tick(px1_r12_drive* d,uint32_t now,bool ok) {
  /* Exactly one call per 10ms scheduler tick; wall-clock dwell is wrap-safe. */
  if(!ok||(d->armed&&(uint32_t)(now-d->last_command)>=COMMAND_TIMEOUT)){px1_r12_stop(d);return;}
  if(!d->armed||d->fault){d->output[0]=d->output[1]=0;emit(d);return;}
  for(unsigned i=0;i<2;i++){
    int out=d->output[i],target=d->target[i];
    bool reverse=(out>0&&target<0)||(out<0&&target>0);
    if(reverse)target=0;
    if(d->reversal_wait[i]){
      if((uint32_t)(now-d->zero_since[i])<REVERSE_DWELL)continue;
      d->reversal_wait[i]=false;
    }
    if(out<target)out=out+SLEW_STEP>target?target:out+SLEW_STEP;
    else if(out>target)out=out-SLEW_STEP<target?target:out-SLEW_STEP;
    if(reverse&&out==0){d->reversal_wait[i]=true;d->zero_since[i]=now;}
    d->output[i]=(int16_t)out;
  }
  emit(d);
}

