# Klipper Auto-paste for Wayland

Choose an entry with **Meta+V** and paste it into the previously focused app automatically, including images in browser message fields.

Experimental patch for **KDE Plasma Workspace 6.7.4 / KWin Wayland**, tested on CachyOS. Not an official KDE feature. X11 is unsupported.

## Install on Arch / CachyOS

This builds a modified `plasma-workspace` package. Save your current package for rollback first. Run as your normal user:

```bash
git clone https://github.com/caduHD4/klipper-autopaste-wayland.git
cd klipper-autopaste-wayland
./build-package.sh
sudo pacman -U ./plasma-workspace-6.7.4-3.3-x86_64.pkg.tar.zst
systemctl --user restart plasma-plasmashell.service
```

Open **Configure Clipboard → General** and enable **Automatically paste after choosing an entry**. It defaults to off. Click the destination field, press **Meta+V**, then choose text or an image. The destination must support pasting that content. Terminals using Ctrl+Shift+V may need manual paste.

The build needs Arch's `base-devel` and the dependencies listed in `PKGBUILD`; `makepkg --syncdeps` prompts to install missing dependencies. KDE source signature verification remains enabled. A Plasma shell restart briefly hides panels, without closing your applications.

## After Plasma updates

The build script refuses versions other than **6.7.4**, avoiding an accidental downgrade. A distro update may replace this modification. New Plasma versions need a patch compatibility check, rebuild and playback-independent clipboard tests: see [porting](docs/PORTING.md). There is no automatic update or universal binary installer.

## Remove / rollback

Uncheck the option to disable auto-paste. To remove the patch, reinstall your saved, matching official `plasma-workspace` package, then restart `plasma-plasmashell.service`. Keep the Plasma package set consistent; do not downgrade one package to an older upstream release.

If you previously used the author's **per-user library override**, follow [these removal steps](docs/PORTING.md#existing-per-user-override) too.

## How it works

The patch waits for the selected clipboard data and a Wayland acknowledgement that the popup closed, restores the original window, and sends the standard Paste shortcut through KWin's authenticated fake-input interface. It checks the destination again before injection. Closing the destination, reopening history or timing out cancels pending paste.

Includes the complete patch, pinned package recipe, sync lifetime test and [validation notes](docs/VALIDATION.md). Build outputs, clipboard history and personal configuration are excluded.

GPL-2.0-or-later; upstream file notices remain applicable. See [NOTICE](NOTICE.md) for KDE and original merge-request attribution.
