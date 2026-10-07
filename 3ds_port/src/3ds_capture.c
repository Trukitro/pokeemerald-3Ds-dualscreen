/*
 * Screen captures for the test harness (3ds_autotest.c): what each screen's
 * framebuffer holds, written to the SD card as a BMP.
 *
 * The framebuffers are the console's own: 240 pixels wide and the screen's
 * width tall, a column of the picture per row, bottom to top - the top screen
 * BGR8 and the bottom one RGB565 as this port sets them up. A BMP is written
 * bottom row first, which is the order a column is in.
 */
#include <3ds.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#include "3ds_platform.h"
#include "3ds_log.h"

#define CAPTURE_DIR "sdmc:/3ds/emerald3ds/shots"

static void Put32(u8 *p, u32 v) { p[0] = v; p[1] = v >> 8; p[2] = v >> 16; p[3] = v >> 24; }

static bool WriteBmp(const char *path, const u8 *fb, GSPGPU_FramebufferFormat format, unsigned width)
{
    const unsigned height = 240, row = width * 3;    /* 400 and 320: no padding */
    u8 header[54] = {'B', 'M'};
    u8 *pixels = malloc(row * height);
    FILE *file;
    bool ok;

    if (pixels == NULL || fb == NULL)
    {
        free(pixels);
        return false;
    }
    /* Pixel (x, y) of the picture is fb[x * 240 + (239 - y)]: row r of the
     * file, counted from the bottom, is index r of every column. */
    for (unsigned r = 0; r < height; ++r)
        for (unsigned x = 0; x < width; ++x)
        {
            u8 *out = pixels + r * row + x * 3;

            if (format == GSP_RGB565_OES)
            {
                u16 c = ((const u16 *)fb)[x * 240 + r];

                out[0] = (c & 31) * 255 / 31;
                out[1] = ((c >> 5) & 63) * 255 / 63;
                out[2] = (c >> 11) * 255 / 31;
            }
            else if (format == GSP_RGBA8_OES)
            {
                const u8 *in = fb + (x * 240 + r) * 4;

                out[0] = in[1]; out[1] = in[2]; out[2] = in[3];
            }
            else
                memcpy(out, fb + (x * 240 + r) * 3, 3);     /* BGR8, a BMP's own order */
        }
    Put32(header + 2, sizeof(header) + row * height);
    Put32(header + 10, sizeof(header));
    Put32(header + 14, 40);
    Put32(header + 18, width);
    Put32(header + 22, height);
    header[26] = 1;
    header[28] = 24;
    Put32(header + 34, row * height);
    file = fopen(path, "wb");
    ok = file != NULL && fwrite(header, 1, sizeof(header), file) == sizeof(header)
      && fwrite(pixels, 1, row * height, file) == row * height;
    if (file != NULL)
        fclose(file);
    free(pixels);
    return ok;
}

bool CtrCapture_Save(const char *name)
{
    char path[160];
    u16 w, h;
    u8 *fb;
    bool ok;

    mkdir(CAPTURE_DIR, 0777);
    /* The buffer being shown, not the one the next frame is drawn to. */
    gspWaitForVBlank();
    fb = gfxGetFramebuffer(GFX_TOP, GFX_LEFT, &w, &h);
    snprintf(path, sizeof(path), CAPTURE_DIR "/%s_top.bmp", name);
    ok = WriteBmp(path, fb, gfxGetScreenFormat(GFX_TOP), 400);
    fb = gfxGetFramebuffer(GFX_BOTTOM, GFX_LEFT, &w, &h);
    snprintf(path, sizeof(path), CAPTURE_DIR "/%s_bottom.bmp", name);
    ok = WriteBmp(path, fb, gfxGetScreenFormat(GFX_BOTTOM), 320) && ok;
    CtrLog_Write(CTR_LOG_VIDEO, "capture %s: %s", name, ok ? "written" : "FAILED");
    return ok;
}
