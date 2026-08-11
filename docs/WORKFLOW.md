# Asset Workflow

## 1. Decide ownership before creating folders

Choose the canonical destination first:

- `brand/` — first-party personal, repository or lab identity
- `profile/` — GitHub profile-specific compositions
- `projects/<project>/` — assets owned by a specific project
- `logos/` — third-party/brand logo collections and curated logo references
- `library/` — reusable cross-project visual building blocks
- `references/` — inspiration/research that is not automatically reusable

Define target size, format, light/dark behavior and intended use before production.

## 2. Create or collect

Original editable masters belong in `source/`. For third-party material, record the original source, author/organization, license/terms and trademark restrictions before importing or editing it.

Large mirrored logo sets should preserve their upstream/source-oriented organization under `logos/<source>/`; do not manually move thousands of files into semantic category folders.

## 3. Normalize only when appropriate

First-party and curated reusable assets can follow the shared palette, typography, spacing and visual-family rules. Raw mirrored collections should normally remain unmodified so provenance and future synchronization stay clear.

## 4. Register provenance and metadata

For third-party assets/collections, update `THIRD_PARTY.md` and the relevant records under `manifest/`. Record source snapshots under `manifest/sources/`. Logo categories, tags, aliases, variants and duplicate relationships belong under `manifest/logos/` rather than being encoded only in physical folder paths.

## 5. Publish to the owning domain

Approved outputs live with the thing that owns them:

```text
brand/...                identity assets
profile/github/...       profile-only compositions
projects/<project>/...   project-owned assets
library/...              reusable shared assets
logos/...                logo collections / canonical variants
```

`exports/` is a batch/local export workspace, not a second permanent copy of every published asset.

## 6. Screenshots and references

Sanitized screenshots of your own software belong under `projects/<project>/screenshots/`. Screenshots of external websites, GitHub profiles or designs kept for inspiration belong under `references/screenshots/` with source context.

## 7. Validate

Run:

```bash
python scripts/validate/validate_assets.py
```

Check relevant images in GitHub light and dark themes, verify file sizes, and confirm no secrets, private URLs, personal data or local paths appear in screenshots.

## 8. Release and reuse

Use canonical paths for active development. When a visual kit or shared asset set becomes stable, tag a repository release; long-lived documentation can pin that tag instead of depending indefinitely on `main`.

## Lifecycle summary

```text
discover / create
      ↓
provenance + license review
      ↓
source collection OR editable master
      ↓
classify / dedupe / tag
      ↓
curate or compose for profile/project
      ↓
validate / optimize
      ↓
manifest index
      ↓
README / docs / site reuse
      ↓
archive when superseded
```
