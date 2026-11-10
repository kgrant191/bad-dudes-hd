# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.8.0

A **Level 1–5 test build**. Level 5 adds a painted canyon, distant mountains,
colored freight cars, detailed locomotive vents, metal bogies and rails.
Scrolling and the original moving tile-bank swaps remain game-controlled.

Missing acrobat flips, weapon thrusts, small-ninja attacks and burning recoil
frames now keep their HD artwork. Returning earlier bosses also have the
train stage's alternate costume palette. These shared mappings apply wherever
the same enemies appear, including earlier levels. The chain-claw boss has
new movement, attacks, airborne poses and the visible falling-foot fragment.
His face and body retain their separate palette identities.

The main character's recorded moves and damage flashes were checked; no
additional hero frames were missing. Both approved heroes, the fixed dog
animation/recoil and inward-facing `( hero )` charge arcs remain included.

The supplied movie contains 15,268 inputs, including the Level 4 exit and a
short Level 6 opening. Through the Level 5 clear, all **1,937 observed visible
sprite tile/palette combinations** have detailed mappings. All **588 train
and canyon background keys** are covered by painted cells, matching aliases,
color variants or transparent sky cells. Level 6 scenery is still pending.
Unrecorded animations and alternating two-player states remain unverified.
This is not a full-game release.

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
then merge `develop` and create the v1.0.0 release. The v0.7.2 checkpoint is
approved and pushed on this development branch. v0.8.0 is prepared for user
testing and has not been pushed or released.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
