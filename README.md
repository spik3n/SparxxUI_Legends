# SparxxUI for EverQuest Legends

The classic **Sparxx** look, rebuilt for **EverQuest Legends**, in seven accent
colors — plus the animated 3D target ring.

EverQuest Legends uses a different UI window set than retail EverQuest (a
classic-era client: `EQUI_CharacterSelect`, `EQUI_BuffWindow1`–`17`,
`EQUI_AbilityDisplayWindow`, a required `EQUI_Animations.xml`, and so on). A
retail-era Sparxx skin cannot load on it. These themes use the Legends window
set and wear the Sparxx frames, backgrounds and coloring, so they load cleanly
on Legends.

## Themes

Each theme is a complete skin. They share identical windows and Sparxx chrome
and differ only in accent color:

| Theme | Accent |
|---|---|
| `SparxxDark`     | Steel / silver — classic all-dark |
| `SparxxObsidian` | Deep blue-gray, the moodiest tint |
| `SparxxVenom`    | Teal / cyan |
| `SparxxEmber`    | Warm amber / orange |
| `SparxxRed`      | Crimson |
| `SparxxGold`     | Yellow-gold |
| `SparxxBronze`   | Antique bronze |

HP-red, mana-blue, casting and item-link colors are kept in every theme so
gauges and links stay readable.

## The 3D target ring

`TargetRing/` holds the animated con-colored ring that renders under your target
in the world (grey → green → light blue → dark blue → white → yellow → red by
difficulty), shared by every theme so it isn't duplicated seven times. The
installer copies it into whichever theme you install. It is the same ring for
all themes — its color signals target difficulty, not the UI accent.

## Install (installer)

1. Run `Install.bat` (or `python install.py`).
2. Choose a theme from the list.
3. When the folder browser opens, select your EverQuest Legends folder (the one
   containing `eqgame.exe`).
4. In game, load it:

   ```
   /loadskin <ThemeName> 1
   ```

   e.g. `/loadskin SparxxVenom 1`. The `1` keeps your current window positions.

The installer copies the chosen theme and the shared target ring into
`<EverQuest Legends>\uifiles\<ThemeName>\`.

## Install (manual)

No installer needed — it's the same drop-in copy EverQuest UIs have always used:

1. Copy one theme folder (e.g. `SparxxVenom`) into your Legends `uifiles`
   folder, so you have `...\uifiles\SparxxVenom\`.
2. Copy the **contents** of `TargetRing/` into that same theme folder (so the
   ring's `.tga` files and `TargetIndicator.ini` sit beside `EQUI.xml`). Skip
   this step if you don't want the 3D ring.
3. In game: `/loadskin SparxxVenom 1`.

Close EverQuest before copying — it rewrites UI files on exit.

## Notes

- If windows look misplaced the first time, that's saved positions, not the
  skin — drag them, or remove your `UI_<character>_<server>.ini` to start fresh.
- To remove the ring later, delete `TargetIndicator.ini` and the ring `.tga`
  files from the theme folder; the client falls back to its default ring.
- Requirements for the installer: Python 3 (Tkinter, included with the standard
  Windows Python, is used for the folder browser; if it's unavailable the script
  asks you to paste the path instead).
