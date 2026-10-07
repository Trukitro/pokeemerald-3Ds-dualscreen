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
 *     wait FRAMES            let chunks build, animations run
 *     shot NAME              shots/NAME_top.bmp and shots/NAME_bottom.bmp
 *     quit                   write autotest.done and leave
 *
 * devtools/autotest.py writes the script from map names and reads the
 * captures back. An emulator is not the console: this is for seeing a change
 * and for comparing a sweep before and after it, not for accepting it.
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
#include "port_log.h"

#include "3ds_platform.h"

#define AUTOTEST_PATH "sdmc:/3ds/emerald3ds/autotest.txt"
#define AUTOTEST_DONE "sdmc:/3ds/emerald3ds/autotest.done"
#define AUTOTEST_LINES 600
/* The copyright screen has set the save blocks up by then. */
#define AUTOTEST_FIRST_FRAME 240
/* A warp that never reaches the field is skipped, not waited on for ever. */
#define AUTOTEST_WARP_TIMEOUT 900

enum { OP_WARP, OP_VOXEL, OP_WAIT, OP_SHOT, OP_QUIT };

typedef struct
{
    u8 op;
    s16 arg[4];
    char name[40];
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
        else if (!strcmp(op, "wait") && sscanf(text, "%*s %d", &a) == 1)
            line->op = OP_WAIT;
        else if (!strcmp(op, "shot") && sscanf(text, "%*s %39s", line->name) == 1)
            line->op = OP_SHOT;
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
        --sWait;
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
        case OP_WAIT:
            sWait = line->arg[0] > 0 ? (unsigned)line->arg[0] : 1;
            return;
        case OP_SHOT:
            CtrCapture_Save(line->name);
            return;         /* a frame between captures */
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
