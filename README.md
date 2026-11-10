# Bad Dudes HD

A work-in-progress **4x HD graphics pack** for Bad Dudes (NES), built for MesenCE.

![Bad Dudes HD preview](validation/visual_index.png)

## Current build: v0.6.0

A **Level 1–3 test build**. Level 3 now has painted sewer masonry, overhead
pipes, ladders, flowing and recessed drains, and the broken-wall boss area.
The live HUD supports Level 3's alternate white palette and keeps the gold
player labels, moving scores, timer and health bars.

The new recording adds a red ninja dagger attack, green ninja boss states,
appearance/white-flash/disappearance/defeat frames, and a narrow raised-fist
victory pose for both heroes. Familiar ninja and super-punch animations reuse
the approved artwork when the game switches CHR banks or uniform colors.
The earlier truck-wheel and emerald-cab fixes remain included.

The complete 10,341-input Level 3 recording has detailed mappings for all
1,411 observed visible gameplay sprite tile/palette combinations. All 212
captured Level 3 scenery keys use the painted references. Coverage is limited
to recorded states; later levels, unrecorded moves and alternating two-player
play still need testing. This is not a complete full-game release.

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
then merge `develop` and create the v1.0.0 release. The v0.5.1 checkpoint is approved on this development branch. v0.6.0 is
prepared for user testing and has not been pushed or released.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup, tile mapping, validation
and the next art pass. `art/` contains the source illustrations; `scripts/`
assembles them into `pack/`; `metadata/` holds the captured tile mappings.
The source ROM is required to rebuild and must remain outside this repository.
