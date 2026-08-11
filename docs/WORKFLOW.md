# Asset Workflow

## 1. Define purpose

Decide whether the asset is a brand mark, README hero, project cover, architecture diagram, illustration, icon, background, screenshot or animation. Define target size and light/dark behavior first.

## 2. Create or collect

Original work goes to `source/`. For third-party work, save the original source page, author and license before downloading or editing.

## 3. Normalize

Apply the shared palette, typography and line language. Do not force every project to look identical; preserve the family distinction while maintaining the shared identity.

## 4. Register provenance

For third-party assets, update `THIRD_PARTY.md` and `manifest/assets.yml`. Record modifications such as recoloring, cropping, background removal, tracing, compositing or animation.

## 5. Export

Export optimized assets to `exports/` when they are intended for reuse across repositories. Project-specific assets may also live under `project-covers/<project>/`.

## 6. Validate

Run:

```bash
python scripts/validate_assets.py
```

Check the image visually in GitHub light and dark themes when relevant.

## 7. Release and reuse

When a visual kit becomes stable, tag a repository release. Long-lived documentation should reference a stable tag or release asset rather than a mutable branch when practical.
