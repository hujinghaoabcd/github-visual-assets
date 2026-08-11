# Repository Structure v2

## Goals

1. Separate first-party identity from third-party assets.
2. Separate project/profile ownership from generic reuse.
3. Keep large logo collections organized by source.
4. Put semantic classification in metadata instead of moving files between category folders.
5. Avoid duplicate binaries across projects/library/site/exports.
6. Keep provenance and licensing visible before reuse.

## Content domains

- `brand/` — personal/repository/lab identity
- `profile/` — GitHub profile compositions
- `projects/` — project-owned visual kits
- `logos/` — large logo database and curated variants
- `library/` — cross-project reusable components
- `references/` — inspiration/research only

## Support domains

- `templates/` — production templates
- `source/` — editable masters
- `manifest/` — metadata/indexes
- `scripts/` — automation
- `site/` — asset browser
- `docs/` — governance
- `archive/` — retired assets
- `staging/` — review metadata
- `exports/` — batch export workspace

## Duplication rule

Prefer one canonical file plus references. Copy only when a project intentionally forks/modifies an asset; the new copy then needs its own metadata/provenance.
