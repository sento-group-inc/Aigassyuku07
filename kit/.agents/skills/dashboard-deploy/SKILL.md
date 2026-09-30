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
3. `Environment Variables` を開き、次の2つを入れる。`.env.local` の2行をまるごと `Key` の欄に貼ると、自動で Key と Value に分かれる

   | Key（名前） | Value（値） |
   |---|---|
   | `NEXT_PUBLIC_SUPABASE_URL` | `https://` で始まるURL |
   | `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Publishable key（`.env.local` の同じ名前の行の値） |

   - **Key の名前は `NEXT_PUBLIC_` から始まるまま変えない。** Vercelが「`NEXT_PUBLIC_` は値がブラウザに公開される」と警告しても、この2つは公開してよい値。警告に従って名前から `NEXT_PUBLIC_` を外すと、本番に値が渡らず動かない。警告が出たら、名前はそのままにして、種類（Environment / Type）を `Config` にする
   - `service_role`（secret）キーは入れない
4. `Deploy` を押す。完了画面が出たら、表示されたURL（`https://my-dashboard-xxxx.vercel.app`）を控える。完了画面が出ないときは、下の「つまずき」の No Deployment を見る。本番URLは、プロジェクト → `Domains` の一番上（`〜.vercel.app`）でも分かる
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
| `/protected` を開くと「A server error occurred」と出る（ログイン画面は出る） | 環境変数の**名前**を疑う。`NEXT_PUBLIC_` が外れていないか、綴りが `.env.local` と同じかを見て、直したら再デプロイする |
| 環境変数を直したのに変わらない | 環境変数は再デプロイしないと反映されない。`Deployments` → 一番上の `⋯` → `Redeploy` |
| Deploy を押しても完了画面が出ず、`No Deployment`（`DEPLOYMENT_NOT_FOUND`）のまま | GitHubの `main` に1つ push またはマージすると、自動で本番が作られる。または `Deployments` から作り直す |
| 本番でログインするとlocalhostへ飛ぶ | Supabaseの `Site URL` が本番URLになっていない |
| 画面は出るが一覧が空 | 本番のSupabaseでSQLを実行していない、または環境変数が別プロジェクトを指している |
| マージしたのに変わらない | `Deployments` の一番上がそのコミットか確認する。止まっていれば `Redeploy` |

手順の骨格は、実案件のデプロイ手順（データベースを先・アプリを後、本番に破壊的な操作を向けない）から借りて、合宿向けに簡単にした。
