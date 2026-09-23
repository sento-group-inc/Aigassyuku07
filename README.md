# AI合宿 — 会社用ダッシュボード構築キット

**題材は「自社のダッシュボードを1本作る」。学ぶのは、その過程で使う環境とAI活用の型そのもの。**

まる1日で、自社の業務画面を自分のURLで開けるところまで行きます。2日目以降は、配布したキットとガイドエージェントで自走できます。

> 手順の出典は、実際に会計事務所のダッシュボードを作ったときに回った手順（担当メンバーへのヒアリング 2026-09-18）。実案件のリポジトリは非公開で、顧客情報を含むためこのリポジトリには持ち込んでいません。

## 最初にやること

1. [PREP.md](PREP.md) を読んで、当日までに用意する（困りごとメモ・道具・clone・アカウント）
2. このリポジトリをcloneする
3. `kit/`で`./setup.sh --check-services`を実行し、足りないものを確認する
4. [PROMPT.md](PROMPT.md) のプロンプトをCodex（またはClaude）に貼る
5. あとはガイドが順番に案内します

```bash
git clone https://github.com/sento-group-inc/Aigassyuku07.git
cd Aigassyuku07/kit
./setup.sh --check-services
```

**公開URL（当日投影用）**: https://aigassyuku07.vercel.app

## 当日の流れ

| Step | やること | 使うスキル | 終わりの状態 |
|---|---|---|---|
| 0 | 環境を確かめる | `guide` | `setup.sh`が通る |
| 1 | 題材を決めて、READMEを書く | `grill-with-docs` | READMEに困りごとの1文、CONTEXT.mdに業務の言葉 |
| 2 | 画面を作る | `dashboard-screen` | `docs/prototype.html`を開いて操作できる |
| 3 | スキーマとER図を作る | `dashboard-schema` | 「この情報はどこに入るか」に全部答えられる |
| 4 | ロードマップを書く | `dashboard-roadmap` | S1（ログインして一覧）が今日中に終わる大きさ |
| 5 | キーを棚卸しする | `dashboard-keys` | 置き場所の表があり、値はどこにも無い |
| 6 | 土台を作る（DB・アプリ・リポジトリ） | `dashboard-repo` | 手元で画面が開き、GitHubにリポジトリがある |
| 7 | docsとAGENTS.md / CLAUDE.mdを整える | `dashboard-docs` | AIが作業前に読む状態 |
| 8 | ログインと一覧を作る（S1） | `dashboard-auth` → `dashboard-slice` | ログインすると一覧が見え、PRがマージ済み |
| 9 | 本番へ出す | `dashboard-deploy` | 本番URLでログインして一覧が動く |
| 10 | 次の一手と振り返り | `guide` → `reflect` | 明日やることが1行で書かれている |

詳しい手順は [site/build.html](site/build.html)、時間割は [site/schedule.html](site/schedule.html) にあります。

## 持ち帰るもの

| 持ち帰るもの | 何ができるようになるか |
|---|---|
| 自社ダッシュボードの本番URL | 自社の1業務が、ログインして一覧・更新できる |
| 手元の環境（`setup.sh` / スキル一式） | 2日目以降も同じ手順で作れる |
| `CLAUDE.md` + `docs/` | AIが作業前にスキーマ・UIガイドライン・ロードマップを読んでから着手する |
| `docs/roadmap.md`の残スライス | 「次のスライス」を渡すだけで機能を足せる |
| ガイドエージェント | 「次は何をすればいい？」と聞けば次が出る |

## リポジトリの構成

```
Aigassyuku07/
├── site/        講義サイト（当日投影。Vercelで配信）
├── kit/         参加者がcloneして使う雛形（AGENTS.md / CLAUDE.md / .claude/skills / docs）
├── docs/        制作ロードマップ・設計・スクリーンショット台帳
├── reference/   実例（会計事務所のダッシュボード）のサニタイズ済み解説
└── assets/      画像
```

## 開発の流れ（実例で回った順序）

1. **困りごとを文章にする**（README駆動。grill-with-docsで詰める）
2. **画面の試作を作る**（まだコードにしない）
3. **スキーマを組ませ、ER図で漏れを潰す**
4. **スキーマが固まった瞬間にロードマップを書かせる**
5. **外部連携に必要なキーを棚卸しする**
6. **DB・アプリ・リポジトリを作り、コードを手元へ**
7. **`docs/`を整える**（スキーマの背景・UIガイドライン・インフラ）
8. **`AGENTS.md` / `CLAUDE.md`に「作業前に読むドキュメント」を書く**
9. **ロードマップ通りにスライス→PR→レビュー→マージを回す**

## ライセンス・扱い

社内の合宿用教材です。参加企業は自社の開発に自由に使えます。他社への再配布はsento.groupへ確認してください。

## このサイトの公開（運営メモ）

`site/` をVercelで配信します。

1. VercelでこのリポジトリをImport
2. **Root Directoryに `site` を指定**（リポジトリ直下には`index.html`が無いため）
3. Framework PresetはOther、Build Commandは空

リンク切れの確認は `./scripts/check-links.sh`、サイトで案内しているスキルが実在するかは `./scripts/check-skills.sh` で行います。
