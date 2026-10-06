#!/usr/bin/env bash
# README.md からリンクを辿って、キットの全ファイルに到達できるかと、.agents/skills のコピーずれを検査する。
# リンク先がフォルダなら、その中のファイルはすべて到達済みとみなす。

set -u

kit="$(cd "$(dirname "$0")/.." && pwd)"

python3 - "$kit" <<'PY'
import re, sys
from pathlib import Path

kit = Path(sys.argv[1])
link = re.compile(r'\]\(([^)#\s]+)')
seen, dirs, broken = set(), set(), []
queue = [kit / "README.md"]
while queue:
    page = queue.pop()
    if page in seen:
        continue
    seen.add(page)
    if page.suffix not in {".md", ".html"}:
        continue
    text = page.read_text(encoding="utf-8")
    targets = link.findall(text) + re.findall(r'href="([^"#]+)"', text)
    for target in targets:
        if target.startswith(("http", "mailto:")):
            continue
        dest = (page.parent / target).resolve()
        if not dest.exists():
            broken.append(f"{page.relative_to(kit)} -> {target}")
        elif dest.is_dir():
            dirs.add(dest)
            queue.extend(p for p in dest.rglob("*") if p.is_file())
        else:
            queue.append(dest)

skip = {".agents", "workspaces", "lp-check", "node_modules"}
unreached = []
for f in kit.rglob("*"):
    rel = f.relative_to(kit)
    if not f.is_file() or rel.parts[0] in skip or f.name in {".gitignore", ".DS_Store"}:
        continue
    if f.resolve() not in seen and not any(d in f.resolve().parents for d in dirs):
        unreached.append(str(rel))

for b in broken:
    print(f"BROKEN    リンク先が無い: {b}")
for u in sorted(unreached):
    print(f"UNREACHED README から辿れない: {u}")
print(f"辿れたファイル: {len(seen)}  /  リンク切れ: {len(broken)}  /  辿れない: {len(unreached)}")
sys.exit(1 if broken or unreached else 0)
PY
status=$?

if ! diff -rq "$kit/.claude/skills" "$kit/.agents/skills" >/dev/null 2>&1; then
  echo "DRIFT     .agents/skills が .claude/skills と違う（rm -rf .agents/skills && cp -R .claude/skills .agents/skills）"
  status=1
fi

exit $status
