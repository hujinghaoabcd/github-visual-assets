# Third-Party Asset Registry

Every imported third-party visual asset must have traceable provenance and usage terms before it is reused across projects.

## Required fields

| Field | Description |
|---|---|
| Asset | Local path / asset ID |
| Source | Original asset page/repository |
| Author | Creator / organization |
| License | Exact license or usage terms |
| Retrieved | Date downloaded |
| Modified | Recoloring, cropping, animation, tracing, etc. |
| Used in | Repositories / pages where the asset appears |

## Registered collections

### svglogos

- **Path:** `logos/svglogos/`
- **Source site:** https://svglogos.dev/
- **Upstream repository:** https://github.com/gilbarbara/logos
- **Author / curator:** Gil Barbara and upstream contributors
- **Collection license:** CC0-1.0; a copy is stored with the imported collection
- **Retrieved:** automated by `scripts/import/svglogos.sh`
- **Modified:** No; SVG files are mirrored as published upstream
- **Metadata:** `manifest/sources/svglogos.json`
- **Notes:** Individual logos and brand marks remain the property of their respective owners and can be subject to trademark/brand usage rules.

## Rule for references

`references/` is for visual research/inspiration. It must not be treated as a redistributable asset library merely because a screenshot or link is stored there.

## Asset template

```markdown
### asset-id
- **Path:** `library/illustrations/...`
- **Source:** https://...
- **Author:** ...
- **License / terms:** ...
- **Retrieved:** YYYY-MM-DD
- **Modified:** No / describe changes
- **Used in:** ...
- **Notes:** ...
```
