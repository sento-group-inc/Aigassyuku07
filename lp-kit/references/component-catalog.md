# Component Catalog

最終確認: 2026-08-26。リンク先・license・価格は変わりうるため、採用時に再確認する。

## 選定原則

1. ページ全体の参照は2〜3本。component集をページ全体の参照にしない。
2. componentは「このsectionで何を理解・比較・判断させるか」が言える時だけ使う。
3. 既存stackとtokensへ合わせて削る。見た目を足すためだけに新しい依存を入れない。
4. 外部code、有料部品、生成creditsの導入はHuman Gate。
5. motionは階層、説明、feedback、state変化のいずれかを担う時だけ使う。

## A. ページ全体の文法

| Source | 役割 | 採用範囲 | 非採用範囲 |
|---|---|---|---|
| [Landbook](https://land-book.com/) / [Godly](https://godly.website/) | 実在LPの全体構成 | type scale、余白、密度、写真tone、section rhythm | 固有layout・配色・copyの複製 |
| [SaaS Landing Page](https://saaslandingpage.com/) | B2B/SaaS LP | problem→promise→proof→offer→CTAの流れ | SaaSらしい見た目の無条件流用 |
| 対象Projectの既存LP / `DESIGN.md` | ブランド正本 | 色、書体、voice、既存component | 外部一般則による上書き |

### 参照の検索・完成像の作成

| Source | 役割 | 導入境界 |
|---|---|---|
| [Fudge](https://design.withfudge.com/) | 実在サイトの検索、比較、画面監査、DESIGN.md化 | native MCPが使える時だけqueryする。使えない時はbrowser screenshotで代替。料金・capture・保存は採用時に再確認する |
| [pen.dev](https://www.pen.dev/) | 実装前のcanvas、design↔code、同一repoでのvisual target管理 | open file formatだがsource codeは非公開と公式docsに明記。install・activation・MCP追加はHuman Gate。必須依存にしない |

## B. Sectionと基礎component

| Source | 向く仕事 | 導入境界 |
|---|---|---|
| [21st.dev](https://21st.dev/) | hero、pricing、testimonial、CTA等の候補探索 | 個別componentのcode、依存、responsive、accessibility、licenseを比較。`21st add`はHuman Gate |
| [shadcn/ui](https://ui.shadcn.com/) | accessibleな基礎componentとcopy-own運用 | open codeをproject tokensへ合わせる。CLI addは外部code導入としてHuman Gate |
| [coss ui](https://coss.com/ui) | Base UI系のform、dialog、accordion等 | LPの相談formやFAQに必要な時だけ。licenseを採用時に再確認 |
| [ReUI](https://reui.io/components) | marketing block、hero、CTA、複雑なproduct UI | free / Proを分け、個別licenseと価格を確認。Proは明示承認まで使わない |

## C. AIプロダクトの画面を見せる時

| Source | 向く仕事 | 導入境界 |
|---|---|---|
| [Beautiful UI](https://www.beautifului.dev/) | approval、tool chips、task row、context、diff等、AI-nativeな具体画面 | MIT。LP内の架空dashboardではなく、実際のYumoriの行為を示す小さなproduct demoへ限定 |

## D. Motionとinteraction

| Source | 向く仕事 | 導入境界 |
|---|---|---|
| [beUI](https://beui.dev/) | React / Next.jsのpurposeful motion | MIT。Motion + Tailwind依存を確認し、1ページの主役motionは原則1〜2個まで |
| [Rare UI](https://www.rareui.com/) | 印象を残す単発のanimated component | free / open-source表記は確認済み。個別licenseが確認できるまでcode導入しない |
| [Transitions.dev](https://transitions.dev/) | state change、feedback、text transitionの実例 | free / Proを分ける。Pro契約はHuman Gate。動きを説明できない場合は使わない |
| [You Don't Need Animations](https://emilkowal.ski/ui/you-dont-need-animations) | motion採否の判断基準 | 目的と閲覧頻度を先に確認。毎回触るUIではmotionを減らす |

## E. 監査と知識

| Source | 役割 | 導入境界 |
|---|---|---|
| [UI Skills](https://www.ui-skills.com/) | accessibility、motion、craftの外部Skill / playbook候補発見 | 外部Skillを一括installしない。既存Skillとの差分を確認し、足りない規則だけ一次資料で裏取り |
| [Design System Checklist](https://www.designsystemchecklist.com/) | 継続UIのtoken・状態・component網羅確認 | LP単発で巨大design systemを作らない。継続Projectの`DESIGN.md`作成時だけ使う |

## Reference Contractへの記録単位

外部候補を採用する時は、最低限次を1行ずつ残す。

- URL / 確認日
- ページのどの仕事に使うか
- 借りる文法またはcomponent
- 借りない固有要素
- license / paid境界
- 追加依存とbundle影響
- mobile / keyboard / reduced-motionの確認方法
