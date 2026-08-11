#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_REPO="https://github.com/gilbarbara/logos.git"
DEST_DIR="logos/svglogos"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Cloning SVG Logos upstream..."
git clone --depth 1 "$UPSTREAM_REPO" "$TMP_DIR/upstream"

SOURCE_DIR="$TMP_DIR/upstream/logos"
COUNT="$(find "$SOURCE_DIR" -maxdepth 1 -type f -name '*.svg' | wc -l | tr -d ' ')"
UPSTREAM_SHA="$(git -C "$TMP_DIR/upstream" rev-parse HEAD)"

if [ "$COUNT" -lt 1800 ]; then
  echo "ERROR: only $COUNT SVG files found; refusing to import an incomplete collection." >&2
  exit 1
fi

rm -rf "$DEST_DIR"
mkdir -p "$DEST_DIR" manifest/sources
cp "$SOURCE_DIR"/*.svg "$DEST_DIR"/
cp "$TMP_DIR/upstream/LICENSE.txt" "$DEST_DIR/LICENSE.txt"
cp "$TMP_DIR/upstream/logos.json" "manifest/sources/svglogos-upstream.json"

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
Path("manifest/sources/svglogos.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

cat > "$DEST_DIR/README.md" <<EOF
# SVG Logos mirror

Automated mirror of the SVG files used by SVG Logos.

- Website: https://svglogos.dev/
- Upstream: https://github.com/gilbarbara/logos
- Upstream commit: \`$UPSTREAM_SHA\`
- Imported SVG files: **$COUNT**
- Collection license: CC0-1.0 (see \`LICENSE.txt\`)
- Metadata snapshot: \`manifest/sources/svglogos.json\`

Individual logos and brand marks remain the property of their respective owners and may be subject to trademark/brand usage rules.

Do not edit mirrored SVG files manually. Re-run \`scripts/import/svglogos.sh\` or the GitHub Actions importer.
EOF

echo "Done: $COUNT SVG files imported into $DEST_DIR"
