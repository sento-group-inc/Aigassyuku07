# 外部連携に必要なキー

> これは雛形。Step 5で埋める。**値は絶対に書かない。置き場所だけ書く。**

| # | サービス | 何に使うか | 必要なもの | 取得場所 | 置き場所 | 状態 |
|---|---|---|---|---|---|---|
| 1 | GitHub | コードの置き場 | アクセストークン | Settings → Developer settings | CLIの認証（`gh auth login`） | 未 |
| 2 | Supabase | データベースとログイン | Project URL / Publishable key | 画面上部の `Connect` | `.env.local` と Vercel の Environment Variables | 未 |
| 3 | Vercel | 公開 | （連携のみ） | — | GitHub連携 | 未 |

## 注意

- Publishable key はブラウザに渡ってよいキー。ただし**テーブルにRLS（行ごとの鍵）を必ず付ける**。
- **`service_role`（secret）キーは使わない。** 使うときもサーバー専用で、ブラウザ側のコードに出さない。
- スクリーンショットを撮るときは、キーが写らないようにする。
- 漏れた疑いがあるときは、その場で作り直す（無効化して再発行）。
