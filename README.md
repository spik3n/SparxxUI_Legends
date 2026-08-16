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

## Install — Auto installer (optional)

Prefer to have it done for you? The installer is a small menu that copies
everything automatically. It needs Python — a free, one‑time install.

### Step 1 — Install Python (one time)

**Don't get it from the Microsoft Store** — there are too many confusing options
there. Use the official installer:

1. In your web browser, go to **https://www.python.org/downloads/**
2. Click the big yellow **Download Python 3.x** button near the top. Any Python
   **3** version works — newer is fine.
3. Run the file you just downloaded. On the **very first screen**, tick the
   checkbox **“Add python.exe to PATH”** at the bottom — this step matters.
4. Click **Install Now**, let it finish, then **Close**.

*(Already have Python? Skip to Step 2. To check: press **Win + R**, type `cmd`,
Enter, then `python --version` — if it prints `Python 3.x`, you're good.)*

### Step 2 — Run the installer

1. Unzip the download and open the `SparxxUI_Legends` folder.
2. Double‑click **`Install.bat`**. A small text window opens.
   - If Windows shows a blue **“Windows protected your PC”** box, click
     **More info → Run anyway** (it's just a `.bat` that starts the installer).
3. It lists the themes — type the **number** of the one you want (or the number
   for **Install ALL themes** / **Target ring only**) and press **Enter**.
4. It asks about the **target ring** — type the number for your choice (no spin /
   slow / normal / fast, or keep the game's default) and press **Enter**.
5. A **folder‑picker window** opens — browse to your **EverQuest Legends** folder
   (the one with `eqgame.exe`) and click **Select Folder**.
6. It copies everything and prints **Done**. Close the window.

### Step 3 — Load it in game

Start EverQuest and type:
```
/loadskin SparxxVenom 1
```
Use whichever theme you installed (the installer prints the exact command). The
`1` keeps your window positions.

The installer copies the theme into `uifiles\<ThemeName>\` and the ring into
`uifiles\default\`. If any of this feels like too much, the **Manual** method
above does the same thing with no Python.

## Notes

- If windows look misplaced the first time, that's saved positions, not the
  skin — drag them, or remove your `UI_<character>_<server>.ini` to start fresh.
- To remove the ring later, delete the ring files and `TargetIndicator.ini` from
  `uifiles\default`; the client falls back to its built-in ring.
- The installer uses Python's built‑in Tkinter (bundled with the python.org
  installer) for the folder browser. If it's ever missing, the script just asks
  you to paste your game folder path instead.

## Troubleshooting

**“`python` is not recognized” when running the installer**
You skipped the **“Add python.exe to PATH”** checkbox during the Python install.
Easiest fix: re‑run the python.org installer, choose **Modify**, and enable that
option (or just uninstall/reinstall and tick the box). Or skip Python entirely
and use the **Manual** install — it does the same thing.

**The UI didn't change after `/loadskin`**
- Make sure the theme folder is directly inside `uifiles` — i.e.
  `...\uifiles\SparxxVenom\EQUI.xml`, not `...\uifiles\SparxxVenom\SparxxVenom\`.
- The name in `/loadskin` must match the folder exactly, e.g.
  `/loadskin SparxxVenom 1` for the `SparxxVenom` folder.
- Copy files while EverQuest is **closed** — it rewrites UI files when it exits.

**The target ring didn't appear**
- The ring files go in **`uifiles\default`**, not the theme folder — the client
  only reads the ring from there.
- The ring loads at startup, so you need a **full game restart** (quit to
  desktop and relaunch), not `/loadskin`.
- Note: the game's launcher can restore `uifiles\default` on patch days, which
  removes the ring — just re‑install it if that happens.

**Windows are off‑screen, overlapping, or in weird spots**
That's your **saved window positions**, not the skin. Drag them where you want,
or to start fresh close the game and delete your `UI_<character>_<server>.ini`
(in the main EverQuest folder) — the game rebuilds it at default positions.

**Buff/song timers aren't showing**
The timer text is drawn on the buff icon, and the client only draws it when
"Show Buff Timer" is on: **Options → Display → Show Buff Timer**.

**It looks broken / I want to undo everything**
Delete the theme folder from `uifiles`, load the stock UI with
`/loadskin default 1` (or `/loadskin default_modern 1`), and remove the ring
files from `uifiles\default` if you added them.

## Credits

- **SparxxUI** — the original EverQuest interface this look is based on.
- Rebuilt and themed for **EverQuest Legends**; target ring and installer added
  for this release.
