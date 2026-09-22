#!/usr/bin/env bash
# 環境の現在地を調べる。インストールも設定変更もしない。

set -u

ok=0
ng=0

check_cmd() {
  local name="$1" cmd="$2" hint="$3"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '  OK   %-12s %s\n' "$name" "$($cmd --version 2>&1 | head -1)"
    ok=$((ok + 1))
  else
    printf '  NG   %-12s 入っていません。%s\n' "$name" "$hint"
    ng=$((ng + 1))
  fi
}

echo "== ツール =="
check_cmd git git "https://git-scm.com/downloads からインストール"
check_cmd node node "https://nodejs.org からLTSをインストール"
check_cmd npm npm "Node.jsに同梱されています"
check_cmd gh gh "https://cli.github.com からインストール"

echo
echo "== Node.jsのバージョン =="
if command -v node >/dev/null 2>&1; then
  major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
  if [ "$major" -ge 20 ] 2>/dev/null; then
    echo "  OK   Node.js $(node -v)（20以上）"
    ok=$((ok + 1))
  else
    echo "  NG   Node.js $(node -v)。20以上に上げてください"
    ng=$((ng + 1))
  fi
else
  echo "  --   Node.jsが無いので確認できません"
fi

echo
echo "== GitHubのサインイン =="
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    echo "  OK   $(gh auth status 2>&1 | sed -n 's/.*account \(.*\) (keyring).*/\1/p' | head -1) でサインイン済み"
    ok=$((ok + 1))
  else
    echo "  NG   未サインイン。次を実行してください: gh auth login"
    ng=$((ng + 1))
  fi
else
  echo "  --   gh が無いので確認できません"
fi

echo
echo "== AIエージェント =="
if [ -d "$HOME/.codex" ]; then
  echo "  OK   Codexの設定ディレクトリあり（$HOME/.codex）"
  ok=$((ok + 1))
else
  echo "  --   Codex未検出。Codexアプリを起動してサインインしてください"
fi
if [ -d "$HOME/.claude" ]; then
  echo "  OK   Claudeの設定ディレクトリあり（$HOME/.claude）"
  ok=$((ok + 1))
else
  echo "  --   Claude未検出。Claudeを使う場合だけ必要です"
fi

echo
echo "== JEV（型つきの判断） =="
if [ -f "$HOME/.config/typesafe/api-key" ]; then
  echo "  OK   キー登録済み（値は表示しません）"
  ok=$((ok + 1))
elif [ -n "${JEV_API_KEY:-}" ] || [ -n "${TYPESAFE_API_KEY:-}" ]; then
  echo "  OK   環境変数で設定済み（値は表示しません）"
  ok=$((ok + 1))
else
  echo "  --   未設定。当日の案内に従って登録します（無くても先に進めます）"
fi

echo
echo "== 作業フォルダ =="
if [ -f "./AGENTS.md" ] && [ -d "./.claude/skills" ]; then
  echo "  OK   kit/ の中にいます"
  ok=$((ok + 1))
else
  echo "  NG   kit/ の中で実行してください（cd kit してから ./setup.sh）"
  ng=$((ng + 1))
fi

echo
echo "----------------------------------------"
echo "OK: $ok  /  要対応: $ng"
echo
if [ "$ng" -eq 0 ]; then
  echo "次: リポジトリ直下の PROMPT.md をエージェントに貼ってください。"
else
  echo "次: 上の NG を直してから、もう一度 ./setup.sh を実行してください。"
  echo "    直せないものは当日の午前で拾います。抱え込まないでください。"
fi

exit 0
