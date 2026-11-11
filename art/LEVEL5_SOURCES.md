# Level 5 source registration

Generated painted references preserve the recorded native geometry:
- level5_train.png: frame 300, steel/green freight car and canyon.
- level5_engine.png: frame 13410, emerald engine and roof vents.
- level5_freight.png: frame 10860, gold sliding doors and car transitions.
- level5_enemy_actions.png: four-by-two attack, flip and burning-recoil atlas.
- level5_boss.png: chain-claw boss atlas, explicit art_rect regions.

scripts/level5_art.py registers the scenery's horizontal boundaries before
slicing tiles. Native layout IDs/palettes are in metadata/level5_*.tiles.
Original sky cells expose the existing level2_sky.png. Runtime images are
compiled into pack/tiles.png; these source images are not required to play.

Earlier source artwork is unchanged. The returning minibosses use the
existing boss, boss_actions and level2_boss sheets with the new palette.
No ROM or movie is included in the repository or install ZIP.
