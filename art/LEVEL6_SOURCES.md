# Level 6 artwork sources

Generated with the built-in image tool from original emulator geometry guides.
The ROM and movie remain outside the repository and installation ZIP.
Registration, uniform recoloring, scaling and tile slicing are deterministic
build operations. Source images retain their generated alpha and resolution.

## Cave references

The common prompt was: repaint the exact NES cave layout as detailed painted
arcade scenery; preserve every platform edge, pillar, stalactite, rock cluster
and black opening. Use mossy emerald mineral rock, blue-gray limestone boulders
with turquoise edge light, dark teal rear walls and shaded mossy cones. Keep
orthographic side view, the original walkable heights and a solid black HUD
strip. No characters, text, grid or new scenery. Later references used
`level6_cave.png` or `level6_depths.png` as the painting/material reference.

| File | Geometry frame | Main feature |
| --- | ---: | --- |
| level6_cave.png | 300 | Main cave, left pillar, raised platform |
| level6_pillar.png | 1950 | Descending platform, right pillar, lower floor |
| level6_depths.png | 9960 | Dark rear wall and floor spikes |
| level6_ceiling.png | 7890 | Alternate upper rock mass and shallow floor |
| level6_rock_wall.png | 420 | Alternate upper green rock cells |

`level6_art.py` registers the generated horizontal bands to the native game
heights, then maps captured tile/palette pairs. Two partial cliff boundaries
reuse a painted limestone swatch under their native contours.

## Small ninja actions

`small_ninja_actions.png`: two equal columns, one row, transparent. Exact
native pose guide plus `small_ninjas.png` identity reference. Prompt: same
compact masked blue ninja, full sleeves, tied hood, dark gloves/boots and
consistent head/body scale. Left: planted side-on sai thrust to the right,
other arm at waist. Right: airborne recoil facing right, head upper-right,
chest arched, arm down-right, legs bent behind toward lower-left. Detailed
painted arcade shading, complete figures, no text/grid/floor/glow. Both cells
are blue; the game palette selects the gray and other existing uniform colors.

The original seven-pose source sheet is unchanged. Its fitting now uses one
shared scale with native head/torso tile reuse across the relevant poses.

## Staff fighter

`level6_boss.png`: four columns by four rows, fourteen painted source cells,
last two empty. Prompt: same lean muscular bald martial artist, green sleeveless
deep-V kung-fu vest and loose trousers, black sash and wraps, bare feet,
brown bo staff with metal ends. Match every captured pose and orientation:
three walking guards, diagonal-staff recoil, two lying defeats, four turning
phases, planted-staff side kick and three crouching/thrust phases. Consistent
painted arcade anatomy, transparent background, complete limbs/weapons, no
text/grid/shadows. Two source cells corresponded to incomplete captures of
full poses, so runtime uses twelve complete layouts rather than fitting art
to those partial rectangles.

## Falling stone

`level6_falling_stone.png`: two equal columns, transparent. Prompt: narrow
jagged blue-gray limestone shard pointing downward, followed by the same shard
broken into small separated angular fragments; cyan/white edge facets matching
the cave stalactites, tall narrow footprint, no glow or other objects.

The new dog leap reuses approved `level4_dogs.png` cell 2 at its existing scale.
No earlier source image was repainted or overwritten.
