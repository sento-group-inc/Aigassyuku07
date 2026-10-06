---
name: extract-design
version: "1.0.0-kit.1"
description: "参考サイトURLから配色・書体・余白・レイアウト・動きを実測し、制作へ渡すデザイン仕様を抽出するときに使う。"
allowed-tools: Bash, Read, Write, Glob
---

# Extract Design

参考URLを「雰囲気」だけで処理せず、live DOMと実画像から再利用可能なデザイン証拠へ変換する独立した前処理Skill。既存Skillを守るための補助機能ではなく、URL参照を含む制作で最初に使う一次入口とする。

## 境界

- **このSkill**: 参考サイトを実測し、Reference Contractを作る。
- **`lp`**: Reference Contractを受け取り、LPの完成像・実装・採点へ進める。
- **完全複製**（ユーザーが所有・許諾済みのサイト）は本Skillの対象外。依頼があれば許諾を確認したうえで通常の実装Skill（`lp`）へ渡す。

参考にする依頼は複製指示ではない。ブランド名、ロゴ、写真、文章、固有レイアウトを移植せず、文字階層、密度、余白、色の役割、形状、状態、動きの文法へ抽象化する。

## 前提確認

```bash
command -v designlang
designlang --version
designlang doctor
```

この環境の検証済み版は `designlang 13.1.0`。`npx designlang`はnpmの別バージョンを取得し得るため使わない。見つからない、またはdoctorが失敗した場合は、推測で続けず導入状態を修復する。

別端末でCLIがない場合は、`UPSTREAM.md`と同じcommit、license、hash、rollback先を確認し、費用・権限昇格・secret・新providerを伴わなければ `bash scripts/install-designlang.sh` で自律導入する。費用・権限昇格・秘密情報が絡む場合だけユーザーに確認する。npm latestは使わない。

## Process

### 1. 目的と対象を固定する

開始前に次を1〜2行ずつ置く。

1. 参考URL
2. 何を作るか
3. 借りたい観点（例: editorialな文字階層、余白、motion）
4. 借りないもの（ロゴ、文章、写真、固有コンポーネント等）
5. desktop / mobile / dark mode等の必要範囲

### 2. 抽出する

単一ページの標準:

```bash
designlang <url> --out <output-dir> --full --ignore-widgets --emit-agent-rules
```

複数ページで共通systemを確認する場合:

```bash
designlang site <url> --out <output-dir>
```

認証・Cookieが必要なサイトは、ユーザーが閲覧権限を持つ場合だけ `--cookie-file` を使う。secretをログや成果物へ残さない。読み込み失敗、同意画面、bot block、部分取得は隠さず記録する。

### 3. 証拠を読む

生成ファイル名を固定で仮定せず、出力ディレクトリを列挙する。最低限、次を読む。

- agent-native `DESIGN.md` またはdesign-language Markdown
- DTCG design tokens / CSS variables
- responsive・interaction・motionの記録
- accessibility / contrastの結果
- visual preview HTML
- desktop・mobile・component screenshots

JSONやMarkdownだけで完了扱いにしない。previewと主要screenshotsを実際に開き、抽出値が視覚上の主役と一致するか確認する。

`intent`、`material`、component library、voice、accessibility score等の分類結果は自動推定として扱う。実画面・DOM・別出力で裏取りできない分類、`[object Object]`等の壊れた値、画面と矛盾するscoreはVerifiedへ入れず、Partial / unverifiedへ落とす。

### 4. Reference Contractへ変換する

抽出結果をそのままtarget projectへコピーせず、次の形で制作Skillへ渡す。

```markdown
## Reference Contract
- Source URL:
- Evidence paths:
- Verified design grammar:
  - typography:
  - spacing / density:
  - color roles:
  - shape / border / shadow:
  - imagery:
  - interaction / motion:
- Borrow:
- Do not copy:
- Target-project adaptation:
- Partial / unverified:
```

`Verified design grammar`には実測値と確認した画面だけを書く。印象や意図の推定は`Inferred`と明記する。project-owned `DESIGN.md`やブランドガイドがある場合、外部抽出値は証拠であり正本ではない。

### 5. 制作と検証へ戻す

Reference Contract完成後に`lp`へ戻す。制作後は同じviewportで参考画面と成果物を比較し、構図、文字階層、rhythm、assets、motionの順に確認する。参考サイトへの類似度ではなく、借りると決めた文法がtargetの目的へ変換されたかを合格条件にする。

## 完了チェックリスト

- [ ] `designlang --version`と`designlang doctor`を確認した
- [ ] 目的、借りる観点、借りない要素を固定した
- [ ] desktop / mobile / interactionを必要範囲で抽出した
- [ ] Markdown / tokensだけでなくpreviewとscreenshotsを開いた
- [ ] VerifiedとInferredを分けたReference Contractを作った
- [ ] brand assets・文章・固有レイアウトを無断コピーしていない
- [ ] 抽出失敗・partial・未確認を明記した
- [ ] 制作依頼なら`lp`へ戻した

## 失敗パターン

| 失敗 | 症状 | 修正 |
|---|---|---|
| npm latestへ漂流 | `npx designlang`で監査版と異なるCLIが動く | globalの`designlang`を使いversionをread-backする |
| tokens即コピー | 外部CSS variablesをproject正本へそのまま貼る | Reference Contractで役割へ抽象化してから適応する |
| JSONだけで完了 | 抽出値と実画面の主役がずれる | previewとdesktop/mobile screenshotsを開く |
| classifierの過信 | libraryやintentの自動ラベルを事実として制作へ渡す | 実画面・DOM・別出力で裏取りし、未確認はInferred / Partialへ落とす |
| 完全複製との混同 | 参考依頼でブランドやレイアウトをコピーする | grammarだけ借り、clone明示時は許諾確認後に lp 経由の実装Skillへ渡す |
| 制作まで抱える | 抽出SkillがLP/UI全体を支配する | Reference Contract完成後にlpへ戻す |

## Provenance

上流とローカル差分は[`UPSTREAM.md`](UPSTREAM.md)、ライセンスは[`LICENSE`](LICENSE)を参照する。
