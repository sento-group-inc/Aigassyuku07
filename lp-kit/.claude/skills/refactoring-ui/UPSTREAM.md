# Upstream provenance

- Repository: https://github.com/s0xDk/refactoring-ui-skill
- Pinned commit: `48872143abb0a8feb6d9bf58e222afbd800210b0`
- Imported: 2026-08-29
- License: MIT for the repository contents. The book *Refactoring UI* is a separate copyrighted work and is not included.

## Snapshot policy

`upstream/` contains the complete repository payload at the pinned commit: `SKILL.md`, `README.md`, `LICENSE`, `assets/`, and `references/`. The snapshot is kept unmodified so adoption does not begin as selective extraction.

The root `SKILL.md` is the Wajima runtime wrapper. It adds direct Japanese triggers, Project priority rules, a real-display completion loop, and local adaptation guidance without rewriting the snapshot.

## Update procedure

1. Fetch a candidate upstream commit into a temporary directory.
2. Compare the complete old and new snapshots, including LICENSE.
3. Re-evaluate against the user outcome, existing/new/zero options, and the full upstream candidate.
4. Replace `upstream/` only after explicit external-code approval.
5. Update this commit, Registry, Ledger, runtime sync, and read-back evidence.

Do not hand-edit files under `upstream/`.
