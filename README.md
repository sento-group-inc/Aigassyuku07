# AI合宿 — 会社用ダッシュボード構築キット

**題材は「自社のダッシュボードを1本作る」。学ぶのは、その過程で使う環境とAI活用の型そのもの。**

まる1日で、自社の業務画面を自分のURLで開けるところまで行きます。2日目以降は、配布したキットとガイドエージェントで自走できます。

> 手順の出典は、実際に会計事務所のダッシュボードを作ったときに回った手順（担当メンバーへのヒアリング 2026-09-18）。実案件のリポジトリは非公開で、顧客情報を含むためこのリポジトリには持ち込んでいません。

> **社内メンバーの方へ**: 合宿前のトライアル手順は [TRIAL.md](TRIAL.md) にあります。

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

| Step | 段階 | やること | 使うスキル | モデル |
|---|---|---|---|---|
| 0 | 準備 | 環境とAIの初期設定 | `guide` / `ai-setup` | どれでも |
| 1 | 1 粗く作る | 困りごとを1文にしてログを始める | `dev-log` | 安い |
| 2 | 1 粗く作る | MVPを作って触り、声をログにためる | `dashboard-mvp` | 安い |
| 3 | 2 研究する | MVPとログを研究し docs/research.md に残す | `dashboard-research` | 賢い |
| 4 | 3 計画する | 作り直すための計画一式（スキーマ・ロードマップ・キー） | `dashboard-plan` | 賢い |
| 5 | 4 作り直す | 土台（DB・アプリ・リポジトリ） | `dashboard-repo` | 安い |
| 6 | 4 作り直す | ログインと一覧（S1） | `dashboard-auth` → `dashboard-slice` | 安い |
| 7 | 4 作り直す | 本番へ出す | `dashboard-deploy` | 安い |
| 8 | 締め | 次の一手と振り返り | `guide` → `reflect` | どれでも |

詳しい手順は [site/build.html](site/build.html)、時間割は [site/schedule.html](site/schedule.html) にあります。

## 持ち帰るもの

| 持ち帰るもの | 何ができるようになるか |
|---|---|
| 自社ダッシュボードの本番URL | 自社の1業務が、ログインして一覧・更新できる |
| 手元の環境（`setup.sh` / スキル一式 / AIの初期設定） | 2日目以降も同じ手順・同じモデルの使い分けで作れる |
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

## 開発の流れ

1. **とにかく粗く作る** — 安いモデル（Luna / Sol、Sonnet）で素早くMVPを作り、触って出た声をログにためる
2. **研究する** — いちばん賢いモデル（Astra、Opus）にMVPとログを見せ、あらゆる品質を上げる方法を研究させる
3. **計画する** — 研究から、ゼロから作り直せる計画一式（スキーマ・ロードマップ・キー・画面の原則）を作る
4. **ゼロから作り直す** — 安いモデルに戻し、計画だけを見て作り直す（MVPのコードは流用しない）

前提: 要望・決定・詰まりは `docs/log.md` に書きながら進める。モデルを替えると会話の文脈は消え、渡るのはファイルだけなので。

## ライセンス・扱い

社内の合宿用教材です。参加企業は自社の開発に自由に使えます。他社への再配布はsento.groupへ確認してください。

## このサイトの公開（運営メモ）

`site/` をVercelで配信します。

1. VercelでこのリポジトリをImport
2. **Root Directoryに `site` を指定**（リポジトリ直下には`index.html`が無いため）
3. Framework PresetはOther、Build Commandは空

リンク切れの確認は `./scripts/check-links.sh`、サイトで案内しているスキルが実在するかは `./scripts/check-skills.sh` で行います。
