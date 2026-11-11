BAD DUDES HD - v1.0.0
4x HD graphics pack for Bad Dudes (NES)

INSTALL
Use standalone MesenCE 2.2.1, the tested emulator for these packs. [Download MesenCE](https://github.com/nesdev-org/MesenCE/releases/tag/2.2.1). These packs use modern Mesen 2 / MesenCE HD-pack features; original Mesen 0.9.x and RetroArch’s legacy Mesen core are not compatible. That core supports pack format 106, while these projects use newer features. A separate MesenCE-based RetroArch core now exists, but these releases have not been validated with it. Standalone MesenCE is the supported setup described here.

1. Download Bad_Dudes_HD_v1.0.0.zip from the game’s Releases page. Leave the ZIP compressed.
2. Open your own supported ROM in MesenCE.
3. Choose Tools > HD Packs (NES) > Install HD Pack and select the downloaded ZIP.
4. When MesenCE reports that installation succeeded, click OK to reset the game and load the HD pack.

No manual extraction or folder renaming is needed for this normal installation. To update a pack, open the same ROM and install the newer release ZIP through the same menu.

## Troubleshooting

### Original graphics still appear

- Open Settings > NES > General, turn on Enable HD packs, and apply the change.
- Close and reopen the ROM after changing settings or pack files. After installation, choose OK when asked to reset the game and load the pack.
- Use the game’s release HD-pack ZIP, not GitHub’s automatic source-code ZIP or a screenshots ZIP. Keep the downloaded ZIP intact for the installer. If your browser automatically extracts downloads, download it again with automatic extraction disabled.
- Confirm that you opened the supported ROM for that pack. Different regions, revisions, translations, patches and file headers can produce different SHA-1 hashes.

### Check the active HD pack folder

In MesenCE, open Settings > Preferences > Files and check Data storage location. The HdPacks folder inside that location is authoritative; portable installations, redirected Documents folders and migrated Mesen2 setups can use another path.

| System | Default MesenCE HD pack folder |
| --- | --- |
| Windows | %USERPROFILE%\Documents\MesenCE\HdPacks\ |
| macOS | ~/Library/Application Support/MesenCE/HdPacks/ |

On Windows, paste the path into File Explorer’s address bar. On Mac, use Finder Go > Go to Folder… (Shift–Command–G). Older or migrated setups may instead use Documents\Mesen2\HdPacks on Windows, ~/Library/Application Support/Mesen2/HdPacks/ on Mac, or an older ~/.config/Mesen2/HdPacks/ location. Use the location shown in Preferences rather than creating folders in all of these places.

The folder inside HdPacks must match the ROM’s filename exactly, without .nes, including spaces, punctuation and capitalization. For example:

| ROM filename | Required pack file |
| --- | --- |
| Bad Dudes (NES).nes | HdPacks/Bad Dudes (NES)/hires.txt |

This is a naming example, not a different supported ROM version. Renaming a ROM does not change its contents or hash. The installer normally handles the folder name for the ROM you have open. If you rename the ROM later, reinstall the pack with that ROM open or rename its pack folder to match.

Make sure hires.txt is directly inside the ROM-named folder, alongside all the pack assets, with no extra nested pack folder. Keep the asset filenames unchanged. If an installation is incomplete, download the release ZIP again and reinstall it through the menu.

### Check the ROM’s SHA-1

Hash the extracted .nes file itself, not the ROM ZIP or the HD-pack ZIP. Compare all 40 characters against the tested hash below; uppercase versus lowercase does not matter. A different hash means the file is not the exact tested ROM, even when its title or filename looks right. Compatibility with other dumps is not guaranteed. Do not try to fix a mismatch by renaming the file.

Tested full-file SHA-1: 26E184E350F50BFA06038379A84F3B685B7509B8

Windows PowerShell (replace the example path with your ROM):


Get-FileHash -Algorithm SHA1 -LiteralPath "C:\path\to\Bad Dudes (USA).nes"


macOS Terminal:


shasum -a 1 "/path/to/Bad Dudes (USA).nes"



INCLUDED
- All seven stages, moving trucks, train, caves, final factory and helicopter.
- Distinct artwork for both playable heroes, weapons, effects and palette states.
- Detailed enemies and bosses, including attack, recoil and defeat states.
- Illustrated title, selection, briefing and ending screens.
- Updated HUD, menus, live credits and palette-fade transitions.

TESTED SCOPE
MesenCE 2.2.1. Includes the approved v0.11.1 player/lives-screen correction.
The player/lives interstitial now uses matching gold digits and a centered dash.
All previous artwork and rule definitions are preserved. New exact-palette
overrides cover menu digits 0-9 and the dash; gameplay counters are unchanged.
The preceding full regression included a complete 91,532-input second-character
playthrough, a 1,017-input game-over recording and a final 12,331-input cave replay.
These recordings do not exercise every possible input or alternating-player state.
Native damage blinking, boss palette cycling, sprite limits and clipping remain.
Ending figures and flags are still illustrations; dialogue and credits stay live.

4x rendering: 1024 x 960 before aspect-ratio correction.
Gameplay timing, collisions and audio remain game-controlled.
No ROM, emulator, recording or source build files are included.
Supported whole-ROM SHA1: 26E184E350F50BFA06038379A84F3B685B7509B8
HD pack format: 109.

Project and updates: https://github.com/kgrant191/bad-dudes-hd

