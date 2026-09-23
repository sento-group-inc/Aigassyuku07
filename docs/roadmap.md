# 制作ロードマップ（スライス）

このリポジトリ自身をどう作るかと、当日参加者がやることを同じ形式で持つ。**番号＝実施順**。各スライスは「作る → 実際に動かして確認 → 次へ」で閉じる。

## 目的と成功条件

**手段**は「自社の業務ダッシュボードを1本作る」。**学ぶこと**は、その過程で使う環境とAI活用の型そのもの。

当日の終了時（まる1日）に、参加者が次を持っていること。

1. 自社ダッシュボードの本番URL（ログインして1画面が一覧・更新できる）
2. 手元の環境（Codex または Claude、スキル16本、`setup.sh`）
3. `README.md` / `CONTEXT.md` / `AGENTS.md` / `CLAUDE.md` / `docs/schema.md` / `docs/ui-guidelines.md` / `docs/roadmap.md`
4. 2日目以降に自分でスライスを足せる状態（ガイドエージェントに聞けば次が出る）

## 前提（本人回答 2026-09-22）

| 項目 | 決定 |
|---|---|
| 参加者の環境 | Codex と Claude の両方。**画面・スクショはCodex基準**、Claudeの差分は注記で吸収 |
| 事前準備 | PC準備の案内を配布し、事前にcloneさせる（`PREP.md` / `PROMPT.md`） |
| 公開範囲 | **public**。事前配布してcloneさせる |
| 日程と規模 | **2026-10-06（火）・07（水）／10社** |
| 時間 | **初日がまる1日**。2日目は各社が個別学習へ進む前提で、初日から自社題材でよい |
| 題材 | 各社の実業務。会計事務所の実例は「こう作った」の参照として見せる |
| JEV | **扱わない**（2026-09-23 本人決定）。ページ・スキル・設定スクリプトを撤去 |
| 認証 | 初日のゴールは「ログインして一覧」を維持。Next.js公式 with-supabase テンプレートで土台を作り、S1をログインに固定（2026-09-23） |

## 学ぶ内容（ページとキットの対応）

| 学ぶこと | 講義ページ | キット側の実体 |
|---|---|---|
| なぜやるのか（腹落ち） | `why.html`（eli5） | — |
| 事前準備 | `prep.html` | `PREP.md` |
| 合宿スケジュール | `schedule.html` | — |
| 環境セットアップと使い方 | `setup.html` | `kit/setup.sh`（`--check-services`） / `kit/.agents/skills`（Codex用） |
| README駆動開発 | `readme-driven.html` | `grill-with-docs`（README / CONTEXT.md / ADR） |
| pstack / poteto-mode / reflect / 原則 | `pstack.html` | `poteto-mode` / `pstack-guide` / `reflect` |
| 配布スキル16本 | `skills.html` | `kit/.claude/skills/`（`scripts/check-skills.sh`で実在を検査） |
| 使うリポジトリと出典 | `repos.html` | — |
| ダッシュボードを作る10ステップ | `build.html` | `kit/.claude/skills/dashboard-*/` / `site/samples/`（見本） |
| 実例（会計事務所のダッシュボード） | `reference/case-accounting.md` | — |
| 順番に案内する | 当日の進行 | `kit/.claude/skills/guide/` |

---

## 制作スライス（このリポジトリを作る）

手前で価値が出る順に切る。S0〜S3 で「配って見せられる」状態、S4〜S8 で「学べる」状態、S9〜S11 で「当日回る」状態になる。

### S0. 骨格と公開

`README.md` / `PREP.md` / `PROMPT.md` / ディレクトリ（`site/` `kit/` `docs/` `reference/` `assets/`）を作り、publicにしてVercelへ繋ぐ。

- 検証: `gh repo view`でpublicをread-back。Vercelの本番URLで`index.html`が開く。
- 手戻り防止: 公開前に、キットへクライアント情報が混ざっていないかgrepする。

### S1. 講義サイトの器

`site/assets/style.css`と共通ナビを作り、全ページが同じ見た目で並ぶようにする。

- 検証: ローカルHTTPサーバで全ページを開き、リンク切れ0（`scripts/check-links.sh`）。

### S2. why（eli5）ページ

「なぜ会社のシステムを自分で作るのか」を、比喩と図で説明する。冒頭で腹落ちさせる担当。

- 検証: 専門用語ゼロで読み切れるか、初見の1人に読ませて引っかかった語を潰す。

### S3. 環境セットアップページ

Codex中心に、インストール → サインイン → リポジトリ → 最初のプロンプトまでを、**画面ごとのスクリーンショット付き**で並べる。Claude参加者向けの差分を注記で添える。

- 検証: まっさらな状態から`setup.sh`を通し、`codex`が起動して1往復できる。
- 依存: `docs/screenshots.md`の自動取得分。

### S4. pstack / poteto-mode ページ

`/poteto-mode`の意味、21原則の使い方、`/reflect`、`workflow-orchestrator`との役割分担を、実際の1回の開発の流れで説明する。

- 検証: 本文中の原則名と説明が`SKILL.md`と一致しているか照合する。

### S5. 配布スキルページ

キットのスキル16本を、いつ使うかと呼び方で説明する（2026-09-23 JEVを外し、grill-with-docs・poteto-mode・reflect・eli5・dashboard-repo・dashboard-auth を追加）。

- 検証: 各スキルの発火条件が`SKILL.md`のdescriptionと矛盾しない。

### S6. ダッシュボードを作る8ステップ

実案件のヒアリングで出た手順を、当日そのまま使える粒度で書く（Artifacts → スキーマ/ER → ロードマップ → キー棚卸し → Secret → docs/CLAUDE.md → スライス実装ループ → デプロイ）。

- 検証: キットのスキル名とページ内のコマンドが一致している。

### S7. キット本体

`kit/`に`setup.sh`、`CLAUDE.md`、`AGENTS.md`、`.claude/skills/`、`docs/`テンプレ、`.env.example`を置き、clone直後に使えるようにする。

- 検証: 新しいディレクトリで`git clone` → `./setup.sh` → ダミーデータで1画面起動までを実走。

### S8. ガイドエージェント

`kit/.claude/skills/guide/`。参加者が「次は何をすればいい？」と聞くと、現在地を判定して**使うスキルと次の1手**を指定する。進行台本は`kit/docs/guide-steps.md`に持つ。

- 検証: 3つの異なる開始状態（未着手／スキーマ済み／デプロイ済み）で、返す次手が変わることを確認。

### S9. 参照実装の解説

実案件の構造（`docs/`の役割、CLAUDE.mdの読み込み指示、ロードマップのスライス、UIガイドラインの効き方）を、顧客情報を除いた形で解説する。

- 検証: 掲載したファイル名・行数・構成が実物と一致している。

### S10. スクリーンショット差し込み

`docs/screenshots.md`の台帳に従って画像を生成し、各ページへ挿入する。**自動で撮れるもの**と**人が撮るべきもの**を分けてある。

- 検証: 画像のaltと説明文が画面の実物と一致している。

### S11. 当日リハーサル

キットだけを使い、参加者と同じ手順を頭から通す。詰まった箇所を`docs/known-issues.md`へ追記し、講義ページへ反映する。

- 検証: まる1日でデプロイまで到達できるか、所要時間を実測して時間割を直す。

---

## 当日のスライス（参加者がやること）

正本は `kit/docs/guide-steps.md`（Step 0〜10）。時間割は `site/schedule.html`。

| Step | やること | 使うスキル | 終わりの状態 |
|---|---|---|---|
| 0 | 環境を確かめる | `guide` | `setup.sh`が通る |
| 1 | 題材を決めて、READMEを書く | `grill-with-docs` | README冒頭に困りごとの1文、CONTEXT.mdに業務の言葉 |
| 2 | 画面を作る | `dashboard-screen` | `docs/prototype.html`を開いて操作できる |
| 3 | スキーマとER図 | `dashboard-schema` | 「この情報はどこに入るか」に全部答えられる |
| 4 | ロードマップ | `dashboard-roadmap` | S1（ログインして一覧）が今日中に終わる大きさ |
| 5 | キー棚卸し | `dashboard-keys` | 置き場所の表があり、値はどこにも無い |
| 6 | 土台（DB・アプリ・リポジトリ） | `dashboard-repo` | 手元で画面が開き、GitHubにリポジトリがある |
| 7 | docs と AGENTS.md / CLAUDE.md | `dashboard-docs` | AIが作業前に読む状態 |
| 8 | ログインと一覧（S1） | `dashboard-auth` → `dashboard-slice` | ログインすると一覧が見え、PRがマージ済み |
| 9 | 本番へ | `dashboard-deploy` | 本番URLでログインして一覧が動く |
| 10 | 次の一手と振り返り | `guide` → `reflect` | 明日やることが1行で書かれている |

## 未決・保留

- **why（腹落ち）の深掘り（S2）**: 2026-09-22 本人指示により、**後日あらためて対話して決める**。それまでは現行版を暫定とする
- 当日の時間割の実測（S11。2026-09-23 本人指示で時間の現実性は優先度を下げた。Codexで`guide`のStep 0判定までは実走確認済み）
- スクリーンショットのうちログインが要る6枚（`docs/screenshots.md`の「未」）
