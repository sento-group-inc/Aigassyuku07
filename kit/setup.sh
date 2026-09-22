#!/usr/bin/env bash
# 環境の現在地を調べる。インストールも設定変更もしない。

set -u

ok=0
ng=0

mark_ok()   { printf '  OK   %s\n' "$1"; ok=$((ok + 1)); }
mark_ng()   { printf '  NG   %s\n' "$1"; ng=$((ng + 1)); }
mark_info() { printf '  --   %s\n' "$1"; }

check_cmd() {
  local name="$1" cmd="$2" hint="$3"
  if command -v "$cmd" >/dev/null 2>&1; then
    mark_ok "$(printf '%-12s %s' "$name" "$($cmd --version 2>&1 | head -1)")"
  else
    mark_ng "$(printf '%-12s 入っていません。%s' "$name" "$hint")"
  fi
}

check_tools() {
  echo "== ツール =="
  check_cmd git git "https://git-scm.com/downloads"
  check_cmd node node "https://nodejs.org/ja/download （20以上）"
  check_cmd npm npm "Node.jsに同梱"
  check_cmd gh gh "https://cli.github.com/"

  echo
  echo "== Node.jsのバージョン =="
  if command -v node >/dev/null 2>&1; then
    local major
    major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
    if [ "$major" -ge 20 ] 2>/dev/null; then
      mark_ok "Node.js $(node -v)（20以上）"
    else
      mark_ng "Node.js $(node -v)。20以上に上げてください: https://nodejs.org/ja/download"
    fi
  else
    mark_info "Node.jsが無いので確認できません"
  fi

  echo
  echo "== AIエージェント =="
  if [ -d "$HOME/.codex" ]; then mark_ok "Codexの設定あり（$HOME/.codex）"; else mark_info "Codex未検出。起動してサインインしてください"; fi
  if [ -d "$HOME/.claude" ]; then mark_ok "Claudeの設定あり（$HOME/.claude）"; else mark_info "Claude未検出。使う場合だけ必要です"; fi

  echo
  echo "== 作業フォルダ =="
  if [ -f "./AGENTS.md" ] && [ -d "./.claude/skills" ]; then
    mark_ok "kit/ の中で実行しています"
  else
    mark_ng "kit/ の中で実行してください（cd kit してから ./setup.sh）"
  fi
}

check_services() {
  echo "== 外部サービス =="

  if [ -n "${JEV_API_KEY:-}" ] || [ -n "${TYPESAFE_API_KEY:-}" ]; then
    mark_ok "JEVのキー: 環境変数で設定済み（値は表示しません）"
  elif [ -f "$HOME/.config/typesafe/api-key" ]; then
    mark_ok "JEVのキー: 登録済み（値は表示しません）"
  else
    mark_ng "JEVのキー: 未設定。https://typesafe.ai → Sign In で取得し、python3 tools/jev-configure.py で保存"
  fi

  if command -v gh >/dev/null 2>&1; then
    if gh auth status >/dev/null 2>&1; then
      mark_ok "GitHub: $(gh auth status 2>&1 | sed -n 's/.*account \(.*\) (keyring).*/\1/p' | head -1) でサインイン済み"
    else
      mark_ng "GitHub: 未サインイン。gh auth login"
    fi
  else
    mark_info "GitHub: gh が無いので確認できません（https://cli.github.com/）"
  fi

  if command -v supabase >/dev/null 2>&1; then
    mark_ok "Supabase CLI: $(supabase --version 2>&1 | head -1)"
  else
    mark_info "Supabase CLI: 未導入（当日はブラウザ操作でも進められます） https://supabase.com/dashboard"
  fi

  if command -v vercel >/dev/null 2>&1; then
    mark_ok "Vercel CLI: $(vercel --version 2>&1 | head -1)"
  else
    mark_info "Vercel CLI: 未導入（当日はGitHub連携で進められます） https://vercel.com/new"
  fi
}

print_links() {
  echo
  echo "----------------------------------------"
  echo "足りないものの入手先"
  echo "  JEV（APIキー）  https://typesafe.ai → Sign In"
  echo "  Node.js         https://nodejs.org/ja/download"
  echo "  git             https://git-scm.com/downloads"
  echo "  GitHub CLI      https://cli.github.com/"
  echo "  Supabase        https://supabase.com/dashboard"
  echo "  Vercel          https://vercel.com/new"
  echo "  一覧            docs/links.md"
}

mode="tools"
if [ "${1:-}" = "--check-services" ]; then
  mode="services"
fi

if [ "$mode" = "services" ]; then
  check_services
else
  check_tools
fi

echo
echo "----------------------------------------"
echo "OK: $ok  /  要対応: $ng"
print_links
echo
if [ "$ng" -eq 0 ]; then
  echo "次: リポジトリ直下の PROMPT.md をエージェントに貼ってください。"
else
  echo "次: 上の NG を直してから、もう一度実行してください。"
  echo "    直せないものは当日の午前で拾います。抱え込まないでください。"
fi

exit 0
