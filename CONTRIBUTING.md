# Contributing

This repository is a curated visual system rather than a general image dump. Add assets only when they fit the design system or serve a clear reusable purpose.

## Before adding an asset

1. Confirm the source and license.
2. Prefer SVG for logos, icons, diagrams and simple illustrations.
3. Keep editable masters in `source/` and publish-ready files in `exports/` when appropriate.
4. Use lowercase kebab-case names.
5. Register third-party assets in both `THIRD_PARTY.md` and `manifest/assets.yml`.
6. Avoid committing fonts, random stock-photo dumps, uncompressed videos, or opaque files with unclear provenance.
7. Run `python scripts/validate_assets.py` before committing.

## Design changes

Changes to brand tokens, logo geometry, typography policy, or core templates should update the relevant documentation and `CHANGELOG.md`.
