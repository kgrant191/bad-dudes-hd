# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.9.0

A **Level 1–6 test build** for MesenCE. The cave stage now has painted emerald
rock, mossy pillars and stalagmites, blue-gray limestone platforms, shadowed
rear walls, spikes and falling stone fragments. Scrolling, platforms and
hazards stay attached to the original game geometry.

The small ninja uses one artwork scale across its seven existing poses.
Running and jump transitions reuse identical native head/torso cells, removing
the stretching caused by fitting every pose to a different rectangle. The sai
attack now matches the small ninja's costume and proportions. Its newly
recorded airborne recoil has detailed art in both blue and gray uniforms.
These shared enemy corrections also apply in earlier stages.

The cave's staff fighter has twelve complete recorded layouts covering walking,
turning, jumping, kick, crouched thrust, recoil and defeat. A newly observed dog
leap reuses the approved dog artwork and scale. The earlier train, boss-chain,
dog-recoil, charge-arc, player and font fixes remain included.

The supplied 12,331-input Level 6 movie was replayed in MesenCE. All **1,485
observed visible gameplay sprite tile/palette combinations** have detailed
mappings, and all **209 cave background keys** are replaced. An earlier Level 4
movie is also replayed for shared-enemy regression checks. See
`validation/v0.9.0_validation.json` for measured results and limits.

The recording reaches **Stage 6 Clear**; it does not verify the transition
into the next level or its gameplay. Unrecorded animations and
alternating two-player states remain unverified. This is not a full-game release.

## Install

Load your own **Bad Dudes (USA).nes** in MesenCE, then choose
**Tools > HD Packs (NES) > Install HD Pack** and select the install ZIP.
Enable HD packs in NES settings and reload the game if needed.

For manual installation, copy the contents of `pack/` into
`HdPacks/Bad Dudes (USA)/`. The folder name must match your ROM's base filename.
All eight PNGs and `hires.txt` must be together. This repository's Code > Download
ZIP also contains an installable `pack/hires.txt` directory.

Tested with MesenCE 2.2.1. No ROM, emulator or movie recording is included.
The pack changes presentation; gameplay and music are unchanged.

## Development

Approved checkpoints are accumulated on `develop`. Keep `main` at the current
baseline until the full remake and final regression testing are complete,
then merge `develop` and create the v1.0.0 release. The v0.8.2 checkpoint at
`bf56adb886c0e2002c6e17e80ccbd6b693e69523` is approved and pushed to develop.
v0.9.0 is a local test build prepared from that commit. No push, merge, tag or
release has been performed for v0.9.0.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
