# スクリーンショット台帳

講義サイトに挿入する画像の一覧。**秘密情報が写った画像は使わない。** APIキー・トークン・DB接続文字列・顧客名・アカウント名が写る場合は、撮り直すか隠す。

## 撮り方

| 区分 | 手段 |
|---|---|
| 自動 | `agent-browser`（公開ページ・見本・ローカルHTML）。`setup.sh`は実出力を端末風HTMLに表示して撮影し、アカウント名を伏せる |
| 半自動 | 本人が `agent-browser --headed` でログイン → エージェントが画面を開いて撮る（送信・作成ボタンは押さない）。一覧に顧客のプロジェクト名が出る画面は検索で絞るか開かない。アカウント名・組織名は撮影前に伏せる |
| 撮らない | bot検知（CAPTCHA）で止まるページ。CAPTCHAは突破しない |

## 台帳

| 画像 | 画面 | 区分 | 挿入先 | 状態 |
|---|---|---|---|---|
| `setup/01-setup-sh.png` | `./setup.sh` の実出力 | 自動 | prep / setup | 取得済み（2026-09-23） |
| `setup/02-check-services.png` | `./setup.sh --check-services` の実出力 | 自動 | setup | 取得済み |
| `setup/03-codex-open.png` | Codexで `kit` フォルダを開いた直後 | 本人撮影 | setup | 取得済み（本人撮影。ユーザー名と社内フォルダ名をぼかし） |
| `setup/04-first-prompt.png` | 入力欄に最初のプロンプトを貼った送信直前 | 本人撮影 | setup | 取得済み（本人撮影） |
| `build/01a-grill-prompt.png` | grill-with-docs のプロンプトにメモを貼った送信直前 | 本人撮影 | readme-driven | 取得済み（本人撮影） |
| `skills/02-skill-chip.png` | 選んだスキルが入力欄にチップとして入った画面 | 本人撮影 | skills | 取得済み |
| `skills/01-skill-picker.png` | 入力欄で `$` と打ちスキル候補が出た画面 | 本人撮影 | skills | 取得済み（本人撮影） |
| `prep/03-vercel-signup.png` | Vercel サインアップ | 自動 | prep | 取得済み |
| `prep/04-supabase-signin.png` | Supabase サインイン | 自動 | prep | 取得済み |
| `build/01-readme.png` | 見本: README と CONTEXT.md | 自動（`site/samples/readme.html`） | build Step 1 | 取得済み |
| `build/02-prototype.png` | 見本: 画面の試作 | 自動（`site/samples/prototype.html`） | build Step 2 | 取得済み |
| `build/03-er.png` | 見本: スキーマとER図 | 自動（`site/samples/schema.html`） | build Step 3 | 取得済み |
| `build/04-roadmap.png` | 見本: ロードマップ | 自動（`site/samples/roadmap.html`） | build Step 4 | 取得済み |
| `build/05-keys.png` | 見本: キー棚卸し表 | 自動（`site/samples/roadmap.html#keys`） | build Step 5 | 取得済み |
| `build/06-template.png` | with-supabase テンプレート（公式デモ） | 自動 | build Step 6 | 取得済み |
| `build/07-supabase-new-project.png` | Supabase の Create a new project（組織名を伏せ、作成は押さない） | 半自動 | build Step 6 | 取得済み（2026-09-24） |
| `build/08-login.png` | テンプレートのログイン画面（公式デモ） | 自動 | build Step 8 | 取得済み |
| `build/11-vercel-import.png` | Vercel の Import（検索でキットのリポジトリだけ表示） | 半自動 | build Step 9 | 取得済み（2026-09-24） |
| `build/12-vercel-ready.png` | Vercel のデプロイ完了（講義サイト自身。ユーザー名を伏せた） | 半自動 | build Step 9 | 取得済み（2026-09-24） |

撮らないと決めたもの: openai.com/codex と github.com/signup（bot検知で止まる）、ガイドとグリルの返答画面（応答例のテキストで代替）、SupabaseのAdd userとGitHubのPR画面（デモ環境を作らない方針。2026-09-24本人判断）。

## 置き場と命名

```
site/assets/images/<ページ名>/<連番>-<内容>.png
```

ページは `scripts/build-site.py` から生成する。画像をこの名前で置いて `python3 scripts/build-site.py` を実行すると、「撮影待ち」「ここに画像」の枠が自動で画像に置き換わる。最後に `./scripts/check-links.sh` を通す。
