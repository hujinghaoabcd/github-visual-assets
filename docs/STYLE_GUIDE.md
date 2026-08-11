# Visual Style Guide

## 1. Principle

The system should feel **scientific, modern, spatial and engineered**, not decorative for its own sake. Visual assets must help identify a project, explain it, or make documentation easier to scan.

## 2. Shared identity

All project families share: base dark/light neutrals, one primary blue, consistent title hierarchy, rounded geometry, restrained gradients, clear spacing, vector-first assets and traceable provenance.

## 3. Family cues

### Geo / GIS
Use cyan/blue, map lines, geodesic arcs, coordinate grids, earth contours, spatial nodes, remote-sensing or cartographic motifs. Avoid generic neon globes unless they support the project concept.

### Research
Use clean light backgrounds, indigo accents, plots, equations, structured grids, paper-like spacing and restrained decoration. Prioritize publication clarity.

### AI / Data
Use indigo/violet, graphs, connected nodes, tensor/data-flow abstractions and layered representations. Avoid excessive cyberpunk effects.

### Software
Use teal/blue, interface windows, terminal/code motifs, product cards and clear UI geometry. Keep it closer to a mature developer product than a game UI.

## 4. Color

Core colors are defined in `brand/colors/tokens.json`. Family color should usually occupy less area than neutral background colors; accents are for focus, not full-page saturation.

## 5. Typography

Use strong sans-serif titles and readable system fallbacks. Chinese and Latin text should have compatible weight and visual density. Code labels use monospace. Do not commit font binaries.

## 6. Radius and line language

Prefer 16–28 px radius on large cards/banners, 6–10 px on small UI elements, and rounded line caps for diagrams and network motifs.

## 7. Dark / light mode

Whenever an asset contains text or thin strokes, verify contrast on both GitHub themes. If one file cannot work reliably in both, export explicit `-light` and `-dark` variants.

## 8. Image discipline

Do not mix unrelated illustration styles in one project. A repository should ideally use one illustration family, one icon family and one diagram language.
