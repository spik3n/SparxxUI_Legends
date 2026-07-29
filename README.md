# SparxxUI for EverQuest Legends

The classic **Sparxx** look, rebuilt for **EverQuest Legends**, in seven accent
colors — plus a con-colored 3D target ring.

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

`TargetRing/` holds the con-colored ring that renders under your target in the
world (grey → green → blue → white → yellow → red by difficulty).

**Important:** the Legends client reads the ring only from the game's
`uifiles\default` folder — **not** the active skin folder. So the ring is
installed into `default` once; it then works no matter which Sparxx theme you
load. (The installer does this for you.)

### Spin options

`TargetRing/options/` has drop-in variants — copy one over
`default\TargetIndicator.ini`, then fully restart EverQuest (the ring is cached
at launch):

| File | Behavior |
|---|---|
| `no-spin.ini`    | Static ring (default). Loads fastest — 9 textures instead of ~574. |
| `spin-slow.ini`  | Slow rotation. |
| `spin.ini`       | Normal rotation. |
| `spin-fast.ini`  | Fast rotation. |

To hand-tune: in a spinning file, `Duration` sets how long the 82-frame cycle
takes — higher = slower. `FrameCount=0` with `Texture=<Color>_0` = no spin.

## Install (installer)

1. Run `Install.bat` (or `python install.py`).
2. Choose a single theme, or pick **Install ALL themes** to drop in every color.
3. When the folder browser opens, select your EverQuest Legends folder (the one
   containing `eqgame.exe`).
4. In game, load it:

   ```
   /loadskin <ThemeName> 1
   ```

   e.g. `/loadskin SparxxVenom 1`. The `1` keeps your current window positions.

The installer copies the chosen theme into `uifiles\<ThemeName>\` and the target
ring into `uifiles\default\`.

## Install (manual)

No installer needed — it's the same drop-in copy EverQuest UIs have always used:

1. Copy one theme folder (e.g. `SparxxVenom`) into your Legends `uifiles`
   folder, so you have `...\uifiles\SparxxVenom\`.
2. Copy the **contents** of `TargetRing/` (the frame `.tga` files and
   `TargetIndicator.ini`, not the `options/` folder) into `...\uifiles\default\`.
   Skip this step if you don't want the con-colored ring.
3. In game: `/loadskin SparxxVenom 1`.

Close EverQuest before copying — it rewrites UI files on exit. The ring only
updates on a full client restart, not `/loadskin`.

## Notes

- If windows look misplaced the first time, that's saved positions, not the
  skin — drag them, or remove your `UI_<character>_<server>.ini` to start fresh.
- To remove the ring later, delete the ring files and `TargetIndicator.ini` from
  `uifiles\default`; the client falls back to its built-in ring.
- Requirements for the installer: Python 3 (Tkinter, included with the standard
  Windows Python, is used for the folder browser; if it's unavailable the script
  asks you to paste the path instead).
