"""
SparxxUI for EverQuest Legends - installer.

Pick a theme, browse to your EverQuest Legends folder, and the matching skin
(plus the shared 3D target ring) is copied into uifiles ready to load.
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


def choose_theme():
    print("Available themes:\n")
    for i, name in enumerate(THEMES, 1):
        print(f"  {i}. {name}")
    while True:
        pick = input(f"\nChoose a theme [1-{len(THEMES)}]: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(THEMES):
            return THEMES[int(pick) - 1]
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


def main():
    print("SparxxUI for EverQuest Legends - installer\n")
    theme = choose_theme()
    theme_dir = os.path.join(HERE, theme)
    if not os.path.isdir(theme_dir):
        sys.exit(f"Theme folder not found next to this script: {theme_dir}")

    print("\nOpening a folder browser - pick your EverQuest Legends folder...")
    game = browse_folder()
    if not game or not os.path.isdir(game):
        sys.exit("No valid folder selected.")

    uifiles = resolve_uifiles(game)
    dest = os.path.join(uifiles, theme)

    if os.path.isdir(dest):
        ans = input(f"\n{dest}\nalready exists. Overwrite it? [y/N]: ").strip().lower()
        if ans != "y":
            sys.exit("Cancelled.")
        shutil.rmtree(dest)
    os.makedirs(dest)

    print(f"\nInstalling {theme} ...")
    copy_into(theme_dir, dest)
    if os.path.isdir(RING):
        copy_into(RING, dest)
        print("Added shared 3D target ring.")
    else:
        print("Note: TargetRing folder not found - skin installed without the ring.")

    print("\nDone.")
    print(f"Installed to: {dest}")
    print(f"In game, load it with:  /loadskin {theme} 1")


if __name__ == "__main__":
    main()
