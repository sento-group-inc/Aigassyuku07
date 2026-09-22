# kit — 参加者の作業フォルダ

このフォルダを自分のリポジトリの土台にします。`setup.sh`で環境を確認し、ガイドに沿って進めます。

## 使い方

```bash
cd kit
./setup.sh          # 足りないものを表示する（何もインストールしない）
```

そのあと、Codex（またはClaude）でこのフォルダを開き、リポジトリ直下の [PROMPT.md](../PROMPT.md) を貼ってください。

## 中身

| パス | 役割 |
|---|---|
| `AGENTS.md` | Codex向けの入口。作業前に読むもの、守る決まり |
| `CLAUDE.md` | Claude向けの入口。同じ内容をClaudeの読み方で |
| `.claude/skills/` | この合宿で使うスキル一式（Claude Codeは自動で読む。Codexは`AGENTS.md`経由） |
| `docs/` | 設計ドキュメントの置き場。**作業前にAIが読む正本** |
| `docs/guide-steps.md` | 当日の進行台本。ガイドはこれを見て次の一手を決める |
| `.env.example` | 必要な環境変数の一覧（値は入れない） |

## 自分のリポジトリにする

```bash
mkdir my-dashboard && cd my-dashboard
git init
cp -r ../Aigassyuku07/kit/* .
git add -A && git commit -m "chore: 合宿キットから初期化"
gh repo create my-dashboard --private --source=. --push
```

会社名やプロジェクト名は`AGENTS.md`と`CLAUDE.md`の冒頭を書き換えてください。

## 大事な約束

- **実データを入れない。** 顧客名・個人情報・本番の接続情報は、この段階では使いません。ダミーデータで作ります。
- **キーは`docs/keys.md`に「どこにあるか」だけ書く。** 値そのものは書かない。
- 迷ったら「次は何をすればいい？」と聞けば、ガイドが現在地から案内します。
