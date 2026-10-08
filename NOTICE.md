# Attribution and source

- KDE Plasma Workspace: https://invent.kde.org/plasma/plasma-workspace
- Pinned tag: **v6.7.4**, commit `fd05f4c88ab093aee23ce137bf6f2412437c9bba`.
- Original auto-paste work: Guillermo Steren and contributors, KDE merge request [!6432](https://invent.kde.org/plasma/plasma-workspace/-/merge_requests/6432). The local port used MR commit `98a6dcc44b0cbc3e64530f16f81aaacb388a0421`; the MR was closed/unmerged at the time of this experiment.
- This derivative retains Wayland/KWin input only and adds clipboard-data completion, popup unmap acknowledgement, original-window restoration and cancellation/destination checks.
- `PKGBUILD` derives from the Arch/CachyOS Plasma Workspace 6.7.4 recipe; existing maintainer notices are preserved. This repository is independently maintained and is not an official Arch, CachyOS or KDE package.

The patch preserves upstream copyright/SPDX notices. Newly added Klipper code uses GPL-2.0-or-later. Individual upstream file licenses still apply; obtaining the complete upstream source through the pinned recipe preserves its license files. No KDE binaries or user clipboard databases are included here.
