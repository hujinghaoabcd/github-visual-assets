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

No third-party binary assets are bundled in the initial repository scaffold.

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
