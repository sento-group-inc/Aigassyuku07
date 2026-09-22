# 外部連携に必要なキー

> これは雛形。Step 5で埋める。**値は絶対に書かない。置き場所だけ書く。**

| # | サービス | 何に使うか | 必要なもの | 取得場所 | 置き場所 | 状態 |
|---|---|---|---|---|---|---|
| 1 | GitHub | コードの置き場 | アクセストークン | Settings → Developer settings | CLIの認証（`gh auth login`） | 未 |
| 2 | Supabase | データベース | Project URL / anon key / service_role key | Project Settings → API | ホスティングの環境変数 | 未 |
| 3 | Vercel | 公開 | （連携のみ） | — | GitHub連携 | 未 |
| 4 | TypeSafe (JEV) | 型つきの判断 | APIキー | 管理画面 | `~/.config/typesafe/api-key` か環境変数 | 未 |

## 注意

- **`service_role`キーはサーバー専用。** ブラウザ側のコードに出さない。
- スクリーンショットを撮るときは、キーが写らないようにする。
- 漏れた疑いがあるときは、その場で作り直す（無効化して再発行）。
