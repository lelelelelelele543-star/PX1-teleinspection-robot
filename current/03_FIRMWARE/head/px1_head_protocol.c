#include "px1_head_protocol.h"

static void put_u16(uint8_t *p, uint16_t v) { p[0]=(uint8_t)(v&0xffu); p[1]=(uint8_t)(v>>8); }
static uint16_t get_u16(const uint8_t *p) { return (uint16_t)p[0] | ((uint16_t)p[1]<<8); }
static void put_i16(uint8_t *p, int16_t v) { put_u16(p,(uint16_t)v); }
static int16_t get_i16(const uint8_t *p) { return (int16_t)get_u16(p); }

px1_result_t px1_encode_cmd_head(uint16_t sequence,
                                 const px1_cmd_head_t *cmd,
                                 uint8_t *out,
                                 size_t out_capacity,
                                 size_t *out_len)
{
    if (!cmd) return PX1_ERR_ARG;
    uint8_t p[PX1_CMD_HEAD_PAYLOAD_LEN];
    p[0]=cmd->enable ? 1u : 0u;
    p[1]=cmd->flags;
    put_i16(&p[2],px1_clamp_demand(cmd->pan));
    put_i16(&p[4],px1_clamp_demand(cmd->rotate));
    put_u16(&p[6],px1_clamp_light(cmd->light));
    return px1_encode_frame(PX1_CMD_HEAD_TYPE,sequence,p,sizeof p,out,out_capacity,out_len);
}

px1_result_t px1_parse_cmd_head(const px1_frame_t *frame,
                                px1_cmd_head_t *cmd)
{
    if (!frame || !cmd) return PX1_ERR_ARG;
    if (frame->type != PX1_CMD_HEAD_TYPE) return PX1_ERR_TYPE;
    if (frame->payload_len != PX1_CMD_HEAD_PAYLOAD_LEN) return PX1_ERR_LENGTH;
    cmd->enable=frame->payload[0] != 0u;
    cmd->flags=frame->payload[1];
    cmd->pan=px1_clamp_demand(get_i16(&frame->payload[2]));
    cmd->rotate=px1_clamp_demand(get_i16(&frame->payload[4]));
    cmd->light=px1_clamp_light(get_u16(&frame->payload[6]));
    return PX1_OK;
}

px1_result_t px1_encode_head_telemetry(uint16_t sequence,
                                       const px1_head_telemetry_t *tm,
                                       uint8_t *out,
                                       size_t out_capacity,
                                       size_t *out_len)
{
    if (!tm) return PX1_ERR_ARG;
    uint8_t p[PX1_HEAD_TELEMETRY_PAYLOAD_LEN];
    put_u16(&p[0],tm->status_flags);
    put_u16(&p[2],tm->fault_flags);
    put_i16(&p[4],tm->pan_cdeg);
    put_i16(&p[6],tm->rotate_cdeg);
    put_u16(&p[8],tm->pan_ma);
    put_u16(&p[10],tm->rotate_ma);
    put_i16(&p[12],tm->hottest_c10);
    return px1_encode_frame(PX1_HEAD_TELEMETRY_TYPE,sequence,p,sizeof p,out,out_capacity,out_len);
}

px1_result_t px1_parse_head_telemetry(const px1_frame_t *frame,
                                      px1_head_telemetry_t *tm)
{
    if (!frame || !tm) return PX1_ERR_ARG;
    if (frame->type != PX1_HEAD_TELEMETRY_TYPE) return PX1_ERR_TYPE;
    if (frame->payload_len != PX1_HEAD_TELEMETRY_PAYLOAD_LEN) return PX1_ERR_LENGTH;
    tm->status_flags=get_u16(&frame->payload[0]);
    tm->fault_flags=get_u16(&frame->payload[2]);
    tm->pan_cdeg=get_i16(&frame->payload[4]);
    tm->rotate_cdeg=get_i16(&frame->payload[6]);
    tm->pan_ma=get_u16(&frame->payload[8]);
    tm->rotate_ma=get_u16(&frame->payload[10]);
    tm->hottest_c10=get_i16(&frame->payload[12]);
    return PX1_OK;
}
