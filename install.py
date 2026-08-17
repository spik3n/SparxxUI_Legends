"""
SparxxUI for EverQuest Legends - installer.

Pick a Sparxx theme (or a patch-safe "Modified Default / Modified Modern" skin), browse to
your EverQuest Legends folder, and the skin(s) plus the shared 3D target ring are copied into
uifiles ready to load.

  - A Sparxx theme installs as a custom skin; the ring goes into uifiles\\default (the themes
    fall back to default, so the ring shows for any of them).
  - "Modified Default / Modified Modern" are patch-safe classic-UI copies of your own
    default / default_modern skin (LaunchPad won't overwrite a custom name); the ring is
    installed straight into them so it survives patches. They match the map-pack overlay
    skins, so one skin can carry both the overlay and the ring.
"""
import os
import sys
import glob
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
RING = os.path.join(HERE, "TargetRing")
THEMES = [
    "SparxxDark", "SparxxObsidian", "SparxxVenom", "SparxxEmber",
    "SparxxRed", "SparxxGold", "SparxxBronze",
]
# (new skin name, base skin to copy) - generated from the user's own EQL UI
MODIFIED = [("Modified Default", "default"), ("Modified Modern", "default_modern")]

RING_OPTIONS = [
    ("no-spin.ini",   "Sparxx ring, no spin - static (fastest to load)"),
    ("spin-slow.ini", "Sparxx ring, slow spin"),
    ("spin.ini",      "Sparxx ring, normal spin"),
    ("spin-fast.ini", "Sparxx ring, fast spin"),
    ("",              "Keep the game's default ring (don't install the Sparxx ring)"),
]


def choose_target():
    """Returns (themes, modified): a list of Sparxx theme names and a list of (new_name, base)
    pairs to generate. Both empty means 'target ring only' (into default)."""
    print("Available themes:\n")
    for i, name in enumerate(THEMES, 1):
        print(f"  {i}. {name}")
    n = len(THEMES)
    all_opt, md_opt, mm_opt, both_opt, ring_opt = n + 1, n + 2, n + 3, n + 4, n + 5
    print(f"  {all_opt}. Install ALL Sparxx themes")
    print(f"  {md_opt}. Modified Default  (patch-safe copy of your 'default' skin + ring)")
    print(f"  {mm_opt}. Modified Modern   (patch-safe copy of your 'default_modern' skin + ring)")
    print(f"  {both_opt}. Both Modified skins")
    print(f"  {ring_opt}. Target ring only (into default)")
    while True:
        pick = input(f"\nChoose [1-{ring_opt}]: ").strip()
        if pick.isdigit():
            k = int(pick)
            if 1 <= k <= n:   return ([THEMES[k - 1]], [])
            if k == all_opt:  return (list(THEMES), [])
            if k == md_opt:   return ([], [MODIFIED[0]])
            if k == mm_opt:   return ([], [MODIFIED[1]])
            if k == both_opt: return ([], list(MODIFIED))
            if k == ring_opt: return ([], [])
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


def make_modified_skin(uifiles, base, new_name):
    """Copy the user's own default / default_modern skin to a custom name LaunchPad won't
    overwrite (so it survives patches), and strip the Gameface (EQLSUI*) files so it is a
    classic-UI skin - identical to the map-pack overlay skins, so one skin can carry both the
    ring and the map overlay. Reuses the skin if it already exists (e.g. the map-pack installer
    made it) so the two don't clobber each other. Returns the dest path, or None."""
    src = os.path.join(uifiles, base)
    dst = os.path.join(uifiles, new_name)
    if os.path.isdir(dst):
        print(f"  '{new_name}' already exists - adding the ring to it.")
    else:
        if not os.path.isdir(src):
            print(f"  ! '{base}' skin not found in uifiles - can't create '{new_name}'.")
            return None
        print(f"  Copying '{base}' -> '{new_name}' (patch-safe classic-UI skin)...")
        shutil.copytree(src, dst)
    stripped = glob.glob(os.path.join(dst, "EQLSUI*.xml"))
    for f in stripped:
        os.remove(f)
    if stripped:
        print(f"    stripped {len(stripped)} Gameface (EQLSUI) files -> classic UI.")
    return dst


def install_ring(uifiles, spin_file, dest_skin="default"):
    """Install the con-colored 3D ring into uifiles\\<dest_skin>. For Sparxx themes that's
    'default' (the themes fall back to it); for a Modified skin it's the skin itself, so the
    ring survives patches. spin_file selects the rotation variant from TargetRing/options/."""
    if not os.path.isdir(RING):
        return False
    dest = os.path.join(uifiles, dest_skin)
    os.makedirs(dest, exist_ok=True)
    copy_into(RING, dest)  # ring frames + TargetIndicator.ini; skips the options/ subfolder
    chosen = os.path.join(RING, "options", spin_file)
    if os.path.isfile(chosen):
        shutil.copy2(chosen, os.path.join(dest, "TargetIndicator.ini"))
    print(f"  + target ring installed into uifiles\\{dest_skin} ({spin_file})")
    return True


def main():
    print("SparxxUI for EverQuest Legends - installer\n")
    themes, modified = choose_target()
    spin_file = choose_spin()

    print("\nOpening a folder browser - pick your EverQuest Legends folder...")
    game = browse_folder()
    if not game or not os.path.isdir(game):
        sys.exit("No valid folder selected.")
    uifiles = resolve_uifiles(game)

    # For an all-install, decide overwrite once up front (Sparxx themes only;
    # Modified skins handle reuse themselves so they don't clobber the map overlay).
    overwrite = True
    existing = [t for t in themes if os.path.isdir(os.path.join(uifiles, t))]
    if existing:
        ans = input(f"\n{len(existing)} of these are already in uifiles. "
                    f"Overwrite them? [y/N]: ").strip().lower()
        overwrite = (ans == "y")

    print(f"\nInstalling to: {uifiles}\n")

    installed = [(t, install_one(t, uifiles, overwrite)) for t in themes]
    installed = [t for t in installed if t[1]]

    made = []
    for new_name, base in modified:
        if make_modified_skin(uifiles, base, new_name):
            made.append(new_name)

    # Ring destinations: into each Modified skin (patch-safe), else into default.
    ring_done = []
    if spin_file:
        for skin in (made if made else ["default"]):
            if install_ring(uifiles, spin_file, skin):
                ring_done.append(skin)
        if not ring_done:
            print("  (TargetRing folder not found - ring not installed)")
    elif themes or made:
        print("  + kept the game's default target ring (Sparxx ring not installed)")

    print("\nDone.")
    if installed:
        print("Load a theme in game with /loadskin <name> 1, for example:")
        for name, _ in installed:
            print(f"  /loadskin {name} 1")
    if made:
        print("Load a patch-safe skin in game with:")
        for name in made:
            print(f'  /loadskin "{name}" 1')
    if ring_done:
        print("Fully restart EverQuest to load the target ring.")
    if not installed and not made and not ring_done:
        print("Nothing was installed.")


if __name__ == "__main__":
    main()
