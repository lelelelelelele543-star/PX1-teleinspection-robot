#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "px1_stream.h"

static int feed_buf(px1_stream_t *s, const uint8_t *buf, size_t len, px1_frame_t *out)
{
    int frames = 0;
    for (size_t i=0; i<len; ++i) {
        px1_stream_result_t r = px1_stream_feed(s, buf[i], out);
        if (r == PX1_STREAM_FRAME) frames++;
    }
    return frames;
}

int main(void)
{
    px1_stream_t s;
    px1_stream_init(&s);
    px1_frame_t f;

    px1_cmd_drive_t cmd = {true, 0, 500, -250, 700};
    uint8_t frame[PX1_MAX_FRAME];
    size_t frame_len = 0;
    assert(px1_encode_cmd_drive(42, &cmd, frame, sizeof frame, &frame_len) == PX1_OK);

    /* Noise before a valid frame must be ignored and resynchronized. */
    const uint8_t noise[] = {0x00,0xFF,0x12,0xA5,0x00,0x33};
    assert(feed_buf(&s, noise, sizeof noise, &f) == 0);
    assert(feed_buf(&s, frame, frame_len, &f) == 1);
    assert(f.sequence == 42 && f.type == PX1_CMD_DRIVE_TYPE);

    px1_cmd_drive_t parsed;
    assert(px1_parse_cmd_drive(&f, &parsed) == PX1_OK);
    assert(parsed.left == 500 && parsed.right == -250 && parsed.light == 700);

    /* A corrupt CRC frame followed by a good one must not latch bad motion. */
    uint8_t corrupt[PX1_MAX_FRAME];
    memcpy(corrupt, frame, frame_len);
    corrupt[8] ^= 0x55u;
    unsigned good_before = s.good_frames;
    assert(feed_buf(&s, corrupt, frame_len, &f) == 0);
    assert(s.bad_frames >= 1u);
    assert(feed_buf(&s, frame, frame_len, &f) == 1);
    assert(s.good_frames == good_before + 1u);

    /* Fragmentation at arbitrary byte boundaries is normal on UART DMA/ring buffers. */
    px1_stream_init(&s);
    assert(feed_buf(&s, frame, 3, &f) == 0);
    assert(feed_buf(&s, frame+3, 2, &f) == 0);
    assert(feed_buf(&s, frame+5, frame_len-5, &f) == 1);

    /* Repeated SOF0 must still permit the next complete SOF pair. */
    px1_stream_init(&s);
    uint8_t prefix[] = {PX1_SOF0, PX1_SOF0};
    assert(feed_buf(&s, prefix, sizeof prefix, &f) == 0);
    assert(feed_buf(&s, frame+1, frame_len-1, &f) == 1);

    /* Invalid version is rejected, then the next good frame is recovered. */
    px1_stream_init(&s);
    uint8_t badver[PX1_MAX_FRAME];
    memcpy(badver, frame, frame_len);
    badver[2] = 0x7Fu;
    assert(feed_buf(&s, badver, frame_len, &f) == 0);
    assert(feed_buf(&s, frame, frame_len, &f) == 1);

    puts("PX1 stream parser tests: PASS");
    return 0;
}
