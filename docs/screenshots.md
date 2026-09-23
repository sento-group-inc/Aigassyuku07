# スクリーンショット台帳

講義サイトに挿入する画像の一覧。**秘密情報が写った画像は使わない。** APIキー・トークン・DB接続文字列・顧客名・アカウント名が写る場合は、撮り直すか隠す。

## 撮り方

| 区分 | 手段 |
|---|---|
| 自動 | `agent-browser`（公開ページ・見本・ローカルHTML）。`setup.sh`は実出力を端末風HTMLに表示して撮影し、アカウント名を伏せる |
| 半自動 | 本人が `agent-browser --headed` でログイン → エージェントが画面を開いて撮る（送信・作成ボタンは押さない） |
| 撮らない | bot検知（CAPTCHA）で止まるページ。CAPTCHAは突破しない |

## 台帳

| 画像 | 画面 | 区分 | 挿入先 | 状態 |
|---|---|---|---|---|
| `setup/01-setup-sh.png` | `./setup.sh` の実出力 | 自動 | prep / setup | 取得済み（2026-09-23） |
| `setup/02-check-services.png` | `./setup.sh --check-services` の実出力 | 自動 | setup | 取得済み |
| `setup/03-codex-open.png` | Codexで `kit` フォルダを開いた画面 | 半自動（デスクトップアプリ） | setup | 未 |
| `prep/03-vercel-signup.png` | Vercel サインアップ | 自動 | prep | 取得済み |
| `prep/04-supabase-signin.png` | Supabase サインイン | 自動 | prep | 取得済み |
| `build/01-readme.png` | 見本: README と CONTEXT.md | 自動（`site/samples/readme.html`） | build Step 1 | 取得済み |
| `build/02-prototype.png` | 見本: 画面の試作 | 自動（`site/samples/prototype.html`） | build Step 2 | 取得済み |
| `build/03-er.png` | 見本: スキーマとER図 | 自動（`site/samples/schema.html`） | build Step 3 | 取得済み |
| `build/04-roadmap.png` | 見本: ロードマップ | 自動（`site/samples/roadmap.html`） | build Step 4 | 取得済み |
| `build/05-keys.png` | 見本: キー棚卸し表 | 自動（`site/samples/roadmap.html#keys`） | build Step 5 | 取得済み |
| `build/06-template.png` | with-supabase テンプレート（公式デモ） | 自動 | build Step 6 | 取得済み |
| `build/07-supabase-connect.png` | Supabase の Connect（値は隠す） | 半自動 | build Step 6 | 未 |
| `build/08-login.png` | テンプレートのログイン画面（公式デモ） | 自動 | build Step 8 | 取得済み |
| `build/09-supabase-users.png` | Supabase の Add user | 半自動 | build Step 8 | 未 |
| `build/10-pr.png` | GitHub の PR 画面 | 半自動（github.com はbot検知） | build Step 8 | 未 |
| `build/11-vercel-import.png` | Vercel の Import | 半自動 | build Step 9 | 未 |
| `build/12-vercel-ready.png` | Vercel のデプロイ完了（Ready） | 半自動 | build Step 9 | 未 |

撮らないと決めたもの: openai.com/codex と github.com/signup（どちらもbot検知で止まる）。本文のリンクで代替する。

## 置き場と命名

```
site/assets/images/<ページ名>/<連番>-<内容>.png
```

画像を置いたら、該当ページの `<div class="shot">ここに画像: …</div>` を `<img src="…" alt="…">` に置き換え、`./scripts/check-links.sh` を通す。
