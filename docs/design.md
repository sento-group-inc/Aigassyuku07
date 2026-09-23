# 講義サイト設計

## 読者の順番

参加者は当日、この順で読む。迷ったら`index.html`の「最初に見る順番」に戻る。

```
index → prep → schedule → why → setup → readme-driven → build（10ステップ） → pstack → skills → repos → day2
```

## ページ一覧

| ファイル | 役割 | 主な内容 |
|---|---|---|
| `index.html` | 入口 | 全体図、読む順番、この日にやること、持ち帰るもの |
| `prep.html` | 事前準備 | 困りごとメモ（宿題）、道具、Codex、clone、アカウント、最終チェック |
| `schedule.html` | 日程 | 2日間の全体図、時間割、チェックポイント、発表フォーマット |
| `why.html` | 腹落ち | なぜ会社のシステムを自分で作るのか（本文は本人との対話まで据え置き） |
| `setup.html` | 環境 | 当日の朝。setup.sh → キットを開く → 最初の一言。スキルの呼び方 |
| `readme-driven.html` | 進め方 | 書いてから作る。grill-with-docs で README / CONTEXT.md / ADR に残す |
| `build.html` | 実践 | 10ステップ。各Stepにたとえ・使うスキル・あなたがやること・終わりの状態 |
| `pstack.html` | 開発の型 | 道具箱の全体図、いつ何を使うか、poteto-mode、原則、reflect |
| `skills.html` | 道具 | キットのスキル16本（`scripts/check-skills.sh`と一致） |
| `repos.html` | 一覧 | 当日使うリポジトリ・サービスと、スキルの出典 |
| `day2.html` | 自走 | 2日目以降の進め方と、詰まったときの聞き方 |

## 共通の作り

- 1ページ1テーマ。冒頭に「このページの地図」（Mermaid、10ノード以内）と、たとえ1つ。末尾に「覚えること（3つ）」。eli5の型。
- 手順は番号付きで、**どこを押すか**の画像を添える（`docs/screenshots.md`）。
- コマンドはコピーしてそのまま貼れる形で載せる。置き換えが要る箇所は明示する。
- Codexの画面を基本にし、Claudeは「Claudeの場合はここが違う」の注記ブロックで扱う。
- 図はMermaid（jsDelivr CDN）で描く。画像はローカル参照のみ。

## 当日の時間割

正本は `site/schedule.html`。
