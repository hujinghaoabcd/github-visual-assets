# Contributing

This repository is a curated visual asset system, not a general image dump.

## Before adding an asset

1. Decide ownership: `brand`, `profile`, `projects`, `logos`, `library`, or `references`.
2. Confirm source, license and trademark/brand restrictions when third-party material is involved.
3. Prefer SVG for logos, icons, diagrams and simple illustrations.
4. Keep editable masters in `source/`; do not duplicate final assets in `exports/` and their canonical destination.
5. Use safe, descriptive file names.
6. Register provenance/metadata in `THIRD_PARTY.md` and/or `manifest/`.
7. Do not commit font binaries, secrets, private screenshots or unknown-license asset dumps.
8. Run `python scripts/validate/validate_assets.py` before committing.

For large logo imports, preserve source-oriented folders and classify through `manifest/logos/`.
