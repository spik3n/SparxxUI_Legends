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

## Gallery

| | |
|:---:|:---:|
| **Dark** | **Obsidian** |
| ![SparxxDark](SparxxUI_pictures/SparxxDark.png) | ![SparxxObsidian](SparxxUI_pictures/SparxxObsidian.png) |
| **Venom** | **Ember** |
| ![SparxxVenom](SparxxUI_pictures/SparxxVenom.png) | ![SparxxEmber](SparxxUI_pictures/SparxxEmber.png) |
| **Red** | **Gold** |
| ![SparxxRed](SparxxUI_pictures/SparxxRed.png) | ![SparxxGold](SparxxUI_pictures/SparxxGold.png) |
| **Bronze** | **3D target ring** |
| ![SparxxBronze](SparxxUI_pictures/SparxxBronze.png) | ![Target ring](SparxxUI_pictures/TargetRing.png) |
| **Target ring markers** | **Buff & song timers** |
| ![Target ring markers](SparxxUI_pictures/TargetRingMark.png) | ![Buff and song timers](SparxxUI_pictures/Buffs_and_Songs.png) |

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

## Installing — pick one

There are two ways to install. **If you're not comfortable with computer stuff,
use the Manual method** — it's just copying folders and needs no extra software.
The Installer is an optional convenience that automates the copying, but it needs
Python.

## Install — Manual (easiest, no Python needed)

Same drag‑and‑drop copy EverQuest UIs have always used:

1. **Get the files.** On this project's GitHub page, click the green **`< > Code`**
   button → **Download ZIP** (or grab a package from **Releases**). Unzip it.
2. **Find your game folder** — the EverQuest Legends folder that has `eqgame.exe`
   in it. Open the **`uifiles`** folder inside it.
3. **Copy in a theme.** Drag one theme folder (for example `SparxxVenom`) into
   `uifiles`, so you end up with `...\uifiles\SparxxVenom\`.
4. **(Optional) 3D target ring.** Open the `TargetRing` folder, select everything
   **except** the `options` folder, and copy those files into `...\uifiles\default\`.
   Skip this if you don't want the ring.
5. **Load it in game.** Start EverQuest and type:
   ```
   /loadskin SparxxVenom 1
   ```
   Use whichever theme folder you copied. The `1` keeps your window positions.

Close EverQuest before copying files — it rewrites UI files when it exits. The
ring only updates on a **full game restart**, not `/loadskin`.

## Install — Installer (optional, needs Python)

The installer just automates the steps above with a little menu. First install
Python (see below), then:

1. Double‑click **`Install.bat`** (or run `python install.py`).
2. Choose a single theme, **Install ALL themes**, or **Target ring only**.
3. Choose the **target ring** (no spin / slow / normal / fast, or keep the game's
   default ring).
4. When the folder browser opens, pick your EverQuest Legends folder (the one with
   `eqgame.exe`).
5. In game: `/loadskin <ThemeName> 1`  (e.g. `/loadskin SparxxVenom 1`).

It copies the theme into `uifiles\<ThemeName>\` and the ring into `uifiles\default\`.

### Getting Python (only if you use the Installer)

**Don't get it from the Microsoft Store** — there are too many confusing options
there. Use the official installer instead:

1. In your web browser, go to **https://www.python.org/downloads/**
2. Click the big yellow **Download Python 3.x** button near the top. Any Python
   **3** version works — newer is fine.
3. Run the file you just downloaded. On the **very first screen**, tick the
   checkbox **“Add python.exe to PATH”** at the bottom — this step matters.
4. Click **Install Now**, let it finish, then **Close**.
5. (Optional check) Press **Win + R**, type `cmd`, press Enter, then type
   `python --version`. If it prints something like `Python 3.13.0`, you're set.

If that feels like too much, just use the **Manual** method above — it does the
exact same thing without Python.

## Notes

- If windows look misplaced the first time, that's saved positions, not the
  skin — drag them, or remove your `UI_<character>_<server>.ini` to start fresh.
- To remove the ring later, delete the ring files and `TargetIndicator.ini` from
  `uifiles\default`; the client falls back to its built-in ring.
- The installer uses Python's built‑in Tkinter (bundled with the python.org
  installer) for the folder browser. If it's ever missing, the script just asks
  you to paste your game folder path instead.
