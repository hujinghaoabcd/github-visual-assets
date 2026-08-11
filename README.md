<p align="center">
  <img src="brand/repository/banners/readme-hero.svg" alt="GitHub Visual Assets" width="100%" />
</p>

<h1 align="center">GitHub Visual Assets</h1>

<p align="center">A scalable personal visual asset management system for GitHub profiles, research, Geo/GIS, AI, software projects and reusable design resources.</p>

## Repository model

This repository is organized by **ownership and reuse**, not only by file format.

```text
brand/          first-party personal / repository / lab identity
profile/        GitHub profile-specific visual kit
projects/       one complete visual kit per first-party project
logos/          large logo database, grouped by source + curated subset
library/        reusable banners, illustrations, animations, icons, backgrounds, badges and mockups
references/     inspiration / screenshots / moodboards; not automatically redistributable
templates/      reusable production templates
source/         editable design masters
manifest/       taxonomy, provenance, aliases, variants, duplicates and indexes
scripts/        import / sync / classify / dedupe / optimize / validate tools
site/           future searchable asset browser
docs/           architecture, workflow, naming and licensing guidance
archive/        retired / superseded first-party assets
staging/        metadata review before permanent import
exports/        batch-export workspace
```

### Six primary content domains

| Domain | Purpose |
|---|---|
| `brand/` | personal, repository and GeoInnovate-Lab identity |
| `profile/` | GitHub profile README visuals |
| `projects/` | project-owned visual kits |
| `logos/` | brand/logo database and source collections |
| `library/` | shared reusable visual building blocks |
| `references/` | visual research and inspiration only |

## Important rules

1. **Do not duplicate shared assets.** Projects/profile reference canonical files from `library/` or `logos/` unless intentionally modified.
2. **Large logo sets stay source-oriented.** Classification lives in `manifest/logos/`; do not physically move tens of thousands of SVGs between category folders.
3. **Project screenshots belong to the project.** External inspiration screenshots belong in `references/screenshots/`.
4. **Editable source is not the published asset.** Masters live in `source/`; approved outputs live with their owning brand/profile/project/library entry.
5. **Unknown-license material is not a reusable asset.** Keep provenance and usage terms traceable.

## Project visual kit

Copy `projects/_template/` for each repository. A mature kit can contain identity, README visuals, covers, publication graphics, social cards, diagrams, figures, screenshots, demos, documentation artwork and previews.

## GitHub profile visual kit

`profile/github/` is a dedicated system for hero artwork, intro blocks, section headers, research presentation, tech-stack compositions, project cards, statistics, contribution art, social/contact sections, decorations and previews.

## Logo database

`logos/svglogos/` currently contains the SVG Logos mirror. Future source collections such as WorldVectorLogo, detain/svg-logos, Simple Icons, Devicon, SVGL and Dashboard Icons have dedicated folders. Canonical brand IDs, aliases, variants and duplicate relationships belong in `manifest/logos/`.

## Starter catalog

See [`CATALOG.md`](CATALOG.md).

## Documentation

- [`docs/architecture/REPOSITORY_STRUCTURE.md`](docs/architecture/REPOSITORY_STRUCTURE.md)
- [`docs/architecture/ASSET_LIFECYCLE.md`](docs/architecture/ASSET_LIFECYCLE.md)
- [`docs/STYLE_GUIDE.md`](docs/STYLE_GUIDE.md)
- [`docs/ASSET_SPEC.md`](docs/ASSET_SPEC.md)
- [`docs/NAMING.md`](docs/NAMING.md)
- [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
- [`docs/LICENSING.md`](docs/LICENSING.md)

## Licensing

Code/helpers use [`LICENSE`](LICENSE). Original visual assets use [`LICENSE-ASSETS`](LICENSE-ASSETS) unless stated otherwise. Third-party sources and restrictions are tracked in [`THIRD_PARTY.md`](THIRD_PARTY.md) and `manifest/`.
