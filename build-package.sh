#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -euo pipefail
if [[ $# -gt 1 || (${1:-} != '' && ${1:-} != '--check') ]]; then
    echo 'Usage: ./build-package.sh [--check]' >&2
    exit 2
fi
for tool in pacman makepkg; do
    command -v "$tool" >/dev/null || { echo "Required Arch/CachyOS tool missing: $tool" >&2; exit 1; }
done
installed=$(pacman -Q plasma-workspace)
installed=${installed#plasma-workspace }
upstream=${installed%%-*}
if [[ "$upstream" != '6.7.4' ]]; then
    echo "Refusing: installed Plasma Workspace is $installed; this patch supports 6.7.4 only. See docs/PORTING.md." >&2
    exit 1
fi
if [[ ${1:-} == '--check' ]]; then
    echo "Compatible upstream version: $installed. Build and clipboard testing are still required."
    exit 0
fi
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
CMAKE_BUILD_PARALLEL_LEVEL=${CMAKE_BUILD_PARALLEL_LEVEL:-3} makepkg --syncdeps
