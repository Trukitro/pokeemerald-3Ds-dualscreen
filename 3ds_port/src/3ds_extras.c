/*
 * The optional settings of the ENHANCEMENTS and CHEATS pages of OPTIONS
 * (3ds_extras.h). Each feature adds its line to gCtrExtras and, for the game
 * code that reads it, a function below.
 */
#include <string.h>
#include "global.h"
#include "3ds_extras.h"
#include "3ds_platform.h"

const char *const gCtrExtrasOffOn[2] = {"OFF", "ON"};

const CtrExtra gCtrExtras[] =
{
    /* Features add their lines here. */
    {CTR_EXTRAS_CHEATS, "INSTANT VICTORY", "instant_victory", 2, 0, gCtrExtrasOffOn, NULL, NULL, NULL},
    {0},
};

/* The last line only keeps the array from being empty. */
const unsigned gCtrExtraCount = ARRAY_COUNT(gCtrExtras) - 1;

int CtrExtras_Value(const CtrExtra *extra)
{
    int value = CtrSettings_GetInt(extra->key, extra->fallback);

    return value >= 0 && value < extra->count ? value : extra->fallback;
}

/* One step either way, wrapping round like the game's options; an action
 * runs instead. */
void CtrExtras_Step(const CtrExtra *extra, int direction)
{
    if (extra->count == 0)
    {
        if (extra->act)
            extra->act();
        return;
    }
    CtrSettings_SetInt(extra->key, (CtrExtras_Value(extra) + (direction < 0 ? extra->count - 1 : 1)) % extra->count);
    if (extra->act)
        extra->act();
}

int CtrExtras_Get(const char *key)
{
    for (unsigned i = 0; i < gCtrExtraCount; ++i)
        if (strcmp(gCtrExtras[i].key, key) == 0)
            return CtrExtras_Value(&gCtrExtras[i]);
    return 0;
}

bool CtrExtras_PageUsed(unsigned page)
{
    for (unsigned i = 0; i < gCtrExtraCount; ++i)
        if (CTR_EXTRAS_TAB(gCtrExtras[i].page) == page)
            return true;
    return false;
}
