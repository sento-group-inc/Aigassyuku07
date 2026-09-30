---
name: dashboard-auth
description: 最初のスライスで、社員だけがログインでき、ログインした人だけがダッシュボードの一覧を見られる状態を作るときに使う。
---

# dashboard-auth — ログインして一覧が見える

たとえるなら、**社員証で開くドア**。ドア（ログイン画面）はテンプレートに付いている。ここでは「社員証を配る人を決める」と「ドアの内側に一覧を置く」をやる。

前提: `dashboard-repo` が終わり、http://localhost:3000 が開く。

## 手順

### 1. 勝手に登録できないようにする（Supabaseの画面）

社内用なので、知らない人が自分でアカウントを作れないようにする。

1. Supabase → `Authentication` → `Sign In / Providers`
2. `Allow new users to sign up` を**オフ**にして保存

### 2. 社員のアカウントを作る（Supabaseの画面）

1. `Authentication` → `Users` → `Add user` → `Create new user`
2. メールアドレスとパスワードを入れ、`Auto Confirm User` に**チェック**して作成
3. まず自分のアカウントを1つ作る

### 3. テーブルとダミーデータを作る

`docs/schema.md` の最初のテーブルを、AIにSQLにしてもらう。

```text
docs/schema.md の最初のテーブルを作るSQLを supabase/migrations/0001_init.sql に書いて。
ダミーデータを10行入れて、RLSを有効にし、ログインした人だけが読み書きできるポリシーを付けて。
2回流してもエラーにならない書き方（create table if not exists など）にして。
```

できたSQLを、Supabase → `SQL Editor` に貼って `Run` する。**実行する前に、何が作られるかAIに説明してもらう。**

`Run` は**1回だけ**押す。成功すると `Success. No rows returned` と出る。`already exists` と出たら、1回目で成功している。

RLS（行ごとの鍵）は必ず付ける。付けないと、公開キーを知っている人なら誰でもデータを読めてしまう。

### 4. ドアの内側に一覧を置く

テンプレートの `app/protected/page.tsx` が「ログインした人だけが見られるページ」。ここを一覧画面にする。

```text
app/protected/page.tsx を、docs/roadmap.md の S1 のとおり一覧画面にして。
DBやログイン情報を読む部分は <Suspense> で囲んで（テンプレートの元の page.tsx と同じ形）。
データは Supabase の〈テーブル名〉から読んで。見た目は docs/ui-guidelines.md に従って。mvp/index.html は見た目の参考にだけして、コードは使わないで。
トップページ（/）はログインしていれば /protected へ、していなければ /auth/login へ送って。
```

### 5. 確かめる

| 確かめること | 期待 |
|---|---|
| ログアウトした状態で http://localhost:3000/protected を開く | ログイン画面へ送られる |
| 作ったアカウントでログインする | 一覧が出て、ダミーデータが10行見える |
| 間違ったパスワードでログインする | エラーが出て入れない |

3つとも期待どおりなら、1スライス目として `dashboard-slice` の手順でPR→マージする。

## 終わりの状態

- ログインしないと一覧が見えない
- ログインすると、ダミーデータの一覧が見える
- テーブルにRLSが付いている（Supabase → `Table Editor` でテーブル名の横に `RLS enabled`）

## つまずき

| 症状 | 対処 |
|---|---|
| ログインしても一覧が空 | RLSのポリシーが無い、またはダミーデータが入っていない。SQL Editorで `select count(*) from テーブル名;` |
| 「Email not confirmed」と出る | ユーザー作成時の `Auto Confirm User` を忘れた。ユーザーを消して作り直す |
| ログイン後に変な画面へ飛ぶ | `app/page.tsx` の転送先を確認する |
| ログイン画面がずっと再読み込みを繰り返す | `npm run dev` が動いたまま設定ファイルを変えたか `npm run build` をした。`Ctrl+C` で止め、`.next` フォルダを消して、`npm run dev` を起動し直す |
| ビルドが「Suspense」のエラーで通らない | DBやログイン情報を読む部品を `<Suspense>` で囲む |
| ログイン画面が英語で、「Sign up」のリンクが残っている | テンプレートの仕様。登録は手順1で止めてあるので押しても登録できない。日本語化・リンク削除は後のスライスでやる |
