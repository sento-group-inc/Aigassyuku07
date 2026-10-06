# Canary — designlang.app

## Fixture

- Date: 2026-08-29
- Source: https://designlang.app
- CLI: `designlang 13.1.0`
- Command: `designlang https://designlang.app --out <temp> --full --ignore-widgets --emit-agent-rules`
- Purpose: 参考URLからdesktop / mobile / interactionを含むdesign evidenceを作り、Reference Contractへ変換できるか確認する

## Execution evidence

- Exit code: 0
- Duration: 54.0s
- Files: 81
- Responsive screenshots: 8（mobile / tablet / desktop / wide × light / dark）
- Component screenshots: 15
- Interactions: 10 state changes
- Visual read-back: `desktop-dark.png`、`mobile-dark.png`、`hero.png`を実際に開いた

## Reference Contract

- Source URL: https://designlang.app
- Evidence: generated `DESIGN.md`、DTCG tokens、responsive index、component screenshot index、desktop / mobile / hero images
- Verified design grammar:
  - typography: Geist / Geist Mono。Heroは大きなsans、terminal・metadataはmono
  - spacing / density: dark canvas上でsection間を大きく空け、情報密度の高いカード群と交互に配置
  - color roles: ほぼ黒のbackground、白い見出し、赤をHero glow・CTA・状態表示へ限定
  - shape / border / shadow: 小〜中radius、薄い赤／白border、暗部へ溶けるshadow
  - imagery: product evidenceをUI captureと実例cardで見せる
  - responsive: mobileでは一列化し、Heroコピー・terminal・card gridの順序を保持
- Borrow: dark editorial hierarchy、red glowの局所利用、実物証拠を並べるsection rhythm、sans / monoの役割分担
- Do not copy: designlangのロゴ、文章、terminal内容、実例画像、固有section順
- Target-project adaptation: targetブランド色・実データ・主行為へ置換し、同じレイアウトを再現しない
- Partial / unverified:
  - component libraryの`bootstrap`判定は実画面から確認できず、誤検出の可能性が高い
  - generated `DESIGN.md`のbreakpointsが`[object Object]`になっており、値として利用不可
  - 17% WCAG scoreは自動抽出結果。主要CTAと本文の個別contrast再計測なしには採用しない

## Result

抽出、visual read-back、Reference Contract化まで到達した。自動分類をVerifiedへ昇格させないガードが必要なことも実利用で確認した。
