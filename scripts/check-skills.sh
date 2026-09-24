#!/usr/bin/env bash

set -u

root="$(cd "$(dirname "$0")/.." && pwd)"
skills="$root/kit/.claude/skills"
missing=0

referenced="$(
  {
    grep -ohE '<b>\$[a-z0-9-]+' "$root"/site/*.html | sed 's/.*\$//'
    grep -ohE 'skills/[a-z0-9-]+/SKILL\.md' "$root"/site/*.html | sed 's#skills/##;s#/SKILL.md##'
    grep -ohE '<code>(guide|eli5|reflect|poteto-mode|grill-with-docs|[a-z]+-guide|dashboard-[a-z]+)</code>' "$root"/site/*.html | sed 's/<[^>]*>//g'
    grep -ohE '^\| `[a-z0-9-]+` \|' "$root"/kit/AGENTS.md "$root"/kit/CLAUDE.md | sed 's/^| `//;s/` |$//'
    grep -ohE '(guide|eli5|reflect|poteto-mode|grill-with-docs|dashboard-[a-z]+) ?(スキル|で)' "$root"/PROMPT.md | sed -E 's/ ?(スキル|で)$//'
  } | sort -u
)"

for name in $referenced; do
  if [ ! -f "$skills/$name/SKILL.md" ]; then
    printf 'MISSING  案内されているが実体がない: %s\n' "$name"
    missing=$((missing + 1))
  fi
done

for dir in "$skills"/*/; do
  name="$(basename "$dir")"
  if ! grep -q "skills/$name/SKILL.md" "$root/site/skills.html"; then
    printf 'UNLISTED 実体はあるが道具のページに載っていない: %s\n' "$name"
    missing=$((missing + 1))
  fi
  if ! grep -q "^name: $name$" "$dir/SKILL.md"; then
    printf 'NAME     SKILL.md の name がフォルダ名と違う: %s\n' "$name"
    missing=$((missing + 1))
  fi
done

if [ ! -e "$root/kit/.agents/skills/guide/SKILL.md" ]; then
  echo "MISSING  kit/.agents/skills（Codex用のリンク）が .claude/skills を指していない"
  missing=$((missing + 1))
fi

count="$(printf '%s\n' "$referenced" | grep -c .)"
echo "----------------------------------------"
echo "案内されているスキル: $count  /  問題: $missing"
[ "$missing" -eq 0 ] && echo "OK: 案内しているスキルはすべて実在します。"
[ "$missing" -eq 0 ]
