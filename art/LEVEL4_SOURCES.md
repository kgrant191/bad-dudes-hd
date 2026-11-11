# Level 4 source artwork

Generated with the built-in image generator using original emulator tile
layouts as geometry guides and the approved painted arcade style. The source
ROM and movie are not distributed. Runtime tiles remain game-controlled.

Six background references retain the native tree, leaf, stone, platform and
negative-space geometry, with individual emerald leaves, mossy bark and warm
golden rocks. Actors and HUD lettering were omitted from these references:

| Artwork | Recorded frame | Feature |
| --- | ---: | --- |
| level4_forest.png | 300 | Main forest, grass and cliff materials |
| level4_ferns.png | 4620 | Fern wall and tall cut log |
| level4_tall_tree.png | 30 | Foreground trunk and broken branch |
| level4_lower_forest.png | 4980 | Lower tree and descending cliff |
| level4_cliff_edge.png | 750 | Alternate descending stone edge |
| level4_broken_stump.png | 6660 | Short jagged stump |

Transparent sprite atlases preserve the captured silhouettes, cell order,
side-view orientation and animation phases. No grid, labels or floor:

- `level4_boss.png`: 4 columns, 4 rows; 15 poses and last cell empty. Broad
  muscular mohawk fighter, rounded gunmetal shoulder armor, gray chest and
  leg guards, dark tactical cloth and mesh upper arms. Native sprite coverage
  can clip parts of kicks; those missing source tiles are not filled in.
- `level4_dogs.png`: 3 columns, 2 rows; upright alternating strides, extended
  leap and three gathered/running phases. Lean reddish-brown pointed-ear dog,
  pale muzzle and chest, detailed painted fur.
- `level4_fire.png`: 3 columns, 2 rows; three upright ignition phases and
  three running phases. Intact masked ninja surrounded by stylized warm
  orange/gold flame tongues, no injury detail.
- `level4_sword.png`: 3 columns, 1 row; gray kneeling ninja holding a vertical
  sword, diagonal sword and overhead horizontal sword, respectively.

The source images retain their generated resolution. Scene registration,
cell slicing, palette variants and pose context are in `level4_art.py`,
`actor_art.py` and `metadata/v7_actions.json`. The small gray ninja reuses the
approved `small_ninjas.png` poses with a uniform-only palette transformation.


## v0.7.1 recoil and scale correction

The six existing dog source cells are unchanged; the slicer uses one common
scale instead of independently stretching each frame to its native silhouette.
A new single-cell transparent `level4_dog_recoil.png` uses the native recoil
layout as the exact pose/orientation guide and `level4_dogs.png` as the identity
reference. Prompt: one complete lean reddish-brown pointed-ear dog recoiling
upward/backward, nearly upright, muzzle left and slightly upward, front paws
left, curving torso, hind paws pulled up, tail lower left; matching white muzzle,
chest and paws, illustrated arcade fur, no humanoid shape, injury, floor, glow,
labels or scene. Generated with the built-in image tool; original alpha retained.
