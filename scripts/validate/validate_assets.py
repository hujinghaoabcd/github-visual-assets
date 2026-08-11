#!/usr/bin/env python3
"""Repository validation for the scalable visual asset architecture."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOTS = [
    "brand", "profile", "projects", "logos", "library", "references",
    "templates", "source", "exports", "archive", "staging",
]
ALLOWED_SUFFIXES = {
    ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".json", ".jsonl",
    ".md", ".yml", ".yaml", ".drawio", ".psd", ".ai", ".fig", ".sketch",
    ".aep", ".mp4", ".mov", ".webm", ".txt", ".html", ".css",
}
FORBIDDEN_FONT_SUFFIXES = {".ttf", ".otf", ".woff", ".woff2", ".eot"}
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MAX_NORMAL_BYTES = 20 * 1024 * 1024
MAX_HARD_BYTES = 50 * 1024 * 1024


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "README.md", "LICENSE", "LICENSE-ASSETS", "THIRD_PARTY.md",
        "manifest/assets.yml", "manifest/taxonomy/categories.yml",
        "docs/STYLE_GUIDE.md", "docs/ASSET_SPEC.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for root_name in ASSET_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            errors.append(f"missing asset root: {root_name}/")
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            suffix = path.suffix.lower()
            if suffix in FORBIDDEN_FONT_SUFFIXES:
                errors.append(f"font binary should not be committed: {rel}")
            if suffix and suffix not in ALLOWED_SUFFIXES:
                warnings.append(f"unusual asset type: {rel}")
            if path.name not in {"README.md", ".gitkeep"} and not NAME_RE.match(path.name):
                errors.append(f"unsafe filename: {rel}")
            size = path.stat().st_size
            if size > MAX_HARD_BYTES:
                errors.append(f"file exceeds 50 MiB hard policy: {rel}")
            elif size > MAX_NORMAL_BYTES:
                warnings.append(f"large file; consider Git LFS/object storage: {rel}")

    if warnings:
        print("Warnings:")
        for item in warnings:
            print(f"  - {item}")
    if errors:
        print("Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("Asset validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
