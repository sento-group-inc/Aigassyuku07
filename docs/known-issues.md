# 既知の詰まりどころ（症状・原因・対処）

リハーサルと制作中に見つかったもの。講義ページの「うまくいかないとき」表にも反映する。

| 症状 | 原因 | 対処 | 反映先 |
|---|---|---|---|
| Codexが最初に `~/.codex/skills/guide` を探して見つからない | Codexはリポジトリ内のスキルを `.agents/skills/` から読む | `kit/.agents/skills` を `.claude/skills` へのリンクにした。開くフォルダは `kit`（親フォルダではない） | setup「エージェントがスキルを知らないと言う」 |
| Codexの読み取り専用モードで `setup.sh --check-services` のGitHubがNGになる | サンドボックス内では `gh auth status` が認証情報を読めないことがある | 参加者のターミナルで直接 `./setup.sh --check-services` を実行する | guide の案内（Step 0） |
| 講義サイトから JEV を案内していた | 2026-09-23 方針変更で扱わない。旧 `jev-configure.py` はAPI側のUser-Agent制限（Cloudflare 1010）で403になっていた | ページ・スキル・スクリプトを撤去し、`/jev` は `/setup` へ転送 | — |
| 「ログインして一覧」の手順が無かった | 8ステップに認証の工程が無かった | with-supabase テンプレート＋`dashboard-auth`（サインアップ停止・Add user・RLS）で Step 8 に固定 | build Step 6・8 |
| agent-browser で openai.com / github.com の画面が撮れない | bot検知（CAPTCHA） | 撮らない。リンクで代替 | docs/screenshots.md |
