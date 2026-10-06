#!/usr/bin/env python3
"""LP案件workspaceの必須構造を検証する。"""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = {
    "01_LP_BRIEF.md": ["## 1. LPの役割", "## 3. 約束する変化", "## 6. ページ構成", "## 8. Unknowns"],
    "02_DESIGN_CONTRACT.md": ["## 制作品質契約", "## Brand Grammar", "## Responsive Contract"],
    "03_REFERENCE_CONTRACT.md": ["## 採用候補", "## Component Selection", "## Human Gates"],
    "04_VERIFICATION_RECORD.md": ["## Content", "## 実表示", "## Code", "## CTA / Release", "## Evidence"],
    "05_QUALITY_SCORECARD.md": ["## 合格ライン", "## 採点ログ", "## 最終判定"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="LP workspaceの構造検証")
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    errors: list[str] = []
    for filename, headings in REQUIRED.items():
        path = workspace / filename
        if not path.is_file():
            errors.append(f"missing: {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in headings:
            if heading not in text:
                errors.append(f"{filename}: missing heading {heading}")
        if "{{" in text or "}}" in text:
            errors.append(f"{filename}: unresolved template token")

    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"ok: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

