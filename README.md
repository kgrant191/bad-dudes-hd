# Bad Dudes HD

A **4x HD graphics pack for Bad Dudes (NES)**, built for MesenCE. Play the
original game with detailed characters, enemies and environments across all
seven stages. Gameplay, collisions, timing and music stay controlled by the game.

**[Download the HD pack](https://github.com/kgrant191/bad-dudes-hd/releases)**

## Before and after

Original NES on the left; Bad Dudes HD on the right. Each pair comes from the
same frame of the same recorded playthrough.

![City streets: original NES and Bad Dudes HD](docs/images/before-after-street.png)
![Highway: original NES and Bad Dudes HD](docs/images/before-after-highway.png)
![Train: original NES and Bad Dudes HD](docs/images/before-after-train.png)
![Caves: original NES and Bad Dudes HD](docs/images/before-after-cave.png)

## What's included in v1.0.0

- All seven stages, including the moving trucks, train, caves, final factory
  and helicopter battle.
- Distinct artwork for both playable heroes, including their weapons,
  effects and palette variants.
- Detailed enemies and bosses, with attack, recoil and defeat states.
- Illustrated title, selection, briefing and ending screens.
- Updated HUD, menus and live credit lettering, with HD art retained through
  the game's palette fades.

Ending figures and flags are still illustrations; dialogue and scrolling
credits remain live. Original damage blinking, sprite limits and clipping are
preserved.

## Install

Use **standalone MesenCE 2.2.1**, the tested emulator for these packs. [Download MesenCE](https://github.com/nesdev-org/MesenCE/releases/tag/2.2.1). These packs use modern Mesen 2 / MesenCE HD-pack features; original Mesen 0.9.x and RetroArch’s **legacy Mesen core** are not compatible. That core supports pack format 106, while these projects use newer features. A separate MesenCE-based RetroArch core now exists, but these releases have not been validated with it. Standalone MesenCE is the supported setup described here.

1. Download **Bad_Dudes_HD_v1.0.0.zip** from the game’s Releases page. Leave the ZIP compressed.
2. Open your own supported **ROM in MesenCE**.
3. Choose **Tools > HD Packs (NES) > Install HD Pack** and select the downloaded ZIP.
4. When MesenCE reports that installation succeeded, click **OK** to reset the game and load the HD pack.

No manual extraction or folder renaming is needed for this normal installation. To update a pack, open the same ROM and install the newer release ZIP through the same menu.

[Full installation guide and troubleshooting](docs/INSTALLATION.md).

No ROM or emulator is included. Supply your own supported ROM.

## Development

The release uses the approved v0.11.0 artwork and mappings. The final regression
covered a full second-character playthrough, the complete ending and return to
menus, a separate game-over recording, and a final cave replay. Evidence and
recorded-state limits are in `validation/`.

See [DEVELOPMENT.md](DEVELOPMENT.md) for build setup and
[RELEASE_NOTES.md](RELEASE_NOTES.md) for the release notes. `art/` contains source
illustrations, `scripts/` builds the pack, and `metadata/` holds tile mappings.
The source ROM is required to rebuild and must remain outside this repository.

