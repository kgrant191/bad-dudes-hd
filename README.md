# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.10.0

A **Level 1–7 test build** for MesenCE. The final factory now has painted
emerald steel panels, vents, dragon relief, catwalks, elevator shafts and
moving metal doors. The helicopter has detailed bodywork, animated rotors,
opening cabin and skids tied to the original scrolling geometry.

The final masked boss has detailed attack, recoil and defeated states. The
returning armored boss retains his detailed poses in the final stage's olive
palette. New small-ninja layouts, palette variants, an airborne specialist
and the presidential rescue are covered. Earlier approved artwork remains
included.

The rescue leads into illustrated office and White House ending screens.
The game's dialogue and scrolling credits stay live; the ending illustrations
use static character and flag artwork, like the earlier illustrated menus.

The supplied **20,087-input final-level movie** is replayed in MesenCE, with
**2,487 observed gameplay sprite tile/palette keys** mapped to detailed art.
A complete **12,331-input Level 6 replay** checks earlier gameplay against
v0.9.0. Measured results and limits are in `validation/v0.10.0_validation.json`.

This is a test checkpoint awaiting approval. Next comes the user's full
player 2 playthrough and regression, then promotional before/after screenshots
and video, followed by the v1.0.0 release. The current movie ends during the
opening credits; later credits and unrecorded two-player states are unverified.

## Install

Load your own **Bad Dudes (USA).nes** in MesenCE, then choose
**Tools > HD Packs (NES) > Install HD Pack** and select the install ZIP.
Enable HD packs in NES settings and reload the game if needed.

For manual installation, copy the contents of `pack/` into
`HdPacks/Bad Dudes (USA)/`. The folder name must match your ROM's base filename.
All ten PNGs and `hires.txt` must be together. This repository's Code > Download
ZIP also contains an installable `pack/hires.txt` directory.

Tested with MesenCE 2.2.1. No ROM, emulator or movie recording is included.
The pack changes presentation; gameplay and music are unchanged.

## Development

Approved checkpoints are accumulated on `develop`. Keep `main` at the current
baseline until the full remake and final regression testing are complete,
then merge `develop` and create the v1.0.0 release. The v0.8.2 checkpoint at
`bf56adb886c0e2002c6e17e80ccbd6b693e69523` is approved and pushed to develop.
v0.9.0 at `26e3d2a574e7364e6483891705aa0afe0ef1c1cc` is approved locally.
v0.10.0 is the next local test checkpoint; its source bundle includes both
checkpoints from the last confirmed pushed v0.8.2 base. No new push, merge,
tag or release has been performed.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
