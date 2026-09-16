#include "px1_stream.h"
#include <string.h>

static void reset_keep_suffix(px1_stream_t *s)
{
    size_t keep = 0u;
    if (s->len >= 1u && s->buf[s->len - 1u] == PX1_SOF0) keep = 1u;
    if (keep) s->buf[0] = PX1_SOF0;
    s->dropped_bytes += (uint32_t)(s->len - keep);
    s->len = keep;
}

void px1_stream_init(px1_stream_t *s)
{
    if (!s) return;
    memset(s, 0, sizeof(*s));
}

px1_stream_result_t px1_stream_feed(px1_stream_t *s,
                                    uint8_t byte,
                                    px1_frame_t *frame)
{
    if (!s || !frame) return PX1_STREAM_DROPPED;

    if (s->len == 0u) {
        if (byte != PX1_SOF0) {
            s->dropped_bytes++;
            return PX1_STREAM_DROPPED;
        }
        s->buf[s->len++] = byte;
        return PX1_STREAM_NONE;
    }

    if (s->len == 1u) {
        if (byte == PX1_SOF1) {
            s->buf[s->len++] = byte;
            return PX1_STREAM_NONE;
        }
        if (byte == PX1_SOF0) {
            /* Repeated first sync byte: keep the latest one. */
            s->dropped_bytes++;
            s->buf[0] = PX1_SOF0;
            return PX1_STREAM_DROPPED;
        }
        s->dropped_bytes += 2u;
        s->len = 0u;
        return PX1_STREAM_DROPPED;
    }

    if (s->len >= sizeof(s->buf)) {
        reset_keep_suffix(s);
        s->bad_frames++;
        return PX1_STREAM_DROPPED;
    }

    s->buf[s->len++] = byte;

    if (s->len == 3u && s->buf[2] != PX1_PROTOCOL_VERSION) {
        reset_keep_suffix(s);
        s->bad_frames++;
        return PX1_STREAM_DROPPED;
    }

    if (s->len >= 7u) {
        uint8_t payload_len = s->buf[6];
        if (payload_len > PX1_MAX_PAYLOAD) {
            reset_keep_suffix(s);
            s->bad_frames++;
            return PX1_STREAM_DROPPED;
        }
        size_t expected = 9u + (size_t)payload_len;
        if (s->len < expected) return PX1_STREAM_NONE;

        size_t consumed = 0u;
        px1_result_t r = px1_decode_frame(s->buf, s->len, frame, &consumed);
        if (r == PX1_OK) {
            s->good_frames++;
            s->len = 0u;
            return PX1_STREAM_FRAME;
        }

        reset_keep_suffix(s);
        s->bad_frames++;
        return PX1_STREAM_DROPPED;
    }

    return PX1_STREAM_NONE;
}
