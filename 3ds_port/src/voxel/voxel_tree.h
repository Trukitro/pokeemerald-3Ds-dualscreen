/* General tileset trees: ground trunk and a north-leaning cutout crown. */
#ifndef CTR_VOXEL_TREE_H
#define CTR_VOXEL_TREE_H

#include "voxel_mesh_builder.h"

/* The texture is twice as wide as it is tall (gen_voxel_trees.py). Every u
 * here is written in units of its left, square half - the drawn trees' - and
 * halved once the tree pass has run (ctr_voxel.c's TreeTexels): the right
 * half, u from 1 to 2, is the trees taken from the tilesets. */
#define VOXEL_TREE_TEXTURE_DIM 64u
#define VOXEL_TREE_TEXTURE_WIDTH 128u
#define VOXEL_TREE_TEXTURE_PATH "romfs:/voxel/trees.rgba5551"

/* A small tree is one cell: its trunk, with the whole crown standing on it. */
#define VOXEL_TREE_SMALL 4
/* The island's tree (Dewford's tileset): a small tree in its own drawing. */
#define VOXEL_TREE_ISLAND 5

/* General-only IDs: -1 for other art, the 2x2 quadrant (row*2+col) of a
 * large tree, or VOXEL_TREE_SMALL. */
int VoxelTree_Part(int metatileId);
/* Remove the old canopy from the cell above a tree, leaving its ground. */
int VoxelTree_GroundMetatile(int metatileId);
/* The same two for a cell of `inst`, whose secondary tileset may have trees
 * of its own (VoxelWorld_IslandTrees): these are what the passes ask. */
int VoxelTree_PartIn(const VoxelMapInstance *inst, int metatileId);
int VoxelTree_GroundIn(const VoxelMapInstance *inst, int metatileId);

/* Rows of tufts that stand on a cell of grass (VoxelWorld_Grass). */
#define VOXEL_GRASS_TUFT_ROWS 2

/* Appended after the ordinary terrain; these vertices use the tree texture. */
void VoxelTree_EmitInstance(VoxelBuilder *builder, const VoxelMapInstance *inst,
                            int x0, int y0, int x1, int y1);
void VoxelTree_EmitBorder(VoxelBuilder *builder, int x0, int y0, int x1, int y1);

#endif
