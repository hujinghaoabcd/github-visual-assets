#!/usr/bin/env python3
"""Migrate github-visual-assets to the scalable v2 visual asset architecture.

This migration is intentionally idempotent. It preserves existing assets, moves
legacy top-level asset folders into their new domains, creates the full folder
skeleton, updates paths/metadata/workflows, and rewrites the repository overview.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def git_mv(src: str, dst: str) -> None:
    s = ROOT / src
    d = ROOT / dst
    if not s.exists():
        return
    if d.exists():
        # Merge directories safely if a destination was created by an earlier run.
        if s.is_dir() and d.is_dir():
            for child in list(s.iterdir()):
                target = d / child.name
                if target.exists():
                    continue
                run("git", "mv", str(child.relative_to(ROOT)), str(target.relative_to(ROOT)))
            try:
                s.rmdir()
            except OSError:
                pass
            return
        return
    d.parent.mkdir(parents=True, exist_ok=True)
    run("git", "mv", src, dst)


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_leaf(path: str) -> None:
    p = ROOT / path
    p.mkdir(parents=True, exist_ok=True)
    marker = p / ".gitkeep"
    if not any(p.iterdir()):
        marker.write_text("", encoding="utf-8")


def remove_placeholder_dir(path: str, fallback: str) -> None:
    p = ROOT / path
    if not p.exists():
        return
    files = [x for x in p.rglob("*") if x.is_file()]
    substantive = [x for x in files if x.name not in {"README.md", ".gitkeep"}]
    if substantive:
        git_mv(path, fallback)
    else:
        run("git", "rm", "-r", path)


def replace_text(path: str, replacements: dict[str, str]) -> None:
    p = ROOT / path
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Move current assets into the new ownership model.
# ---------------------------------------------------------------------------
git_mv("brand/logo", "brand/repository/logo")
git_mv("brand/banners", "brand/repository/banners")

git_mv("banners", "library/banners")
git_mv("illustrations", "library/illustrations")
git_mv("animations", "library/animations")
git_mv("icons", "library/icons")
git_mv("badges", "library/badges")
git_mv("backgrounds", "library/backgrounds")

git_mv("logos/svglogos", "collections/logos/svglogos")

remove_placeholder_dir("project-covers", "projects/_unassigned/project-covers")
remove_placeholder_dir("screenshots", "projects/_unassigned/screenshots")

# Move operational files into function-based script / manifest folders.
git_mv("scripts/import_svglogos.sh", "scripts/import/svglogos.sh")
git_mv("scripts/validate_assets.py", "scripts/validate/validate_assets.py")
git_mv("manifest/svglogos-source.json", "manifest/sources/svglogos.json")
git_mv("manifest/svglogos-upstream.json", "manifest/sources/svglogos-upstream.json")

# ---------------------------------------------------------------------------
# 2. Materialize the complete folder model. Empty leaves get .gitkeep.
# ---------------------------------------------------------------------------
leaves = [
    # Brand
    "brand/personal/logo", "brand/personal/avatar", "brand/personal/signature",
    "brand/personal/colors", "brand/personal/typography",
    "brand/geo-innovate-lab/logo", "brand/geo-innovate-lab/colors",
    "brand/geo-innovate-lab/typography", "brand/geo-innovate-lab/brand-guide",
    # GitHub profile
    "profile/github/hero", "profile/github/intro", "profile/github/about",
    "profile/github/section-headers", "profile/github/tech-stack",
    "profile/github/research", "profile/github/project-cards",
    "profile/github/stats", "profile/github/contribution-art",
    "profile/github/social", "profile/github/decorations", "profile/github/footer",
    "profile/github/previews",
    # Project template
    "projects/_template/identity/logo", "projects/_template/readme/hero",
    "projects/_template/readme/section-headers", "projects/_template/readme/badges",
    "projects/_template/covers", "projects/_template/social",
    "projects/_template/diagrams", "projects/_template/figures",
    "projects/_template/screenshots", "projects/_template/demos",
    "projects/_template/docs", "projects/_template/previews",
    "projects/_unassigned",
    # Reusable library
    "library/illustrations/coding", "library/illustrations/research",
    "library/illustrations/gis", "library/illustrations/ai",
    "library/illustrations/data", "library/illustrations/office",
    "library/animations/coding", "library/animations/terminal",
    "library/animations/rocket", "library/animations/earth",
    "library/animations/data-flow", "library/animations/loaders",
    "library/backgrounds/gradients", "library/backgrounds/grids",
    "library/backgrounds/maps", "library/backgrounds/particles",
    "library/backgrounds/abstract", "library/backgrounds/patterns",
    "library/backgrounds/textures",
    "library/banners/github", "library/banners/research", "library/banners/gis",
    "library/banners/ai", "library/banners/software",
    "library/icons/ui", "library/icons/maps", "library/icons/charts",
    "library/icons/files", "library/icons/arrows", "library/icons/social",
    "library/badges/custom", "library/badges/shields", "library/badges/status",
    "library/decorations/dividers", "library/decorations/waves",
    "library/decorations/blobs", "library/decorations/dots",
    "library/decorations/shapes",
    "library/mockups/browser", "library/mockups/terminal", "library/mockups/desktop",
    "library/mockups/laptop", "library/mockups/mobile",
    # Upstream collections
    "collections/logos/detain", "collections/logos/worldvectorlogo",
    "collections/logos/simple-icons", "collections/logos/devicon",
    "collections/logos/svgl", "collections/logos/dashboard-icons",
    "collections/logos/vectorlogozone",
    "collections/icons", "collections/illustrations", "collections/animations",
    # References / inspiration (not redistributable assets by default)
    "references/screenshots/websites", "references/screenshots/github-profiles",
    "references/screenshots/readmes", "references/screenshots/dashboards",
    "references/screenshots/apps", "references/moodboards", "references/links",
    "references/palettes", "references/typography",
    # Templates
    "templates/github-profile", "templates/readme", "templates/hero",
    "templates/diagrams", "templates/cards", "templates/posters",
    # Editable masters
    "source/brand", "source/profile", "source/projects", "source/library",
    "source/figma", "source/illustrator", "source/photoshop", "source/drawio",
    "source/blender", "source/animation",
    # Metadata
    "manifest/taxonomy", "manifest/logos", "manifest/sources",
    "manifest/licenses", "manifest/schemas", "manifest/indices",
    # Automation
    "scripts/sync", "scripts/classify", "scripts/dedupe", "scripts/optimize",
    "scripts/thumbnails", "scripts/build-index",
    # Site
    "site/src/components", "site/src/layouts", "site/src/pages",
    "site/src/styles", "site/src/lib", "site/public",
    # Documentation
    "docs/architecture", "docs/workflow", "docs/naming", "docs/licensing",
    "docs/contribution", "docs/site",
    # Archive
    "archive/retired", "archive/superseded",
    # Staging metadata only; raw unreviewed assets stay local in _work/_private.
    "staging/manifests", "staging/review",
]
for leaf in leaves:
    ensure_leaf(leaf)

# ---------------------------------------------------------------------------
# 3. Seed structure docs and metadata.
# ---------------------------------------------------------------------------
write(
    "brand/README.md",
    """# Brand\n\nFirst-party identity only. This area is reserved for the owner's personal identity, the repository identity, and GeoInnovate-Lab identity. Third-party logos never belong here.\n\n- `personal/` — personal logo, avatar, signature, palette and typography references\n- `repository/` — GitHub Visual Assets repository identity\n- `geo-innovate-lab/` — lab identity and brand guide\n\nFont binaries are not vendored here; record font names, licenses and source links instead.""",
)
write(
    "profile/README.md",
    """# Profile\n\nProfile-specific visual systems. `github/` contains assets assembled specifically for the GitHub profile README: hero, intro, section headers, research blocks, tech-stack presentation, project cards, stats framing, contribution art, social links and previews.\n\nReusable generic assets should remain in `library/` and be referenced rather than duplicated.""",
)
write(
    "profile/github/README.md",
    """# GitHub Profile Visual Kit\n\nA complete visual kit for the personal GitHub profile.\n\n```text\nhero/               top-of-profile visual\nintro/              name, title, typing lines\nabout/              about-me illustrations/cards\nsection-headers/    reusable section title artwork\ntech-stack/          profile-specific stack compositions (not duplicate logo masters)\nresearch/            research fields, papers, timeline visuals\nproject-cards/       cards pointing to selected repositories\nstats/               wrappers/configuration for dynamic GitHub statistics\ncontribution-art/    snake/calendar/activity visuals\nsocial/              profile contact/social compositions\ndecorations/         profile-only decorative elements\nfooter/              footer artwork\npreviews/            desktop/mobile/full-profile previews\n```\n""",
)
write(
    "projects/README.md",
    """# Projects\n\nOne directory per first-party GitHub project. Copy `_template/` when starting a visual kit. `_unassigned/` is only a temporary holding area for legacy project assets whose owning project is not yet known.\n\nEach project may contain `identity`, `readme`, `covers`, `social`, `diagrams`, `figures`, `screenshots`, `demos`, `docs` and `previews`. Shared imagery belongs in `library/`, not duplicated here.""",
)
write(
    "projects/_template/README.md",
    """# Project Visual Kit Template\n\nCopy this folder to `projects/<repository-name>/`. Keep only sections the project actually needs.\n\n- `identity/` — project logo/icon/colors\n- `readme/` — README hero, section headers and badges\n- `covers/` — repository/social/project covers\n- `social/` — platform-specific share cards/posters\n- `diagrams/` — architecture, workflow and method diagrams\n- `figures/` — plots, maps and publication figures\n- `screenshots/` — sanitized product/terminal/UI screenshots\n- `demos/` — GIF/WebM/demo media references\n- `docs/` — documentation-specific artwork\n- `previews/` — rendered visual-kit previews\n""",
)
write(
    "projects/_template/project.yml",
    """schema_version: 1\nproject_id: replace-me\nrepository: owner/repository\nfamily: software\nstatus: active\nprimary_asset: identity/logo/logo.svg\ntags: []\n""",
)
write(
    "library/README.md",
    """# Library\n\nCurated, reusable visual building blocks that can be shared by profiles and multiple projects. Library assets are reviewed for provenance/usage and should not be raw mirrors of external collections.\n\nMain groups: illustrations, animations, backgrounds, banners, functional icons, badges, decorations and mockups.""",
)
write(
    "collections/README.md",
    """# Collections\n\nLarge third-party/upstream collections kept as close to upstream as practical. Do not manually reorganize mirrored files by semantic category; classification belongs in `manifest/`.\n\n`collections/logos/` is the home for SVG Logos, WorldVectorLogo mirrors, Simple Icons, Devicon and other brand collections. Individual marks can still be restricted by trademark/brand rules even when the collection itself has an open-data/open-source license.""",
)
write(
    "collections/logos/README.md",
    """# Logo Collections\n\nPhysical storage is source-oriented; logical browsing is metadata-oriented.\n\n```text\nsvglogos/\ndetain/\nworldvectorlogo/\nsimple-icons/\ndevicon/\nsvgl/\ndashboard-icons/\nvectorlogozone/\n```\n\nThe website should group aliases and variants into canonical brands through `manifest/logos/` instead of treating every SVG file as a separate brand.""",
)
write(
    "references/README.md",
    """# References\n\nDesign research and inspiration. Content here is **not automatically a reusable or redistributable asset**. Keep source URLs and context. Examples include screenshots of websites/README pages, moodboards, palettes, typography references and link collections.""",
)
write(
    "templates/README.md",
    """# Templates\n\nReusable production templates for GitHub profiles, README layouts, hero banners, project kits, project/social covers, diagrams, cards and posters. Templates create first-party outputs; they are not third-party raw collections.""",
)
write(
    "source/README.md",
    """# Editable Sources\n\nEditable master/project files such as Figma, Illustrator, Photoshop, draw.io, Blender and animation project files. Publish-ready SVG/PNG/WebP/GIF outputs belong in their owning `brand/`, `profile/`, `projects/` or `library/` location rather than being duplicated here. Large binary masters should use Git LFS or external storage.""",
)
write(
    "exports/README.md",
    """# Exports\n\nTemporary/local batch export workspace. Final approved assets should be moved to their owning area (`brand/`, `profile/`, `projects/`, or `library/`). Generated exports are ignored by default to prevent duplicate copies from inflating Git history.""",
)
write(
    "manifest/README.md",
    """# Manifest\n\nMachine-readable metadata is the source of truth for search, categories, provenance, licenses, aliases, variants and duplicate detection. At large scale the website should read manifests/indexes rather than infer meaning from folder names.\n\n- `assets.yml` — existing first-party starter registry\n- `taxonomy/` — category/tag vocabularies\n- `logos/` — canonical brand/alias/variant/dedup metadata\n- `sources/` — upstream collection snapshots\n- `licenses/` — source and restriction metadata\n- `schemas/` — validation schemas\n- `indices/` — generated search/checksum indexes\n""",
)
write(
    "scripts/README.md",
    """# Automation\n\nAutomation is grouped by responsibility: `import`, `sync`, `classify`, `dedupe`, `optimize`, `thumbnails`, `validate`, `build-index`, and `migrate`. Importers should preserve upstream provenance and write source snapshots to `manifest/sources/`.""",
)
write(
    "site/README.md",
    """# Asset Browser Site\n\nFuture Astro-based browsing/search layer. The site should consume `manifest/` plus canonical repository asset paths and **must not duplicate tens of thousands of source assets into `site/public/`**. Build output belongs in `dist/` and is not committed.""",
)
write(
    "archive/README.md",
    """# Archive\n\nRetired or superseded first-party assets kept for history. Archived items are excluded from the default catalog and website search unless explicitly requested.""",
)
write(
    "staging/README.md",
    """# Staging\n\nReview metadata and import plans before assets enter the permanent library/collections. Do not commit unknown-license binaries here. Use ignored local folders (`_work/`, `_private/`) for raw temporary downloads until provenance and reuse terms are verified.""",
)

write(
    "manifest/taxonomy/categories.yml",
    """version: 1\ncategories:\n  - programming-languages\n  - frontend\n  - backend\n  - mobile\n  - desktop\n  - ai-ml\n  - data-science\n  - gis-geospatial\n  - database\n  - cloud\n  - devops\n  - ci-cd\n  - developer-tools\n  - testing\n  - security\n  - monitoring\n  - web-servers\n  - cms\n  - design\n  - operating-systems\n  - browsers\n  - social\n  - communication\n  - productivity\n  - ecommerce\n  - finance-payment\n  - hardware\n  - science\n  - weather-climate\n  - organizations\n  - other\n""",
)
write(
    "manifest/taxonomy/tags.yml",
    """version: 1\npolicy:\n  case: lowercase-kebab-case\n  multi_value: true\n  note: Tags are open-ended; canonical categories are controlled by categories.yml.\n""",
)
write(
    "manifest/logos/README.md",
    """# Canonical Logo Metadata\n\nPlanned generated/curated files:\n\n- `brands.jsonl` — one canonical record per brand\n- `aliases.json` — spelling/name/slug aliases\n- `variants.jsonl` — source-specific files and forms (icon, wordmark, horizontal, etc.)\n- `duplicates.jsonl` — exact and near-duplicate relationships\n- `checksums.jsonl` — normalized SVG/file hashes\n\nDo not physically move mirrored logos into semantic categories; classify them here.""",
)
write(
    "manifest/schemas/asset.schema.json",
    json.dumps(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Visual Asset Record",
            "type": "object",
            "required": ["id", "path", "kind", "origin", "status"],
            "properties": {
                "id": {"type": "string"},
                "path": {"type": "string"},
                "kind": {"type": "string"},
                "origin": {"enum": ["first-party", "third-party", "generated"]},
                "status": {"enum": ["active", "template", "archived", "review"]},
                "source": {"type": ["string", "null"]},
                "license": {"type": ["string", "null"]},
                "category": {"type": ["string", "null"]},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "additionalProperties": True,
        },
        ensure_ascii=False,
        indent=2,
    ),
)

# ---------------------------------------------------------------------------
# 4. Update imported collection metadata and automation paths.
# ---------------------------------------------------------------------------
source_meta = ROOT / "manifest/sources/svglogos.json"
if source_meta.exists():
    data = json.loads(source_meta.read_text(encoding="utf-8"))
    data["local_path"] = "collections/logos/svglogos/"
    source_meta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

importer = ROOT / "scripts/import/svglogos.sh"
if importer.exists():
    text = importer.read_text(encoding="utf-8")
    text = text.replace('DEST_DIR="logos/svglogos"', 'DEST_DIR="collections/logos/svglogos"')
    text = text.replace('"manifest/svglogos-upstream.json"', '"manifest/sources/svglogos-upstream.json"')
    text = text.replace('"manifest/svglogos-source.json"', '"manifest/sources/svglogos.json"')
    text = text.replace('Path("manifest/svglogos-source.json")', 'Path("manifest/sources/svglogos.json")')
    text = text.replace('local_path": "logos/svglogos/"', 'local_path": "collections/logos/svglogos/"')
    importer.write_text(text, encoding="utf-8")

write(
    ".github/workflows/import-svglogos.yml",
    """name: Import SVG Logos\n\non:\n  workflow_dispatch:\n  push:\n    paths:\n      - \".github/workflows/import-svglogos.yml\"\n      - \"scripts/import/svglogos.sh\"\n\npermissions:\n  contents: write\n\njobs:\n  import:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout repository\n        uses: actions/checkout@v4\n        with:\n          fetch-depth: 0\n\n      - name: Import all SVG Logos files\n        run: bash scripts/import/svglogos.sh\n\n      - name: Commit imported collection\n        run: |\n          if git diff --quiet && git diff --cached --quiet && [ -z \"$(git status --porcelain)\" ]; then\n            echo \"No changes to commit.\"\n            exit 0\n          fi\n          git config user.name \"github-actions[bot]\"\n          git config user.email \"41898282+github-actions[bot]@users.noreply.github.com\"\n          git add collections/logos/svglogos manifest/sources/svglogos-upstream.json manifest/sources/svglogos.json\n          git commit -m \"assets: sync complete SVG Logos collection\"\n          git push\n""",
)
write(
    ".github/workflows/validate-assets.yml",
    """name: Validate assets\n\non:\n  push:\n    branches: [main]\n  pull_request:\n\npermissions:\n  contents: read\n\njobs:\n  validate:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: \"3.12\"\n      - name: Validate repository assets\n        run: python scripts/validate/validate_assets.py\n""",
)

replace_text(
    "manifest/assets.yml",
    {
        "brand/logo/": "brand/repository/logo/",
        "brand/banners/": "brand/repository/banners/",
        "path: banners/": "path: library/banners/",
    },
)
replace_text(
    "THIRD_PARTY.md",
    {
        "`logos/svglogos/`": "`collections/logos/svglogos/`",
        "`scripts/import_svglogos.sh`": "`scripts/import/svglogos.sh`",
        "`manifest/svglogos-source.json`": "`manifest/sources/svglogos.json`",
        "`illustrations/...`": "`library/illustrations/...`",
    },
)

# Ignore generated build/export products while keeping documentation in place.
gitignore = ROOT / ".gitignore"
existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
extra = """\n# Generated site/build output\ndist/\nsite/dist/\nsite/.astro/\nsite/node_modules/\n\n# Generated batch exports (README remains tracked)\nexports/**\n!exports/README.md\n\n# Local intake / download scratch space\n_incoming/\n"""
if "# Generated site/build output" not in existing:
    gitignore.write_text(existing.rstrip() + "\n" + extra, encoding="utf-8")

# ---------------------------------------------------------------------------
# 5. Rewrite top-level documentation around the new architecture.
# ---------------------------------------------------------------------------
write(
    "README.md",
    """<p align=\"center\">\n  <img src=\"brand/repository/banners/readme-hero.svg\" alt=\"GitHub Visual Assets\" width=\"100%\" />\n</p>\n\n<h1 align=\"center\">GitHub Visual Assets</h1>\n\n<p align=\"center\">A scalable personal visual asset management system for GitHub profiles, research, Geo/GIS, AI, software projects and reusable design resources.</p>\n\n## Architecture\n\nThis repository separates **ownership**, **reuse**, **upstream collections**, **references**, and **metadata** so it can grow from a few project images to tens of thousands of visual assets without becoming a flat image dump.\n\n```text\nbrand/          first-party personal / repository / lab identity\nprofile/        GitHub profile-specific visual kit\nprojects/       one visual kit per first-party project\nlibrary/        curated reusable visual building blocks\ncollections/    large source-oriented third-party mirrors\nreferences/     inspiration and research; not automatically reusable\ntemplates/      reusable production templates\nsource/         editable master files\nmanifest/       metadata, taxonomy, provenance, aliases, variants, dedup\nscripts/        import/sync/classify/dedupe/optimize/validate/build tools\nsite/           future browsing/search website\ndocs/           architecture and workflow documentation\narchive/        retired/superseded first-party assets\nstaging/        metadata review before permanent import\nexports/        local/generated export workspace\n```\n\n### Six content domains\n\n| Domain | Meaning | Example |\n|---|---|---|\n| `brand/` | Who I am | personal avatar, repository mark, lab palette |\n| `profile/` | How my GitHub profile is presented | hero, research block, project cards |\n| `projects/` | How each repository is presented | project logo, architecture diagram, screenshots |\n| `library/` | Reusable visual building blocks | coding GIF, GIS background, divider, mockup |\n| `collections/` | Raw/source-oriented third-party sets | SVG Logos, WorldVectorLogo, Devicon |\n| `references/` | Inspiration/reference only | website screenshots, moodboards, palettes |\n\n## Key rule: physical storage != logical classification\n\nLarge upstream logo collections stay grouped by **source** under `collections/`. Categories, tags, canonical brand IDs, aliases, variants and duplicate relationships live in `manifest/`. The future website reads those indexes instead of moving tens of thousands of SVG files between category folders.\n\n## Project visual kit\n\nCopy `projects/_template/` for a new repository. A mature project may contain:\n\n```text\nidentity/\nreadme/\ncovers/\nsocial/\ndiagrams/\nfigures/\nscreenshots/\ndemos/\ndocs/\npreviews/\nproject.yml\n```\n\n## GitHub profile kit\n\n`profile/github/` is reserved for assets assembled specifically for the personal profile: hero, intro, section headers, tech-stack presentation, research blocks, selected project cards, stats framing, contribution art, social blocks, decorations and previews. Generic pieces should remain in `library/` and be referenced rather than copied.\n\n## Current external collection\n\nSVG Logos is mirrored under `collections/logos/svglogos/`. The importer records its exact upstream commit and file count in `manifest/sources/svglogos.json`. Individual logos may still be governed by trademark/brand rules.\n\n## Starter catalog\n\nSee [`CATALOG.md`](CATALOG.md) for the existing first-party starter visuals.\n\n## Provenance and licensing\n\n- Code/helper scripts: [`LICENSE`](LICENSE)\n- Original first-party visual assets: [`LICENSE-ASSETS`](LICENSE-ASSETS)\n- Third-party sources: [`THIRD_PARTY.md`](THIRD_PARTY.md) and `manifest/sources/`\n- Never treat `references/` as a redistributable asset library by default.\n\n## Documentation\n\n- [`docs/architecture/REPOSITORY_STRUCTURE.md`](docs/architecture/REPOSITORY_STRUCTURE.md)\n- [`docs/architecture/ASSET_LIFECYCLE.md`](docs/architecture/ASSET_LIFECYCLE.md)\n- [`docs/STYLE_GUIDE.md`](docs/STYLE_GUIDE.md)\n- [`docs/ASSET_SPEC.md`](docs/ASSET_SPEC.md)\n- [`docs/NAMING.md`](docs/NAMING.md)\n- [`docs/WORKFLOW.md`](docs/WORKFLOW.md)\n- [`docs/LICENSING.md`](docs/LICENSING.md)\n\n<p align=\"center\"><sub>Built as long-term visual infrastructure for open-source and research projects.</sub></p>\n""",
)
write(
    "CATALOG.md",
    """# Starter Asset Catalog\n\nThis page previews first-party starter assets that survived the v2 repository restructure.\n\n## Repository identity\n\n### Repository mark\n<img src=\"brand/repository/logo/primary/repository-mark.svg\" width=\"180\" alt=\"Repository mark\" />\n\n### Core palette\n<img src=\"brand/colors/palette.svg\" width=\"850\" alt=\"Core palette\" />\n\n## Reusable README heroes\n\n### Generic\n<img src=\"library/banners/generic/generic-hero.svg\" width=\"850\" alt=\"Generic hero\" />\n\n### Geo / GIS\n<img src=\"library/banners/gis/gis-hero.svg\" width=\"850\" alt=\"GIS hero\" />\n\n### Research\n<img src=\"library/banners/research/research-hero.svg\" width=\"850\" alt=\"Research hero\" />\n\n### AI / Data\n<img src=\"library/banners/ai/ai-hero.svg\" width=\"850\" alt=\"AI hero\" />\n\n### Software\n<img src=\"library/banners/software/software-hero.svg\" width=\"850\" alt=\"Software hero\" />\n\n## Templates\n\n### Project cover\n<img src=\"templates/project-cover/project-cover-template.svg\" width=\"720\" alt=\"Project cover template\" />\n\n### Social preview\n<img src=\"templates/social-preview/social-preview-template.svg\" width=\"720\" alt=\"Social preview template\" />\n\n### Compact README banner\n<img src=\"templates/banner/readme-banner-template.svg\" width=\"850\" alt=\"Compact README banner template\" />\n\n### Custom badge\n<img src=\"library/badges/custom/research-ready.svg\" width=\"200\" alt=\"Research ready badge\" />\n\n## Background\n<img src=\"library/backgrounds/gradient/base-gradient.svg\" width=\"720\" alt=\"Base gradient background\" />\n\nLarge mirrored collections are intentionally not rendered in this Markdown catalog; the future `site/` index will provide search, filtering and variants.\n""",
)
write(
    "docs/architecture/REPOSITORY_STRUCTURE.md",
    """# Repository Structure v2\n\n## Design goals\n\n1. Keep first-party identity separate from third-party assets.\n2. Keep project/profile ownership separate from generic reuse.\n3. Preserve large upstream collections by source rather than manually rearranging them.\n4. Make metadata the source of truth for search, categories, aliases, variants and duplicates.\n5. Avoid storing the same binary in `projects`, `library`, `site/public` and `exports`.\n6. Make licensing/provenance visible before reuse.\n\n## Top-level ownership model\n\n- `brand/` — personal/repository/lab identity\n- `profile/` — GitHub profile compositions\n- `projects/` — project-owned visual kits\n- `library/` — curated cross-project components\n- `collections/` — large upstream mirrors\n- `references/` — inspiration only\n- `templates/` — production templates\n- `source/` — editable masters\n- `manifest/` — asset database\n- `scripts/` — automation\n- `site/` — catalog UI\n- `archive/` — retired outputs\n- `staging/` — pre-import metadata review\n\n## Duplication rule\n\nPrefer one canonical file plus references. A project may reference `library/animations/coding/...` or a canonical logo variant from `collections/` through metadata. Copy only when a project intentionally forks/modifies an asset and the new copy has its own provenance record.\n""",
)
write(
    "docs/architecture/ASSET_LIFECYCLE.md",
    """# Asset Lifecycle\n\n```text\ndiscover / create\n      ↓\nlicense + provenance review\n      ↓\nsource collection OR editable master\n      ↓\nclassify / dedupe / tag\n      ↓\ncurate or project/profile composition\n      ↓\nvalidate / optimize / thumbnail\n      ↓\nmanifest index\n      ↓\nREADME / docs / site reuse\n      ↓\narchive when superseded\n```\n\nThird-party assets with unclear reuse terms should remain outside the permanent public asset store until reviewed. `references/` is not a shortcut around licensing: it is for context and research, not automatic redistribution.\n""",
)

# Keep old docs functional where they contain known legacy paths.
for path in [
    "docs/ASSET_SPEC.md", "docs/NAMING.md", "docs/WORKFLOW.md",
    "docs/README_INTEGRATION.md", "docs/LICENSING.md", "docs/PROJECT_CHECKLIST.md",
    "CONTRIBUTING.md",
]:
    replace_text(
        path,
        {
            "brand/logo/": "brand/repository/logo/",
            "brand/banners/": "brand/repository/banners/",
            "project-covers/": "projects/",
            "banners/generic/": "library/banners/generic/",
            "banners/gis/": "library/banners/gis/",
            "banners/research/": "library/banners/research/",
            "banners/ai/": "library/banners/ai/",
            "banners/software/": "library/banners/software/",
            "badges/custom/": "library/badges/custom/",
            "backgrounds/gradient/": "library/backgrounds/gradient/",
        },
    )

print("Repository structure v2 migration complete.")
