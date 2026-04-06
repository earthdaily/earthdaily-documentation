#!/usr/bin/env bash
set -e

PRIVATE_REPO="https://github.com/earthdaily/earthdaily-documentation-protected-content.git"
TMP_DIR="/tmp/earthdaily-docs-private"

# Clone or pull the private repo
if [ -d "$TMP_DIR/.git" ]; then
  echo "  Updating existing clone..."
  git -C "$TMP_DIR" pull --quiet
else
  echo "  Cloning private repo..."
  git clone --quiet "$PRIVATE_REPO" "$TMP_DIR"
fi

# Overwrite stubs with real content
echo "  Copying protected pages..."
cp -r "$TMP_DIR/protected/." docs/

echo "  Done."
