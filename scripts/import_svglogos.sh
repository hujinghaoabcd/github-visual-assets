#!/usr/bin/env bash
set -euo pipefail

# Source of truth for svglogos.dev. Import every SVG file, not just README/search results.
UPSTREAM_REPO="https://github.com/gilbarbara/logos.git"
DEST_DIR="logos/svglogos"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Cloning SVG Logos upstream..."
git clone --depth 1 "$UPSTREAM_REPO" "$TMP_DIR/upstream"

SOURCE_DIR="$TMP_DIR/upstream/logos"
COUNT="$(find "$SOURCE_DIR" -maxdepth 1 -type f -name '*.svg' | wc -l | tr -d ' ')"
UPSTREAM_SHA="$(git -C "$TMP_DIR/upstream" rev-parse HEAD)"

# The current collection is expected to contain well over 1,800 SVG files.
# Fail loudly instead of silently importing an incomplete clone.
if [ "$COUNT" -lt 1800 ]; then
  echo "ERROR: only $COUNT SVG files found; refusing to import an incomplete collection." >&2
  exit 1
fi

echo "Importing $COUNT SVG files from $UPSTREAM_SHA..."
rm -rf "$DEST_DIR"
mkdir -p "$DEST_DIR" manifest
cp "$SOURCE_DIR"/*.svg "$DEST_DIR"/
cp "$TMP_DIR/upstream/LICENSE.txt" "$DEST_DIR/LICENSE.txt"
cp "$TMP_DIR/upstream/logos.json" "manifest/svglogos-upstream.json"

python3 - "$COUNT" "$UPSTREAM_SHA" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

count = int(sys.argv[1])
sha = sys.argv[2]
meta = {
    "collection": "SVG Logos",
    "website": "https://svglogos.dev/",
    "upstream_repository": "https://github.com/gilbarbara/logos",
    "upstream_commit": sha,
    "license": "CC0-1.0 (collection); individual logos may be subject to trademark rights",
    "svg_file_count": count,
    "imported_at": datetime.now(timezone.utc).isoformat(),
    "local_path": "logos/svglogos/",
}
Path("manifest/svglogos-source.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

cat > "$DEST_DIR/README.md" <<EOF
# SVG Logos mirror

This directory is an automated mirror of the SVG files used by **SVG Logos** (`svglogos.dev`).

- Upstream: https://github.com/gilbarbara/logos
- Upstream commit: `$UPSTREAM_SHA`
- Imported SVG files: **$COUNT**
- Collection license: CC0-1.0 (see `LICENSE.txt`)
- Trademark note: logos and brand marks remain the property of their respective owners and may be subject to trademark/brand usage rules.

Do not edit files in this directory manually. Re-run `scripts/import_svglogos.sh` or the GitHub Actions importer instead.
EOF

echo "Done: $COUNT SVG files imported into $DEST_DIR"
