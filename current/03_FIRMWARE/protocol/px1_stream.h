#ifndef PX1_STREAM_H
#define PX1_STREAM_H

#include <stddef.h>
#include <stdint.h>
#include "px1_protocol.h"

typedef enum {
    PX1_STREAM_NONE = 0,
    PX1_STREAM_FRAME = 1,
    PX1_STREAM_DROPPED = -1
} px1_stream_result_t;

typedef struct {
    uint8_t buf[PX1_MAX_FRAME];
    size_t len;
    uint32_t dropped_bytes;
    uint32_t bad_frames;
    uint32_t good_frames;
} px1_stream_t;

void px1_stream_init(px1_stream_t *s);
px1_stream_result_t px1_stream_feed(px1_stream_t *s,
                                    uint8_t byte,
                                    px1_frame_t *frame);

#endif
