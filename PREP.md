# 事前準備（10月6日までにやること）

当日は朝から自社のダッシュボードを作り始めます。インストールとアカウント作成は、この準備で済ませてきてください。所要1〜2時間。**詰まったらAIに聞きながら進めてOK**です。

講義サイトの画面つき版: https://aigassyuku07.vercel.app/prep

```mermaid
flowchart LR
  A[0 宿題: 困りごとメモ] --> B[1 道具を入れる]
  B --> C[2 Codexを入れる]
  C --> D[3 キットをclone]
  D --> E[4 アカウントを作る]
  E --> F[5 最終チェック]
```

## 0. 宿題: 困りごとをメモする（いちばん大事）

当日、AIがあなたの業務について質問します（`grill-with-docs`）。材料が多いほど、作るものが良くなります。

**(a) 困りごとを1つ以上**

> 誰が、何に困っていて、何が見えると嬉しいか

例: 案件の進捗が誰にも見えず、毎朝口頭で確認している

**(b) いま使っている帳票の「項目名」**

スプレッドシートや紙の見出しを、そのまま書き写してきてください（中身は不要）。

> 例: 顧客名 / 担当 / 受付日 / 見積金額 / 状況 / 次アクション

うまく書けない人は、ChatGPTやClaudeに次を貼ると、AIが質問しながら引き出してくれます。

```text
私の仕事の困りごとを言語化したいです。業務で「面倒なこと」「誰にも見えていないこと」
「毎回確認していること」を一緒に掘り下げてください。
質問は番号付きでまとめて出し、それぞれに推奨回答を添えてください。
```

**個人情報や実データは持ち込まないでください。** 画面はダミーデータで作ります。

## 1. 道具を入れる（Mac、20分）

ターミナル（`アプリケーション` → `ユーティリティ` → `ターミナル`）を開いて、1行ずつ貼ります。

```bash
# Homebrew（道具を入れる道具）。表示された「Next steps」の2行も実行する
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.js・git・GitHub CLI
brew install node git gh
```

Windowsの人は https://nodejs.org/ja/download ・ https://git-scm.com/downloads ・ https://cli.github.com/ から入れてください。

## 2. Codexを入れてサインインする（10分）

https://openai.com/codex/ からCodexアプリを入れ、会社のChatGPTアカウントでサインインします。Claudeを使う人は https://claude.ai/download も入れてください。

## 3. キットをcloneする（2分）

```bash
cd ~/Documents
git clone https://github.com/sento-group-inc/Aigassyuku07.git
cd Aigassyuku07/kit
./setup.sh
```

`setup.sh`は**何もインストールしません**。足りないものと入手先URLを表示するだけです。

## 4. アカウントを作る（15分）

| サービス | 何に使うか | やること |
|---|---|---|
| GitHub | コードの置き場 | https://github.com/signup で作成 → ターミナルで `gh auth login` |
| Vercel | 本番URLで公開する | https://vercel.com/signup で **Continue with GitHub** |
| Supabase | データベースとログイン | https://supabase.com/dashboard/sign-in で **Continue with GitHub** |

**クレジットカードは不要です。** 無料枠の範囲で作ります。会社で使うので、個人ではなく会社のメールで作るのがおすすめです。

## 5. 最終チェック

```bash
cd ~/Documents/Aigassyuku07/kit
./setup.sh                    # 最後が「要対応: 0」
./setup.sh --check-services   # NG が無い
```

- [ ] 困りごとメモと帳票の項目名がある
- [ ] `./setup.sh` の最後が `要対応: 0`
- [ ] `./setup.sh --check-services` に `NG` が無い
- [ ] Codexを開いてチャットできる
- [ ] Vercel と Supabase にGitHubでサインインできる

## うまくいかないとき

| 症状 | 対処 |
|---|---|
| `command not found: brew` | Homebrewのインストール最後に出た「Next steps」の2行を実行し、ターミナルを開き直す |
| `command not found: node` | `brew install node` のあと、ターミナルを開き直す |
| `gh`で認証を求められる | `gh auth login` → GitHub.com → HTTPS → ブラウザでログイン |
| 会社のPCで管理者権限がない | 情報システム担当に「Homebrew・Node.js・git・GitHub CLI・Codexを入れたい」と事前に依頼してください。間に合わなければ事前に講師へ連絡を |

詰まったら、次をAIに貼ってください。

```text
MacでAI合宿の事前準備をしています。
やりたいこと: Node.js / git / GitHub CLI / Codex を使える状態にしたい
実行したコマンド: [ここに貼る]
出たエラー: [ここに貼る]
初心者にもわかるように、次に確認することと、実行するコマンドを1つずつ教えてください。
```

**解決しなくても大丈夫です。** 当日の10:00〜の時間で拾います。
