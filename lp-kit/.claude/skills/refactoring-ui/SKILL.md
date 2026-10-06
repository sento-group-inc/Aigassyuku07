---
name: refactoring-ui
version: "1.0.0-kit.1"
description: "Web UIの余白・文字・色・階層などの見た目を診断・修正するときに使う。業務フローや内容設計の変更は別途扱う。"
---

# Refactoring UI — Wajima integration

曖昧な見た目の違和感を、余白・文字・色・階層・影・画像・responsiveの具体的な修正へ変える。既存デザインSkillを守る補助ではなく、visual craftの直接入口として使う。

## Source contract

作業前に必ず [`upstream/SKILL.md`](upstream/SKILL.md) を全文読む。upstreamはcommit固定の全体snapshotであり、最初から一部のルールだけを抜き出さない。

- 既存UI改善: [`upstream/references/diagnose.md`](upstream/references/diagnose.md) を最初に読む
- palette / tokens: [`upstream/references/systems.md`](upstream/references/systems.md) と [`upstream/assets/tokens.css`](upstream/assets/tokens.css) を読む
- depth / type / images / component shape: [`upstream/references/techniques.md`](upstream/references/techniques.md) を読む
- 現行CSS・Project正本との接続: [`references/project-adaptation.md`](references/project-adaptation.md) を読む

## 自動発動条件

- 「このUIなんか素人っぽい」「なんか変」「安っぽい」「ごちゃつく」「のっぺりしている」
- 「余白・文字・色・影を直して」「もっとプロっぽく」「make this look better」
- UI実装後のvisual polish、design token、palette、type scale、elevationの見直し

この発話では他の振り分けSkillを先に通す必要はない。内容設計・情報構造・業務flow自体が原因なら、診断後に対応Skillへ戻す。

## 優先順位

1. ユーザーが明示した目的・変更範囲
2. 機能、意味、アクセシビリティ、既存stackの制約
3. 実地確認済みのブランド正本・`DESIGN.md`・design tokens
4. upstreamの一般則

既存正本が目的を満たさない原因なら、その存在を理由に温存しない。変更案と影響範囲を示し、正本側を直す。

## ワークフロー

1. **入口と期待結果を固定**: 対象URL / screenshot / component / repo、主行為、変えてよい範囲を確認する。
2. **実物を見る**: codeだけで判断せず、現在のdesktopと狭幅を表示する。既存tokens、font、brand、statesを確認する。
3. **上位3原因を診断**: `diagnose.md`の順で、hierarchy、grouping、spacing、type、color、depthを評価する。症状→原因→修正を対応づける。
4. **systemから直す**: 個別要素へ場当たり値を足さず、spacing / type / color / shadow / radiusのscaleまたはsemantic roleを直す。
5. **一観点ずつ比較**: composition → hierarchy → typography → spacing → color → depth / imagesの順でbefore/afterを比較する。
6. **実装を検証**: build / lint / test、desktop、375px、keyboard、focus、contrast、overflow、主要stateを確認する。
7. **最終read-back**: 変更したsystem、残した例外、未検証事項をコードと実表示の両方から確認する。

## 完了チェックリスト

- [ ] upstream全体と、作業に必要なreferencesを読んだ
- [ ] 実物のbeforeをdesktopと狭幅で確認した
- [ ] 症状→原因→修正を上位3件以内に絞った
- [ ] 場当たり値ではなくscale / token / semantic roleから直した
- [ ] build / lint / testの対象コマンドを実行した
- [ ] desktop / 375px、keyboard / focus、contrast、overflowを実表示で確認した
- [ ] 利用者が観測するafterと、未検証事項を記録した

## 失敗パターン

| 失敗 | 対処 |
|---|---|
| upstreamから好きな規則だけ先に抜く | 全体snapshotを読み、除外は目的不適合・安全・権利・実地反証の理由と一緒に記録する |
| 既存tokensを無条件で守る | 代表入力の原因がtokensなら、影響範囲を確認してsystem側を直す |
| 見た目だけで情報構造の欠陥を隠す | hierarchyや主行為が決まらない場合は`interface-design`等へ戻す |
| CSS値を直して完成扱いする | 実表示、狭幅、keyboard、contrast、buildまで確認する |
| starter tokensをそのままブランドへ貼る | semantic rolesとscale構造を借り、色・radius・densityは対象Projectへ合わせる |

## Provenance

Upstream、固定commit、ローカル差分、更新手順は [`UPSTREAM.md`](UPSTREAM.md) を正とする。
