#include <assert.h>
#include <stdio.h>
#include "px1_head_protocol.h"

int main(void)
{
    uint8_t buf[PX1_MAX_FRAME];
    size_t n=0,consumed=0;
    px1_frame_t f;

    px1_cmd_head_t c={true,0x12,1200,-1300,1500};
    assert(px1_encode_cmd_head(77,&c,buf,sizeof buf,&n)==PX1_OK);
    assert(px1_decode_frame(buf,n,&f,&consumed)==PX1_OK);
    assert(consumed==n && f.type==PX1_CMD_HEAD_TYPE && f.sequence==77);
    px1_cmd_head_t p;
    assert(px1_parse_cmd_head(&f,&p)==PX1_OK);
    assert(p.enable && p.flags==0x12);
    assert(p.pan==1000 && p.rotate==-1000 && p.light==1000);

    px1_head_telemetry_t t={0x11,0x22,1234,-5678,321,654,455};
    assert(px1_encode_head_telemetry(78,&t,buf,sizeof buf,&n)==PX1_OK);
    assert(px1_decode_frame(buf,n,&f,&consumed)==PX1_OK);
    px1_head_telemetry_t q;
    assert(px1_parse_head_telemetry(&f,&q)==PX1_OK);
    assert(q.status_flags==0x11 && q.fault_flags==0x22);
    assert(q.pan_cdeg==1234 && q.rotate_cdeg==-5678);
    assert(q.pan_ma==321 && q.rotate_ma==654 && q.hottest_c10==455);

    /* Shared CRC/framing must reject head-frame corruption as well. */
    buf[8]^=0x01u;
    assert(px1_decode_frame(buf,n,&f,&consumed)==PX1_ERR_CRC);

    puts("PX1 head protocol tests: PASS");
    return 0;
}
