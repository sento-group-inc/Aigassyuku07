# Upstream provenance

- Repository: https://github.com/Manavarya09/design-extract
- Source path: `skills/extract-design`
- Pinned commit: `f7c2bec6631bca0da6e8f1a0162d1917bbd46c0c`
- CLI package: `designlang` 13.1.0 from the same commit
- Retrieved: 2026-08-29
- License: MIT; see `LICENSE`

## Local divergence

上流Skillは8出力を前提に`npx designlang`を呼ぶ。ローカル版は、監査済み13.1.0へ固定したglobal CLI、同commitから再現導入する`scripts/install-designlang.sh`、`--full`によるresponsive / interaction取得、visual read-back、Reference Contract、`design-orchestrator`へのreturn conditionを追加した。更新時は上流Skill・CLI help・実出力を比較し、この差分を黙って上書きしない。
