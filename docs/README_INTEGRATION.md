# README Integration

## Same repository

Prefer relative paths when the visual asset lives in the same repository:

```html
<img src="docs/assets/hero.svg" width="100%" alt="Project hero" />
```

## Reusing the central visual library

Use the canonical file that owns the asset. For example, a reusable GIS banner can be referenced directly from `library/`:

```html
<img src="https://raw.githubusercontent.com/hujinghaoabcd/github-visual-assets/main/library/banners/gis/gis-hero.svg" width="100%" alt="GIS hero" />
```

Repository identity assets live under `brand/`, GitHub-profile-only compositions under `profile/`, project-specific artwork under `projects/<project>/`, shared visual building blocks under `library/`, and brand/logo collections under `logos/`.

For long-lived documentation, replace `main` with a stable release tag when practical.

## Do not duplicate canonical assets

If several projects use the same illustration, animation, background or logo variant, keep one canonical file and reference it. Copy a file into a project only when the project intentionally modifies/forks that asset; the modified copy then needs its own provenance/metadata.

Do not use files from `references/` as reusable production assets by default. That area is for design research and inspiration and does not imply redistribution rights.

## Recommended README visual order

1. Hero / logo
2. Project title and one-line value proposition
3. Meaningful badges
4. Short overview
5. Architecture / workflow visual
6. Features
7. Installation and quick start
8. Demo / screenshots
9. Results / benchmarks when relevant
10. Citation / license / acknowledgements

Do not turn every README section into an image. Text should remain searchable, accessible and easy to maintain.
