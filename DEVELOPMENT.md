# Development checkpoint - v0.9.0

## Current checkpoint and branch workflow

v0.8.2 is approved and pushed to `develop` at
bf56adb886c0e2002c6e17e80ccbd6b693e69523 (user confirmed November 10, 2026).
v0.9.0 is the next local test build; its source bundle starts at that commit.
Do not push, merge, tag or release without approval. Keep `main` unchanged
until the full remake and final regressions are complete; then publish v1.0.0.
Historical entries below retain their original checkpoint status.

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

1. User-test v0.9.0, especially small-ninja size/animation and the cave boss.
2. Gather the next level and complete its new scenery/enemies.
3. Capture unrecorded moves, alternating two-player states and game over.
4. Assess the publisher splash, then run the final full-game regression.
5. After approval, merge develop to main and prepare the v1.0.0 release.

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


## v0.5.0 Level 2 and weapon coverage

Input: Bad Dudes (USA)(4).mmo, 8,850 inputs, beginning at Level 1's exit
message and covering the complete Level 2 truck stage, claw boss and exit.
The source recording and ROM stay outside the repository and install archive.

- Reuse all approved player/enemy/effect sources and retain their existing
  rule imagery. Add 15 layouts for each hero: dagger and nunchaku guards,
  standing/crouched attacks, overhead attacks and a two-arm victory pose.
  Both normal palettes and the shared warm palette retain hero identity.
- Add eight red-ninja running/guard layouts, seven small blue-ninja layouts
  and ten armored claw-boss layouts. Red-ninja layouts expand across the four
  known uniform colors; the new boss also has its grey damage-palette mapping.
- Weapon pickups use the existing dagger illustration and a new nunchaku
  illustration. Their normal/bright cycle keeps the same shape and alpha.
- The weapon layouts reuse unarmed body tiles. The context search includes
  the approved unarmed layouts and keeps their images as the defaults;
  weapon-specific neighbors select new crops. Old sources are not repainted.
- Level 2 has its own painted skyline, daytime sky, silver/emerald truck, cab
  and roadway. Scene RAM $02C0=1 plus the live HUD gate scopes these rules.
  A y<200 condition prevents scenery overrides from reaching the HUD.
  Identical source cells in banks 5 and 7 share artwork through exact
  pixel-pattern matching, covering the scrolling bank switches.
- The HUD panel now works in Level 2. Both 1P/2P labels remain gold.
- Native stage-message sprites contain an 8x16 cell with a previously blank
  upper half. The new live glyphs use both halves, a pale gold fill and dark
  outline, improving GO TO NEXT STAGE and STAGE 2 CLEAR without changing timing.

Validation: all 1,227 visible gameplay sprite tile/palette combinations in
the new movie have detailed mappings. Actual MesenCE replays cover the level
and its transitions. Earlier red-ninja and missed-super-punch clips are
pixel-identical to v0.4.2 across all 115 and 198 sampled frames respectively.
Only 24 previous rule images change, all the intentionally enlarged stage
message glyph halves; the other 7,414 previous mappings and all six previous
scene PNGs remain identical. Player 2 weapon rendering is additionally
checked by a documented palette-swap/hero-selector diagnostic, not a player-two movie.

Native sprite limits still apply: overlapping fighters can lose sprite rows.
Coverage counts establish mappings for recorded states, not every unrecorded
pose or alternating-two-player situation. Later levels still need recordings.
No push, merge, tag or release is part of this test-build preparation.

## v0.5.1 Truck wheels and cab stability

The user's three screenshots exposed two missed scrolling/animation cases.
The original game swaps the tire's upper-middle cell to blank CHR $700;
the generic black replacement erased the painted tread on that phase.
Separately, the frame-600 trailer reference contains cab-bank fragments
along scanline 96. Those fragments selected hedge crops for one cab bank,
while the other bank used the correct emerald metal from the cab reference.

- Select the cab reference for green cells before resolving exact CHR aliases.
  All 35 observed green bank-5/bank-7 pairs now have identical image bytes.
- Use the hub below blank $700 to select the missing tire crop. Other black
  cells retain their dark fallback. Register the 32 recorded wheel keys to
  a consistent trailer wheel, including fixed-bank right-edge cells.
- Use the green hood above each wheel column to select the cab's larger
  wheel and matching fender in both animation banks. This context remains
  local in X so it works when a wheel enters or leaves the screen.
- Restore the cab rear-panel and window blanks using their immediate
  right-hand neighbor plus tile-origin Y. No fixed screen-X rules are used.
- Reuse all existing source illustrations. All additions are gated by
  Level 2, the live HUD, and the stage area above the HUD.

Replay with tools/verify_v0.5.1.lua; compare the packaged v0.5.0 baseline
and the new capture using tools/check_v0.5.1.py. The coverage JSON records
image-byte comparisons independently of atlas offsets, cab bank parity,
HUD/upper-scene comparisons and consecutive-frame tire checks.

Final validation: complete 8,850-input MesenCE replay, 264 screenshots,
302 complete tire-tread checks across 71 consecutive frames, and 81 stable
cab frames. All 10,099 other rule images and all seven scene PNGs are
unchanged. The HUD and upper scene are pixel-identical at every sampled
frame. All 35 source-art files remain byte-identical to v0.5.0.

The patch is approved for develop and included in the v0.5.1 push bundle.
Main stays unchanged until the full remake and final testing are complete.


## v0.6.0 Level 3 and animation coverage

Input: Bad Dudes (USA)(5).mmo, 10,341 input frames. The movie starts at the
Level 2 exit and covers the full sewer stage, green ninja boss and Stage 3
Clear. An exploratory replay continued past the recording; coverage and final
validation stop at the input count. Do not claim Level 4 coverage.

- Six new source atlases/references preserve original geometry: four sewer
  scenes, five ninja layouts, and a two-cell hero victory sheet. Existing
  art files remain byte-identical. No ROM, movie or emulator is included.
- `level3_art.py` registers the four backgrounds to captured tile positions,
  slices all 212 observed bank-8 tile/palette keys and scopes them to scene
  RAM $02C0=2, the exact live HUD palette and y<200. There are no material
  fallbacks in the recorded Level 3 scenery.
- New HUD gate `hud3` recognizes D9A at (24,208), palette 0F001030. The
  earlier exact 0F001020 gate is retained. Do not ignore the HUD palette:
  doing so can expose artwork during black transition/fade states.
- `v6_actions.json` adds 17 actor/effect layouts. The green uniform palette
  FF0F351A reuses approved basic/specialist ninja artwork; additional CHR
  layouts reuse the matching full pose, preserving relative context checks.
- F80–F9F duplicate the earlier punch-effect bank. FA0/FA1 cover its sparkle;
  FA/FB ninja layouts reuse the approved guard and airborne ninja poses.
- New boss upright, guard, flat defeat and disappearing layouts, plus the
  red ninja dagger extension, are painted. FF303030 uses the new silhouette
  in near-white to retain the native appearance flash.
- Both heroes have the narrow raised-fist victory pose. `player2_cell`
  allows distinct hero cells in the same source sheet. Normal FF0F2620 and
  FF0F2820 and shared FF301638 preserve hero identity through the existing
  $023F selector. The Level 3 recording contains player 1 only.
- All 10,217 existing runtime rule images are byte-identical and present;
  all seven pre-existing scene/panel PNGs remain unchanged.
- Build: 6,982 source keys, 11,561 runtime rules, 7,847 unique atlas cells,
  42 player poses per hero, 144 additional actor/effect layouts.
- Sprite coverage: 1,411/1,411 observed visible gameplay keys, excluding
  intentional black fade states, empty source cells and stage-message glyphs
  (the latter use their existing live font mappings).
- `tools/verify_v0.6.0.lua` captures the full recording with dense checks at
  the dagger attack, boss appearance/sparkle and final defeat/victory.
  `validation/v0.6.0_validation.json` records completed regression results.

Continue with user feedback on v0.6.0, then Level 4 recordings. Unrecorded
moves, alternating two-player cases and later stages still require testing.


## v0.7.0 Level 4 forest and enemy coverage

Input: Bad Dudes (USA)(6).mmo, 9,360 input frames. Covers the forest, dogs,
flaming and sword ninjas, armored boss combat and defeat. Stop at the movie
input count; do not claim coverage of later levels or the following transition.

- Six painted environment references map 217 bank-9 tile/palette keys.
  213 keys are directly registered, one identical-pattern alias shares art,
  and three partial rock corners use matching material under native masks.
- All forest rules require scene RAM $02C0=3, the exact live HUD and y<200.
  `hud4` uses D9A at (24,208), palette 0F071727, with ignore-palette disabled.
  The player-label neighbor check uses the same exact palette. Blank $900
  cells are transparent in the HUD floor only.
- `v7_actions.json` contains 30 layouts: 15 armored-boss states, six dog
  phases, six flame phases, three kneeling sword phases. The sword layouts
  support all five known ninja uniform colors through existing recoloring.
- Level 4 reuses the small ninja tiles with FF0F3510. Extend the existing
  seven layouts to that palette and recolor only the blue uniform pixels.
- No new hero pose indices were observed. All 42 layouts per hero are
  retained. The movie records player 1; it does not verify two-player turns.
- The HUD font already supports the recorded stage-clear digit. Keep its
  tile-driven glyphs; do not bake text into the environment.
- All 11,561 old rule images remain present and byte-identical, independently
  of atlas placement. All seven prior non-atlas runtime PNGs and all earlier
  source artwork remain unchanged. Level 3 is replayed for regression checks.
- Build: 8,145 source keys, 13,225 tile rules, 9,280 unique atlas cells,
  42 poses per hero, 174 additional actor/effect layouts.
- Sprite coverage: 1,561/1,561 recorded visible gameplay tile/palette pairs,
  excluding empty source cells and stage-message glyphs (already mapped by
  the live font). Backgrounds: 217/217 replaced.
- `tools/verify_v0.7.0.lua` samples the full replay with dense flame, sword,
  gray ninja, boss kick, recoil and defeat checks. `validation/` contains
  coverage, source-art notes, capture logs and final regression results.

v0.6.0 is approved and pushed to develop. This v0.7.0 checkpoint awaits user
testing. Do not push or merge without approval; main stays unchanged until
final v1.0.0. Next: address Level 4 feedback, then the next level recording.


## v0.7.1 Dog scale and recoil correction

User screenshots exposed two issues in v0.7.0. The two standing dog poses had
native opaque bounds 100 versus 120 HD pixels wide; fitting each illustration
to that rectangle stretched the second body by 20 percent. `art_scale` now
keeps all six source cells at 0.34 pixels per source pixel. `art_anchor` holds
the two standing cells at the same position and baseline. Their silhouettes
can change slightly with leg/head movement without stretching the torso.
All seven dog layouts have zero painted pixels outside their native tile cells.

The twelve recoil tiles $150C-$1517 with palette FF0F0630 were already counted
as covered because `effects.png` cell 10 mapped them to a humanoid silhouette.
The original movie at frames 4082-4106 shows an upright recoiling dog. Exclude
that palette from the generic effect and add an explicit dog-only recoil pose
from `level4_dog_recoil.png`. Do not change the effect's other palettes.
Coverage checks must distinguish the correct actor artwork from any replacement.

`tools/verify_v0.7.1.lua` captures the complete 9,360-input movie with dense
sampling of both dog encounters. Validation compares non-dog pixels and all
non-dog rule images against v0.7.0, checks the recoil and both standing phases,
and retains the original game-state sequence. No other artwork is modified.

This build supersedes unapproved v0.7.0. Its source bundle starts at approved
v0.6.0 commit 4d33cb03b59f43b35f33fb7205a1eb7c2a22667f and includes both Level 4
commits. Await user testing before push; keep main unchanged.

Final v0.7.1 validation: 565 screenshots over the complete movie; 312 sampled
frames compared against v0.7.0, with no changed pixels outside dog sprite
cells. All 88 dog tile/palette keys select dog artwork, all seven layouts
fit their tile coverage, and 13,154 nonchanged rule images remain byte-identical.


## v0.7.2 Charge arc direction

User approved v0.7.1, then requested inward-facing semicircles before pushing.
Set the existing `flip_art` flag on all nine `effects.png` cell-9 layouts:
F00-F07, F40-F47 and the F80-F87 aliases. Mirror each full painted arc before
slicing; retain native per-tile mirroring so the pair forms `( hero )`.
This covers both characters' normal palettes and the shared warm flash.
No source illustrations are changed. Dog fixes and all other effects remain.

The bundle includes v0.7.0-v0.7.2 starting at approved/pushed v0.6.0 commit
4d33cb03b59f43b35f33fb7205a1eb7c2a22667f. Nothing has been pushed from here;
main remains unchanged. v0.7.1 approval is recorded; this small visual revision
is supplied for the user's final look before pushing.


## v0.8.0 Level 5 train and shared animation repairs

Input: Bad Dudes (USA)(7).mmo, 15,268 inputs. Scene RAM $02C0 is 3 for
206 frames, 4 for 14,763 frames and 5 for the final 299 frames. Scenery rules
require scene 4, the exact live HUD palette and y < 200. The Level 6 opening
is preserved but its scenery is not part of this pass.

Three registered source views (300, 10860, 13410) map the canyon, freight
cars and engine. All 588 observed background keys use painted references,
identical CHR-pattern aliases, costume/material color transforms or explicit
transparent sky cells. Reuse level2_sky.png rather than adding a duplicate.
Freight variants share one registered steel surface before color conversion,
so palette changes cannot splice a differently aligned door/rib reference.
Local body-row checks keep freight roofs/panels consistent during native
attribute swaps; adjacent canyon rock anchors fill ten blank shadow cases.
These extra rules are confined to the live Level 5 scene. The locomotive
keeps its own 0F0B1B2B background palette; it is excluded
from the freight recolor path so its painted panels cannot gain bright blocks.

v8_actions.json adds 20 actor/effect layouts: eight attack/acrobat/recoil
references, ten chain-claw boss/weapon references, a second burning recoil
layout and the visible boot as the boss falls offscreen. The chain's bank-1D
aliases are validated against byte-identical native pixels. Boss head tiles
use FF0F3606; body uses FF0F361C. `tile_palettes` binds each source tile to its
own palette while allowing its damage flash. `art_rect` supports the source
atlas's actual cell bounds without changing existing equal-grid sheets.

The train reuses earlier boss sprites with FF0F1C08. Permit that palette for
boss/boss_actions and the Level 2 boss. Retain skin/armor and recolor the
costume to olive brown. Shared new ninja moves cover the known uniform family;
the small ninja additionally retains FF0F3602. No hero frame was missing.

All 13,225 previous rule images remain byte-identical and no prior rule is
removed. The source illustrations for earlier levels are unchanged. Actual
Level 4 playback is compared against approved v0.7.2. The Level 5 movie is
replayed in full, with extra sampling around burning recoil, acrobat flips
and the chain-claw boss. See validation/v0.8.0_validation.json for results.

Captured visible boss poses are covered. Offscreen body positions and moves
absent from this input cannot be visually validated. Do not claim full-game
or alternating-two-player coverage. Next: user-test v0.8.0, then Level 6.


## v0.8.1 Chain-claw boss correction

The user's second boss movie, Bad Dudes (USA)(8).mmo (578 inputs), exposes
problems missed by v0.8.0: repeated chain cells contained cropped hands/claws,
and the full grounded defeat combined original tiles with an isolated HD boot.
Tile-key coverage alone did not establish correct assembled animation.

Replace the boot-only reference with all twelve cells of the grounded defeat,
19B4-19BF. level5_boss_defeated.png supplies a complete lying figure. Preserve
head/body palette separation and the existing damage-flash handling.

The chain link and claw patterns are identical across the 19A, 19E and 1D6
families. Slice one isolated painted weapon strip into a stable repeated link
and tip; do not select different pieces of whole fighter paintings for each
occurrence of a repeated link. Keep native mirroring, length and movement.
Fit the two forward-attack body references separately from the extending
chain, so chain length cannot compress the body or crop away the hand.
All other actor and scenery mappings must retain their v0.8.0 images.

Validation replays all 578 inputs with screenshots every frame, then the
complete preceding 15,268-input level recording. Inspect assembled boss
poses, including forward and overhead attacks, jumps, flashes and defeat;
compare non-boss rule images and game-state sequences against v0.8.0.
See validation/v0.8.1_validation.json for measured results and limits.

v0.8.1 supersedes the unapproved v0.8.0 build. Neither is pushed. The bundle
starts at approved/pushed v0.7.2 (6b7ada5e7e8419e57f1adb91d7154322227cbf51)
and includes both commits. Await the user's test before any push; main stays
unchanged. Level 6 scenery remains pending.


## v0.8.2 Stable green locomotive panels

User noticed excessive shaking during the boss. Comparing frames 6-374 of
Bad Dudes (USA)(8).mmo shows one native engine-body image but two HD images
alternating every two frames. The source game is not shaking those panels.

The engine's native 580-5FF / A00-A7F bank counterparts are byte-identical,
but generic pattern matching selected differently registered painted rows
for repeated native patterns. Resolve the explicit counterpart from the
13410 engine reference before generic matching. Restrict this to FF-less
background palette 0F0B1B2B and validate the native pixels before aliasing.
Fourteen aliases resolve to the original engine reference; seven replacement
images change. No actor, wheel, other palette or context rule changes.

Replay all 578 inputs with every-frame captures. Check the green body is
identical through the 369-frame fight interval, compare every other pixel
against v0.8.1, retain the same game-state sequence, and compare all rule
images. Two stage-clear screenshots lag the decoded video by one frame;
record those offsets and require an exact adjacent-frame match outside the
engine panel area. Combat frames need no alignment adjustment. The complete preceding level replay remains the v0.8.1 baseline;
this focused fix does not rerun that long recording. See v0.8.2_validation.json.

This supersedes unapproved v0.8.0/v0.8.1. The source bundle includes all three
commits from approved/pushed v0.7.2. Nothing is pushed; main stays unchanged.


## v0.9.0 Level 6 caves and small-ninja stability

Input: Bad Dudes (USA)(9).mmo, 12,331 inputs. Scene RAM $02C0 is 4 for
226 frames and 5 for 12,105 frames. Stop at the movie input count. This movie
contains the cave boss defeat and Stage 6 Clear, but not the next-level entry.

Five registered painted views cover the cave's rock, platforms, pillars,
stalagmites, depth wall and spikes. `level6_art.py` maps 209 bank-B background
keys; two partial cliff-edge cells retain native contours with an adjacent
painted limestone material. Every override requires scene 5, the exact HUD
palette 0F1C2C3B and y<200. `hud6` and `hud_player_label6` keep live gold player
labels and the common HUD panel without leaking into fades or prior levels.
Falling-stone F30-F33 sprite pairs have two painted fragment states.

The small ninja previously fit each pose independently to its native opaque
bounds. The shared head could scale differently when a leg extended or tucked.
All seven `small_ninjas.png` cells now use one `art_scale` of 0.46; fixed anchors
keep the standing baseline and jump transition consistent. The first pose's
native head/torso tiles are reused verbatim in the three layouts sharing them.
`share_native_tiles_from` acts on only the specified source/cell and common
native tile/palette pairs. It does not change other actors' slicing.

`small_ninja_actions.png` replaces the old larger bare-arm sai attack with the
same small full-sleeved ninja and adds airborne recoil tiles 15D6-15E5, missing
from prior movies. Its two cells share scale 0.22. Both blue and gray uniforms
are covered; the pre-existing attack palette family is retained. Uniform-only
recoloring preserves skin, boots and metal. Native flips and timing remain.

`v9_actions.json` adds twelve complete staff-boss poses, small-ninja recoil,
one dog leap and two falling-stone states. Two apparent boss layouts were
partial sprite-limit captures of existing full poses; use the full layouts
instead of fitting paintings to their cropped bounds. The dog leap reuses
`level4_dogs.png` cell 2 at the approved 0.34 scale. No new hero pose is needed.

Validation uses `tools/verify_v0.9.0.lua` to sample the whole new recording and
capture dense small-ninja, dog, boss kick/thrust/recoil/defeat sequences.
All 1,485 observed visible gameplay sprite keys have detailed mappings; counts
exclude native black fades, empty source cells and stage-message glyphs, whose
live-font mappings remain present. All 16,474 earlier rules remain. The only
changed earlier rule images belong to the intended small-ninja family.
Earlier scene PNGs and approved source illustrations remain byte-identical.
A complete Level 4 replay checks shared sprite changes against the prior pack.
Measured results, comparisons and limits are in `validation/v0.9.0_validation.json`.

Native sprite limits, offscreen clipping, gameplay timing and collisions remain
unchanged. Coverage does not establish unrecorded moves, alternating two-player
states, the next level or its entry transition. This checkpoint
awaits user testing and approval before push; main is unchanged.
