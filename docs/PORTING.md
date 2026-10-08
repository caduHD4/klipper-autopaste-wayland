# Reapplying after updates

Only Plasma Workspace 6.7.4 is validated. The repository does not automatically merge new KDE releases.

1. Check `pacman -Q plasma-workspace kwin kwayland`. Keep the distribution's Plasma packages consistent.
2. Get the source matching the installed Workspace version from KDE. In a clean source checkout, test the complete patch without modifying files:

   ```bash
   git apply --check /path/to/klipper-autopaste-wayland/klipper-autopaste.patch
   ```

3. If it conflicts, port the affected code manually. If it applies cleanly, inspect the new APIs anyway; patch application does not prove binary or behavior compatibility.
4. Update `pkgver`, source SHA256 and signing-key information in `PKGBUILD` from the matching official release. Update the supported version in `build-package.sh` only after the source changes are reviewed. Do not keep a copied source checksum from another release or disable signature checking.
5. Build against the installed Qt/KDE/KWayland libraries. Never load an old `libklipper.so` into a different Plasma version.
6. Validate text and image paste in a browser; desktop paste; disabled behavior; cancelled selection; reopening history; closed/changed destination; and retained clipboard data on failure. Paste must occur once, after data restoration and focus confirmation. Run the sync smoke test too.
7. Install only a matching package, retaining the distribution package for rollback. Restart the Plasma shell or log out/in.

Other distributions need their native package recipe. This Arch recipe is not a distro-independent installer.

## Existing per-user override

The original local deployment used a library override in `~/.local/lib/klipper-autopaste` and a scoped user service override. Its launcher checks the exact installed package version and falls back to the system library after an incompatible update. This mechanism is not installed by this public repository.

Before switching to a package-only installation, remove that specific service file if present:

```bash
rm -f ~/.config/systemd/user/plasma-plasmashell.service.d/90-klipper-autopaste.conf
systemctl --user daemon-reload
systemctl --user restart plasma-plasmashell.service
```

Keep other service overrides. The optional directory `~/.local/lib/klipper-autopaste` can be removed after confirming it is no longer loaded. Clipboard history and settings do not need to be deleted.
