---
name: dashboard-deploy
description: 作ったアプリを本番（Vercel）へ出し、自分のURLでログインして一覧が開く状態にするときに使う。マージしたのに本番が変わらないときにも使う。
---

# dashboard-deploy — 本番へ出す

たとえるなら、**お店のシャッターを開ける**。倉庫の棚（データベース）を先に整え、それから店（アプリ）を開ける。逆にすると、お客さんが空の棚を見ることになる。

本番は **Supabase（データ）＋ Vercel（アプリ）**。GitHubの `main` にマージすると、Vercelが自動で本番を作り直す。

## 初回だけ: Vercelにつなぐ（ブラウザ）

1. https://vercel.com/new を開き、GitHubでサインインする
2. `Import Git Repository` から `my-dashboard` の `Import` を押す
3. `Environment Variables` を開き、`.env.local` と同じ2つを入れる
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
4. `Deploy` を押す。完了画面が出たら、表示されたURL（`https://my-dashboard-xxxx.vercel.app`）を控える
5. Supabase → `Authentication` → `URL Configuration`
   - `Site URL` に控えたURLを入れる
   - `Redirect URLs` に `https://my-dashboard-xxxx.vercel.app/**` を足す

## 毎回: 変更を本番へ出す

1. **データベースの変更が先。** `supabase/migrations/` に新しいSQLがあれば、SQL Editorで先に実行する
   - 実行する前に、何が変わるかをAIに説明してもらい、自分で読んでから `Run` する（テーブルの変更は取り消せない）
2. PRを `main` にマージする
3. Vercel → プロジェクト → `Deployments` で、一番上が `Ready` になるまで待つ
4. 本番URLを開き、**ログインして一覧が動く**ことを確かめる
5. URLを `docs/infra.md` に書く

## やってはいけないこと

- 本番のデータを全部消す操作（テーブルの削除、`truncate`、データベースのリセット）を本番に向けて実行しない
- 環境変数の値をチャット・コード・スクリーンショットに出さない
- 失敗したまま押し直しを繰り返さない。最初のエラーを読んで直してから出す

## 終わりの状態

- 本番URLを開き、ログインして一覧が動く
- URLが `docs/infra.md` に書かれている
- 次に足すものが `docs/roadmap.md` にある

## つまずき

| 症状 | 対処 |
|---|---|
| `Build Failed` | Vercelのログの**最初のエラー**をAIに貼る。エラーが複数あっても原因はたいてい1つ |
| 本番でログインするとlocalhostへ飛ぶ | Supabaseの `Site URL` が本番URLになっていない |
| 画面は出るが一覧が空 | 本番のSupabaseでSQLを実行していない、または環境変数が別プロジェクトを指している |
| マージしたのに変わらない | `Deployments` の一番上がそのコミットか確認する。止まっていれば `Redeploy` |

手順の骨格は、実案件のデプロイ手順（データベースを先・アプリを後、本番に破壊的な操作を向けない）から借りて、合宿向けに簡単にした。
