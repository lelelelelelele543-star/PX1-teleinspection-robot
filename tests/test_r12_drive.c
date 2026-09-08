#include "../firmware/crawler/r12/drive_r12.h"
#include <assert.h>
#include <stdio.h>
static unsigned a[2],b[2];
static void write_pair(unsigned m,uint16_t x,uint16_t y){a[m]=x;b[m]=y;assert(!(x&&y));assert(x<=1000&&y<=1000);}
int main(void){
 px1_r12_drive d;px1_r12_init(&d,write_pair);
 assert(!d.armed&&!a[0]&&!b[0]);
 assert(!px1_r12_command(&d,0,1000,1000));
 assert(!px1_r12_arm(&d,0,false));assert(px1_r12_arm(&d,0,true));
 assert(px1_r12_command(&d,0,1000,-1000));
 for(unsigned t=0;t<=100;t+=10)px1_r12_tick(&d,t,true);
 assert(a[0]>0&&b[1]>0);
 assert(px1_r12_command(&d,110,-1000,1000));
 unsigned zero_at=0;
 for(unsigned t=110;t<=230;t+=10){px1_r12_tick(&d,t,true);if(!d.output[0]&&!zero_at)zero_at=t;}
 assert(zero_at&&d.reversal_wait[0]);assert(!a[0]&&!b[0]);
 px1_r12_tick(&d,zero_at+49,true);assert(!d.output[0]);
 px1_r12_tick(&d,zero_at+50,true);assert(d.output[0]<0&&d.output[1]>0);
 assert(!px1_r12_command(&d,359,1001,0));
 px1_r12_tick(&d,360,true);assert(d.fault&&!d.armed&&!a[0]&&!b[0]);
 assert(!px1_r12_command(&d,361,200,200));assert(px1_r12_arm(&d,362,true));
 assert(!d.target[0]&&!d.target[1]);px1_r12_tick(&d,363,false);assert(d.fault&&!d.armed);
 assert(px1_r12_arm(&d,UINT32_MAX-100,true));
 px1_r12_tick(&d,148,true);assert(d.armed);
 px1_r12_tick(&d,149,true);assert(!d.armed&&d.fault);
 puts("PASS: init, explicit arm, bounds, slew, reverse dwell, timeout, interlock, wraparound");
 return 0;
}

