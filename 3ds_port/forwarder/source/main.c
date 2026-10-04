// HOME Menu forwarder for Pokémon Emerald 3Ds Dual Screen.
//
// Installed once as a CIA, it starts sdmc:/3ds/emerald3ds/Emerald3DS.3dsx, so
// updating the game only ever replaces the 3DSX. It asks Luma3DS's hb:ldr to
// load that file and jumps to the title Luma loads 3DSX files through (the
// Homebrew Launcher title, or whatever title Rosalina was switched to).

#include <3ds.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

#define TARGET_SD_PATH "/3ds/emerald3ds/Emerald3DS.3dsx"
#define TARGET_ARGV0   "sdmc:" TARGET_SD_PATH

// Luma3DS shared config page (private layout, stable since v10).
typedef struct {
    u64 hbldr3dsxTid;
    u64 selectedHbldr3dsxTid;
    bool useHbldr;
} LumaSharedConfig;
#define LUMA_SHARED_CONFIG ((volatile LumaSharedConfig *)(OS_SHAREDCFG_VADDR + 0x800))

// hb:ldr reads whole fixed-size buffers, whatever size is declared.
static char sTarget[0x400] __attribute__((aligned(4)));
static u32 sArgv[0x400 / 4];

static Result HbldrSetTarget(Handle h, const char *path)
{
    u32 *cmd = getThreadCommandBuffer();
    strncpy(sTarget, path, sizeof(sTarget) - 1);
    cmd[0] = IPC_MakeHeader(2, 0, 2);
    cmd[1] = IPC_Desc_StaticBuffer(strlen(sTarget) + 1, 0);
    cmd[2] = (u32)sTarget;
    Result res = svcSendSyncRequest(h);
    return R_FAILED(res) ? res : (Result)cmd[1];
}

static Result HbldrSetArgv(Handle h, const char *argv0)
{
    u32 *cmd = getThreadCommandBuffer();
    sArgv[0] = 1;
    strncpy((char *)&sArgv[1], argv0, sizeof(sArgv) - 5);
    cmd[0] = IPC_MakeHeader(3, 0, 2);
    cmd[1] = IPC_Desc_StaticBuffer(sizeof(sArgv), 1);
    cmd[2] = (u32)sArgv;
    Result res = svcSendSyncRequest(h);
    return R_FAILED(res) ? res : (Result)cmd[1];
}

static bool IsLuma(void)
{
    s64 version;
    return R_SUCCEEDED(svcGetSystemInfo(&version, 0x10000, 0));
}

static Result Forward(const char **why)
{
    struct stat st;
    if (stat(TARGET_ARGV0, &st) != 0)
    {
        *why = "The game is not on the SD card.\n\n"
               "Copy the 3ds folder of your installation ZIP\n"
               "to the root of the SD card, so that this file\n"
               "exists:\n\n  " TARGET_ARGV0;
        return -1;
    }
    if (!IsLuma() || !LUMA_SHARED_CONFIG->useHbldr)
    {
        *why = "This shortcut needs Luma3DS.\n\n"
               "Start the game from the Homebrew Launcher.";
        return -1;
    }

    Handle hbldr;
    Result res = srvGetServiceHandle(&hbldr, "hb:ldr");
    if (R_SUCCEEDED(res))
    {
        res = HbldrSetTarget(hbldr, TARGET_SD_PATH);
        if (R_SUCCEEDED(res))
            res = HbldrSetArgv(hbldr, TARGET_ARGV0);
        svcCloseHandle(hbldr);
    }
    if (R_FAILED(res))
    {
        *why = "Luma3DS refused to load the game (hb:ldr).\n\n"
               "Update Luma3DS, or start the game from the\n"
               "Homebrew Launcher.";
        return res;
    }

    // System titles (Download Play) live in NAND, the Homebrew Launcher on SD.
    u64 tid = LUMA_SHARED_CONFIG->hbldr3dsxTid;
    FS_MediaType media = ((tid >> 32) & 0x10) ? MEDIATYPE_NAND : MEDIATYPE_SD;
    res = APT_PrepareToDoApplicationJump(0, tid, media);
    if (R_SUCCEEDED(res))
        res = APT_DoApplicationJump(NULL, 0, NULL);
    if (R_FAILED(res))
        *why = "Could not start the Homebrew Launcher title\n"
               "Luma3DS uses to load homebrew.\n\n"
               "Start the game from the Homebrew Launcher.";
    return res;
}

int main(void)
{
    gfxInitDefault();
    const char *why = NULL;
    Result res = Forward(&why);

    if (R_SUCCEEDED(res))
    {
        while (aptMainLoop())
            svcSleepThread(10 * 1000 * 1000);
    }
    else
    {
        consoleInit(GFX_TOP, NULL);
        printf("\n Pokemon Emerald 3Ds Dual Screen\n\n");
        printf(" %s\n", why);
        if (res != -1)
            printf("\n Error 0x%08lX\n", (unsigned long)res);
        printf("\n\n Press START to exit.\n");
        while (aptMainLoop())
        {
            hidScanInput();
            if (hidKeysDown() & KEY_START)
                break;
            gfxFlushBuffers();
            gfxSwapBuffers();
            gspWaitForVBlank();
        }
    }
    gfxExit();
    return 0;
}
