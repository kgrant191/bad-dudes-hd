# Development checkpoint - v0.4.2

## Approved checkpoint and branch workflow

v0.4.1 was approved after the red-ninja falling-pose fix. The Git bundle
places the complete project on `develop`, directly after the repository's
existing main commit 586f6b869d01371472cb10eaebcb9df69d0ef1b0. It includes
the existing commit, so it can be cloned independently without prerequisites.
The bundle is prepared for the user to push; preparation does not push it.

Continue approved checkpoints on `develop`. Keep `main` unchanged until all
planned stages and final regression checks are complete. At that point merge
to `main`, tag v1.0.0 and publish the install ZIP as the release asset.

## Inputs and replay

- Original input: Bad Dudes (USA).nes, supplied inside Bad Dudes (USA).zip.
- User movie: Bad Dudes (USA).mmo, Mesen 2.2.1 movie format 3, 8,477 inputs.
- Whole-ROM SHA1: 26E184E350F50BFA06038379A84F3B685B7509B8.
- Whole-file CRC32: ADA49341; PRG+CHR CRC32: 161D717B; mapper 4.
- Pinned native emulator: nesdev-org/MesenCE tag 2.2.1, source commit 20ba206.
- Movie includes a starting state. Metadata frame numbers count from replay
  start; the game's native frame counter starts about 25 frames later.
- Reference frames: 600 title pose 1; 720 title/menu pose 2; 840 selection;
  1800 typing briefing; 3000 street; 3840 truck; 5760 boss area; 6240 boss;
  8160 Stage Clear (score 14300).

## Build

The ready-made pack is already included. To regenerate it, install Python 3,
Pillow, NumPy and SciPy. Supply the original ROM and a native xBRZ wrapper:

```sh
export BAD_DUDES_ROM='/absolute/path/Bad Dudes (USA).nes'
export BAD_DUDES_XBRZ_LIBRARY='/absolute/path/scale.so'
python scripts/build.py
```

Pass `--previews /absolute/path/previews` for optional offline layout previews.
These are not a substitute for emulator playback: sprite priority, scanline
limits and transitions must be checked in Mesen.

`tools/scale.cpp` exposes MesenCE's bundled xBRZ scaler. On Linux, with the
matching MesenCE source and extracted MesenCore.so, build it using:

```sh
g++ -shared -fPIC -O2 -I"$MESEN_SOURCE" tools/scale.cpp \
  "$MESEN_CORE" -Wl,-rpath,"$(dirname "$MESEN_CORE")" -o scale.so
```

The wrapper source is provided; compiled binaries and emulator dependencies
are deliberately excluded. MesenCE's upstream license applies to its code.
Repository: https://github.com/kgrant191/bad-dudes-hd.
GitHub main currently contains the initial project README. This checkpoint
contains the complete baseline and new player work; it has not been pushed.

## Art and mapping choices

- All 3,268 captured tile/palette keys have a baseline rule in v0.3.0.
- Conditions and per-scene overrides appear before baseline tile rules.
- Atlas tiles are 32 x 32 pixels at scale 4; tile coordinates use image pixels.
- Title tile FD at screen 0,0 selects pose 1; 1FD selects pose 2.
- Title figures originally mix background tiles and sprites. Full background
  composites at priority 20 replace both halves; bank 1E character sprites
  are hidden during title screens. Menu sprites remain live.
- Selection uses tile 400 and exact palette 0F172737 at 0,0. Bank 4 names and
  selection markers remain live with transparent fill; portrait pieces hide.
- Briefing uses tile DF1 at 0,0. D00-D3F preserve white letter pixels (index 3)
  over new artwork. Remaining briefing pieces and bank 1E portrait hide.
- Gameplay scene byte is RAM $02C0 = 0. A low-priority sky sits behind the
  transparent sky tiles. Other observed values: 7 splash, 8 title pose 1,
  9 title pose 2, 13 selection, 10 briefing. Rendered tile conditions are used
  for intro screens because the scene byte can advance before the screen.
- Environment tiles in banks 5, 6, 7 use painted reference crops where seen.
  Other variants use material masks. Preserve the truck's opaque dark aperture.
- Sky tiles 64F, 65F, 670 become transparent; partial building-edge masks
  on 607, 608, 660, 661, 665, 666, 676 expose one continuous sunset.
- Avoid replacing whole backgrounds for the scrolling stage: geometry, truck
  wheels, scrolling and original occlusion need to stay connected to the game.
- Preserve every player/enemy animation and damage palette when redrawing.
  Player tiles mostly bank 10/11, enemies 12-1C, boss 16. Reuse across scenes
  means bank identity alone is insufficient for unconditional replacements.

## Capture helpers

The native tools are developer utilities pinned to the MesenCE 2.2.1 ABI,
not an emulator distribution. `capture.cpp` runs a ROM and movie through the
exported core. Arguments: HOME ROM MMO LUA RAW_PACK_OR_DASH. A final `-`
uses an installed pack; a directory records the original tile/palette keys.

For metadata access, the source copy of Core/NES/HdPacks/HdNesPpu.h needs
`public:` immediately after the opening class brace. This changes access
control only. The matching compiled core remains unchanged. The helper
includes Core, Utilities and repository-root headers and links MesenCore.so.

Set BAD_DUDES_HOME, BAD_DUDES_CAPTURE_DIR and BAD_DUDES_METADATA_DIR to absolute
directories before replay. Delete HOME/done first. Set SKIP_METADATA=1 for
ordinary screenshot verification. Capture scripts allow file IO in Mesen.
Use a separate output directory for original and HD screenshots.

## Next art pass

1. User-test v0.4.1 in normal play, including both characters and item flashes.
2. Capture unrecorded moves, alternating two-player states and game over.
3. Gather Level 2 and later recordings before adding their art.
4. Replace the publisher splash and assess any unrecorded menu states.

The current title shows its new logo throughout both title poses; the original
logo arrival timing is not reproduced. Scenery still retains the original NES
silhouettes and repeated tile structure. This is a test build, not a complete
HD remake or a full-game release.

## v0.1.1 font correction

Briefing tiles D1E (T) and D23 (Y) now use matching 28-pixel cap widths and
8-pixel stems. The other glyphs and typewriter timing are unchanged. The
correction is conditional on the briefing screen and applies to all captured
briefing palettes. Replayed through frame 2420 with no loader errors.

## v0.2.0 player pass

- `art/player_sheet_main.png` and `art/player_sheet_extra.png` hold 20 painted
  poses generated against the original sprite layouts and approved title hero.
- `metadata/player_poses.json` retains their source tile arrangements and
  representative movie frames. Mirrored poses reuse the corresponding artwork.
- `scripts/player_art.py` anchors each cell to its original sprite bounds and
  slices it into 32-pixel HD tiles. The ROM, gameplay, timing and collision
  logic are unchanged.
- 310 distinct player tile indices observed during gameplay receive detailed
  art for the normal FF0F2620 and warm-flash FF301638 palettes. Unobserved
  player tiles and other palettes retain their existing baseline rules.
- Shared tiles use 24 sprite-relative conditions (48 palette-specific rules)
  to keep pose-specific crops together. Other tiles retain ordinary cached
  matching. Shortest distinguishing neighbor offsets are preferred.
- The source illustrations, selection, briefing background, sky and both
  title composites remain byte-for-byte identical to v0.1.1.
- Final verification uses the supplied 8,477-input movie through frame 8,500,
  including intro typing, combat, truck, boss and Stage Clear (score 14300).
- This pass covers the recorded player. It is not a claim of complete Blade
  and Striker/two-player coverage or all possible moves.

## v0.3.0 recorded Level 1 completion

Additional input: Bad Dudes (USA)_2.mmo, 1,442 inputs, starting mid-stage.
The original 8,477-input movie was replayed through frame 8,500.

- Six additional player layouts cover upward punch, two kick transitions,
  prone knockdown, bent-forward hurt and victory cheer. Hurt/victory tiles
  live in bank 1C, outside the original player's bank 10/11 filter.
- `actor_art.py` slices 78 new layouts: six player, 46 enemy/boss and 26
  effect layouts. Reused tiles use 125 palette-specific local context rules.
- Enemy recolors preserve the game's blue, red, grey and teal palette variants.
- `hud_art.py` draws live glyphs and health segments. The bundled DejaVu Sans
  Mono font and license make this step portable. Scores/timers are never static
  image text. Sprite font tiles matching the HUD glyph shapes share the font.
- The HUD background uses priority 11, separate from the sky at priority 10.
  Mesen selects only one matching background at a given priority.
- Gameplay sky now requires both scene RAM $02C0=0 and the rendered HUD's P
  tile D9A at (24,208), exact palette 0F001020. The scene byte switches early.
  v0.2.0 showed sky at replay frames 2356-2361 and 2430-2437; the new gate
  removes these flashes. Black transition/interstitial behavior remains native.
- Added observed tile/palette keys from both captures in additional_keys.json.
  Visible gameplay sprite coverage: original movie 1,236/1,236 keys; new clip
  613/613 keys. This checks recorded keys, not every possible game state.
- Source sheets may contain small fragments at generated cell boundaries.
  The slicer ignores detached components below 1.2% of the main cell component
  before fitting its bounds to the original sprite-cell coverage.
- Raw recordings, original ROM and compiled emulator tools remain outside
  this checkpoint. No GitHub push or merge has been performed.

For a new capture, `tools/capture_all.cpp` accepts the same arguments as the
original capture helper. Set BAD_DUDES_TILE_CSV to its output CSV path;
background entries are sampled every 30 frames and sprites every frame.
`tools/verify_v0.3.0.lua` uses BAD_DUDES_HOME, BAD_DUDES_CAPTURE_DIR and
BAD_DUDES_FRAMES. Set SKIP_METADATA=1 for screenshot-only checks. Remove the
profile's `done` file before each replay. Reuse the pinned core and headers.


## v0.4.0 player 2 and additional combat coverage

Additional input: Bad Dudes (USA)(2).mmo, 5,617 inputs. This recording chooses
the second hero, adds sword attacks, a crouched ninja punch and four boss poses.

- Both heroes have 26 painted layouts. Normal player palettes are FF0F2620
  (first hero) and FF0F2820 (second hero). The four `player2_*.png` source
  sheets match the short-haired selection portrait and existing pose layouts.
- The shared warm palette FF301638 retains the selected identity. USA ROM CPU
  $C7E4-$C80F chooses the palette table using RAM $023F: bit 0 normally, or
  bit 1 when ($023F & $C0) == $C0. The pack mirrors these masked conditions.
  Captured one-player snapshots verified $00 for hero 1 and $01 for hero 2.
  The alternating two-player branch follows the ROM but lacks movie coverage.
- `metadata/v4_actions.json` adds seven captured layouts: three sword/ninja
  attacks and four boss punch/tumble phases. `actor_art.py` now handles 85
  extra actor/effect layouts, in addition to the original 20 hero layouts.
- Clock tiles F34-F37 and energy-can tiles F22-F23 explicitly cover all three
  normal/warm palettes. Normal art is identical for both heroes. The warm
  phase uses RGB * 0.65 + white * 0.35, preserving alpha byte-for-byte.
  Existing effect art used the warm source palette; an early return previously
  bypassed brightness changes, and the new hero palette lacked mappings.
- 4,212 source tile/palette keys compile into 6,485 runtime rules and 4,222
  unique atlas tiles. All observed visible gameplay sprite keys have detailed
  art: original movie 1,236/1,236; short player 1 clip 613/613; player 2 clip
  1,068/1,068. These counts establish recorded tile coverage, not all moves.
- Actual emulator captures verify the clock's normal/bright cycle, sword
  attacks, crouched punch, both boss punches/tumbles, player 2 hurt/knockdown,
  and the earlier player 1 recording through Stage Clear and Next Stage.
- Title, selection, briefing, sky and HUD PNGs are byte-identical to v0.3.0.
  The previous stage-entry gate remains unchanged. VERSION is now 0.4.0.
- `tools/verify_v0.4.0.lua` captures new-pose and pickup-cycle checkpoints;
  the prior verification script covers player 1 and stage entry. Results and
  review screenshots are included under `validation/`.
- No ROM, raw movie, emulator binary or native build library is distributed.
  This checkpoint has not been pushed to GitHub.

Native sprite limits are retained. The extended boss punch can lose the top
fist row when overlapping the jumping hero (new clip, frame 4701). A separate
original-game replay confirms the same scanline clipping. This is not an HD
fallback; do not compensate with another pose's tiles.


## v0.4.1 red ninja falling-pose fix

Additional input: Bad Dudes (USA)(3).mmo, 712 inputs. The red ninja dropping
from the upper walkway at capture frames 291-326 used original tiles
1230-123F with palette FF0F3516. The pose was already painted in
`ninjas_a.png`, cell 6, but its red palette had never been captured.

- Added the 16 observed tile/palette keys to `additional_keys.json`.
- `build.py` now expands the existing basic-ninja pose keys across the four
  known uniform palettes FF0F3512/FF0F3516/FF0F3510/FF0F351C. This includes
  `ninjas_a.png`, `ninjas_b.png` and the crouched punch in `enemy_actions.png`
  cell 2. No artwork regeneration or animation/ROM change was needed.
- 4,939 source keys, 7,296 tile rules and 4,831 unique atlas cells.
- Replayed the complete new clip in MesenCE, with screenshots every six
  frames. All 350 observed visible gameplay sprite keys have detailed art.
  Inspected the fall at frames 294, 300, 312 and 324, including its landing.
- Compared the actual image bytes for every prior rule against the packaged
  v0.4.0 atlas: all 6,485 existing mappings remain identical. All six scene
  PNGs also remain byte-identical. The atlas was repacked with extra colors.
- `validation/v0.4.1_fall_comparison.png` contains original v0.4.0 captures
  above and fixed v0.4.1 captures below. No HD pack loader errors occurred.
- The source checkpoint remains unpushed. Later stages and unrecorded
  layouts retain the previously documented testing limits.


## v0.4.2 super-punch palette phases and gold player labels

Additional inputs: `1.mmo` (690 frames) and `2.mmo` (1,190 frames), same USA ROM.
The first clip's red ninja is already fully covered by v0.4.1's uniform-family
expansion: every gameplay pixel above the HUD in the new replay is identical
to v0.4.1, including the red ninja jump and hurt sequence.

The second clip exposed 18 missing player-2 effect palette keys: F00-F05,
F12-F1D with FF0F2820. Existing effect sheets already contained these layouts.
`build.py` now expands all hero effect poses across FF0F2620/FF0F2820/FF301638,
covering charge, release and dissipation even when a super punch misses.
This adds 136 possible effect palette keys, including the 18 newly observed.

`hud_tile(t, gold=True)` uses the existing letter gradient for digit glyphs.
Only digits D81/D82 with a neighboring P tile D9A eight pixels to their right,
below y=200, on the live HUD receive this variant. Both player labels qualify;
scores, time and lives keep their original numeric styling. The HUD panel,
font outlines, gameplay logic and animation timing are unchanged.

Validation: both complete clips replayed with screenshots every six frames,
no loader errors. All 7,296 previous rule images and six scene PNGs are
byte-identical to v0.4.1; only new contextual HUD rules change existing labels.
Coverage is recorded in `validation/v0.4.2_coverage.json`. The diagnostic Lua
changes only nametable label digits from 1 to 2, validating actual Mesen
rendering of gold 2P without claiming a two-player gameplay replay.

The user's selected HUD crop was edited with the built-in image tool as a
visual reference (`art/hud_label_reference.png`). Runtime HUD lettering stays
live and is built by code; it does not use a static screenshot overlay.

This checkpoint is prepared for user testing on develop. It has not been
pushed, merged, or released. The approved remote baseline remains v0.4.1.
