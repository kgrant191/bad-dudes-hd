# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.11.0

A **full-game regression test build** for MesenCE, based on the supplied
91,532-input second-character playthrough and 1,017-input game-over recording.

- Preserve HD scenery and HUD art through the native palette fades.
- Cover the cave staff boss's missed recoil pose and the final boss's flying mask.
- Render every ending-credit letter consistently through THE END.
- Select the short-haired second hero's illustration after a player 2 run.
- Update the live Continue/End, Game Over and title-menu lettering.
- Correct the enemy-health label's period across stages.

The detailed Level 1–7 environments, both playable heroes, enemies, bosses,
weapons, effects and illustrated ending screens remain included. The ending
illustrations use static figures and flags; dialogue and scrolling credits
stay controlled by the game.

This checkpoint awaits user review. After approval, the next steps are the
promotional before/after screenshots and video, then the v1.0.0 release.
Validation evidence and recorded-state limits are kept in `validation/`.

## Install

Load your own **Bad Dudes (USA).nes** in MesenCE, then choose
**Tools > HD Packs (NES) > Install HD Pack** and select the install ZIP.
Enable HD packs in NES settings and reload the game if needed.

For manual installation, copy the contents of `pack/` into
`HdPacks/Bad Dudes (USA)/`. The folder name must match your ROM's base filename.
All eleven PNGs and `hires.txt` must be together. This repository's Code > Download
ZIP also contains an installable `pack/hires.txt` directory.

Tested with MesenCE 2.2.1. No ROM, emulator or movie recording is included.
The pack changes presentation; gameplay and music are unchanged.

## Development

Approved checkpoints are accumulated on `develop`. Keep `main` at the current
baseline until the full remake and final regression testing are complete,
then merge `develop` and create the v1.0.0 release. The v0.8.2 checkpoint at
`bf56adb886c0e2002c6e17e80ccbd6b693e69523` is approved and pushed to develop.
v0.9.0 at `26e3d2a574e7364e6483891705aa0afe0ef1c1cc` is approved locally.
v0.10.0 is the preceding final-level test checkpoint. v0.11.0 addresses the
full-game regression findings; its source bundle includes all three checkpoints
from the last confirmed pushed v0.8.2 base. No new push, merge,
tag or release has been performed.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
