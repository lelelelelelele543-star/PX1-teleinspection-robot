#include "px1_protocol.h"
uint16_t px1_crc16(const uint8_t *d,uint16_t n){ uint16_t crc=0xFFFF; while(n--){ crc^=(uint16_t)(*d++)<<8; for(uint8_t i=0;i<8;i++) crc=(crc&0x8000)?(uint16_t)((crc<<1)^0x1021):(uint16_t)(crc<<1); } return crc; }
int16_t px1_clamp1000(int32_t v){ if(v>1000)return 1000; if(v<-1000)return -1000; return (int16_t)v; }
void px1_mix(int16_t d,int16_t s,int16_t *l,int16_t *r){ *l=px1_clamp1000((int32_t)d+s); *r=px1_clamp1000((int32_t)d-s); }
