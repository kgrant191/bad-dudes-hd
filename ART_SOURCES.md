# Player artwork provenance - v0.2.0

The two new sprite sheets were created with the built-in image-generation
tool from the original ROM pose layouts and the approved title-character
illustration. Layout extraction, bounding-box alignment, tile slicing and
palette flashes are deterministic build operations in `scripts/player_art.py`.

## Main sheet prompt

Style transfer for a production Bad Dudes HD game sprite sheet. The first
reference is the exact 4-by-4 pose and placement template; the second is the
approved title hero. Redraw all sixteen fighters as the same muscular,
brown-haired man in a black sleeveless tank top, gray cargo trousers, black
fingerless gloves and black boots. Use detailed hand-painted 1990s arcade
shading, tan skin, modeled muscles, dark hair, visible jaw and eyes, crisp
outlines, cloth folds and a black belt. Preserve each original pose, facing,
silhouette, size and position, including the subtle walk differences,
extended attacks and upside-down tumble. Keep the blank cell gaps. Use a
transparent background with no text, labels, grids, floor shadows or extra
sprites. Preserve the layout for slicing into game tiles.

## Extra sheet prompt

Use the original 2-by-2 pose guide as the edit target and the finished main
sheet as the character and painting reference. Preserve four poses: a low
crouched sweep to the right, an airborne side kick to the left, a crouched
landing reaching down, and a compact forward-curled hurt/tumble pose. Keep
the same tan muscular hero, dark brown hair, black tank top, gloves and
boots, gray cargo trousers, strong outlines and dimensional shading.
Preserve orientation, placement and limb arrangements. Use transparent
alpha with no text, grids, floor shadows or additional figures.

## Validation

The generated images are source assets rather than direct emulator output.
The ready-to-install pack contains their sliced tile atlas. Captures under
`validation/` are actual MesenCE output. The supplied recording covers the
recorded player only; it does not establish all alternate-player or
two-player states.


# Additional artwork provenance - v0.3.0

All seven additional painted sheets below were made with the built-in image
creation tool. ROM-derived pose guides supplied geometry and orientation;
`player_sheet_main.png` supplied the established hero identity. The source
images remain in `art/`; they are compiled into the one runtime tile atlas.

- `player_sheet_missing.png`: 3 columns by 2 rows, four hero poses: prone
  knockdown, overhead punch, high kick, and knee-up kick preparation. Black
  tank, grey combat trousers, brown hair and black boots. A second cutout pass
  removed the initial white backdrop. The slicer mirrors the last cell to
  match its reference direction.
- `player_hit.png`: 2 columns by 1 row, victory cheer with one bent arm overhead
  and a forward-bent hurt reaction, preserving the established hero costume.
- `ninjas_a.png`: 4 columns by 3 rows, six running gait frames, overhead lunges,
  recoil, crouch and punch; blue uniforms with grey and red reference variants.
- `ninjas_b.png`: 3 columns by 3 rows, throw windup, high kick, knee lift,
  horizontal aerial kick, punch, hurt crouch, guard, middle kick, low guard.
- `boss.png`: 4 columns by 3 rows, eleven Karnov poses and one empty cell:
  walking, overhead fists, two guard gaits, recoil, crossed fists, two prone
  defeats, left high kick, kneeling and seated defeat. Stocky bare-chested
  moustached man, red trousers, brown boots and metal wrist cuffs.
- `specialists.png`: 4 columns by 4 rows, fourteen figures: teal masked sword
  fighter walking and aerial poses, plus the red-clad ponytailed woman fighter's
  standing, walking, tuck, guard and recoil poses. Two cells remain empty.
- `effects.png`: 4 columns by 3 rows, brass stopwatch; red energy can; silver
  three-point star; yellow and orange impact sparks; fireball; horizontal
  flame breath; expanding fire ring; explosion; curved flame streak; dissolving
  ninja smoke; silver dagger. The last dagger cell is not currently mapped.

All prompts requested detailed hand-painted arcade remaster styling, exact
reference poses, equal cells, transparent alpha, no labels, grid lines or
background scenery. The compilation code fits source alpha bounds to the
original sprite bounds, slices only the game's existing cells, applies ROM
palette variants and uses nearby-tile rules for shared pieces. This does not
alter the original animation, collision or gameplay logic.

The live HUD is code-drawn text and geometric UI, using the included DejaVu
Sans Mono Bold font under its bundled license. Runtime verification images
are actual MesenCE captures; `actors_review.png` is a build-time slicing review.

# Additional artwork provenance - v0.4.0

Six new source sheets were generated with the built-in image tool. Each uses
transparent alpha and the established painted arcade style. They are included
in `art/`; deterministic bounding-box fitting, palette conversion and tile
slicing compile them into the runtime atlas.

## Player 2 prompt set

The edit target for each sheet was its existing player 1 counterpart; the
right-hand selection portrait was the identity reference. Preserve every pose,
limb arrangement, direction, cell layout, costume and occupied proportions.
Replace the hero identity with the short upright dark-brown crewcut, squared
jaw and face of the right-hand portrait. Keep the black tank, grey cargo
trousers, black gloves and boots, tan skin and muscular build. Detailed painted
arcade shading, crisp outlines, no grid, text, scene, floor shadow or glow;
true transparent alpha. The four targets were:

- `player2_main.png`: 4 x 4, sixteen poses matching `player_sheet_main.png`.
- `player2_extra.png`: 2 x 2, crouched sweep, aerial kick, landing and tumble.
- `player2_missing.png`: 3 x 2, prone, upward punch, high kick, kick preparation;
  last two cells empty. The build mirrors cell 3 like its player 1 counterpart.
- `player2_hit.png`: 2 x 1, victory and bent-forward hurt reaction.

## Additional enemy prompt

Use the ROM-derived 2 x 2 guide for exact poses and `specialists.png` for
character and style. Top left: teal masked swordsman thrusting a long silver
sword horizontally right at shoulder height. Top right: same swordsman with
both arms raised and the sword held horizontally overhead, tip pointing left.
Bottom left: grey masked sleeveless ninja crouched low, punching right.
Bottom right empty. Keep exact side view, direction, silhouette and cell
positions. Detailed painted arcade realism, dark trousers, metal shin wraps,
crisp outlines. No idle substitutions, floor, glow, labels or frames; genuine
transparent background. Saved as `art/enemy_actions.png`.

## Additional boss prompt

Use the ROM-derived 2 x 2 guide for exact pose and layout, and `boss.png` for
the bulky bald moustached strongman with a large belly, red trousers, metal
wristbands and brown boots. Top left: upright shoulder-height punch right.
Top right: distinct forward-leaning punch right, other arm raised back.
Bottom left: upside-down airborne tumble, head lower left and bent red legs
above/right. Bottom right: compact curled diagonal tumble, red legs upper
left and bald head lower right. Preserve full silhouettes and relative
proportions. Detailed painted arcade realism, crisp outlines and wide cell
gaps; no glow, aura, floor, labels or frames; true transparent background.
Saved as `art/boss_actions.png`.

The pickup flash is a runtime color transform of the existing art, preserving
alpha and silhouette exactly. No new pickup illustration was required.


# HUD label reference - v0.4.2

`art/hud_label_reference.png` was generated with the built-in image tool from
the exact HUD screenshot selected by the user. Prompt: change only the numeral
1 in both visible 1P labels from grey to the metallic gold gradient of the P;
keep both labels reading 1P, preserve all other text, colors, health bars,
positions, panel and composition. Keep scores, time and lives grey. The output
is a visual reference, not a runtime HUD texture. The implementation reuses the
existing code-drawn font and letter gradient for context-specific 1/2 glyphs.
No new character/effect illustrations were needed for this patch.

# Level 2 artwork provenance - v0.5.0

All additions were made with the built-in image tool. Approved source assets
remain unchanged. The generation prompts used the following production specs;
ROM-derived guides supplied exact geometry rather than invented animation.

- `player_weapons.png`: style transfer of the exact 4x4 guide, fifteen poses
  and bottom-right empty. Reuse the approved muscular tan, swept-brown-haired
  hero in a black tank, gray cargo trousers, gloves and boots. Row 1: dagger
  guard, nunchaku guard, crouched dagger thrust, crouched dagger windup. Row 2:
  standing dagger thrust, extended nunchaku strike, nunchaku windup, dagger
  preparation. Row 3: crouched dagger guard, nunchaku guard, extended nunchaku
  strike, nunchaku windup. Row 4: upward dagger, upward extended nunchaku,
  front-facing victory with both fists raised, empty. Preserve all positions,
  directions, proportions, limbs and weapons; painted arcade shading, clean
  transparent alpha, no labels, grid, floor, shadows or glow.
- `player2_weapons.png`: identity-preserving edit of the first sheet. Change
  only hair/face to the approved Player 2 short upright dark-brown crewcut and
  squared jaw. Keep every pose, weapon, cell, costume, silhouette and alpha.
- `ninjas_level2.png`: 4x2, eight source running and guard variations, all
  facing right. Use the approved masked ninja with red cloth hood/tunic/pants,
  brown sash, black wraps/boots and tan eye area. Match each knee bend and
  stance; no extra weapons, scene, grid, labels or shadows; transparent alpha.
- `small_ninjas.png`: 4x2, seven poses and final cell empty. Agile compact
  masked navy-blue ninja, black wraps/boots, dark belt. Three walking phases,
  backward airborne recoil, two curled/rotated tumbles and knee-up jump, in
  the guide's exact order and orientation. Match approved painted shading;
  no weapons, labels, grid, glow or floor; transparent alpha.
- `level2_boss.png`: 4x3, ten poses and final two cells empty. Purple cloth,
  grey hood/mask, silver segmented armor and three steel claws on each hand.
  Two walking guards, crouch, overhead claw, two prone states, two tumbling
  states, horizontal claw punch and leaning double-claw lunge. Preserve the
  source directions and silhouettes. An extraction pass removed the first
  output's grey haze/background while retaining the ten characters.
- `nunchaku_pickup.png`: one square pickup icon, two reddish-brown polished
  wooden batons connected at their upper ends by a short silver chain,
  hanging in an inverted V. Compact readable silhouette, painted arcade
  materials, metal endcaps, crisp outline; transparent alpha, no hands, glow,
  floor, labels or scene. The dagger pickup reuses effects.png cell 11.
- `level2_truck.png`: exact background geometry guide at replay frame 600,
  using the approved Level 1 truck illustration only as material/style
  reference. Preserve skyline outlines/windows, trailer joins, wheel centers,
  fuel tanks, roadway and HUD boundary. Pale warm stone nearer towers, dark
  glass, teal distant towers, blue afternoon sky. Ribbed silver trailer,
  emerald band, black tires, chrome hubs/tanks. No actors or new objects;
  bottom HUD region plain dark, with no baked text.
- `level2_cab.png`: frame 7500 background guide with the same Level 2 style.
  Preserve skyline above y=388, parapet/posts to y=510, cropped emerald cab
  at left, road to its right and curb at y=768. Glossy dark green metal,
  opaque windshield, chrome fuel tank and black tire, small DUDES door word.
  Replace the cyan dotted road with slate-blue asphalt, not water. No actors,
  extra vehicles, perspective change or HUD lettering.
- `level2_sky.png`: clean blue painted arcade daytime sky, medium azure at
  top fading lighter below, a few delicate pale clouds near the upper quarter,
  broad clear areas. No horizon, buildings, sun, text or dramatic weather.

`level2_art.py` registers the painted horizontal bands and extracts repeatable
cells. Identical native cells across the two scrolling CHR banks reuse the
same art. The new sky is a scene-gated background; stage letters remain live
code-drawn glyphs, never static screenshot text. The weapon pickup bright
phase uses the existing alpha-preserving brightness transform. As before,
all runtime previews under validation/ are actual emulator captures; the
source sheets and slicing contact sheets are not emulator screenshots.
