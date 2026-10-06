#!/usr/bin/env python3
"""LP案件用の契約ファイルを安全に初期化する。"""

from __future__ import annotations

import argparse
import re
import unicodedata
from datetime import date
from pathlib import Path


SYSTEM_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "lp-brief.md": "01_LP_BRIEF.md",
    "design-contract.md": "02_DESIGN_CONTRACT.md",
    "reference-contract.md": "03_REFERENCE_CONTRACT.md",
    "verification-record.md": "04_VERIFICATION_RECORD.md",
    "quality-scorecard.md": "05_QUALITY_SCORECARD.md",
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip()
    normalized = re.sub(r"\s+", "-", normalized)
    normalized = re.sub(r"[^0-9A-Za-zぁ-んァ-ヶ一-龠ー._-]", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-.")
    if not normalized or normalized in {".", ".."}:
        raise ValueError("案件名から安全なfolder名を作れません")
    return normalized


def render(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="LP制作案件のworkspaceを初期化")
    parser.add_argument("--name", required=True, help="商品・案件名")
    parser.add_argument("--source", default="未決", help="入力正本のpathまたはURL")
    parser.add_argument("--audience", default="未決", help="主対象者")
    parser.add_argument("--cta", default="未決", help="主CTA")
    parser.add_argument(
        "--output-root",
        default="workspaces",
        help="lp-kitからの出力先。絶対pathも可",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = SYSTEM_ROOT / output_root
    output_root = output_root.resolve()
    target = (output_root / slugify(args.name)).resolve()

    if target.parent != output_root:
        raise SystemExit("出力先がoutput root外です")
    if target.exists():
        raise SystemExit(f"既存案件は上書きしません: {target}")

    target.mkdir(parents=True)
    values = {
        "LP_NAME": args.name,
        "SOURCE": args.source,
        "AUDIENCE": args.audience,
        "CTA": args.cta,
        "CREATED_AT": date.today().isoformat(),
    }
    for source_name, target_name in TEMPLATES.items():
        source = SYSTEM_ROOT / "templates" / source_name
        target_file = target / target_name
        target_file.write_text(render(source.read_text(encoding="utf-8"), values), encoding="utf-8")

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

