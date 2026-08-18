# SparxxUI for EverQuest Legends - installer (PowerShell, no dependencies).
#
# Pick a Sparxx theme (or a patch-safe "Modified Default / Modified Modern" skin), browse to
# your EverQuest Legends folder, and the skin(s) plus the shared 3D target ring are copied into
# uifiles ready to load.
#
#   - A Sparxx theme installs as a custom skin; the ring goes into uifiles\default (the themes
#     fall back to default, so the ring shows for any of them).
#   - "Modified Default / Modified Modern" are patch-safe, classic-style copies of your own
#     default / default_modern skin. Modified Modern copies the "modern" UI (the default_modern
#     folder); Modified Default copies the "default" folder. The Gameface (EQLSUI) files are
#     stripped so they render in the classic UI style like the Sparxx themes; LaunchPad won't
#     overwrite the custom name; and the ring is installed into them so it survives patches.
#
# Needs no Python - Windows PowerShell (built in) runs this. Launch it with Install.bat.

$ErrorActionPreference = 'Stop'

$HERE = $PSScriptRoot
if (-not $HERE) { $HERE = Split-Path -Parent $MyInvocation.MyCommand.Path }
$RING = Join-Path $HERE 'TargetRing'

$THEMES = @('SparxxDark','SparxxObsidian','SparxxVenom','SparxxEmber','SparxxRed','SparxxGold','SparxxBronze')
# (new skin name, base skin folder to copy). Modified Modern copies the "modern" UI
# (the default_modern folder); Modified Default copies the "default" folder.
$MODIFIED = @(
    @('Modified Default','default'),
    @('Modified Modern','default_modern')
)
$RING_OPTIONS = @(
    @('no-spin.ini',   'Sparxx ring, no spin - static (fastest to load)'),
    @('spin-slow.ini', 'Sparxx ring, slow spin'),
    @('spin.ini',      'Sparxx ring, normal spin'),
    @('spin-fast.ini', 'Sparxx ring, fast spin'),
    @('',              'Keep the game''s default ring (don''t install the Sparxx ring)')
)


function Choose-Target {
    # Returns a hashtable @{ Themes = <string[]>; Modified = <pair[]> }.
    # Both empty means 'target ring only' (into default).
    Write-Host "Available themes:`n"
    for ($i = 0; $i -lt $THEMES.Count; $i++) {
        Write-Host ("  {0}. {1}" -f ($i + 1), $THEMES[$i])
    }
    $n = $THEMES.Count
    $allOpt = $n + 1; $mdOpt = $n + 2; $mmOpt = $n + 3; $bothOpt = $n + 4; $ringOpt = $n + 5
    Write-Host "  $allOpt. Install ALL Sparxx themes"
    Write-Host "  $mdOpt. Modified Default  (patch-safe copy of your 'default' skin + ring)"
    Write-Host "  $mmOpt. Modified Modern   (patch-safe copy of your 'default_modern' skin + ring)"
    Write-Host "  $bothOpt. Both Modified skins"
    Write-Host "  $ringOpt. Target ring only (into default)"
    while ($true) {
        $pick = (Read-Host "`nChoose [1-$ringOpt]").Trim()
        if ($pick -match '^\d+$') {
            $k = [int]$pick
            if ($k -ge 1 -and $k -le $n) { return @{ Themes = @($THEMES[$k - 1]); Modified = @() } }
            if ($k -eq $allOpt)  { return @{ Themes = $THEMES;  Modified = @() } }
            if ($k -eq $mdOpt)   { return @{ Themes = @();      Modified = @(,$MODIFIED[0]) } }
            if ($k -eq $mmOpt)   { return @{ Themes = @();      Modified = @(,$MODIFIED[1]) } }
            if ($k -eq $bothOpt) { return @{ Themes = @();      Modified = $MODIFIED } }
            if ($k -eq $ringOpt) { return @{ Themes = @();      Modified = @() } }
        }
        Write-Host "Please enter a number from the list."
    }
}


function Choose-Spin {
    Write-Host "`nTarget ring:"
    for ($i = 0; $i -lt $RING_OPTIONS.Count; $i++) {
        Write-Host ("  {0}. {1}" -f ($i + 1), $RING_OPTIONS[$i][1])
    }
    while ($true) {
        $pick = (Read-Host "Choose [1-$($RING_OPTIONS.Count)] (Enter = 1)").Trim()
        if ($pick -eq '') { return $RING_OPTIONS[0][0] }
        if ($pick -match '^\d+$' -and [int]$pick -ge 1 -and [int]$pick -le $RING_OPTIONS.Count) {
            return $RING_OPTIONS[[int]$pick - 1][0]
        }
        Write-Host "Please enter a number from the list."
    }
}


function Browse-Folder {
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
        $dlg.Description = 'Select your EverQuest Legends folder (contains eqgame.exe)'
        $dlg.ShowNewFolderButton = $false
        if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            return $dlg.SelectedPath
        }
    } catch { }
    return (Read-Host 'Paste the path to your EverQuest Legends folder').Trim('"', ' ')
}


function Resolve-Uifiles($folder) {
    # Accept the game root, the uifiles folder, or a folder holding eqgame.exe.
    $folder = [System.IO.Path]::GetFullPath($folder)
    if ((Split-Path $folder -Leaf).ToLower() -eq 'uifiles') { return $folder }
    $ui = Join-Path $folder 'uifiles'
    if (Test-Path $ui -PathType Container) { return $ui }
    New-Item -ItemType Directory -Force -Path $ui | Out-Null
    return $ui
}


function Copy-Into($srcDir, $dstDir) {
    Get-ChildItem -LiteralPath $srcDir -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $dstDir $_.Name) -Force
    }
}


function Install-One($theme, $uifiles, $overwrite) {
    $themeDir = Join-Path $HERE $theme
    if (-not (Test-Path $themeDir -PathType Container)) {
        Write-Host "  ! ${theme}: source folder not found, skipped"
        return $null
    }
    $dest = Join-Path $uifiles $theme
    if (Test-Path $dest -PathType Container) {
        if (-not $overwrite) { Write-Host "  - ${theme}: already installed, skipped"; return $null }
        Remove-Item -LiteralPath $dest -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Into $themeDir $dest
    Write-Host "  + $theme installed"
    return $dest
}


function Make-ModifiedSkin($uifiles, $base, $newName) {
    # Make a patch-safe, classic-style copy of the user's own default / default_modern skin.
    # Copies the base to a custom name LaunchPad won't overwrite, strips the Gameface (EQLSUI*)
    # files so it renders in the classic UI style like the Sparxx themes, and (via the caller)
    # installs the ring. Regenerates the skin if it already exists so a patch's changes to the
    # base skin are picked up.
    $src = Join-Path $uifiles $base
    $dst = Join-Path $uifiles $newName
    if (-not (Test-Path $src -PathType Container)) {
        Write-Host "  ! '$base' skin not found in uifiles - can't create '$newName'."
        return $null
    }
    if (Test-Path $dst -PathType Container) {
        Write-Host "  Refreshing '$newName' from '$base' (picks up patch changes)..."
        Remove-Item -LiteralPath $dst -Recurse -Force
    } else {
        Write-Host "  Copying '$base' -> '$newName' (patch-safe classic-style skin)..."
    }
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
    $stripped = @(Get-ChildItem -LiteralPath $dst -Filter 'EQLSUI*.xml' -File)
    foreach ($f in $stripped) { Remove-Item -LiteralPath $f.FullName -Force }
    if ($stripped.Count -gt 0) {
        Write-Host "    stripped $($stripped.Count) Gameface (EQLSUI) file(s) -> classic UI."
    }
    return $dst
}


function Install-Ring($uifiles, $spinFile, $destSkin = 'default') {
    # Install the con-colored 3D ring into uifiles\<destSkin>. For Sparxx themes that's
    # 'default' (the themes fall back to it); for a Modified skin it's the skin itself, so the
    # ring survives patches. spinFile selects the rotation variant from TargetRing\options.
    if (-not (Test-Path $RING -PathType Container)) { return $false }
    $dest = Join-Path $uifiles $destSkin
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Into $RING $dest   # ring frames + TargetIndicator.ini; skips the options\ subfolder
    $chosen = Join-Path (Join-Path $RING 'options') $spinFile
    if (Test-Path $chosen -PathType Leaf) {
        Copy-Item -LiteralPath $chosen -Destination (Join-Path $dest 'TargetIndicator.ini') -Force
    }
    Write-Host "  + target ring installed into uifiles\$destSkin ($spinFile)"
    return $true
}


function Main {
    Write-Host "SparxxUI for EverQuest Legends - installer`n"
    $target = Choose-Target
    $themes = @($target.Themes)
    $modified = @($target.Modified)
    $spinFile = Choose-Spin

    Write-Host "`nOpening a folder browser - pick your EverQuest Legends folder..."
    $game = Browse-Folder
    if (-not $game -or -not (Test-Path $game -PathType Container)) {
        Write-Host "No valid folder selected."
        exit 1
    }
    $uifiles = Resolve-Uifiles $game

    # For an all-install, decide overwrite once up front (Sparxx themes only; Modified skins
    # handle reuse themselves so they don't clobber the map overlay).
    $overwrite = $true
    $existing = @($themes | Where-Object { Test-Path (Join-Path $uifiles $_) -PathType Container })
    if ($existing.Count -gt 0) {
        $ans = (Read-Host "`n$($existing.Count) of these are already in uifiles. Overwrite them? [y/N]").Trim().ToLower()
        $overwrite = ($ans -eq 'y')
    }

    Write-Host "`nInstalling to: $uifiles`n"

    $installed = @()
    foreach ($t in $themes) {
        $d = Install-One $t $uifiles $overwrite
        if ($d) { $installed += ,@($t, $d) }
    }

    $made = @()
    foreach ($pair in $modified) {
        if (Make-ModifiedSkin $uifiles $pair[1] $pair[0]) { $made += $pair[0] }
    }

    # Ring destinations: into each Modified skin (patch-safe), else into default.
    $ringDone = @()
    if ($spinFile) {
        $targets = if ($made.Count -gt 0) { $made } else { @('default') }
        foreach ($skin in $targets) {
            if (Install-Ring $uifiles $spinFile $skin) { $ringDone += $skin }
        }
        if ($ringDone.Count -eq 0) { Write-Host "  (TargetRing folder not found - ring not installed)" }
    } elseif ($themes.Count -gt 0 -or $made.Count -gt 0) {
        Write-Host "  + kept the game's default target ring (Sparxx ring not installed)"
    }

    Write-Host "`nDone."
    if ($installed.Count -gt 0) {
        Write-Host "Load a theme in game with /loadskin <name> 1, for example:"
        foreach ($it in $installed) { Write-Host "  /loadskin $($it[0]) 1" }
    }
    if ($made.Count -gt 0) {
        Write-Host "Load a patch-safe skin in game with:"
        foreach ($name in $made) { Write-Host "  /loadskin `"$name`" 1" }
    }
    if ($ringDone.Count -gt 0) { Write-Host "Fully restart EverQuest to load the target ring." }
    if ($installed.Count -eq 0 -and $made.Count -eq 0 -and $ringDone.Count -eq 0) {
        Write-Host "Nothing was installed."
    }
}

Main
