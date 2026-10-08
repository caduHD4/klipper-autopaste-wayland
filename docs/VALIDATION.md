# Validation

Host: CachyOS, Plasma Workspace 6.7.4, KWin/KWayland 6.7.5, Wayland.

- Original reproduction: an image selected from history was restored successfully, but Qt never emitted the expected focus callback after popup closure. The pending state remained clipboard-ready / focus-not-ready; no Ctrl+V was sent.
- The user confirmed automatic image paste into a browser after the compositor-acknowledgement/original-destination fix.
- Incremental Klipper builds passed. Independent review identified a null-destination risk; the final guard requires valid window management and exact original destination, including no active application for a desktop capture.
- A real Wayland compositor smoke test verified one sync callback and cancellation when the callback's QObject owner is destroyed.
- The complete patch reverse-checks against the built source. Package-recipe signature/source/patch checksums remain enabled.

The source path and per-user override were tested locally. The complete `plasma-workspace 6.7.4-3.3` package build passed locally. The public patch also applied cleanly to the pristine KDE source tarball, matched the final Klipper source, and passed the sync smoke test rebuilt from that patched tarball. The 3.3 package was built but not installed; the confirmed live deployment uses the per-user library override described in the porting notes. Other Plasma releases, distributions and terminal-specific paste shortcuts are unverified. Sanitized diagnostic logs contained state flags, not clipboard contents; diagnostic instrumentation is absent from the shipped patch.

## Tests

Build-script guards (no package build or installation):

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

After the package recipe has extracted/patched `src/plasma-workspace-6.7.4`, run in a Wayland session:

```bash
c++ -std=c++20 tests/wayland-sync-smoke.cpp \
  src/plasma-workspace-6.7.4/klipper/autopastehelpers.cpp \
  -Isrc/plasma-workspace-6.7.4/klipper \
  $(pkg-config --cflags --libs Qt6Gui KWaylandClient wayland-client) \
  -o /tmp/klipper-wayland-sync-smoke
/tmp/klipper-wayland-sync-smoke
```

This does not paste content; it checks asynchronous acknowledgement and lifetime only. Browser auto-paste still requires an end-to-end test with an editable destination.
