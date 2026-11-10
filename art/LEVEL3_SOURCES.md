# Level 3 source artwork

Generated with the built-in image generator against original emulator tile
layouts and approved Bad Dudes HD character references. Gameplay captures and
the source ROM are not distributed. The Python slicer fits these source
images into live tile mappings; it does not replace the scrolling game with
a static screenshot.

- `level3_sewer.png`: preserve the original horizontal bands and side-on
  silhouettes; chipped damp olive brick and plaster, rusty columns and pipes,
  emerald masonry, dark ribbed drain floor. Omit actors and HUD text.
- `level3_drains.png`: same materials, registered to the original ladder
  recess, circular drain outlet and slime flow; keep platform heights.
- `level3_broken_wall.png`: same materials and exact jagged masonry holes,
  exposed dark bricks, moss and black upper recess.
- `level3_lower_drains.png`: same materials with the low circular pipe flange,
  deep ladder shafts and original raised platform geometry.
- `level3_ninjas.png`: 3 columns, 2 rows; green upright, prone defeat, guard;
  red dagger attack, green disintegration, empty. Transparent cutouts,
  matching approved cloth, mask, boots and proportions. Second image-tool
  pass removes background glow while preserving the sprites.
- `player_level3_victory.png`: 2 columns, 1 row; original shaggy-haired hero
  and crewcut hero, narrow raised-left-fist victory pose with close-set boots,
  black tank top, gray cargo trousers, gloves. Transparent background.

The source images are retained at their generated resolution. Geometry
registration, crop coordinates, palette variants and tile context are in
`scripts/level3_art.py`, `scripts/actor_art.py` and `metadata/v6_actions.json`.
