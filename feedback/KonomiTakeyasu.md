# 体験ログ: KonomiTakeyasu

- 実施日: 2026-09-29
- 使ったAI: Claude（Claudeデスクトップアプリ Codeタブ）
- 題材: 担当者とお客様の間の「業務理解のラリー」を減らす、業務理解ボード（一般化した業務）
- 到達: Step 8（本番URLでログインしてお客様一覧が見える＋振り返り）

## 所要時間

| ページ / Step | 開始 | 終了 | 分 | ひとこと |
|---|---|---|---|---|
| 事前準備 | | 17:37 | 30〜60 | 本人の申告。目安（1〜2時間）より早い。迷ったのは作業フォルダとgh |
| 環境を整える（Step 0） | 17:40 | 17:53 | 13 | 要対応0。Sonnetが選べずHaikuに決めるので少し止まった |
| 困りごとを1文に（Step 1） | 17:53 | 17:57頃 | 4 | Haikuで実施。時刻はAIの推定（Haikuが記録しなかった） |
| MVPを作って触る（Step 2） | 17:57頃 | 18:08 | 約12 | MVPはHaikuが数分で作成。触る前に研究へ進もうとしたのでAIが止めた。直す回はせず |
| 研究（Step 3） | 18:08 | 18:10 | 2 | Opusで実施。質問8問に「全部推奨でOK」で即答 |
| 計画（Step 4） | 18:10 | 18:14 | 4 | Opusで実施。質問なしで計画一式を作成 |
| 土台（Step 5） | 18:15頃 | 18:22 | 約7 | Supabaseのプロジェクトは本人が作成済み。手順2〜6はOpusで実施（段階4は安いモデルの想定） |
| ログインと一覧（Step 6） | 18:24 | 18:46 | 22 | Opusで実施。SQLの2回実行（F8）と画面の再読み込みループ（F1）で止まったが、PRをマージまで |
| 本番（Step 7） | 18:47頃 | 18:59 | 約12 | Key/Value（F9）と No Deployment（F10）で迷ったが、docsのPRをマージしたら自動で本番ができた |
| 次の一手と振り返り（Step 8） | 19:00頃 | 19:10 | 約10 | サイトのまとめプロンプトで実施。reflectの案3つを全部採用し、AGENTS.md と dashboard-deploy に書き込んだ |

## 気づき

### F1. [Step 6 / 開発用サーバー] ログイン画面がずっと再読み込みを繰り返した

- 重さ: 高（進めなくなった）
- やろうとしたこと: SQLのあと、http://localhost:3000 でログインする
- 起きたこと: ログイン画面が出るが、数秒おきに再読み込みを繰り返して入力できない。原因は、Step 5 で起動した開発用サーバー（`npm run dev`）が動いたまま、AIが設定ファイル（next.config.ts）を変え、確認のため同じフォルダで `npm run build` も実行したこと。サーバーを止め、`.next` フォルダを消して起動し直したら直った
- 期待していたこと: コードを変えても、開いている画面がそのまま使える
- 直し案（あれば）: dashboard-slice / dashboard-auth に「画面がずっと再読み込みするときは、npm run dev を止めて（Ctrl+C）起動し直す」をつまずきの表に足す／AIへの指示（AGENTS.md）に「npm run dev が動いているときは npm run build をしない」を足す
- Issue: #6

### F2. [Step 5 / dashboard-repo 手順3] Windowsでは rsync が無く、`.agents/skills` のリンクもただのファイルになっている

- 重さ: 高（進めなくなった）※AIが tar に置き換えて進めた。手順のコマンドをそのまま貼ると止まる
- やろうとしたこと: 手順3のとおり、`rsync -a ... ../Aigassyuku07/kit/ ./` でキットの中身を `my-dashboard` へコピーする
- 起きたこと: このPC（Windows、Git Bash）には rsync が入っていない。AIが tar で同じ除外（.gitignore・setup.sh・.env.example）をしてコピーした。また、Codex用の `.agents/skills`（スキルへのリンク）は、Windowsでは中身が `../.claude/skills` と書かれた1行のファイルになっており、リンクとして働いていない（kit/ でも同じ）。Windows＋Codexの人はスキルが読めない可能性がある
- 期待していたこと: Windowsでも手順どおりに貼って進められる。Codexからもスキルが見える
- 直し案（あれば）: rsync を使わない手順にする（例: AIに「kit の中身を .gitignore・setup.sh・.env.example 以外コピーして」と頼む形にする）／`.agents/skills` はリンクをやめて実体を置くか、Windowsでの扱いを setup.sh で確認する
- Issue: #7

### F3. [事前準備 / Step 5] 作業フォルダの場所で迷った。後の手順が `~/Documents` 決め打ち

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: 「Codexで書類（Documents）フォルダを作業フォルダとして開く」→ そこへcloneする。Step 5 では手順2の `cd ~/Documents` でアプリを作る
- 起きたこと: どこを作業フォルダにするか迷い、結果として `書類` ではなく普段使いの `Github` フォルダ（`~/Github/Aigassyuku07`）にcloneした。TRIAL.mdの「続き」のプロンプト、締めの手順、dashboard-repo の手順2は `~/Documents` 決め打ちなので、この置き方だとパスが合わない。Step 5 ではAIが「Aigassyuku07 の隣」＝ `~/Github/my-dashboard` に読み替えて作った
- 期待していたこと: 置き場所を1つに決めてもらえる。または違う場所に置いても後の手順が壊れない
- 直し案（あれば）: 事前準備に「Windowsでは エクスプローラー → ドキュメント」のように開き方まで書く／すでに別フォルダで使っている人向けに「どこでもよいが、以後の `~/Documents/…` は自分の場所に読み替える」と一言添える／後のプロンプトと dashboard-repo は「cloneした Aigassyuku07 フォルダ（の隣）」と書く
- Issue: #8

### F4. [事前準備 / GitHub CLI] ghを入れたのに、AIからは `gh` コマンドが見つからない

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: キックオフ後、AIがTRIAL.mdの指示どおり `gh api user --jq .login` でユーザー名を調べた
- 起きたこと: `gh: command not found`。`C:\Program Files\GitHub CLI\gh.exe` は存在しており、フルパス指定なら動いた。インストール後にアプリ（Claude）を再起動していないため、PATHが反映されていないと思われる
- 期待していたこと: `gh` がそのまま使える
- 直し案（あれば）: 事前準備のghインストール手順の最後に「入れたら、Claude/Codexのアプリとターミナルをいったん閉じて開き直す」を足す
- Issue: #9

### F5. [2. 環境とAIの初期設定 / Step 0] ClaudeでSonnetがグレーアウトして選べない

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: 段階1用に、サイトの表どおりClaudeのモデルを「Sonnet」へ切り替える
- 起きたこと: Claudeデスクトップアプリ（Codeタブ）のモデル選択で、Sonnetがグレーアウトして選べなかった。選べたのは Opus と Haiku。サイトにもキット（ai-setup）にも、選べないときの代わりが書かれていない。Haikuで進めることにした
- 期待していたこと: 表のモデルが選べる。選べないときの代わり（例: 安いモデルはHaiku）が書いてある
- 直し案（あれば）: モデルの表に「Sonnetが選べないときはHaiku」のような代わりを1行足す／「名前ではなく安い・賢いの役割で選ぶ」の具体例として、選べるモデルの中でいちばん安いものを選ぶよう書く
- Issue: #10

### F6. [TRIAL.md 記録係 / Step 1〜2] 安いモデル（Haiku）に替えると、記録係の仕事が抜けた

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: モデルをHaikuに替えたあとも、「../TRIAL.md を読んで記録係を続けて」と頼んで進めた（AIが気づいた点）
- 起きたこと: Haikuはログ（docs/log.md）への記入とMVP作成はしたが、TRIAL.mdを読まず、所要時間の記録も、guide-steps.md のチェック（Step 1完了）もしなかった。Opusに戻したときに後から埋めた
- 期待していたこと: モデルを替えても、記録と進み具合のチェックが続く
- 直し案（あれば）: 記録係は賢いモデルのまま別セッションで持つ／各スキルの最後に「guide-steps.md のチェックを更新する」を明記する（いまは guide スキルにしか書いていない）
- Issue: #11

### F7. [Step 6 / dashboard-auth 手順4] このNext.jsでは、一覧の部品を `<Suspense>` で囲まないとビルドが通らない

- 重さ: 中（迷ったが進めた）※AIが気づいた点。今回は先に手引きを読んで避けた
- やろうとしたこと: 手順4のプロンプトで、`app/protected/page.tsx` を一覧画面にする
- 起きたこと: テンプレートのNext.js（16）は `cacheComponents` が有効で、ログイン情報やDBを読む部品を `<Suspense>` の外に置くとビルドが失敗する。dashboard-auth のプロンプトにはこの注意が無い。AGENTS.md に自動で足される英語のブロック（F14）には「node_modules の手引きを読め」とあるが、安いモデルが読まずに書くとここで詰まる見込み
- 期待していたこと: プロンプトどおりに頼めば、ビルドまで通る
- 直し案（あれば）: 手順4のプロンプトに「DBを読む部分は <Suspense> で囲んで（テンプレートの元の page.tsx と同じ形）」を1行足す
- Issue: #12

### F8. [Step 6 / dashboard-auth 手順3] SQLの「Run」を2回押すと「already exists」のエラーが出て、失敗したように見える

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: 手順3で、AIが書いたSQLを SQL Editor に貼って Run する
- 起きたこと: Runを2回押していた。1回目で成功していたが、画面に残ったのは2回目の `relation "clients" already exists` のエラー。失敗したと思ってAIに貼った
- 期待していたこと: 成功したかどうかが分かる。2回押しても壊れない
- 直し案（あれば）: 手順3に「成功すると Success. No rows returned と出る。Runは1回だけ。already exists と出たら、1回目で成功している」を足す／SQLを `create table if not exists` などで2回流しても平気な書き方にするよう、プロンプトで頼む
- Issue: #13

### F9. [Step 7 / dashboard-deploy] 「.env.local と同じ2つを入れる」が、Vercelの Key / Value の欄とつながらない

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: Vercelの `Environment Variables` に、`.env.local` と同じ2つを入れる
- 起きたこと: 手元では「URL」と「KEY」として覚えていたが、画面の欄は「Key」と「Value」。どちらに何を入れるか分からず止まった（「KEY」と「Key」が同じ言葉なのも紛らわしい）
- 期待していたこと: 欄の名前どおりに、何を入れるかが書いてある
- 直し案（あれば）: 手順を「Key に `NEXT_PUBLIC_SUPABASE_URL`、Value に URL（`https://` で始まる値）／Key に `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`、Value に KEY」の表にする。「.env.local の2行をまるごと Key の欄に貼ると自動で分かれる」も添える
- Issue: #14

### F10. [Step 7 / dashboard-deploy 手順4] Deployを押しても完了画面が出ず「No Deployment」のまま。本番URLがどれか分からない

- 重さ: 中（迷ったが進めた）
- やろうとしたこと: 環境変数を入れて `Deploy` → 完了画面のURLを控える
- 起きたこと: 画面は「Project "my-dashboard" created. Review the recommended integrations below, then deploy.」で止まり、Deployment欄は「Once you're ready, start deploying…」のまま。Domains画面にはURLが出ているが「No Deployment」の印つき。手順の「完了画面が出たら表示されたURLを控える」と画面が合わず、どれが本番URLか分からなかった。GitHubにPRを1つマージしたら、自動で本番が作られた
- 期待していたこと: 手順どおり完了画面が出て、そこにURLがある
- 直し案（あれば）: 「本番URLは プロジェクト → Domains の一番上（`〜.vercel.app`）」と場所を書く／「No Deployment のままなら、Deployments で作り直すか、GitHubに1つマージすると自動で作られる」を、つまずきの表に足す
- Issue: #15

### F11. [2. 環境とAIの初期設定] スキルの本数がページによって違う

- 重さ: 低（表現・見た目）
- やろうとしたこと: 講義ページを読み進めた（AIが気づいた点）
- 起きたこと: 「2. 環境とAIの初期設定」は「16本のスキル」、トップページは「スキル20本」。kitのCLAUDE.mdの表は20本
- 期待していたこと: 本数がそろっている
- 直し案（あれば）: 「16本」を「20本」にそろえる（または本数を書かない）
- Issue: #16

### F12. [事前準備ほか全ページ] 外部リンクが同じタブで開き、講義サイトを見ながら進めにくい

- 重さ: 低（表現・見た目）
- やろうとしたこと: 講義サイトを見ながら、Codex・Claude・Vercelなどのリンク先で作業する
- 起きたこと: 外部リンクが同じタブで開くため、講義サイトの画面が消え、手順を見ながら進められない
- 期待していたこと: 外部リンクは別タブで開き、講義サイトを横に置いたまま作業できる
- 直し案（あれば）: 外部サイトへのリンクに `target="_blank" rel="noopener"` を付ける（リンク横に「別タブ」の印があるとなおよい）
- Issue: #17

### F13. [PROMPT.md / 4. 作る] ステップ数が「10ステップ」と「8ステップ」で食い違う

- 重さ: 低（表現・見た目）
- やろうとしたこと: setup.sh の最後に出る「PROMPT.md を貼って」に従って PROMPT.md を読んだ（AIが気づいた点）
- 起きたこと: PROMPT.md は「作る（10ステップ）」、講義サイトの目次は「4. 作る（8ステップ）」。guide-steps.md は Step 0〜8
- 期待していたこと: 数がそろっている
- 直し案（あれば）: PROMPT.md の表記をサイトに合わせる
- Issue: #18

### F14. [Step 5 / dashboard-repo 手順5] `npm run dev` で Next.js が AGENTS.md に英語のブロックを書き足す

- 重さ: 低（表現・見た目）※AIが気づいた点
- やろうとしたこと: 手順5で `npm run dev` を実行した
- 起きたこと: Next.js が「Generated AGENTS.md for AI agents」と出し、キットから写した AGENTS.md の末尾に英語のブロック（このNext.jsは新しいので node_modules の説明を読め、という内容）を自動で足した。消しても次の起動でまた足される
- 期待していたこと: キットの AGENTS.md がそのまま残る（または、足されることが手順に書いてある）
- 直し案（あれば）: dashboard-repo に「AGENTS.md の末尾に英語のブロックが足されるが、そのままコミットしてよい」と一言足す／不要なら next.config の `agentRules: false` を案内する
- Issue: #19

### F15. [Step 5 / dashboard-repo 手順6] 作ったリポジトリの既定ブランチが `main` ではなく `master`

- 重さ: 低（表現・見た目）※AIが気づいた点。Vercel は `master` のまま本番を作れた。影響は見当たらない
- やろうとしたこと: 手順6の `gh repo create my-dashboard --private --source=. --push`
- 起きたこと: create-next-app が作ったgitの既定ブランチが `master` だったため、GitHubにも `master` で上がった。キットの他の文書（dashboard-deploy、CLAUDE.md 等）は `main` を前提に書いている所がある
- 期待していたこと: `main` で上がる
- 直し案（あれば）: 手順6の前に `git branch -M main` を入れる
- Issue: #20

### F16. [Step 6 / dashboard-auth] ログイン画面が英語のまま・「Sign up」のリンクが残る

- 重さ: 低（表現・見た目）※AIが気づいた点
- やろうとしたこと: 手順1で新規登録を止めたあと、ログイン画面を見る
- 起きたこと: テンプレートのログイン画面は英語（Login / Email / Password、エラーも「Invalid login credentials」）で、新規登録を止めたのに「Sign up」のリンクが残っている。押すと登録画面が出るが、登録はできない
- 期待していたこと: 新規登録を止めたら、画面からも登録の入口が消える
- 直し案（あれば）: dashboard-auth の手順4に「ログイン画面の文字を日本語にし、Sign up のリンクを消す」を足す（または後のスライスとしてロードマップに入れる）
- Issue: #21

### F17. [Windows / AIの道具] PowerShell でスキルを読むと日本語が文字化けする

- 重さ: 低（表現・見た目）※AIが気づいた点
- やろうとしたこと: AIが PowerShell の `Get-Content` で `.claude/skills/dashboard-auth/SKILL.md` を読んだ
- 起きたこと: Windows PowerShell 5.1 はBOMの無いUTF-8をShift-JISとして読むため、日本語が全部文字化けした。Claudeはファイル読み込みの道具に切り替えて読めたが、PowerShellしか使わないAI（Windows版Codexなど）はスキルを読み違える恐れがある
- 期待していたこと: どの読み方でもスキルが読める
- 直し案（あれば）: setup.sh（またはAGENTS.md）に「Windowsでは `Get-Content -Encoding UTF8` で読む」と書く／スキルのファイルをBOM付きUTF-8にする
- Issue: #22

## よかった所

- setup.sh の結果が「OK / 要対応」で分かれていて、読みやすかった（Step 0 は要対応 0 で通過）
- with-supabaseテンプレートは、.env.local に2つの値を貼るだけでSupabaseとつながり、手順5まで詰まらなかった
- 研究（Step 3）の質問が番号付き・推奨つきだったので、「全部推奨でOK」の1行で8問に答えられた
- Step 2で「ラリーを減らせそうか」という視点をAIが添えたら、業務の中身（確認している4項目、ラリーの原因、お客様も見る画面にしたい）が一気に出た
- 事前準備から本番URL（Step 7）と振り返り（Step 8）まで、約1時間40分（17:37〜19:10）で通せた

## 全体の感想（3行まで）

-
