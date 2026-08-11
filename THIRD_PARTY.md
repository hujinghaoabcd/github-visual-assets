# Third-Party Asset Registry

Every imported third-party visual asset must be listed here **before** it is reused across projects.

## Required fields

| Field | Description |
|---|---|
| Asset | Local path / asset ID |
| Source | Original asset page, not a random mirror |
| Author | Creator / organization |
| License | Exact license or usage terms |
| Retrieved | Date downloaded |
| Modified | Recoloring, cropping, animation, tracing, etc. |
| Used in | Repositories / pages where the asset appears |

## Registered assets

### svglogos

- **Path:** `logos/svglogos/`
- **Source site:** https://svglogos.dev/
- **Upstream repository:** https://github.com/gilbarbara/logos
- **Author / curator:** Gil Barbara and upstream contributors
- **Collection license:** CC0-1.0; a copy is stored with the imported collection
- **Retrieved:** automated by `scripts/import_svglogos.sh`
- **Modified:** No; SVG files are mirrored as published upstream
- **Used in:** GitHub Visual Assets catalog / future project README assets
- **Notes:** Individual logos and brand marks remain the property of their respective owners and may be subject to trademark and brand-usage rules. The importer records the exact upstream commit and file count in `manifest/svglogos-source.json`.

> GitHub Octodex, unDraw, Storyset, LottieFiles, SVG Repo, Devicon, Simple Icons and similar sites are useful sources, but each source has its own terms. Record the exact asset and license rather than assuming the entire website uses one license.

## Template

```markdown
### asset-id

- **Path:** `illustrations/...`
- **Source:** https://...
- **Author:** ...
- **License / terms:** ...
- **Retrieved:** YYYY-MM-DD
- **Modified:** No / describe changes
- **Used in:** ...
- **Notes:** ...
```
