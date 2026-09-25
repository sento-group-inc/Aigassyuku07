import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
SRC = os.path.join(ROOT, "scripts", "site-src")

SECTIONS = [
    ("はじめに", "", [("index", "このサイトの使い方")]),
    ("合宿の前に", "", [("prep", "事前準備")]),
    ("合宿中、手元に置く", "", [
        ("schedule", "日程と時間割"),
        ("skills", "道具（スキル一覧）"),
        ("repos", "リポジトリ一覧"),
    ]),
    ("1日目の講義", "", [
        ("why", "1. なぜやるのか"),
        ("setup", "2. 環境とAIの初期設定"),
        ("flow", "3. 作り方の4段階"),
        ("build", "4. 作る（8ステップ）"),
        ("pstack", "5. 迷ったときの進め方"),
    ]),
    ("2日目から", "", [("day2", "翌日以降の進め方")]),
]
ORDER = [k for _, _, items in SECTIONS for k, _ in items]
LABEL = {k: t for _, _, items in SECTIONS for k, t in items}
SECTION_OF = {k: (i, name) for i, (name, _, items) in enumerate(SECTIONS) for k, _ in items}
BUILD_STEPS = [
    (1, "困りごととログ"), (2, "MVP"), (3, "研究"), (4, "計画"),
    (5, "土台"), (6, "ログインと一覧"), (7, "本番"), (8, "次の一手"),
]

HEAD_SCRIPTS = """<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "strict", flowchart: { htmlLabels: true, curve: "basis" } });
</script>"""

BODY_SCRIPT = """<script>
document.querySelectorAll(".copy-btn").forEach(function (b) {
  b.addEventListener("click", function () {
    var text = b.closest(".prompt").querySelector("pre").innerText;
    navigator.clipboard.writeText(text).then(function () {
      b.textContent = "コピーしました"; b.classList.add("done");
      setTimeout(function () { b.textContent = "コピー"; b.classList.remove("done"); }, 1600);
    });
  });
});
var t = document.querySelector(".nav-toggle");
if (t) t.addEventListener("click", function () { document.body.classList.toggle("nav-open"); });
</script>"""


def fig(path, alt, caption=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    if os.path.exists(os.path.join(SITE, path)):
        return f'<figure><img src="{path}" alt="{html.escape(alt)}" loading="lazy">{cap}</figure>'
    return f'<figure><div class="shot">ここに画像: {html.escape(alt)}</div>{cap}</figure>'


def todo_fig(path, alt, caption=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    if os.path.exists(os.path.join(SITE, path)):
        return f'<figure><img src="{path}" alt="{html.escape(alt)}" loading="lazy">{cap}</figure>'
    return f'<figure><div class="shot todo">撮影待ち: {html.escape(alt)}</div>{cap}</figure>'


def prompt(text, head="AIに貼る（Codex / Claude の入力欄へ）"):
    return (f'<div class="prompt"><div class="prompt-head"><span>{head}</span>'
            f'<button class="copy-btn" type="button">コピー</button></div>'
            f'<pre><code>{html.escape(text.strip())}</code></pre></div>')


def term(cmd, why):
    return (f'<p class="term-note"><b>ここだけターミナルで</b>（{why}）</p>'
            f'<div class="prompt"><div class="prompt-head"><span>ターミナルに貼る</span>'
            f'<button class="copy-btn" type="button">コピー</button></div>'
            f'<pre><code>{html.escape(cmd.strip())}</code></pre></div>')


def mapblock(src, label="このページの地図"):
    return f'<section class="map"><div class="map-label">{label}</div><pre class="mermaid">\n{src.strip()}\n</pre></section>'


def analogy(text):
    return f'<div class="analogy"><div class="k">たとえるなら</div><p>{text}</p></div>'


def remember(items):
    return '<h2>覚えること（3つ）</h2><ol class="remember">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def call(name):
    return f'<div class="call"><span>入力欄で <b>/{name}</b> と打って候補から選ぶ</span><span>Codexは <b>${name}</b> でも可</span><span>文章でも: 「{name}で〜して」</span></div>'


def sidebar(key):
    out = ['<a class="brand" href="index.html">AI合宿</a>',
           '<div class="brand-sub">ダッシュボード構築 ・ 10/6〜7</div>']
    for i, (name, note, items) in enumerate(SECTIONS):
        out.append(f'<div class="side-sec"><div class="side-sec-title">{name}</div>')
        for k, t in items:
            cur = ' aria-current="page"' if k == key else ""
            out.append(f'<a class="side-link" href="{k}.html"{cur}>{t}</a>')
            if k == "build" and key == "build":
                out.append('<div class="side-sub">' + "".join(
                    f'<a href="#step{n}">Step {n} {t2}</a>' for n, t2 in BUILD_STEPS) + "</div>")
        out.append("</div>")
    return "\n".join(out)


def page(key, body):
    i = ORDER.index(key)
    sec_i, sec_name = SECTION_OF[key]
    prev_ = (f'<a class="prev" href="{ORDER[i-1]}.html"><span class="lbl">← 前へ</span>'
             f'<span class="ttl">{LABEL[ORDER[i-1]]}</span></a>') if i > 0 else '<span class="spacer"></span>'
    if i < len(ORDER) - 1:
        nk = ORDER[i + 1]
        next_ = (f'<a class="next" href="{nk}.html"><span class="lbl">次に読む（{SECTION_OF[nk][1]}）</span>'
                 f'<span class="ttl">{LABEL[nk]} →</span></a>')
    else:
        next_ = '<a class="next" href="index.html"><span class="lbl">おつかれさまでした</span><span class="ttl">最初のページへ戻る →</span></a>'
    title = "会社用ダッシュボード構築 — AI合宿" if key == "index" else f"{LABEL[key]} — AI合宿"
    doc = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="assets/style.css">
{HEAD_SCRIPTS}
</head>
<body>

<div class="mobilebar"><a class="brand" href="index.html">AI合宿</a><button class="nav-toggle" type="button">目次</button></div>

<div class="layout">
<nav class="sidebar" aria-label="目次">
{sidebar(key)}
</nav>

<div class="content">
<main>
<div class="crumb"><b>{sec_name}</b></div>

{body.strip()}

<div class="pager2">
  {prev_}
  {next_}
</div>
</main>
<footer>AI合宿 — 会社用ダッシュボード構築キット（2026年10月6日・7日）</footer>
</div>
</div>

{BODY_SCRIPT}
</body>
</html>
"""
    with open(os.path.join(SITE, f"{key}.html"), "w") as f:
        f.write(doc)


def read_src(name):
    with open(os.path.join(SRC, name)) as f:
        return f.read()


FIRST_PROMPT = """このフォルダで作業します。guide スキルを使って、docs/guide-steps.md を読み、
いまの状態（どのステップまで終わっているか）を判定してから、
次にやることを1つだけ指示してください。

指示するときは、必ず次を含めてください。
- 使うスキル名（例: dashboard-mvp, dashboard-research）
- 使うモデル（段階が変わるときは切り替え方も）
- 私がやること（手で操作する箇所があれば「どこを押すか」）
- 終わりの状態（何ができていれば次に進んでよいか）

コマンドの実行が必要なときは、私に頼まずにあなたが実行してください。
私は会社の業務ダッシュボードを作りたいです。困りごとのメモは手元にあります。"""

GRILL_PROMPT = """grill-with-docs で、私の困りごとを詰めてください。
困りごとのメモ: （ここに貼る）
帳票の項目名: （ここに貼る）
決まったことは README.md と CONTEXT.md に書いてください。"""

# ---------------------------------------------------------------- index
page("index", f"""
<h1>自社のダッシュボードを、自分たちで作って公開する</h1>
<p class="lede">題材は「ダッシュボードを1本作る」。持ち帰るのは、その過程で使う環境と進め方そのものです。</p>

<div class="goal"><strong>1日目の終わりに</strong>、自社の画面が自分のURLで開き（ログインして一覧が見える）、明日やることが1行で決まっている状態になります。</div>

<div class="facts">
  <div class="fact"><div class="k">日程</div><div class="v">10月6日(火)・7日(水)</div></div>
  <div class="fact"><div class="k">参加</div><div class="v">10社</div></div>
  <div class="fact"><div class="k">1日目</div><div class="v">講義と作業（まる1日）</div></div>
  <div class="fact"><div class="k">2日目</div><div class="v">自社の個別学習</div></div>
</div>

<h2>このサイトの使い方</h2>
<p><b>左の目次を上から下へ進めば、2日間が過ごせる</b>ように並べてあります。各ページの一番下の青いボタンで、次のページへ進めます。</p>

{mapblock('''
flowchart LR
  A["はじめに<br/>このページ"] --> B["合宿の前に<br/>事前準備"]
  B --> C["合宿中、手元に置く<br/>日程・スキル・リポジトリ"]
  C --> D["1日目の講義<br/>粗く作る→研究→計画→作り直す"]
  D --> E["2日目から<br/>自分で進める"]
''', "目次の全体図")}

<table>
  <tr><th>目次のセクション</th><th>いつ読むか</th><th>中身</th></tr>
  <tr><td>合宿の前に</td><td>10月6日までに</td><td><a href="prep.html">事前準備</a>。困りごとのメモ、Codexのインストール、アカウント作成</td></tr>
  <tr><td>合宿中、手元に置く</td><td>当日の朝と、迷ったとき</td><td><a href="schedule.html">日程と時間割</a>、<a href="skills.html">道具（スキル一覧）</a>、<a href="repos.html">リポジトリ一覧</a></td></tr>
  <tr><td>1日目の講義</td><td>10月6日、講義に合わせて</td><td>なぜやるのか → 環境とAIの初期設定 → 作り方の4段階 → 作る（8ステップ） → 迷ったときの進め方</td></tr>
  <tr><td>2日目から</td><td>10月7日と、その後</td><td><a href="day2.html">翌日以降の進め方</a></td></tr>
</table>

{analogy("自分の会社に<b>台所をひとつ作る</b>2日間です。材料（データ）の置き場と、火の入れ方（手順）を決めれば、料理（画面）はAIが手伝って作ってくれます。1日目は1品作れたら成功です。")}

<h2>完成するとこうなる（見本を触る）</h2>
<p>架空の工務店で作った「リフォーム案件ボード」の見本です。1日目のStep 2（段階1 粗く作る）で作るMVPの例で、ボタンを押すと絞り込みが動きます。</p>
{fig("assets/images/build/02-prototype.png", "見本のダッシュボード", '<a href="samples/prototype.html">見本を開いて触る</a>（データはすべて架空）')}
<div class="grid">
  <div class="card"><h3><a href="samples/prototype.html">MVPの見本</a></h3><p>Step 2（粗く作る）で作る、触れる試作。</p></div>
  <div class="card"><h3><a href="samples/readme.html">README の見本</a></h3><p>Step 3（研究）で書く、困りごとと業務の言葉。</p></div>
  <div class="card"><h3><a href="samples/schema.html">スキーマの見本</a></h3><p>Step 4（計画）で作る、テーブルとER図。</p></div>
  <div class="card"><h3><a href="samples/roadmap.html">ロードマップの見本</a></h3><p>Step 4（計画）で書く、作る順番とキーの表。</p></div>
</div>

<h2>持ち帰るもの</h2>
<div class="grid">
  <div class="card"><h3>本番URL</h3><p>自社の1業務が、ログインして一覧で見える状態。</p></div>
  <div class="card"><h3>手元の環境</h3><p>エージェント、スキル20本、AIの初期設定（モデルの使い分け）。次の案件でも同じ手順が使えます。</p></div>
  <div class="card"><h3>設計ドキュメント</h3><p>README・スキーマ・ロードマップ。AIに毎回説明しなくて済みます。</p></div>
  <div class="card"><h3>残りのスライス</h3><p>明日以降にやることの一覧。ガイドに「次は？」と聞けば進みます。</p></div>
</div>
""")

# ---------------------------------------------------------------- prep
page("prep", f"""
<h1>事前準備</h1>
<p class="lede">当日は朝から自社のダッシュボードを作り始めます。インストールとアカウント作成は、ここで済ませてきてください。所要1〜2時間。</p>

{mapblock('''
flowchart LR
  A["0 宿題<br/>困りごとメモ"] --> B["1 Codexを入れる"]
  B --> C["2 Homebrew<br/>ここだけターミナル"]
  C --> D["3 残りはAIに頼む<br/>道具とキット"]
  D --> E["4 アカウント<br/>GitHub・Vercel・Supabase"]
  E --> F["5 最終チェック<br/>AIに頼む"]
''')}

{analogy("<b>料理教室の前の買い出し</b>です。材料（困りごとのメモ）と道具（ソフトとアカウント）が揃っていれば、教室の時間を全部「作る」に使えます。")}

<div class="note"><p><b>ターミナルの操作はほとんどありません。</b>Codexを入れたあとは、青い枠のプロンプトをコピーしてCodexに貼れば、AIが代わりに実行します。詰まったら当日の10:00〜に拾う時間もあります。</p></div>

<h2>0. 宿題: 困りごとをメモする（いちばん大事）</h2>
<p>当日、AIがあなたの業務について質問します（<code>grill-with-docs</code>）。材料が多いほど、作るものが良くなります。<b>インストールより、これがいちばん効きます。</b></p>
<table>
  <tr><th>メモすること</th><th>例</th></tr>
  <tr><td>(a) 困りごとを1つ以上<br>誰が、何に困っていて、何が見えると嬉しいか</td><td>案件の進捗が誰にも見えず、毎朝口頭で確認している</td></tr>
  <tr><td>(b) いま使っている帳票の項目名<br>スプレッドシートや紙の見出しをそのまま</td><td>顧客名 / 担当 / 受付日 / 見積金額 / 状況 / 次アクション</td></tr>
</table>
<p>うまく書けないときは、ChatGPTやClaudeに次を貼ると、AIが質問しながら引き出してくれます。</p>
{prompt('''私の仕事の困りごとを言語化したいです。業務で「面倒なこと」「誰にも見えていないこと」
「毎回確認していること」を一緒に掘り下げてください。
質問は番号付きでまとめて出し、それぞれに推奨回答を添えてください。''', "ChatGPT / Claude に貼る")}
<div class="note warn"><p><b>個人情報や実データは持ち込まないでください。</b>画面はダミーデータで作ります。項目名（見出し）だけで十分です。</p></div>

<h2>1. Codexを入れてサインインする（10分）</h2>
<p><a href="https://openai.com/codex/">openai.com/codex</a> からCodexアプリを入れ、会社のChatGPTアカウントでサインインします。Claudeを使う人は <a href="https://claude.ai/download">claude.ai/download</a> からClaudeのアプリを入れてください。</p>
<p>入れたら、Codexで <b>書類（Documents）フォルダ</b>を作業フォルダとして開いておきます。</p>

<h2>2. Homebrewを入れる（Mac・10分）</h2>
<p>Homebrewは「道具を入れる道具」です。パスワードの入力が要るので、ここだけはターミナルで行います。</p>
{term('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', "Macのパスワード入力が必要なため")}
<p>ターミナルは <code>アプリケーション</code> → <code>ユーティリティ</code> → <code>ターミナル</code> にあります。貼って <code>return</code> を押し、Macのパスワードを入れます（入力中は何も表示されませんが、入っています）。最後に「Next steps」と出たら、その下の2行も同じように貼って実行します。</p>
<p>Windowsの人はこの手順は不要です。次の3へ進んでください。</p>

<h2>3. 残りの道具とキットは、AIに頼む（10分）</h2>
<p>Codexに次を貼ります。Node.js・git・GitHub CLIを入れて、合宿のキットを取ってきて、足りないものがないか確かめてくれます。</p>
{prompt('''AI合宿の事前準備をしています。次を順番にやってください。コマンドはあなたが実行してください。
1. Node.js（20以上）、git、GitHub CLI（gh）が入っているか確認し、無ければ入れる（MacはHomebrew、Windowsはwinget）
2. このフォルダに https://github.com/sento-group-inc/Aigassyuku07 をcloneする
3. Aigassyuku07/kit フォルダで ./setup.sh を実行し、結果を初心者にも分かる言葉で説明する
NG が出たら、直し方を1つずつ教えてください。''')}
{fig("assets/images/setup/01-setup-sh.png", "setup.shの実行結果", "AIが裏で実行する確認の中身（実際の出力）。最後が「要対応: 0」なら道具は揃っている")}

<h2>4. アカウントを作る（15分）</h2>
<table>
  <tr><th>サービス</th><th>何に使うか</th><th>やること</th></tr>
  <tr><td>GitHub</td><td>コードの置き場</td><td><a href="https://github.com/signup">github.com/signup</a> でアカウントを作る</td></tr>
  <tr><td>Vercel</td><td>本番URLで公開する</td><td><a href="https://vercel.com/signup">vercel.com/signup</a> で <b>Continue with GitHub</b></td></tr>
  <tr><td>Supabase</td><td>データベースとログイン</td><td><a href="https://supabase.com/dashboard/sign-in">supabase.com/dashboard/sign-in</a> で <b>Continue with GitHub</b></td></tr>
</table>
<div class="grid">
  {fig("assets/images/prep/03-vercel-signup.png", "Vercelのサインアップ画面", "Vercel: 「Continue with GitHub」を押す")}
  {fig("assets/images/prep/04-supabase-signin.png", "Supabaseのサインイン画面", "Supabase: 「Continue with GitHub」を押す")}
</div>
<p><b>クレジットカードは不要です。</b>無料枠の範囲で作ります。会社で使うので、会社のメールで作るのがおすすめです。</p>
<p>最後に、手元のPCからGitHubを使えるようにします。ブラウザでのやり取りがあるので、ここもターミナルで行います。</p>
{term("gh auth login", "ブラウザでのログイン確認が必要なため")}
<p>質問には <code>GitHub.com</code> → <code>HTTPS</code> → <code>Login with a web browser</code> の順に、矢印キーと <code>return</code> で答えます。表示された8桁のコードを、開いたブラウザに入れます。</p>

<h2>5. 最終チェック</h2>
{prompt('''Aigassyuku07/kit フォルダで ./setup.sh と ./setup.sh --check-services を実行して、
全部OKかどうかを教えてください。NG があれば直し方も教えてください。''')}
<table>
  <tr><th>確認</th><th>OKの状態</th></tr>
  <tr><td>困りごとメモ</td><td>困りごとの1文と、帳票の項目名がある</td></tr>
  <tr><td>AIの答え</td><td>「要対応: 0」で、GitHubが「サインイン済み」</td></tr>
  <tr><td>Vercel / Supabase</td><td>GitHubでサインインできる</td></tr>
</table>

<h2>うまくいかないとき</h2>
<table>
  <tr><th>症状</th><th>対処</th></tr>
  <tr><td>Homebrewのあとに <code>brew</code> が見つからない</td><td>「Next steps」の2行を実行し忘れている。ターミナルを開き直して、その2行を貼る</td></tr>
  <tr><td>AIが「権限がない」と言う</td><td>Codexの画面に出る「許可」ボタンを押す。分からなければその画面のまま当日持ってくる</td></tr>
  <tr><td>会社のPCで管理者権限がない</td><td>情報システム担当に「Homebrew・Node.js・git・GitHub CLI・Codexを入れたい」と事前に依頼する。間に合わなければ講師へ事前に連絡</td></tr>
</table>

{remember(["いちばん大事なのは<b>困りごとのメモ</b>。インストールより効く", "ターミナルは<b>Homebrewとgh auth loginの2か所だけ</b>。あとはAIに頼む", "解決しなくても大丈夫。<b>当日10:00〜</b>で拾う"])}
""")

# ---------------------------------------------------------------- schedule
page("schedule", f"""
<h1>日程と時間割</h1>
<p class="lede">1日目で自社のURLまで行きます。2日目は各社が自分のペースで個別学習に入ります。</p>

<div class="facts">
  <div class="fact"><div class="k">1日目</div><div class="v">10月6日(火) 9:30〜18:00</div></div>
  <div class="fact"><div class="k">2日目</div><div class="v">10月7日(水) 個別学習</div></div>
  <div class="fact"><div class="k">参加</div><div class="v">10社</div></div>
</div>

{mapblock('''
flowchart LR
  subgraph D1["1日目 10/6"]
    direction TB
    A["午前<br/>環境・初期設定<br/>段階1 粗く作る"] --> B["午後前半<br/>段階2 研究<br/>段階3 計画"]
    B --> C["午後後半<br/>段階4 作り直す<br/>本番・発表"]
  end
  subgraph D2["2日目 10/7"]
    direction TB
    E["ログから今日の1スライス"] --> F["安いモデルで実装→本番"]
  end
  D1 --> D2
''', "2日間の全体図")}

{analogy("<b>登山の行程表</b>です。どこで休憩し、どこまで登っていれば順調かが書いてあります。遅れても、次のチェックポイントで立て直せます。")}

<h2>1日目（10月6日）の時間割</h2>
<table>
  <tr><th>時刻</th><th>内容</th><th>モデル</th><th>講義ページ</th></tr>
  <tr><td>09:30</td><td>オープニング。なぜやるのかを腹落ちさせる</td><td>—</td><td><a href="why.html">1. なぜやるのか</a></td></tr>
  <tr><td>10:00</td><td>環境とAIの初期設定・Step 0</td><td>—</td><td><a href="setup.html">2. 環境とAIの初期設定</a></td></tr>
  <tr><td>10:20</td><td>作り方の4段階を知る</td><td>—</td><td><a href="flow.html">3. 作り方の4段階</a></td></tr>
  <tr><td>10:40</td><td><b>段階1 粗く作る</b>。困りごとをログに書き、MVPを作って触る・Step 1〜2</td><td>安い</td><td><a href="build.html#step1">4. Step 1〜2</a></td></tr>
  <tr><td>12:00</td><td>昼食</td><td>—</td><td>—</td></tr>
  <tr><td>13:00</td><td><b>段階2 研究する</b>・Step 3</td><td>賢い</td><td><a href="build.html#step3">4. Step 3</a></td></tr>
  <tr><td>14:00</td><td><b>段階3 計画する</b>・Step 4</td><td>賢い</td><td><a href="build.html#step4">4. Step 4</a></td></tr>
  <tr><td>15:00</td><td><b>段階4 ゼロから作り直す</b>。土台、ログインと一覧・Step 5〜6</td><td>安い</td><td><a href="build.html#step5">4. Step 5〜6</a></td></tr>
  <tr><td>16:45</td><td>本番へ出して動作確認・Step 7</td><td>安い</td><td><a href="build.html#step7">4. Step 7</a></td></tr>
  <tr><td>17:15</td><td>発表（1社5分）と次の一手・振り返り・Step 8</td><td>—</td><td><a href="build.html#step8">4. Step 8</a></td></tr>
</table>

<h2>チェックポイント</h2>
<p>次の3つを過ぎたら講師に声をかけてください。一度止めて確認する方が、後で速くなります。</p>
<table>
  <tr><th>時刻</th><th>できていてほしいもの</th><th>できていなければ</th></tr>
  <tr><td>12:00</td><td>触れるMVPがあり、ログに要望が5つ以上ある</td><td>題材を小さくする。スプレッドシートの列名をそのまま画面にする</td></tr>
  <tr><td>15:00</td><td>研究と計画（スキーマ・ロードマップ）がある</td><td>最優先で戻る。無いと作り直しが迷走する</td></tr>
  <tr><td>17:00</td><td>本番URLがある</td><td>無くても大丈夫。原因をログに書いて、次の一手にする</td></tr>
</table>

<h2>発表フォーマット（1社5分）</h2>
<table>
  <tr><th>項目</th><th>話すこと</th></tr>
  <tr><td>作ったもの</td><td>何の業務を、どう見えるようにしたか（画面を見せる）</td></tr>
  <tr><td>できたこと</td><td>本番URL、動いている操作</td></tr>
  <tr><td>詰まったこと</td><td>どこで止まったか（<b>ここが一番価値があります</b>）</td></tr>
  <tr><td>次にやること</td><td>明日の1スライス</td></tr>
</table>

<h2>2日目（10月7日）</h2>
<p>各社が自分のペースで進めます。会場は開放し、詰まったところを個別に拾います。進め方は<a href="day2.html">翌日以降の進め方</a>にあります。</p>
<table>
  <tr><th>時刻</th><th>やること</th></tr>
  <tr><td>09:30</td><td>ガイドに「次は何をすればいい？」と聞き、<b>今日の1スライス</b>を決める</td></tr>
  <tr><td>10:00〜</td><td>安いモデルでスライスを実装 → PR → マージ → 本番（要望はログへ）</td></tr>
  <tr><td>終わり</td><td><code>reflect</code>で学びを残し、明日の1スライスを決める</td></tr>
</table>

<h2>うまくいかないときの合図</h2>
<table>
  <tr><th>症状</th><th>やること</th></tr>
  <tr><td>同じエラーで10分止まっている</td><td>エラー文をそのまま講師に見せる（自分で直そうとしない）</td></tr>
  <tr><td>何を作るか決まらない</td><td>いま使っているスプレッドシートの列名をそのまま持ってくる</td></tr>
  <tr><td>時間が足りない</td><td>スコープを半分に割る。半分でも「動く」を作る</td></tr>
</table>

{remember(["1日目のゴールは<b>本番URLでログインして一覧が見える</b>こと", "<b>12時・15時・17時</b>のチェックポイントで講師に声をかける", "発表で一番価値があるのは<b>詰まった場所</b>"])}
""")

# ---------------------------------------------------------------- skills
SK = [
    ("進行役と土台", [
        ("guide", "「次は何をすればいい？」に、現在地と次の一手を1つだけ返す。<b>迷ったらまずこれ</b>", "全Step"),
        ("ai-setup", "段階ごとに使うモデル（安い／賢い）を確認・切り替える。PC全体への反映も手伝う", "Step 0・段階の変わり目"),
        ("dev-log", "要望・気づき・決定・詰まりを docs/log.md に1行ずつ残す", "いつでも"),
    ]),
    ("段階1 粗く作る（安いモデル）", [
        ("dashboard-mvp", "困りごとの1文から、触れる粗い試作（mvp/index.html）を素早く作る", "Step 2"),
    ]),
    ("段階2・3 研究と計画（賢いモデル）", [
        ("dashboard-research", "MVPとログを6つの観点で研究し、docs/research.md に残す", "Step 3"),
        ("grill-with-docs", "ユーザーしか知らないことを番号付きの質問で詰め、README / CONTEXT.md に残す", "Step 3"),
        ("dashboard-plan", "作り直すための計画一式を作る（下の4本を順に使う）", "Step 4"),
        ("dashboard-schema", "画面の情報をテーブルとつながりに落とし、ER図で漏れを潰す", "Step 4"),
        ("dashboard-roadmap", "確認できる単位に切り、手前で価値が出る順に並べる", "Step 4"),
        ("dashboard-keys", "必要なキーと置き場所の表を作る（値は書かない）", "Step 4"),
        ("dashboard-docs", "docs と AGENTS.md / CLAUDE.md を整え、AIの前提をそろえる", "Step 4"),
    ]),
    ("段階4 ゼロから作り直す（安いモデル）", [
        ("dashboard-repo", "Supabase・ログイン付きアプリの土台・GitHubリポジトリを作る", "Step 5"),
        ("dashboard-auth", "社員だけがログインでき、ログインすると一覧が見える状態を作る", "Step 6"),
        ("dashboard-slice", "1スライスを実装 → 動かして確認 → PR → マージ", "Step 6〜"),
        ("dashboard-deploy", "データベースを先、アプリを後の順で本番へ出す", "Step 7"),
    ]),
    ("進め方（pstack）", [
        ("poteto-mode", "足りないものを1つ見つけ、次の一手を理由つきで案内する", "迷ったとき"),
        ("pstack-guide", "場面から開発の原則を引く（足す前に引く、実物で示す…）", "迷ったとき"),
        ("reflect", "学びを3つまで拾い、docsやスキルへ残す案を出す", "Step 8・毎日"),
    ]),
    ("伝える・見た目", [
        ("eli5", "前提知識のない人に、たとえ1つと覚える3つで説明する", "社内説明"),
        ("lp-guide", "参考サイトを3つ集め、借りる範囲を決めてから画面を作る", "見た目に迷ったとき"),
    ]),
]
rows = ""
for group, items in SK:
    rows += f'<tr><th colspan="3">{group}</th></tr>'
    for name, what, when in items:
        rows += (f'<tr><td><a href="https://github.com/sento-group-inc/Aigassyuku07/blob/main/kit/.claude/skills/{name}/SKILL.md">'
                 f'<code>{name}</code></a></td><td>{what}</td><td>{when}</td></tr>')

page("skills", f"""
<h1>道具 — キットに入っているスキル</h1>
<p class="lede"><b>結論:</b> 覚えるのは <code>guide</code> と「ログして」の一言だけ。ほかのスキルは、ガイドが「次はこれ」と教えてくれます。</p>

{mapblock('''
flowchart LR
  G["guide<br/>進行役"] --> A["段階1<br/>dashboard-mvp"]
  G --> B["段階2・3<br/>research・grill・plan"]
  G --> C["段階4<br/>repo・auth・slice・deploy"]
  L["dev-log<br/>いつでもログ"] -.-> A
  L -.-> B
  L -.-> C
  M["ai-setup<br/>段階ごとのモデル"] -.-> G
''')}

{analogy("スキルは<b>料理のレシピカード</b>です。AIはカードを読んでから手を動かすので、毎回同じ手順で作れます。カードは20枚ありますが、全部を覚えるのは先生（ガイド）の仕事です。")}

<h2>呼び方</h2>
<p>Codex（またはClaude）の入力欄に、スキル名を入れて頼みます。どの書き方でも動きます。</p>
{call("guide")}
{fig("assets/images/skills/01-skill-picker.png", "Codexの入力欄で /grill と打ち、スキルの候補が出ている画面", "① 入力欄で <code>/</code> に続けて名前の一部を打つと、候補が出る")}
  {fig("assets/images/skills/02-skill-chip.png", "候補から選んだスキルが入力欄にチップとして入った画面", "② 選ぶと入力欄にチップとして入る。続けて頼みたいことを書いて送る")}
<p>スキルの中身は <code>kit/.claude/skills/〈名前〉/SKILL.md</code> にあります（Codexは同じものを <code>kit/.agents/skills/</code> から読みます）。普通の文章なので、開いて読めば何をするか分かります。</p>

<h2>一覧（20本）</h2>
<table>
  <tr><th>名前</th><th>何をするか</th><th>いつ</th></tr>
  {rows}
</table>

<h2>ガイドの返し方</h2>
<p>ガイドは毎回、次の形で1つだけ返します。</p>
<table>
  <tr><th>項目</th><th>例</th></tr>
  <tr><td>現在地</td><td>Step 3（スキーマとER図）</td></tr>
  <tr><td>次の一手</td><td>画面に出ている情報を全部書き出し、テーブルにまとめる</td></tr>
  <tr><td>使うスキル</td><td><code>dashboard-schema</code></td></tr>
  <tr><td>あなたがやること</td><td>AIが出した表を見て、足りない項目を言う</td></tr>
  <tr><td>終わりの状態</td><td><code>docs/schema.md</code> にテーブル一覧とER図がある</td></tr>
</table>

<h2>出典</h2>
<p><code>grill-with-docs</code> は <a href="https://github.com/mattpocock/skills">mattpocock/skills</a>（MIT）、<code>poteto-mode</code> / <code>pstack-guide</code> / <code>reflect</code> は <a href="https://github.com/cursor/plugins/tree/main/pstack">pstack</a>（MIT）を合宿向けに日本語で書き直したものです。<code>dashboard-*</code> は実案件で回った手順を、顧客情報を除いて一般化しました。詳しくは<a href="repos.html">リポジトリ一覧</a>。</p>

{remember(["覚えるのは <b><code>guide</code> だけ</b>", "呼び方は <b>Codex <code>$名前</code> / Claude <code>/名前</code> / 文章</b> のどれでも", "中身は <b>SKILL.md を開けば読める</b>普通の文章"])}
""")

# ---------------------------------------------------------------- repos
page("repos", f"""
<h1>リポジトリ一覧</h1>
<p class="lede">今回の合宿で使うリポジトリとサービス、手順の出典をまとめました。<b>当日使うのは「当日使う」の表だけ</b>で十分です。</p>

{mapblock('''
flowchart LR
  K["合宿キット<br/>Aigassyuku07"] --> T["アプリの土台<br/>with-supabase"]
  T --> S["データとログイン<br/>Supabase"]
  T --> V["公開<br/>Vercel"]
  K --> G["コードの置き場<br/>GitHub"]
  K -. 出典 .-> P["pstack / grill-with-docs"]
''')}

{analogy("<b>台所の道具と、レシピ本の棚</b>です。当日使う道具は手の届く所に、レシピの出典は棚に並べておきます。")}

<h2>当日使う</h2>
<table>
  <tr><th>リポジトリ / サービス</th><th>何に使うか</th><th>いつ</th></tr>
  <tr><td><a href="https://github.com/sento-group-inc/Aigassyuku07">sento-group-inc/Aigassyuku07</a></td><td>この合宿のキット（スキル16本・docs雛形・setup.sh）と講義サイト</td><td>事前準備〜</td></tr>
  <tr><td><a href="https://github.com/vercel/next.js/tree/canary/examples/with-supabase">vercel/next.js — with-supabase</a></td><td>ログイン画面つきのアプリの土台。Step 6でAIが作る</td><td>Step 6</td></tr>
  <tr><td><a href="https://supabase.com/dashboard">Supabase</a>（<a href="https://github.com/supabase/supabase">supabase/supabase</a>）</td><td>データベースとログイン（社員アカウント）</td><td>Step 6・8</td></tr>
  <tr><td><a href="https://vercel.com/new">Vercel</a>（<a href="https://github.com/vercel/vercel">vercel/vercel</a>）</td><td>GitHubにつなぐだけで本番URLを作る</td><td>Step 9</td></tr>
  <tr><td><a href="https://github.com/">GitHub</a> / <a href="https://github.com/cli/cli">cli/cli</a></td><td>コードの置き場と、PCからの操作（<code>gh</code>）</td><td>Step 6・8</td></tr>
  <tr><td><a href="https://openai.com/codex/">Codex</a>（<a href="https://github.com/openai/codex">openai/codex</a>）</td><td>合宿のメインのAIエージェント</td><td>全Step</td></tr>
  <tr><td><a href="https://claude.ai/download">Claude Code</a></td><td>Claudeを使う人のエージェント。同じキットで動く</td><td>全Step</td></tr>
</table>

<h2>スキルの出典</h2>
<table>
  <tr><th>リポジトリ</th><th>キットのどのスキルか</th><th>ライセンス</th></tr>
  <tr><td><a href="https://github.com/cursor/plugins/tree/main/pstack">cursor/plugins — pstack</a></td><td><code>poteto-mode</code> / <code>pstack-guide</code> / <code>reflect</code>（日本語で書き直し）</td><td>MIT</td></tr>
  <tr><td><a href="https://github.com/mattpocock/skills">mattpocock/skills</a></td><td><code>grill-with-docs</code>（日本語で書き直し。CONTEXT.md・ADRの書式を同梱）</td><td>MIT</td></tr>
</table>

<h2>慣れてきたら</h2>
<table>
  <tr><th>リポジトリ</th><th>何ができるか</th></tr>
  <tr><td><a href="https://github.com/vercel-labs/agent-browser">vercel-labs/agent-browser</a></td><td>AIにブラウザを操作させ、公開した画面を確認・撮影させる（この講義サイトのスクリーンショットもこれで撮影）</td></tr>
  <tr><td><a href="https://github.com/supabase/cli">supabase/cli</a></td><td>データベースの変更をファイル（migration）で管理する。スライスが増えてきたら</td></tr>
  <tr><td><a href="https://github.com/cursor/plugins/tree/main/pstack">pstack本体</a></td><td>複数案の競争（arena / swarm）、詳細設計（architect）など、合宿で入れなかった道具</td></tr>
</table>

<h2>便利そうなリポジトリを見つけたら</h2>
{prompt("このリポジトリが私たちのダッシュボード作りに使えるか、何に使えるかを3行で教えて。URL: （ここに貼る）")}

{remember(["当日使うのは <b>キット・with-supabase・Supabase・Vercel・GitHub</b>", "スキルの一部は <b>pstack と mattpocock/skills（MIT）</b>の日本語版", "便利そうなものは<b>AIに「使えるか」を先に聞く</b>"])}
""")

# ---------------------------------------------------------------- why
why_body = read_src("why-body.html")
why_map = mapblock('''
flowchart LR
  A["昔: 料理を頼む<br/>システムは外注"] --> B["今: 台所を持つ<br/>言葉にすれば形になる"]
  B --> C["でも壁がある<br/>考慮点・移行・権限・保守"]
  C --> D["壁の手前で頼む<br/>限界を早く正確に知る"]
''')
page("why", why_body.replace("<h2>", why_map + "\n\n<h2>", 1))

# ---------------------------------------------------------------- setup
page("setup", f"""
<h1>環境とAIの初期設定</h1>
<p class="lede">当日の朝にやることです。インストールは<a href="prep.html">事前準備</a>で済んでいる前提で、キットを開いてガイドに最初の一言を送るところまで進めます。画面はCodex基準で説明します。</p>

<div class="goal"><strong>このページを終えると</strong>、エージェントがキットを読んで「次にやること」を返してくれ、段階ごとにどのモデルを使うかが分かる状態になります。</div>

{mapblock('''
flowchart LR
  A["1 キットを開く<br/>Codex / Claude"] --> B["2 最初の一言<br/>コピーして貼る"]
  B --> C["AIが環境を確認<br/>setup.sh"]
  C --> D["ガイドが<br/>次の一手を返す"]
''')}

{analogy("<b>料理教室の調理台</b>に立つところです。レシピ（キット）を開き、先生（ガイド）に「何から始めますか？」と聞けば、道具が揃っているかも先生が確かめてくれます。")}

<h2>当日の手順</h2>
<ol class="steps">
  <li>
    <h3>キットをエージェントで開く</h3>
    <p>Codexを起動し、<code>書類</code> → <code>Aigassyuku07</code> → <code>kit</code> フォルダを作業フォルダとして開きます。<b>開くのは <code>kit</code> です</b>（親の <code>Aigassyuku07</code> ではありません）。</p>
    {fig("assets/images/setup/03-codex-open.png", "Codexでkitフォルダを選んでいる画面", "Codexの入力欄の「+」からフォルダを選び、<code>Aigassyuku07</code> の中の <code>kit</code> を選んで「開く」")}
    <div class="note claude"><p><b>Claudeを使う人:</b> Claude Codeで同じフォルダを開きます。<code>CLAUDE.md</code>が読まれ、<code>.claude/skills/</code>のスキルが使えます。</p></div>
  </li>
  <li>
    <h3>最初の一言を送る</h3>
    <p>下のプロンプトをコピーして、入力欄に貼って送ります。</p>
    {prompt(FIRST_PROMPT)}
    {fig("assets/images/setup/04-first-prompt.png", "入力欄に最初のプロンプトを貼った、送信する直前の画面", "入力欄に貼ったら、右下の送信ボタン（または return）で送る")}
    <p>AIが <code>setup.sh</code> を自分で実行して環境を確かめ、「現在地・次の一手・使うスキル・終わりの状態」を返してくれば成功です。</p>
    <div class="note"><p><b>実際の応答例（Codexでリハーサルした結果）</b></p><pre><code>{html.escape(read_src("guide-reply.txt").strip())}</code></pre></div>
  </li>
</ol>

<h2>AIの初期設定（モデルの使い分け）</h2>
<p>このキットでは、<b>仕事の種類でAIのモデルを使い分けます</b>。手を動かす量が多い仕事は安くて速いモデル、全体を見直す仕事はいちばん賢いモデルに任せます。講師が普段使っている設定と同じ考え方です。</p>
{analogy("<b>職人と設計士の使い分け</b>です。量の多い作業は腕の速い職人（安いモデル）に、図面の見直しは設計士（賢いモデル）に。全部を設計士に頼むと高くて遅く、全部を職人に任せると直すべき所に気づけません。")}
<table>
  <tr><th>仕事</th><th>使うモデル</th><th>Codex（2026年10月時点）</th><th>Claude</th></tr>
  <tr><td>作る・作り直す（段階1・4）</td><td>安くて速い</td><td>GPT-5.6 Luna / Sol</td><td>Sonnet</td></tr>
  <tr><td>研究・計画（段階2・3）</td><td>いちばん賢い</td><td>GPT-6 Astra</td><td>Opus</td></tr>
  <tr><td>手伝い役のAI（サブエージェント）</td><td>本体より一段下</td><td>—</td><td>本体Opusなら Sonnet</td></tr>
  <tr><td>見直し役のAI（レビュー）</td><td>本体と同じ</td><td>—</td><td>本体と同じ</td></tr>
</table>
<p>モデルの名前は数か月で変わります。名前ではなく「安い／賢い」の役割で覚えてください。</p>

<h3>このキットでの前提</h3>
<ul>
  <li><b>ChatGPT（Codex）やClaudeの有料プラン（Pro等）を契約している前提</b>です。上の表のモデルが選べます。</li>
  <li>キットの設定は<b>キットのフォルダの中だけ</b>に効きます。あなたのPC全体の設定（<code>~/.codex</code>、<code>~/.claude</code>）は書き換えません。</li>
  <li><b>Codex</b>は、段階ごとに入力欄右下のモデル選択で切り替えます（フォルダ単位のモデル設定がCodexには効かないため）。</li>
  <li><b>Claude Code</b>は、キットの <code>.claude/settings.json</code> で手伝い役のAIを <code>sonnet</code> にしてあります。本体は <code>/model</code> と打って切り替えます。</li>
</ul>
{fig("assets/images/setup/04-first-prompt.png", "Codexの入力欄右下にモデル選択がある画面", "Codexは入力欄の右下（この画像では「GPT-5.6 Sol 中」）を押して、段階に合うモデルを選ぶ")}

<h3>PC全体に恒久的に入れたいとき</h3>
<p>合宿のあとも同じ使い分けを全部の作業で使いたくなったら、次を貼ってください。AIが変更内容を見せ、同意してから書き換えます（元のファイルは残します）。</p>
{prompt("""ai-setup で、このモデルの使い分けを私のPC全体の設定に恒久的に入れたいです。
どのファイルに何を書くかを先に見せてください。私が「OK」と言ってから書き換え、元のファイルは .bak として残してください。""")}

<h2>AIが裏でやっている確認</h2>
<p>ガイドは最初に <code>setup.sh</code> を実行して、道具が揃っているかを確かめます。自分で確かめたいときは、次を貼ってください。</p>
{prompt("./setup.sh と ./setup.sh --check-services を実行して、結果を初心者にも分かる言葉で教えてください。NG があれば直し方も。")}
<div class="grid">
  {fig("assets/images/setup/01-setup-sh.png", "setup.shの実行結果", "道具の確認。最後が「要対応: 0」ならOK")}
  {fig("assets/images/setup/02-check-services.png", "setup.sh --check-servicesの実行結果", "GitHubにサインイン済みかの確認")}
</div>

<h2>スキルの呼び方</h2>
<p>キットには16本のスキル（AIへの手順書）が入っています。呼び方は3通りあり、どれでも動きます。</p>
{call("guide")}
<p><b>覚えるのは <code>guide</code> だけ</b>で大丈夫です。次に使うスキルは、ガイドが教えてくれます。一覧は<a href="skills.html">道具（スキル一覧）</a>にあります。</p>

<h2>うまくいかないとき</h2>
<table>
  <tr><th>症状</th><th>対処</th></tr>
  <tr><td>エージェントがスキルを知らないと言う</td><td>開いているフォルダが <code>kit</code> か確認する。親の <code>Aigassyuku07</code> を開いていると読めない</td></tr>
  <tr><td>「コマンドを実行してよいか」と聞かれる</td><td>内容を読んで「許可」を押す。分からなければ講師を呼ぶ</td></tr>
  <tr><td>GitHubが「未サインイン」と言われる</td><td>ターミナルで <code>gh auth login</code> を実行する（<a href="prep.html">事前準備の4</a>）</td></tr>
  <tr><td>会社のPCで入れられない</td><td>隣の人と2人1組で1台を使い、自社の題材で進める。帰社後のインストール依頼は<a href="prep.html">事前準備</a>の依頼文を使う</td></tr>
</table>

{remember(["開くのは <b><code>kit</code> フォルダ</b>（親フォルダではない）", "作る・作り直すは<b>安いモデル</b>、研究・計画は<b>いちばん賢いモデル</b>", "覚えるのは <b><code>guide</code> と「ログして」</b>だけ"])}
""")

# ---------------------------------------------------------------- flow
page("flow", f"""
<h1>作り方の4段階</h1>
<p class="lede"><b>結論:</b> 最初から完璧な計画は立てません。<b>粗く作って、賢いAIに研究させ、計画して、ゼロから作り直す</b>。この順番がいちばん速く、いちばん良いものができます。</p>

<div class="goal"><strong>このページを読むと</strong>、今日の作業がなぜこの順番なのか、そして途中で何を守ればよいかが分かります。</div>

{mapblock('''
flowchart LR
  A["1 粗く作る<br/>安いモデル<br/>MVPを最速で"] --> B["2 研究する<br/>賢いモデル<br/>品質を上げる方法"]
  B --> C["3 計画する<br/>賢いモデル<br/>作り直しの図面"]
  C --> D["4 ゼロから作り直す<br/>安いモデル<br/>図面だけ見て"]
  L["開発ログ docs/log.md<br/>要望・決定・詰まり"] -.-> A
  L -.-> B
  L -.-> C
  L -.-> D
''')}

{analogy("<b>段ボールの模型→一級建築士の診断→図面→本物の建築</b>です。まず段ボールで置いてみて、プロに弱い所を洗い出してもらい、図面に起こしてから、本物は図面どおりに建てます。段ボールの模型は、本物の材料にはしません。")}

<h2>4つの段階</h2>
<ol class="steps">
  <li><h3>とにかく粗く実装する</h3><p><b>安いモデル</b>（Codex は Luna / Sol、Claude は Sonnet）で、触れるMVP（最小の試作）を15〜30分で作ります。完成度は気にしません。触って出た「ここが使いにくい」「これも見たい」を全部ログに残すのが目的です。</p></li>
  <li><h3>研究する</h3><p><b>いちばん賢いモデル</b>（Codex は Astra、Claude は Opus）にMVPとログを見せ、あらゆる品質を上げるための研究をさせます。使う人・画面・データの形・権限と安全・運用・範囲の6つの観点で調べ、あなたにしか分からないことは質問してもらいます。研究によって、洗練された前提（コンテキスト）がファイルにできあがります。</p></li>
  <li><h3>計画する</h3><p>研究をもとに、ブラッシュアップ計画を作ります。スキーマ（データの形）、ロードマップ（作る順番）、キーの置き場所、画面の原則、AIへの指示。<b>安いモデルが、この計画だけを読んで作り直せる</b>ことが基準です。</p></li>
  <li><h3>ゼロから作り直す</h3><p><b>安いモデルに戻し</b>、計画だけを見てゼロから作り直します。今度はログイン・データベース・本番URLまで作ります。MVPのコードは使いません。</p></li>
</ol>

<h2>なぜ、この順番がいいのか</h2>
<table>
  <tr><th></th><th>先に完璧な計画を立てる</th><th>粗く作ってから研究・計画する</th></tr>
  <tr><td>最初の一歩</td><td>何を決めればいいか分からず止まる</td><td>15分で触れるものが出る</td></tr>
  <tr><td>要望の出方</td><td>頭の中で考えた要望だけ</td><td>触ったから出る、本当の要望</td></tr>
  <tr><td>計画の質</td><td>想像で書くので外れる</td><td>MVPと声を材料にするので当たる</td></tr>
  <tr><td>費用</td><td>高いモデルで何度もやり直す</td><td>高いモデルは研究と計画だけ</td></tr>
</table>

<h2>この流れを支える前提（ここを外すと崩れる）</h2>
<div class="note warn"><p>4段階はモデルを替えながら進むので、<b>会話の中身は次の段階に引き継がれません</b>。AIの記憶にも頼れません。引き継げるのはファイルだけです。だから次の4つを必ず守ります。</p></div>
<table>
  <tr><th>前提</th><th>なぜ</th><th>どうやるか</th></tr>
  <tr><td><b>ログに書きながら進める</b></td><td>要望や決定は会話に埋もれ、モデルを替えた瞬間に消える</td><td>出たその場で <code>docs/log.md</code> に1行。「ログして」と言えばAIが書く（<code>dev-log</code>）</td></tr>
  <tr><td><b>モデルを替える前に、ファイルへ書き出す</b></td><td>次のモデルが読めるのはファイルだけ</td><td>段階の変わり目で「ここまでをログに書いて」と頼んでから切り替える</td></tr>
  <tr><td><b>研究と計画は必ずファイルに残す</b></td><td>会話で終わると、作り直すモデルに伝わらない</td><td><code>docs/research.md</code> と計画の docs。答えは <code>README.md</code> / <code>CONTEXT.md</code> へ</td></tr>
  <tr><td><b>MVPは捨てる</b></td><td>粗いコードを流用すると、粗さまで引き継ぐ</td><td>作り直しでは <code>mvp/</code> を見た目の参考に見るだけ。コードは計画から新しく書く</td></tr>
</table>

<h2>開発ログの書き方</h2>
<p>形式は1行1件。種類は「要望・気づき・決定・詰まり・済」の5つです。</p>
<pre><code>- 2026-10-06 [要望] 担当者ごとの件数を一覧の上に出したい（営業部長から）
- 2026-10-06 [決定] 見積金額は万円単位で持つ（円単位が要る業務がないため）
- 2026-10-06 [詰まり] 並び順が保存されない → MVPなので研究で扱う</code></pre>
{prompt("担当者ごとの件数を一覧の上に出したい。営業部長からの要望。ログして。", "こう言うだけでAIがログに書く（例）")}

<h2>「書いてから作る」との関係</h2>
<p>README（何のためか）やスキーマを先に文章で固めることは、今でも大事です。変わったのは<b>タイミング</b>です。いきなり書くのではなく、MVPを触ったあとの研究で書きます。材料があるので、的外れな文章になりません。質問で詰める <code>grill-with-docs</code> も、研究の中で使います。</p>

{remember(["<b>粗く作る→研究→計画→ゼロから作り直す</b>。高いモデルは研究と計画だけ", "モデルを替えると会話は消える。<b>ログとファイルに書きながら進める</b>", "<b>MVPは捨てる</b>。作り直しは計画だけを見る"])}
""")

# ---------------------------------------------------------------- build
def step(n, title, analogy_text, skill, you, done, extra="", model=""):
    sk = call(skill) if skill else ""
    md = f'<dt>使うモデル</dt><dd>{model}</dd>' if model else ""
    return f"""<li id="step{n}">
    <h3>Step {n}. {title}</h3>
    <p class="flow">{analogy_text}</p>
    {sk}
    <dl class="meta-row">{md}<dt>あなたがやること</dt><dd>{you}</dd><dt>終わりの状態</dt><dd>{done}</dd></dl>
    {extra}
  </li>"""

CHEAP = "安くて速いモデル（Codex: Luna / Sol、Claude: Sonnet）"
SMART = "いちばん賢いモデル（Codex: Astra、Claude: Opus）"
SWITCH_PROMPT = "ここまでで出た要望・決定・詰まりを docs/log.md に書いて。次のモデルがファイルだけ読んで続きから始められるようにして。"

page("build", f"""
<h1>作る — 4段階・8ステップ</h1>
<p class="lede"><a href="flow.html">作り方の4段階</a>を、当日の手順にしたものです。Step 0（環境とAIの初期設定）は<a href="setup.html">2. 環境とAIの初期設定</a>で済んでいます。</p>

<div class="goal"><strong>このページを終えると</strong>、自社の画面が本番URLで開き、ログインして一覧が見えます。</div>

{mapblock('''
flowchart TB
  subgraph A["段階1 粗く作る（安いモデル）"]
    direction LR
    S1["1 困りごととログ"] --> S2["2 MVPを作って触る"]
  end
  subgraph B["段階2・3 研究と計画（賢いモデル）"]
    direction LR
    S3["3 研究する"] --> S4["4 計画する"]
  end
  subgraph C["段階4 ゼロから作り直す（安いモデル）"]
    direction LR
    S5["5 土台"] --> S6["6 ログインと一覧"] --> S7["7 本番"]
  end
  A --> B --> C --> S8["8 次の一手と振り返り"]
''')}

<div class="note warn"><p><b>ずっと守ること:</b> 要望・決定・詰まりは、出たその場で「ログして」と言う（<code>docs/log.md</code>）。<b>段階が変わってモデルを替える前には、下のプロンプトでここまでをログに書き出す。</b>会話は次のモデルに引き継がれず、渡るのはファイルだけです。</p></div>
{prompt(SWITCH_PROMPT, "段階が変わる前に毎回貼る")}

<h2>どのStepでも使う一言</h2>
{prompt("次は何をすればいい？ guide で現在地を判定して、次の一手を1つだけ教えて。使うモデルも教えて。コマンドはあなたが実行して。")}

<h2>段階1 粗く作る（安いモデル）</h2>
<ol class="steps">
{step(1, "困りごとを1文にして、ログを始める", "何を作るかを1文にし、これから出る声を全部ためる入れ物（開発ログ）を作ります。", "dev-log",
 "事前準備で書いた困りごとメモと帳票の項目名を貼る",
 "<code>docs/log.md</code> の最初に「〈誰〉が〈何〉に困っている。〈何〉が見えると嬉しい。」と帳票の項目名がある",
 prompt("""dev-log で、次の困りごとと帳票の項目名を docs/log.md の最初に書いて。
困りごと: （ここに貼る）
帳票の項目名: （ここに貼る）"""), CHEAP)}
{step(2, "MVPを作って触る", "段ボールの模型です。15〜30分で触れるものを作り、触って出た声をログにためます。雑でかまいません。あとで捨てます。", "dashboard-mvp",
 "ブラウザで開いて触り、「ここ使いにくい」「これも見たい」をそのまま言う（AIがログに書く）。2〜3回小さく直してもらう",
 "<code>mvp/index.html</code> を自分で操作でき、<code>docs/log.md</code> に要望・気づきが5つ以上ある",
 prompt("dashboard-mvp で、docs/log.md の困りごとから mvp/index.html に触れるMVPを作って、ブラウザで開いて。ダミーデータで、15〜30分で。") +
 fig("assets/images/build/02-prototype.png", "MVPの見本", '見本（架空の会社）: 段階1で作るMVPの例。<a href="samples/prototype.html">実物を開いて触る</a>'), CHEAP)}
</ol>

<h2>段階2・3 研究と計画（賢いモデル）</h2>
<div class="note"><p><b>ここでモデルを切り替えます。</b>先に上の「段階が変わる前に毎回貼る」プロンプトを送ってから、入力欄右下（Claudeは <code>/model</code>）でいちばん賢いモデルを選びます。</p></div>
<ol class="steps">
{step(3, "研究する", "段ボールの模型を一級建築士に見てもらいます。素人では気づけない弱い所と、良くする方法を洗い出し、ファイルに残します。", "dashboard-research",
 "AIの番号付きの質問に「1はA、2は推奨でOK」のように答える。あなたにしか分からないこと（業務のルール、誰が使うか）だけが聞かれる",
 "<code>docs/research.md</code> に6つの観点（使う人・画面と操作・データの形・権限と安全・運用・範囲）の結論があり、<code>README.md</code> に困りごとと使う人、<code>CONTEXT.md</code> に業務の言葉が3つ以上ある",
 prompt("""dashboard-research で、mvp/index.html と docs/log.md を研究して、docs/research.md に残して。
私にしか分からないことは、番号付きの質問にまとめて推奨回答つきで聞いて。""") +
 fig("assets/images/build/01a-grill-prompt.png", "質問で詰めるスキルを入力欄に入れた画面", "研究の中で、質問で詰めるスキル（grill-with-docs）も使われる。自分で呼ぶときは <code>/grill</code> と打って候補から選ぶ") +
 fig("assets/images/build/01-readme.png", "研究で書かれるREADMEとCONTEXT.mdの見本", '見本（架空の会社）: 研究で書かれるREADMEとCONTEXT.md。<a href="samples/readme.html">実物を開く</a>'), SMART)}
{step(4, "ブラッシュアップ計画を作る", "建築士の図面一式です。職人（安いモデル）は図面だけを見て作るので、必要なことは全部図面に書きます。", "dashboard-plan",
 "表とER図を見て「この情報はどこに入る？」と聞く。ロードマップの並び順が「先に見たいもの」からになっているか確かめる",
 "<code>docs/schema.md</code>（ER図つき）、<code>docs/roadmap.md</code>（<b>S1は「ログインして一覧が見える」</b>）、<code>docs/keys.md</code>、<code>docs/ui-guidelines.md</code>、<code>AGENTS.md</code> が埋まり、ログの要望が全部どれかのスライスに入っている",
 prompt("dashboard-plan で、docs/research.md と docs/log.md から、ゼロから作り直すための計画一式を作って。安いモデルが計画だけ読んで作り直せる粒度で。") +
 fig("assets/images/build/03-er.png", "スキーマとER図の見本", '見本: スキーマとER図。<a href="samples/schema.html">実物を開く</a>') +
 fig("assets/images/build/04-roadmap.png", "ロードマップの見本", '見本: ロードマップ（作る順番）。<a href="samples/roadmap.html">実物を開く</a>') +
 fig("assets/images/build/05-keys.png", "キー棚卸し表の見本", "見本: キーの置き場所（値は書かない）"), SMART)}
</ol>

<h2>段階4 ゼロから作り直す（安いモデル）</h2>
<div class="note"><p><b>ここでモデルを安いモデルに戻します。</b>先に「段階が変わる前に毎回貼る」プロンプトを送ってから切り替えます。MVPのコードは使わず、計画の docs だけを見て作ります。</p></div>
<ol class="steps">
{step(5, "土台を作る（DB・アプリ・リポジトリ）", "倉庫（Supabase）を借り、ログイン画面つきの店舗の箱（with-supabaseテンプレート）を建て、鍵を決まった場所にしまいます。", "dashboard-repo",
 """<ol>
<li><b>ブラウザで:</b> <a href="https://database.new">database.new</a> でSupabaseのプロジェクトを作る（Project name は <code>my-dashboard</code>、Region は <code>Asia-Pacific</code>、<code>Enable automatic RLS</code> にチェック。パスワードは <code>Generate a password</code> で作ってパスワード管理ツールへ）</li>
<li><b>AIに頼む:</b> 下のプロンプトを貼る。アプリの箱を作り、キットの中身（計画・ログ・スキル）をコピーし、<code>.env.local</code> を開いてくれる</li>
<li><b>ブラウザで:</b> Supabaseの画面上部の <code>Connect</code> を押し、Project URL と Publishable key を、開いた <code>.env.local</code> に貼って保存する（値はチャットに貼らない）</li>
<li><b>AIに頼む:</b> 「続けて」と送る。画面が開くか確かめ、GitHubにリポジトリを作ってくれる</li>
</ol>""",
 "<a href=\"http://localhost:3000\">localhost:3000</a> で画面が開き、GitHubにリポジトリがある。<code>.env.local</code> はGitHubに上がっていない",
 fig("assets/images/build/07-supabase-new-project.png", "Supabaseで新しいプロジェクトを作る画面", "Supabaseの「Create a new project」。組織名は伏せてある。入力したら下の「Create new project」を押す") +
 prompt("""dashboard-repo の手順2〜6を進めてください。Supabaseのプロジェクトは作りました。
コマンドはあなたが実行してください。.env.local を作ったら、そのファイルを開いて止まってください。
キーの値は私がファイルに直接貼ります（チャットには貼りません）。貼ったら「続けて」と言います。""") +
 fig("assets/images/build/06-template.png", "with-supabaseテンプレートの画面", "できあがるアプリの最初の画面（テンプレートの公式デモ）。ここからログイン画面につながっている") +
 '<div class="note"><p>ここから先は、新しくできた <code>my-dashboard</code> フォルダをCodex（またはClaude）で開き直して進めます。計画・ログ・スキルはコピー済みなので、そのまま <code>guide</code> に聞けます。</p></div>', CHEAP)}
{step(6, "ログインと一覧を作る（S1）", "社員証で開くドアを付け、ドアの内側に一覧を置きます。ドアそのものはテンプレートに付いています。", "dashboard-auth",
 """<ol>
<li><b>ブラウザで:</b> Supabase → <code>Authentication</code> → <code>Sign In / Providers</code> → <code>Allow new users to sign up</code> をオフ（知らない人が登録できないように）</li>
<li><b>ブラウザで:</b> <code>Authentication</code> → <code>Users</code> → <code>Add user</code> → <code>Create new user</code>。<code>Auto Confirm User</code> にチェックして自分のアカウントを作る</li>
<li><b>AIに頼む:</b> 下のプロンプトを貼る。計画のスキーマからSQLと一覧画面を作ってくれる</li>
<li><b>ブラウザで:</b> AIの説明を読んでから、SQLをSupabaseの <code>SQL Editor</code> に貼って <code>Run</code></li>
<li><b>AIに頼む:</b> 「確かめて、PRを作ってマージして」と送る</li>
</ol>""",
 "ログインしないと一覧が見えず、ログインするとダミーデータの一覧が見える。PRがマージされている",
 prompt("""dashboard-auth で最初のスライス（ログインして一覧が見える）を、docs/schema.md と docs/roadmap.md のとおりに作ってください。
Supabaseでのサインアップ停止とユーザー作成は済ませました。mvp/ のコードは使わないでください。
SQLは supabase/migrations/0001_init.sql に書き、何が作られるかを説明してから私に渡してください。""") +
 fig("assets/images/build/08-login.png", "ログイン画面", "テンプレートに付いているログイン画面（公式デモ）") +
 '<div class="note warn"><p><b>RLS（行ごとの鍵）は必ず付けます。</b>付けないと、公開キーを知っている人なら誰でもデータを読めてしまいます。<code>dashboard-auth</code> はRLS付きのSQLを書きます。</p></div>', CHEAP)}
{step(7, "本番へ出す", "お店のシャッターを開けます。倉庫の棚（データベース）を先に整え、それから店（アプリ）を開けます。", "dashboard-deploy",
 """<ol>
<li><b>ブラウザで:</b> <a href="https://vercel.com/new">vercel.com/new</a> → <code>my-dashboard</code> の <code>Import</code></li>
<li><b>ブラウザで:</b> <code>Environment Variables</code> に <code>.env.local</code> と同じ2つを入れて <code>Deploy</code></li>
<li><b>ブラウザで:</b> 出たURLを、Supabase → <code>Authentication</code> → <code>URL Configuration</code> の <code>Site URL</code> と <code>Redirect URLs</code> に入れる</li>
<li><b>AIに頼む:</b> 下のプロンプトで確認と記録をしてもらう</li>
</ol>""",
 "<b>本番URLを開き、ログインして一覧が動く。</b>URLが <code>docs/infra.md</code> に書かれている",
 fig("assets/images/build/11-vercel-import.png", "VercelでGitHubのリポジトリをImportする画面", "「Import Git Repository」の検索欄にリポジトリ名を入れ、「Import」を押す") +
 fig("assets/images/build/12-vercel-ready.png", "Vercelのデプロイ完了画面", "StatusがReadyになったら、Domainsの本番URLを開く（この講義サイト自身のデプロイ画面。ユーザー名は伏せてある）") +
 prompt("dashboard-deploy の手順で、本番URL（ここに貼る）でログインして一覧が動くか確かめる方法を教えて。動いたら docs/infra.md にURLを書いて、ログに［済］で残して。") +
 '<div class="note warn"><p>キーが写る画面は撮らないでください。撮る必要があるときは、値の部分を隠してから撮ります。</p></div>', CHEAP)}
</ol>

<h2>締め</h2>
<ol class="steps">
{step(8, "次の一手を決めて、振り返る", "明日の自分へのメモを残します。料理のあとにレシピへ書き込むのと同じです。", "reflect",
 "ガイドに、ログの要望と計画を照らして次のスライスを1つ選んでもらう。<code>reflect</code> が出した学びの案から残すものを選ぶ",
 "「明日はこれをやる」が1行で書かれ、学びが1つ以上ファイルに残っている",
 prompt("""今日の結果をまとめてください。
- できたこと（本番URLと、動いている操作）
- docs/log.md の要望のうち、満たせたもの・残ったもの
- 次にやるスライス（docs/roadmap.md に印を付ける）
そのあと reflect で、今日の学びを残す案を出してください。"""))}
</ol>

<h2>時間が押したとき</h2>
<table>
  <tr><th>優先</th><th>やること</th><th>理由</th></tr>
  <tr><td>1</td><td>本番URL（Step 7）</td><td>「できた」の実感が次につながる</td></tr>
  <tr><td>2</td><td>計画（Step 4）</td><td>明日、安いモデルだけで作り直しを進められる</td></tr>
  <tr><td>3</td><td>研究（Step 3）</td><td>計画の質を決める</td></tr>
  <tr><td>4</td><td>MVPの作り込み</td><td>捨てるので一番後回しでよい</td></tr>
</table>

{remember(["<b>粗く作る→研究→計画→ゼロから作り直す</b>。段階でモデルを替える", "<b>段階が変わる前に、ログへ書き出す</b>。次のモデルに渡るのはファイルだけ", "作り直しは<b>計画だけを見る</b>。MVPのコードは使わない"])}
""")

# ---------------------------------------------------------------- pstack
page("pstack", f"""
<h1>迷ったときの進め方 — pstack</h1>
<p class="lede"><b>結論:</b> 順序を暗記しないでください。「開発をガイドして」と頼めば、足りないものから次の一手が出ます。</p>

<div class="goal"><strong>このページを読むと</strong>、開発の進め方をAIに任せつつ、自分で判断すべきところが分かります。</div>

{mapblock('''
flowchart LR
  A["粗く作る<br/>試せば分かることは試す"] --> B["研究<br/>2〜3案・観点で調べる"]
  B --> C["計画<br/>データの形・順番"]
  C --> D["作り直す<br/>1スライスずつ"]
  D --> E["検証<br/>実物で確かめる"]
  E --> F["振り返り<br/>reflect"]
  F -. 次のスライス .-> D
''')}

{analogy("pstackは包丁1本ではなく、<b>調べる・比べる・焼く・味見する道具が揃った道具箱</b>です。中身を全部覚える必要はありません。「次は何？」と聞けば、今使う1本を渡してくれます。")}

<h2>pstack とは</h2>
<p>「速く行きたいなら、先に深く行く」という進め方の束です。作者はpoteto（Lauren Tan）で、MITライセンスで公開されています（<a href="repos.html">リポジトリ一覧</a>）。合宿では、その中から参加者に効くものだけを日本語のスキルにして入れています。</p>
<p>合宿の<a href="flow.html">作り方の4段階</a>は、pstackの考え方をそのまま使っています。<b>試せば分かることは、議論する前に小さく作って試す</b>（粗く作る）。<b>作ったものを材料に、構造を先に深く考える</b>（研究と計画）。<b>計画ができたら、小さく作って実物で確かめる</b>（作り直す）。</p>

<h2>いつ、何を使うか</h2>
<table>
  <tr><th>タイミング</th><th>使うスキル</th><th>一言</th></tr>
  <tr><td>着手直後</td><td><code>dashboard-mvp</code></td><td>議論より先に、安いモデルで触れるものを作る</td></tr>
  <tr><td>形を決める</td><td><code>dashboard-research</code> / <code>grill-with-docs</code></td><td>賢いモデルで観点ごとに研究し、答えはファイルに残す</td></tr>
  <tr><td>作り直す前</td><td><code>dashboard-plan</code></td><td>計画だけで作り直せる粒度まで書く</td></tr>
  <tr><td>いつでも</td><td><code>dev-log</code></td><td>要望・決定・詰まりをログに。モデルを替えても消えない</td></tr>
  <tr><td>実装中</td><td><code>dashboard-slice</code></td><td>1スライス＝1PR。動かして確かめてからマージ</td></tr>
  <tr><td>迷ったとき</td><td><code>poteto-mode</code></td><td>足りないものを1つ見つけて、次の一手を理由つきで</td></tr>
  <tr><td>原則を思い出したい</td><td><code>pstack-guide</code></td><td>場面から原則を引く</td></tr>
  <tr><td>一区切りついた</td><td><code>reflect</code></td><td>学びをdocsやスキルへ残す</td></tr>
</table>

<h2>poteto-mode — 開発のカーナビ</h2>
{prompt("poteto-mode で、いまの状態から足りないものを1つ見つけて、次の一手を理由つきで教えてください。")}
<p>次の形で答えが返ってきます。</p>
<pre><code>私の理解: 営業担当が、案件の進み具合を毎朝口頭で確認していて困っている。
現在地: 画面の試作はあるが、データの形が決まっていない。
次の一手: 画面の項目をテーブルに落とし、ER図にする（使うスキル: dashboard-schema）
なぜ今これか: データの形が決まらないと、実装しても作り直しになるため。
確認のしかた: 「この情報はどこに入る？」に全部答えられたら次へ。</code></pre>
<p>上から順に「最初に足りないもの」を見つけます。済んでいる工程はやり直しません。</p>
<table>
  <tr><th>足りないもの</th><th>次の一手</th></tr>
  <tr><td>誰が何に困っているかが言えない</td><td>困りごとを1文にし、READMEに書く</td></tr>
  <tr><td>使う場面が思い浮かばない</td><td>「誰が、いつ、何を押して、何が分かるか」を1つ書く</td></tr>
  <tr><td>画面の良し悪しが決められない</td><td>2〜3案を同じダミーデータで並べて比べる</td></tr>
  <tr><td>データの形が決まっていない</td><td>テーブルに落とし、ER図にする</td></tr>
  <tr><td>作業が大きすぎる</td><td>確認できる単位に切る</td></tr>
  <tr><td>動くものがない／確認していない</td><td>1スライス作って、実際に動かす</td></tr>
</table>

<h2>よく使う原則（場面で覚える）</h2>
<table>
  <tr><th>場面</th><th>原則</th><th>やること</th></tr>
  <tr><td>何か足したくなった</td><td>足す前に引く</td><td>先に要らないものを消す。消せないなら足さない</td></tr>
  <tr><td>設計で迷っている</td><td>2〜3案を並べる</td><td>比べてから決める。1案で決めない</td></tr>
  <tr><td>聞けば分かるか迷った</td><td>試せば分かることは試す</td><td>小さく作って動かし、結果で決める</td></tr>
  <tr><td>作る順番で迷う</td><td>検証できる単位で切る</td><td>1つ確認してから次へ</td></tr>
  <tr><td>完了と言いたくなった</td><td>実物で示す</td><td>ログではなく、画面を開いて操作した結果を見る</td></tr>
  <tr><td>エラーが出た</td><td>根本原因を直す</td><td>再現 → なぜ → 根本を直す</td></tr>
  <tr><td>同じ指示を繰り返している</td><td>仕組みにする</td><td>文章で足さず、docs・スキル・テストにする</td></tr>
</table>

<h2>reflect — 振り返りをレシピに書き込む</h2>
{prompt("reflect で、この会話でうまくいったことと遠回りしたことから、残す学びの案を3つまで出してください。")}
<p>作業が一区切りしたときに、今回うまくいった進め方を、次に使い回せる形にします。AIが「どのファイルに、何を書き足すか」の案を出すので、残すものを選びます。</p>
<table>
  <tr><th>使うタイミング</th><th>何が得られるか</th></tr>
  <tr><td>1スライスをマージした、本番に出せた</td><td>次に同じことをする時間が短くなる</td></tr>
  <tr><td>遠回りしたあと、正しい道が見つかった</td><td>同じ遠回りをしなくなる</td></tr>
  <tr><td>AIに同じ注意を2回した</td><td>次からAIが最初から守る</td></tr>
</table>
<div class="note"><p><b>反映は自分で選びます。</b>提案されたものを全部入れる必要はありません。書くほどAIが読む量が増えるので、効くものだけ残します。</p></div>

<h2>合宿では使わないもの（興味があれば）</h2>
<p>pstack本体には、複数案を並列で競わせる <code>arena</code> / <code>swarm</code>、詳細設計の <code>architect</code>、別のAIによる二重レビューなど、さらに強力な道具があります。仕組みが分かってきたら、<a href="repos.html">リポジトリ一覧</a>の本体を覗いてみてください。</p>

{remember(["<b>試せば分かることは試す</b>。粗く作る→研究→計画→作り直す", "迷ったら <b><code>poteto-mode</code></b>。足りないものから次の一手が出る", "一区切りしたら <b><code>reflect</code></b> で学びを残す"])}
""")

# ---------------------------------------------------------------- day2
page("day2", f"""
<h1>翌日以降の進め方</h1>
<p class="lede">ここからの主役はあなたです。AIは手を動かしますが、決めるのはあなたです。</p>

<div class="goal"><strong>このページを読むと</strong>、毎日の回し方と、誰に何を頼めばいいかが分かります。</div>

{mapblock('''
flowchart LR
  A["朝<br/>ログとロードマップから1スライス"] --> C["安いモデルで実装→動かす"]
  C --> D["PR→マージ→本番"]
  D --> E["夕方<br/>reflectで振り返る"]
  E -. 翌朝 .-> A
  D -. 要望がたまったら .-> R["賢いモデルで研究・計画し直す"]
  R -.-> A
''')}

{analogy("<b>毎日1皿ずつ増えていく定食屋のメニュー</b>です。1日1皿を確実に出し、出した皿のレシピを書き残す。これを続けると、メニュー（機能）が自然に揃います。")}

<h2>毎日の始め方</h2>
<ol class="steps">
  <li><h3>今日やるスライスを1つ選ぶ</h3>{prompt("docs/roadmap.md の未完了から、今日やるスライスを1つだけ選んで。理由も1行で。")}</li>
  <li><h3>作る（安いモデル）</h3>{prompt("dashboard-slice で、そのスライスを実装して。動かして確かめてから、PRを作ってマージして。DBの変更があれば dashboard-deploy の順で本番に出して。出た要望はログに書いて。")}</li>
  <li><h3>要望がたまったら、研究し直す（賢いモデル）</h3><p>ログに要望が10件ほどたまったら、または大きな変更の前に、賢いモデルで研究と計画をやり直します。4段階は1回きりではなく、何度でも回せます。</p>{prompt("dashboard-research で、今のアプリと docs/log.md のたまった要望を研究して、docs/research.md を更新して。そのあと dashboard-plan で docs/roadmap.md に次のスライスを足して。")}</li>
  <li><h3>一日の終わりに振り返る</h3>{prompt("今日の結果をまとめて、明日の1スライスを決めて。そのあと reflect で学びを残す案を出して。")}</li>
</ol>

<h2>自分で進める部分と、頼る部分</h2>
<table>
  <tr><th></th><th>自分でやる</th><th>外に頼む</th></tr>
  <tr><td>決めること</td><td>何を作るか、優先順位、業務のルール</td><td>—</td></tr>
  <tr><td>作ること</td><td>指示、確認、採用の判断</td><td>実装はAIが担当</td></tr>
  <tr><td>詰まったとき</td><td>詰まった場所の記録</td><td>設計・移行・公開の判断</td></tr>
</table>

<h2>自分たちの限界の見つけ方</h2>
<p>次に当てはまったら、それが限界のサインです。早めに共有した方が得です。</p>
<table>
  <tr><th>サイン</th><th>起きていること</th></tr>
  <tr><td>考慮点が多すぎて決められない</td><td>業務の例外を全部同時に解こうとしている</td></tr>
  <tr><td>いまのデータを移せない</td><td>データの持ち主・形式・重複が整理できていない</td></tr>
  <tr><td>公開や権限で止まる</td><td>誰が見てよいかの決めが要る</td></tr>
  <tr><td>自分たちしか触れない</td><td>引き継ぎの設計が要る</td></tr>
</table>

<h2>人に聞くときの型</h2>
{prompt('''【何をしたいか】案件の進捗を、全員が見えるようにしたい
【いまどこまで】一覧画面は本番で動いている。編集がまだ
【どこで止まったか】誰が編集できるかの決め方で止まっている
【自分で試したこと】担当者全員に編集権限を付ける案を試したが、間違って消されるのが怖い
【決めたいこと】編集と閲覧の分け方''', "人やAIに聞くときの型（中身を書き換えて使う）")}
<p>この5行があれば、答えはすぐ返ってきます。<b>詰まった場所が具体的なほど、助けが正確になります。</b></p>

<h2>続けるコツ</h2>
<table>
  <tr><th>やること</th><th>なぜ</th></tr>
  <tr><td>1スライス＝1PRを守る</td><td>小さく出すほど、詰まっても戻れる</td></tr>
  <tr><td>週に1回、docsを更新する</td><td>AIへの説明が減り続ける</td></tr>
  <tr><td>一区切りごとに <code>reflect</code></td><td>うまくいった進め方が自分の環境に残る</td></tr>
  <tr><td>決めた理由を書き残す（ADR）</td><td>半年後の自分とAIが同じ判断をやり直さずに済む</td></tr>
  <tr><td>社内への説明は <code>eli5</code></td><td>前提知識のない人にも、変わったことが伝わる</td></tr>
</table>

{remember(["<b>1日1スライス</b>。複数選ばない", "終わったら <b>PR→マージ→本番→reflect</b>", "人に聞くときは<b>5行の型</b>で"])}
""")

print("generated", len(ORDER), "pages")
