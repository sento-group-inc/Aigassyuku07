#!/usr/bin/env bash
set -euo pipefail

DESIGNLANG_VERSION="13.1.0"
DESIGNLANG_COMMIT="f7c2bec6631bca0da6e8f1a0162d1917bbd46c0c"
DESIGNLANG_REPO="https://github.com/Manavarya09/design-extract.git"

if command -v designlang >/dev/null 2>&1 && [ "$(designlang --version)" = "$DESIGNLANG_VERSION" ]; then
  designlang doctor
  exit 0
fi

node_major="$(node --version | sed -E 's/^v([0-9]+).*/\1/')"
if [ "$node_major" -lt 20 ]; then
  printf 'designlang requires Node.js >= 20; found %s\n' "$(node --version)" >&2
  exit 1
fi

install_tmp="$(mktemp -d /tmp/designlang-install.XXXXXX)"
cleanup() {
  rm -rf "$install_tmp"
}
trap cleanup EXIT

mkdir -p "$install_tmp/pkg"
git clone --depth 1 "$DESIGNLANG_REPO" "$install_tmp/repo"
git -C "$install_tmp/repo" fetch --depth 1 origin "$DESIGNLANG_COMMIT"
git -C "$install_tmp/repo" checkout --detach "$DESIGNLANG_COMMIT"
npm pack "$install_tmp/repo" --pack-destination "$install_tmp/pkg"

package_tarball="$install_tmp/pkg/designlang-$DESIGNLANG_VERSION.tgz"
test -f "$package_tarball"
npm install -g "$package_tarball"

test "$(designlang --version)" = "$DESIGNLANG_VERSION"
designlang doctor
