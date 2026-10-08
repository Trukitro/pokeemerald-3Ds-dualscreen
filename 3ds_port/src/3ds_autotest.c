/*
 * A test harness for the emulator: a script on the SD card that puts the
 * player on a list of maps and captures the screens at each.
 *
 * Nothing happens unless sdmc:/3ds/emerald3ds/autotest.txt exists, which no
 * player's card has. With it, the game is started as a new game without the
 * intro or the truck, and the script's lines run in order:
 *
 *     warp GROUP NUM X Y     put the player there and wait for the field
 *     voxel 0|1              the VOXEL 3D option
 *     flash LEVEL            the dark of a cave at that level, animated as
 *                            the move does it (1 is after Flash, 7 before)
 *     audit NAME             shots/NAME_audit.txt: what every cell of the
 *                            map is in the voxel view (Audit, below)
 *     wait FRAMES            let chunks build, animations run
 *     perf NAME FRAMES       stand there that long and add a line to perf.txt:
 *                            what the frames took (Perf, below)
 *     shot NAME              shots/NAME_top.bmp and shots/NAME_bottom.bmp
 *     quit                   write autotest.done and leave
 *
 * devtools/autotest.py writes the script from map names and reads the
 * captures back. An emulator is not the console: this is for seeing a change
 * and for comparing a sweep before and after it, not for accepting it.
 * `perf` is the exception: it is for the console, where the same script run
 * by two builds says what one costs over the other (devtools/perf_run.py).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "global.h"
#include "main.h"
#include "overworld.h"
#include "new_game.h"
#include "load_save.h"
#include "palette.h"
#include "play_time.h"
#include "safari_zone.h"
#include "script.h"
#include "sound.h"
#include "sprite.h"
#include "task.h"
#include "field_player_avatar.h"
#include "event_object_lock.h"
#include "field_screen_effect.h"
#include "port_log.h"

#include "3ds_platform.h"
#include "3ds_video.h"
#if CTR_VOXEL_ENABLED
#include "voxel/voxel_world.h"
#include "voxel/voxel_building.h"
#include "voxel/voxel_tree.h"
#include "voxel/voxel_relief.h"
#include "voxel/voxel_sign.h"
#endif

#define AUTOTEST_PATH "sdmc:/3ds/emerald3ds/autotest.txt"
#define AUTOTEST_DONE "sdmc:/3ds/emerald3ds/autotest.done"
#define AUTOTEST_PERF "sdmc:/3ds/emerald3ds/perf.txt"
/* Which build wrote a line of perf.txt: the card is shared by all of them. */
#ifndef AUTOTEST_BUILD
#define AUTOTEST_BUILD "fork"
#endif
#define AUTOTEST_LINES 600
/* The copyright screen has set the save blocks up by then. */
#define AUTOTEST_FIRST_FRAME 240
/* A warp that never reaches the field is skipped, not waited on for ever. */
#define AUTOTEST_WARP_TIMEOUT 900

enum { OP_WARP, OP_VOXEL, OP_FLASH, OP_AUDIT, OP_WAIT, OP_SHOT, OP_PERF, OP_KEYS, OP_BIKE, OP_QUIT };

/* The buttons a script holds down ("keys MASK FRAMES": 3ds_input.c's order -
 * A 1, B 2, right 16, left 32, up 64, down 128), so that a thing is tried by
 * moving through it and not only by standing in it. */
uint32_t gCtrAutotestButtons;

typedef struct
{
    u8 op;
    s16 arg[4];
    char name[72];
} AutotestLine;

static AutotestLine *sLines;
static unsigned sCount, sNext;
static int sState;          /* 0 unread, 1 running, 2 waiting for the field, -1 off */
static unsigned sWait;
static bool sStarted;

bool CtrCapture_Save(const char *name);     /* 3ds_capture.c */

static void Load(void)
{
    FILE *file = fopen(AUTOTEST_PATH, "r");
    char text[128], op[16];

    sState = -1;
    if (file == NULL)
        return;
    sLines = calloc(AUTOTEST_LINES, sizeof(*sLines));
    while (sLines != NULL && sCount < AUTOTEST_LINES && fgets(text, sizeof(text), file) != NULL)
    {
        AutotestLine *line = &sLines[sCount];
        int a = 0, b = 0, c = 0, d = 0;

        if (sscanf(text, "%15s", op) != 1 || op[0] == '#')
            continue;
        if (!strcmp(op, "warp") && sscanf(text, "%*s %d %d %d %d", &a, &b, &c, &d) == 4)
            line->op = OP_WARP;
        else if (!strcmp(op, "voxel") && sscanf(text, "%*s %d", &a) == 1)
            line->op = OP_VOXEL;
        else if (!strcmp(op, "flash") && sscanf(text, "%*s %d", &a) == 1)
            line->op = OP_FLASH;
        else if (!strcmp(op, "wait") && sscanf(text, "%*s %d", &a) == 1)
            line->op = OP_WAIT;
        else if (!strcmp(op, "shot") && sscanf(text, "%*s %71s", line->name) == 1)
            line->op = OP_SHOT;
        else if (!strcmp(op, "audit") && sscanf(text, "%*s %71s", line->name) == 1)
            line->op = OP_AUDIT;
        else if (!strcmp(op, "perf") && sscanf(text, "%*s %71s %d", line->name, &a) == 2)
            line->op = OP_PERF;
        else if (!strcmp(op, "keys") && sscanf(text, "%*s %d %d", &a, &b) == 2)
            line->op = OP_KEYS;
        else if (!strcmp(op, "bike"))
            line->op = OP_BIKE;
        else if (!strcmp(op, "quit"))
            line->op = OP_QUIT;
        else
            continue;
        line->arg[0] = a; line->arg[1] = b; line->arg[2] = c; line->arg[3] = d;
        ++sCount;
    }
    fclose(file);
    remove(AUTOTEST_DONE);
    if (sCount != 0)
        sState = 1;
    CtrLog_Write(CTR_LOG_GAME, "autotest: %u lines", sCount);
}

/*
 * What stands and what lies flat, cell by cell, asked of the voxel world
 * itself - not judged from a picture, where a drawing lying on the ground
 * and a model of it look much alike. A cell the game blocks is something
 * the player cannot walk through: a wall, a piece of furniture, a tree, a
 * building. If nothing stands there in the voxel view, it is flat, and
 * that is what is still to be made. A row of the map a line:
 *
 *     .  open ground          M  a model's cell        T  a tree
 *     R  relief off the ground S  a sign or a lamp     W  water
 *     F  furniture stood up by its behaviour           V  nothing (void)
 *     #  BLOCKED AND FLAT: nothing stands on it
 *
 * and after the rows, a line for every '#': "x y metatile".
 */
#if CTR_VOXEL_ENABLED
/* Is the cell's relief anything but level ground at its map's base? A map
 * read off its drawing writes every blocked cell, level or not: a building
 * nobody has modelled has a cell there, flat on the ground, and is not
 * relief. */
static bool Lifted(const VoxelMapInstance *inst, int x, int y)
{
    const int16_t *g = VoxelRelief_Cell(inst, x, y);

    for (unsigned i = 0; g != NULL && i < VOXEL_RELIEF_SIDE * VOXEL_RELIEF_SIDE; ++i)
        if (g[i] != 0)
            return true;
    return false;
}
#endif

static void Audit(const char *name)
{
#if CTR_VOXEL_ENABLED
    const VoxelMapInstance *inst = VoxelWorld_Instance(0);
    char path[160];
    FILE *file;

    snprintf(path, sizeof(path), "sdmc:/3ds/emerald3ds/shots/%s_audit.txt", name);
    file = fopen(path, "w");
    if (file == NULL || inst == NULL)
    {
        if (file != NULL)
            fclose(file);
    fclose(file);
        return;
    }
    fprintf(file, "map %d %d size %d %d indoor %d\n", inst->mapGroup, inst->mapNum,
            inst->width, inst->height, (int)inst->indoor);
    for (int pass = 0; pass < 2; ++pass)
        for (int y = inst->originY; y < inst->originY + inst->height; ++y)
        {
            for (int x = inst->originX; x < inst->originX + inst->width; ++x)
            {
                int metatile = VoxelWorld_GetMetatileId(x, y);
                VoxelVisualShape shape = VoxelWorld_ClassifyTile(x, y);
                char c = '.';

                if (shape == VOXEL_SHAPE_VOID) c = 'V';
                else if (VoxelBuildings_CellAt(inst, x, y, NULL, NULL)) c = 'M';
                else if (VoxelWorld_UsesTreeSprites(inst) && VoxelTree_PartIn(inst, metatile) >= 0) c = 'T';
                else if (VoxelSign_IsCell(inst, x, y)) c = 'S';
                else if (shape == VOXEL_SHAPE_WATER) c = 'W';
                else if (shape != VOXEL_SHAPE_FLAT && shape != VOXEL_SHAPE_DECAL) c = 'F';
                else if (Lifted(inst, x, y)) c = 'R';
                else if (VoxelWorld_GetCollision(x, y) != 0) c = '#';
                if (pass == 0)
                    fputc(c, file);
                else if (c == '#')
                    fprintf(file, "%d %d %03X\n", x - inst->originX, y - inst->originY, metatile);
            }
            if (pass == 0)
                fputc('\n', file);
        }
    fclose(file);
    /* and, beside it, the relief under every model's cell: where a model
     * stands and where its ground lies ("x y low centre high", in pixels) */
    snprintf(path, sizeof(path), "sdmc:/3ds/emerald3ds/shots/%s_models.txt", name);
    file = fopen(path, "w");
    if (file == NULL)
        return;
    for (int y = inst->originY; y < inst->originY + inst->height; ++y)
        for (int x = inst->originX; x < inst->originX + inst->width; ++x)
        {
            const int16_t *g = VoxelRelief_Cell(inst, x, y);
            int low, high;

            if (g == NULL || !VoxelBuildings_CellAt(inst, x, y, NULL, NULL))
                continue;
            low = high = g[0];
            for (unsigned k = 1; k < VOXEL_RELIEF_SIDE * VOXEL_RELIEF_SIDE; ++k)
            {
                if (g[k] < low) low = g[k];
                if (g[k] > high) high = g[k];
            }
            fprintf(file, "%d %d %d %d %d shape %d\n", x - inst->originX, y - inst->originY, low,
                    g[2 * VOXEL_RELIEF_SIDE + 2], high, (int)VoxelWorld_ClassifyTile(x, y));
        }
    fclose(file);
#else
    (void)name;
#endif
}

/*
 * What standing in a place costs. The display shows a frame every 16.7 ms or
 * waits for the next one, so the time between frames is what the player sees
 * (fps, and how many frames came late); the work in them is how near to that
 * edge a place is, and whose it is: the CPU's to compose the frame, or the
 * GPU's to draw it. The file is only written when the frames are over.
 */
static struct
{
    const char *name;
    unsigned frames, late;
    float frameMs, frameMax, workMs, workMax, cpuMs, gpuMs;
} sPerf;

static void PerfFrame(void)
{
    const CtrTiming *timing = CtrPlatform_GetTiming();
    const CtrVideoStats *video = CtrVideo_GetStats();

    ++sPerf.frames;
    sPerf.frameMs += timing->frameMs;
    sPerf.workMs += timing->workMs;
    sPerf.cpuMs += video->cpuMs;
    sPerf.gpuMs += video->gpuMs;
    if (timing->frameMs > sPerf.frameMax) sPerf.frameMax = timing->frameMs;
    if (timing->workMs > sPerf.workMax) sPerf.workMax = timing->workMs;
    if (timing->frameMs > 25.0f) ++sPerf.late;
}

static void PerfEnd(void)
{
    FILE *file = fopen(AUTOTEST_PERF, "a");
    float n = sPerf.frames ? (float)sPerf.frames : 1.0f;

    if (file != NULL)
    {
        fprintf(file, "%s %s voxel=%d frames=%u fps=%.2f frame=%.2f frameMax=%.2f late=%u "
                      "work=%.2f workMax=%.2f cpu=%.2f gpu=%.2f\n",
                AUTOTEST_BUILD, sPerf.name, (int)CtrSettings_Voxel(), sPerf.frames,
                sPerf.frameMs > 0.0f ? 1000.0f * n / sPerf.frameMs : 0.0f, sPerf.frameMs / n,
                sPerf.frameMax, sPerf.late, sPerf.workMs / n, sPerf.workMax,
                sPerf.cpuMs / n, sPerf.gpuMs / n);
        fclose(file);
    }
    memset(&sPerf, 0, sizeof(sPerf));
}

/* CB2_NewGame without the truck: the new save, and the field wherever the
 * first warp says. */
static void StartGame(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    StopMapMusic();
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    ResetSafariZoneFlag();
    NewGameInitData();
    ResetInitialPlayerAvatarState();
    PlayTimeCounter_Start();
    ScriptContext_Init();
    UnlockPlayerFieldControls();
    sStarted = true;
}

static void Warp(const AutotestLine *line)
{
    if (!sStarted)
        StartGame();
    SetWarpDestination(line->arg[0], line->arg[1], WARP_ID_NONE, line->arg[2], line->arg[3]);
    WarpIntoMap();
    gFieldCallback = NULL;
    gFieldCallback2 = NULL;
    SetMainCallback2(CB2_LoadMap);
}

void CtrAutotest_Frame(u32 frame)
{
    if (sState == 0 && frame >= AUTOTEST_FIRST_FRAME)
        Load();
    if (sState <= 0)
        return;
    if (sWait != 0)
    {
        if (sPerf.name != NULL)
        {
            PerfFrame();
            if (sWait == 1)
                PerfEnd();
        }
        --sWait;
        if (sWait == 0)
            gCtrAutotestButtons = 0;
        if (sState == 2 && CtrGame_IsOverworld() && !gPaletteFade.active)
        {
            sState = 1;
            sWait = 0;
        }
        if (sWait != 0)
            return;
        sState = 1;
    }
    while (sNext < sCount)
    {
        const AutotestLine *line = &sLines[sNext++];

        switch (line->op)
        {
        case OP_WARP:
            Warp(line);
            sState = 2;
            sWait = AUTOTEST_WARP_TIMEOUT;
            return;
        case OP_VOXEL:
            CtrSettings_SetVoxel(line->arg[0] != 0);
            break;
        case OP_FLASH:
            AnimateFlash(line->arg[0]);
            SetFlashLevel(line->arg[0]);
            break;
        case OP_WAIT:
            sWait = line->arg[0] > 0 ? (unsigned)line->arg[0] : 1;
            return;
        case OP_PERF:
            memset(&sPerf, 0, sizeof(sPerf));
            sPerf.name = line->name;
            sWait = line->arg[0] > 0 ? (unsigned)line->arg[0] : 1;
            return;
        case OP_SHOT:
            CtrCapture_Save(line->name);
            return;         /* a frame between captures */
        case OP_KEYS:
            gCtrAutotestButtons = (uint32_t)line->arg[0];
            sWait = line->arg[1] > 0 ? (unsigned)line->arg[1] : 1;
            return;
        case OP_BIKE:
            SetPlayerAvatarTransitionFlags(PLAYER_AVATAR_FLAG_MACH_BIKE);
            break;
        case OP_AUDIT:
            Audit(line->name);
            break;
        case OP_QUIT:
            sNext = sCount;
            break;
        }
    }
    {
        FILE *done = fopen(AUTOTEST_DONE, "w");

        if (done != NULL)
        {
            fprintf(done, "%u lines\n", sCount);
            fclose(done);
        }
    }
    CtrLog_Write(CTR_LOG_GAME, "autotest: done");
    sState = -1;
    CtrPlatform_Shutdown();
    exit(0);
}
