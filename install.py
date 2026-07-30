"""
SparxxUI for EverQuest Legends - installer.

Pick one theme or all of them, browse to your EverQuest Legends folder, and the
skin(s) plus the shared 3D target ring are copied into uifiles ready to load.
"""
import os
import sys
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
RING = os.path.join(HERE, "TargetRing")
THEMES = [
    "SparxxDark", "SparxxObsidian", "SparxxVenom", "SparxxEmber",
    "SparxxRed", "SparxxGold", "SparxxBronze",
]

RING_OPTIONS = [
    ("no-spin.ini",   "Sparxx ring, no spin - static (fastest to load)"),
    ("spin-slow.ini", "Sparxx ring, slow spin"),
    ("spin.ini",      "Sparxx ring, normal spin"),
    ("spin-fast.ini", "Sparxx ring, fast spin"),
    ("",              "Keep the game's default ring (don't install the Sparxx ring)"),
]


def choose_themes():
    print("Available themes:\n")
    for i, name in enumerate(THEMES, 1):
        print(f"  {i}. {name}")
    all_opt = len(THEMES) + 1
    ring_opt = len(THEMES) + 2
    print(f"  {all_opt}. Install ALL themes")
    print(f"  {ring_opt}. Target ring only (no theme)")
    while True:
        pick = input(f"\nChoose [1-{ring_opt}]: ").strip()
        if pick.isdigit():
            n = int(pick)
            if 1 <= n <= len(THEMES):
                return [THEMES[n - 1]]
            if n == all_opt:
                return list(THEMES)
            if n == ring_opt:
                return []          # ring only
        print("Please enter a number from the list.")


def choose_spin():
    print("\nTarget ring:")
    for i, (_, label) in enumerate(RING_OPTIONS, 1):
        print(f"  {i}. {label}")
    while True:
        pick = input(f"Choose [1-{len(RING_OPTIONS)}] (Enter = 1): ").strip()
        if pick == "":
            return RING_OPTIONS[0][0]
        if pick.isdigit() and 1 <= int(pick) <= len(RING_OPTIONS):
            return RING_OPTIONS[int(pick) - 1][0]
        print("Please enter a number from the list.")


def browse_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory(
            title="Select your EverQuest Legends folder (contains eqgame.exe)")
        root.destroy()
        if path:
            return path
    except Exception:
        pass
    return input("Paste the path to your EverQuest Legends folder: ").strip('" ')


def resolve_uifiles(folder):
    """Accept the game root, the uifiles folder, or a folder holding eqgame.exe."""
    folder = os.path.abspath(folder)
    if os.path.basename(folder).lower() == "uifiles":
        return folder
    ui = os.path.join(folder, "uifiles")
    if os.path.isdir(ui):
        return ui
    if os.path.isfile(os.path.join(folder, "eqgame.exe")):
        os.makedirs(ui, exist_ok=True)
        return ui
    # last resort: create uifiles under whatever was chosen
    os.makedirs(ui, exist_ok=True)
    return ui


def copy_into(src_dir, dst_dir):
    for name in os.listdir(src_dir):
        s = os.path.join(src_dir, name)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(dst_dir, name))


def install_one(theme, uifiles, overwrite):
    theme_dir = os.path.join(HERE, theme)
    if not os.path.isdir(theme_dir):
        print(f"  ! {theme}: source folder not found, skipped")
        return None
    dest = os.path.join(uifiles, theme)
    if os.path.isdir(dest):
        if overwrite is False:
            print(f"  - {theme}: already installed, skipped")
            return None
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    copy_into(theme_dir, dest)
    print(f"  + {theme} installed")
    return dest


def install_ring(uifiles, spin_file):
    """The target ring loads from uifiles\\default regardless of the active skin,
    so it's installed there once (not into every theme). spin_file selects the
    rotation variant from TargetRing/options/."""
    if not os.path.isdir(RING):
        return False
    dest = os.path.join(uifiles, "default")
    os.makedirs(dest, exist_ok=True)
    copy_into(RING, dest)  # ring frames + TargetIndicator.ini; skips the options/ subfolder
    chosen = os.path.join(RING, "options", spin_file)
    if os.path.isfile(chosen):
        shutil.copy2(chosen, os.path.join(dest, "TargetIndicator.ini"))
    print(f"  + target ring installed into uifiles\\default ({spin_file})")
    return True


def main():
    print("SparxxUI for EverQuest Legends - installer\n")
    themes = choose_themes()
    spin_file = choose_spin()

    print("\nOpening a folder browser - pick your EverQuest Legends folder...")
    game = browse_folder()
    if not game or not os.path.isdir(game):
        sys.exit("No valid folder selected.")
    uifiles = resolve_uifiles(game)

    # For an all-install, decide overwrite once up front.
    overwrite = True
    existing = [t for t in themes if os.path.isdir(os.path.join(uifiles, t))]
    if existing:
        ans = input(f"\n{len(existing)} of these are already in uifiles. "
                    f"Overwrite them? [y/N]: ").strip().lower()
        overwrite = (ans == "y")

    print(f"\nInstalling to: {uifiles}\n")
    installed = [install_one(t, uifiles, overwrite) for t in themes]
    installed = [t for t in zip(themes, installed) if t[1]]

    ring_done = False
    if spin_file:
        ring_done = install_ring(uifiles, spin_file)
        if not ring_done:
            print("  (TargetRing folder not found - ring not installed)")
    elif themes:
        print("  + kept the game's default target ring (Sparxx ring not installed)")

    print("\nDone.")
    if installed:
        print("Load a theme in game with /loadskin <name> 1, for example:")
        for name, _ in installed:
            print(f"  /loadskin {name} 1")
        if ring_done:
            print("Fully restart EverQuest to load the target ring.")
    elif ring_done:
        print("Target ring installed. Fully restart EverQuest to load it.")
    else:
        print("Nothing was installed.")


if __name__ == "__main__":
    main()
