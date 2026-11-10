# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.4.2

A Level 1 test build with detailed artwork for both selectable heroes,
ninjas, specialist enemies, the boss, pickups, combat effects and a live HUD.

Version 0.4.2 completes the super-punch charge, release and dissipating-effect
palettes for both heroes, including punches that miss. Both `1P` and `2P` HUD
labels are fully gold; score, time and lives digits retain their existing color.

Version 0.4.1 fixes the red ninja falling from the upper platform. The build
also covers all four known uniform colors for existing basic-ninja poses,
preventing the same missing-palette fallback on other color/pose combinations.

Version 0.4.0 added player 2's short-haired identity across 26 animation
layouts, including attacks, upward punch, hurt, knockdown and victory.
Three additional ninja/sword-fighter poses and four boss punch/tumble poses
cover the latest recording. Clock and energy-can pickups retain the same
HD art throughout the native flash cycle, alternating normal and brighter
versions. Character flashes preserve the selected hero's identity.

The earlier stage-entry background fix, approved title, selection, briefing
font correction, scenery and live HUD remain in place. All six supplied
recordings have detailed mappings for every observed visible gameplay
sprite tile/palette key. Unrecorded moves, two-player states and later stages
still need recordings; the publisher splash retains its baseline treatment.

## Install

Load your own **Bad Dudes (USA).nes** in MesenCE, then choose
**Tools > HD Packs (NES) > Install HD Pack** and select the install ZIP.
Enable HD packs in NES settings and reload the game if needed.

For manual installation, copy the contents of `pack/` into
`HdPacks/Bad Dudes (USA)/`. The folder name must match your ROM's base filename.
All seven PNGs and `hires.txt` must be together. This repository's Code > Download
ZIP also contains an installable `pack/hires.txt` directory.

Tested with MesenCE 2.2.1. No ROM, emulator or movie recording is included.
The pack changes presentation; gameplay and music are unchanged.

## Development

Approved checkpoints are accumulated on `develop`. Keep `main` at the current
baseline until the full remake and final regression testing are complete,
then merge `develop` and create the v1.0.0 release. The v0.4.1 checkpoint is
approved for this development branch; it is not a full-game release.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
