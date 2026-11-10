# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.7.0

A **Level 1–4 test build**. Level 4 now has painted forest canopies, mossy
trunks, fern walls, golden stone ledges, fallen logs and broken stumps.
Its live HUD keeps the established gold labels, moving scores, health and timer.

Dogs have six walking/running phases, sword ninjas have the newly recorded
kneeling attacks, and flaming ninjas retain their standing and running
animations. The armored boss has detailed movement, attack, recoil and defeat
poses. The small ninja's gray uniform now uses the existing HD animation set.
The approved hero artwork and earlier sewer/truck fixes remain included.

The complete 9,360-input Level 4 recording has detailed mappings for all
1,561 observed visible gameplay sprite tile/palette combinations. All 217
captured forest scenery keys are replaced: 214 use registered painted cells
and three partial rock corners use matching painted material with native masks.
Coverage is limited to recorded states; later levels, unrecorded moves and
alternating two-player play still need testing. This is not a full-game release.

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
then merge `develop` and create the v1.0.0 release. The v0.6.0 checkpoint is
approved and pushed on this development branch. v0.7.0 is prepared for user
testing and has not been pushed or released.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
