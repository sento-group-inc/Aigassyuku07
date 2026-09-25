---
name: dashboard-repo
description: Step 5（段階4 ゼロから作り直す）で、データベース（Supabase）とアプリの土台（ログイン画面つき）を作り、GitHubのリポジトリにして、手元で画面が開く状態にするときに使う。
---

# dashboard-repo — 土台を作る（DB・アプリ・リポジトリ）

たとえるなら、**お店の開店準備**。倉庫（データベース）を借り、店舗（アプリ）の箱を建て、鍵（キー）を決まった場所にしまう。ここまでで、まだ商品（画面）は並べない。

アプリの箱は、Next.js公式の **with-supabase テンプレート**を使う。**ログイン画面が最初から付いている**ので、ゼロから作らなくてよい。

## 手順

### 1. データベースを作る（ブラウザ）

1. https://database.new を開き、Supabaseにサインインする
2. `New project` で次を入れる
   - Name: `my-dashboard`（自由）
   - Database Password: `Generate a password` を押し、**パスワード管理ツールに保存**（ファイルやチャットに書かない）
   - Region: `Asia-Pacific`（地域の一覧が出る場合は `Northeast Asia (Tokyo)`）
   - Security: `Enable automatic RLS` があれば**チェックを入れる**（新しいテーブルに行ごとの鍵が自動で付く）
3. `Create new project` を押し、数分待つ

### 2. アプリの箱を作る（ターミナル）

キットをcloneしたフォルダ（`~/Documents`）で実行する。`my-dashboard` は `Aigassyuku07` の**隣**にできる。

```bash
cd ~/Documents
npx create-next-app@latest --example with-supabase my-dashboard
cd my-dashboard
```

### 3. キットの設計ドキュメントとスキルを持ってくる

Step 1〜4で `kit/` に書いたもの（ログ・研究・計画・README・スキル）を、新しいアプリへコピーする。`mvp/` もコピーされるが、見た目の参考に見るだけで、コードは使わない。

```bash
rsync -a --exclude .gitignore --exclude setup.sh --exclude .env.example ../Aigassyuku07/kit/ ./
```

`README.md` はテンプレートのものが、Step 3で書いた自分のREADMEに置き換わる。

### 4. 鍵を置く（`.env.local`）

```bash
cp .env.example .env.local
```

Supabaseの画面上部にある `Connect` を押し、表示された2つの値を `.env.local` に貼る。

| 名前 | どこにあるか | ブラウザに渡ってよいか |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Connect → Project URL | よい |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Connect → Publishable key（または anon key） | よい（ただし次のStepでRLSを必ず付ける） |

`service_role`（secret）キーは**使わない**。使うときもブラウザ側のコードには絶対に書かない。

### 5. 手元で開く

```bash
npm run dev
```

http://localhost:3000 を開き、テンプレートの画面が出れば成功。

### 6. GitHubのリポジトリにする

```bash
git add -A
git commit -m "chore: with-supabaseテンプレートと合宿キットで初期化"
gh repo create my-dashboard --private --source=. --push
```

`.env.local` がコミットされていないことを確認する（`git status` に出てこなければOK）。

## 終わりの状態

- http://localhost:3000 で画面が開く
- GitHubに `my-dashboard` リポジトリがあり、`.env.local` は入っていない
- `docs/keys.md` の「置き場所」列が埋まっている

## つまずき

| 症状 | 対処 |
|---|---|
| `npx` が見つからない | Node.jsが入っていない。`./setup.sh` をもう一度実行する |
| 画面に「Supabaseの環境変数がない」と出る | `.env.local` の名前が間違っている。上の表と1文字ずつ比べる |
| `gh repo create` で止まる | `gh auth login` をしてからやり直す |
| 会社のPCで `npx` が使えない | 講師に声をかける。ブラウザだけで進める手順（Vercelの Deploy ボタンからテンプレートを作る）に切り替える |
