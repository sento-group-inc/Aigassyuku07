# LP制作キット — 資料から、賞を狙えるLPまで

自分の商品の資料を渡すと、AI が参照サイトを選び、LPを作り、**Awwwards・Webby Awards・FWA の審査基準で採点して、合格ラインを超えるまで自分で磨き直す**ためのキットです。

ダッシュボードの合宿キット（`../kit/`）とは別物です。LPを作りたい時だけ使います。

全体の流れは [map.html](map.html) を開くと1枚の図で見られます。

## 3ステップで始める

1. Claude Code（または Codex）を開く
2. [PROMPT.md](PROMPT.md) の ＝＝＝ の間をコピーして貼る（clone は AI がやる）。最初は資料に `SAMPLE_BRIEF.md` を指定して試し運転する
3. AI が参照の候補を出したら一言返す。あとは採点と磨き直しまで AI が進める。**1本の目安は30〜40分**（標準モード）

自分で clone する場合:

```bash
git clone https://github.com/sento-group-inc/Aigassyuku07.git
cd Aigassyuku07/lp-kit
```

撮影と機械検査には Node.js と Playwright を使います（初回だけ）。

```bash
npm i --prefix "$TMPDIR/lp-check" playwright-core && npx --prefix "$TMPDIR/lp-check" playwright-core install chromium
```

## いつ・どれを読むか

| いつ | 読むもの | 読む人 |
|---|---|---|
| 最初に | この README、[map.html](map.html) | 人 |
| 作り始める時 | [PROMPT.md](PROMPT.md)（コピーして貼る） | 人 |
| 試し運転 | [SAMPLE_BRIEF.md](SAMPLE_BRIEF.md)（架空の和菓子屋の定期便） | 人・AI |
| 品質の基準を知りたい時 | [QUALITY_BAR.md](QUALITY_BAR.md)（3つの賞の審査基準・採点表・標準／本気モード・磨き直しのループ） | 人・AI |
| AI が作る時（自動で読む） | [lp スキル](.claude/skills/lp/SKILL.md) | AI |
| 参照サイト・部品を選ぶ時 | [component-catalog.md](references/component-catalog.md) | AI |
| 動きを決める時 | [motion-roles.md](references/motion-roles.md) | AI |

## 中に入っているもの

### 工程を担うスキル（`.claude/skills/`）

`lp` が司令塔で、必要な工程でだけ他のスキルを呼びます。

| スキル | 役割 | 必要なもの |
|---|---|---|
| [lp](.claude/skills/lp/SKILL.md) | 資料 → 参照 → 実装 → 採点 → 磨き直しの全体を進める | なし |
| [nattoku](.claude/skills/nattoku/) | 受け手が価値・証拠・条件を理解して決められるか点検する | なし |
| [haraochi](.claude/skills/haraochi/) | 「なるほど」と腹に落ちる1点を設計する | なし |
| [shakuyo](.claude/skills/shakuyo/) | 狙う印象から参照ブランドを選び、共通する文法を抜き出す | なし |
| [extract-design](.claude/skills/extract-design/) | 参照URLの色・書体・余白・動きを実測する | `designlang` CLI（無ければ撮影で代用） |
| [design-taste-frontend](.claude/skills/design-taste-frontend/) | テンプレート臭のないLPを実装する | なし |
| [refactoring-ui](.claude/skills/refactoring-ui/) | 階層・余白・色・影を具体的に直す | なし |
| [oil-motion](.claude/skills/oil-motion/) | 生成動画を使うスクロール演出（上級） | 有料の動画生成APIキー・Python・ffmpeg |
| [akaire](.claude/skills/akaire/) | 画面上で囲んだ指摘を位置つきで AI に渡す | なし |

Codex は `.agents/skills/` を読みます。中身は `.claude/skills/` と同じコピーです。

### 記録ファイルの雛形とスクリプト

| ファイル | 役割 |
|---|---|
| [templates/](templates/) | 案件ごとに作る5つの記録ファイルの雛形（Brief・Design・Reference・Verification・[Quality Scorecard](templates/quality-scorecard.md)） |
| [scripts/new_lp_workspace.py](scripts/new_lp_workspace.py) | `workspaces/<商品名>/` に5つの記録ファイルを作る |
| [scripts/validate_lp_workspace.py](scripts/validate_lp_workspace.py) | 記録ファイルの抜けを検査する |
| [scripts/check-lp.js](scripts/check-lp.js) | PC・スマホで撮影し、横スクロール・小さすぎる文字・見えない文字・表示速度・フォーカス表示などを検査する（10秒前後） |
| [scripts/check-kit.sh](scripts/check-kit.sh) | このキットの README から全ファイルへ辿れるか、`.agents` のコピーがずれていないかを検査する（キットを直す人向け） |
| `workspaces/` | 作った LP と記録が入る場所（Git には入れない） |

## 終わった時にできているもの

- `workspaces/<商品名>/site/index.html` — ブラウザで開ける LP
- `workspaces/<商品名>/01〜05_*.md` — 誰に何を約束したか、何を参照して何を借りたか、何を確かめたか、毎周の点数と直したこと
- `lp-check/` — PC・スマホのスクリーンショット

公開（Vercel などへの反映）は、このキットの外で自分で決めてから行います。

## このキットを直す時

- スキルを直したら `.agents/skills/` にも同じ内容をコピーする（`rm -rf .agents/skills && cp -R .claude/skills .agents/skills`）
- ファイルを足したら、この README から辿れるようにする
- 最後に `bash scripts/check-kit.sh` を通す

## 出どころとライセンス

`lp` `nattoku` `haraochi` `shakuyo` `akaire` は sento.group 製。`design-taste-frontend` `refactoring-ui` `extract-design` `oil-motion` は外部のスキルを取り込んだもので、各フォルダの `LICENSE` と `UPSTREAM.md` に出どころがあります。扱いはリポジトリ全体の [README](../README.md) の「ライセンス・扱い」に従います。
