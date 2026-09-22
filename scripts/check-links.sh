#!/usr/bin/env bash
# site/ 内のローカルリンクと画像参照が実在するかを確認する。

set -u

root="$(cd "$(dirname "$0")/.." && pwd)"
site="$root/site"
missing=0
checked=0

cd "$site" || exit 1

for page in *.html; do
  while IFS= read -r target; do
    case "$target" in
      http*|mailto:*|"#"*|"") continue ;;
    esac
    clean="${target%%#*}"
    clean="${clean%%\?*}"
    [ -z "$clean" ] && continue
    checked=$((checked + 1))
    if [ ! -e "$clean" ]; then
      printf 'MISSING  %s -> %s\n' "$page" "$target"
      missing=$((missing + 1))
    fi
  done < <(grep -o 'href="[^"]*"' "$page" | sed 's/href="//;s/"$//'; grep -o 'src="[^"]*"' "$page" | sed 's/src="//;s/"$//')
done

echo "----------------------------------------"
echo "検査した参照: $checked  /  見つからない: $missing"

if [ "$missing" -eq 0 ]; then
  echo "OK: すべての参照先が存在します。"
  exit 0
fi
exit 1
