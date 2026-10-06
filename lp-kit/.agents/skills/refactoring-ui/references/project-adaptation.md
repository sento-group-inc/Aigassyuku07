# Project adaptation

Upstreamの原則を全体として評価・保持しつつ、現行Projectへ適用するときの境界を定める。これは既存Skill保護のための除外表ではない。

## Color notation

upstreamの「hexではなくHSL」は、色同士の関係を読める形にするための規則として扱う。ProjectがOKLCHを採用している、または新規paletteで知覚的な均等性が重要ならOKLCHを使ってよい。重要なのは、semantic roles、明示的なramp、contrast実測、runtimeでの場当たり生成を避けること。

## Existing design systems

既存tokensや`DESIGN.md`は先に読むが、存在だけでは採用理由にならない。代表入力の原因がscale、contrast、radius、shadow、densityにある場合は、個別overrideではなく正本を修正候補にする。

## Radius and elevation

一貫性は単一値に限定しない。button / input / cardなど役割別scaleが明文化され、画面全体で反復されるなら許容する。shadowもupstream値を固定themeとして貼らず、z-axisの意味と対象Projectのmaterial languageを守る。

## Responsive starting point

mobile-firstを既定にする。ただしdesktop専用の高密度業務UIでは、主利用環境から設計してよい。その場合も375pxでoverflow、情報欠落、操作不能がないかを確認し、対応外なら明示する。

## Exclusion ledger

upstream規則を適用しない場合は、次のいずれかを記録する。

- user outcomeとの不適合
- accessibility / function / stack制約
- verified brand正本との衝突
- 実表示での反証
- 権利・安全・費用リスク

「既存Skillに同じ規則がある」「今の構成を変えたくない」は除外理由にしない。
