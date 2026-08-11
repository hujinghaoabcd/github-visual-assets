# Asset Specification

## Recommended dimensions

| Asset | Size | Notes |
|---|---:|---|
| Avatar | 800 × 800 | central 80% safe zone |
| README Hero | 1600 × 600 | default repository header |
| Compact Banner | 1600 × 400 | dense README pages |
| Social Preview | 1280 × 640 | GitHub repository social image |
| Project Cover | 1200 × 630 | general sharing / cards |
| Square Card | 1000 × 1000 | catalog / social use |
| Documentation Header | 1600 × 360 | documentation landing pages |
| Logo | SVG master | scalable vector preferred |
| Logo PNG | 512 / 1024 square | transparent background |
| Screenshot | 1600 px+ wide | crop intentionally |

## Format policy

- **SVG:** logos, icons, diagrams, banners with vector art, lightweight illustrations.
- **PNG:** transparency, screenshots when lossless detail matters.
- **WebP:** compact raster illustrations and screenshots for web delivery.
- **GIF:** only when README compatibility is more important than compression.
- **Lottie JSON:** source animation when redistribution is licensed; export a README-safe fallback too.

## Export quality

Remove editor metadata, hidden layers and unused definitions. Keep SVG `viewBox`. Raster exports should be large enough for HiDPI viewing without being unnecessarily huge.

## File size policy

Aim for <2 MiB for common README assets. Optimize decorative animations aggressively. Files >20 MiB trigger a repository warning; files >50 MiB fail validation and should usually use Git LFS or release assets.
