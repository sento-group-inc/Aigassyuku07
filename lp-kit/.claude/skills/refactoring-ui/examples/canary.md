# Canary

## Representative input

> このUIなんか素人っぽい。余白・文字・色・影を直して、プロっぽくして。

## Expected route

1. `refactoring-ui`が直接発火する。
2. 現在のUIをdesktopと375pxで開く。
3. `upstream/SKILL.md`と`upstream/references/diagnose.md`を読む。
4. 上位3症状を原因と修正へ対応づける。
5. 個別の場当たり値ではなくtokens / scale / semantic rolesを修正する。
6. build、実表示、keyboard、contrast、overflowを確認する。

## Fail conditions

- 振り分けの説明だけで止まり、UIを修正しない
- upstreamの一部だけを読む前提で開始する
- 既存tokensを理由なく固定する
- CSS差分だけで完了し、afterを表示しない
