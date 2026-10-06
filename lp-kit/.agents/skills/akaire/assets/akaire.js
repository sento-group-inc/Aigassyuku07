/* akaire.js — HTML成果物に赤入れ（マーカー&メモ）UIを注入するスニペット。
 * 外部依存ゼロ・自己完結。レビュー時のみ<body>末尾に<script>として埋め込み、納品時は除去する。
 * 使い方: 右下「赤入れ」ボタンON→ドラッグで囲む→メモ入力→「コピー」でMarkdown化した指摘一覧をクリップボードへ。
 */
(function () {
  'use strict';
  var KEY = 'akaire:' + location.pathname;
  var marks = [];
  try { marks = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { marks = []; }
  var active = false, startX = 0, startY = 0, dragBox = null;

  var css = document.createElement('style');
  css.textContent =
    '.akaire-mark{position:absolute;border:2px solid #d33;background:rgba(221,51,51,.08);z-index:99990;pointer-events:auto;cursor:pointer;}' +
    '.akaire-mark .akaire-tag{position:absolute;top:-12px;left:-12px;width:22px;height:22px;border-radius:50%;background:#d33;color:#fff;font:bold 13px/22px sans-serif;text-align:center;}' +
    '#akaire-bar{position:fixed;right:16px;bottom:16px;z-index:99999;font:13px/1.4 sans-serif;display:flex;gap:8px;align-items:center;}' +
    '#akaire-bar button{padding:8px 14px;border:1px solid #d33;border-radius:4px;background:#fff;color:#d33;cursor:pointer;font-weight:bold;}' +
    '#akaire-bar button.on{background:#d33;color:#fff;}' +
    '#akaire-panel{position:fixed;right:16px;bottom:64px;z-index:99998;width:300px;max-height:50vh;overflow:auto;background:#fff;border:1px solid #ccc;border-radius:4px;padding:10px;font:12px/1.5 sans-serif;box-shadow:0 4px 16px rgba(0,0,0,.15);display:none;}' +
    '#akaire-panel .akaire-item{border-bottom:1px solid #eee;padding:6px 0;display:flex;gap:6px;}' +
    '#akaire-panel .akaire-item b{color:#d33;}' +
    '#akaire-panel .akaire-del{margin-left:auto;cursor:pointer;color:#999;border:none;background:none;}' +
    'body.akaire-active{cursor:crosshair;}';
  document.head.appendChild(css);

  var bar = document.createElement('div');
  bar.id = 'akaire-bar';
  bar.innerHTML = '<button id="akaire-toggle">赤入れ</button><button id="akaire-copy">コピー</button>';
  document.body.appendChild(bar);
  var panel = document.createElement('div');
  panel.id = 'akaire-panel';
  document.body.appendChild(panel);

  function nearestText(x, y) {
    var el = document.elementFromPoint(
      Math.min(x - window.scrollX, window.innerWidth - 1),
      Math.min(y - window.scrollY, window.innerHeight - 1)
    );
    if (!el || el.closest('#akaire-bar,#akaire-panel,.akaire-mark')) return '';
    return (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  }
  function save() { localStorage.setItem(KEY, JSON.stringify(marks)); }
  function render() {
    document.querySelectorAll('.akaire-mark').forEach(function (n) { n.remove(); });
    panel.innerHTML = '';
    marks.forEach(function (m, i) {
      var d = document.createElement('div');
      d.className = 'akaire-mark';
      d.style.cssText = 'left:' + m.x + 'px;top:' + m.y + 'px;width:' + m.w + 'px;height:' + m.h + 'px;';
      d.innerHTML = '<span class="akaire-tag">' + (i + 1) + '</span>';
      d.title = m.note;
      document.body.appendChild(d);
      var row = document.createElement('div');
      row.className = 'akaire-item';
      row.innerHTML = '<b>' + (i + 1) + '</b><span></span><button class="akaire-del">×</button>';
      row.querySelector('span').textContent = m.note;
      row.querySelector('.akaire-del').onclick = function () { marks.splice(i, 1); save(); render(); };
      panel.appendChild(row);
    });
    panel.style.display = marks.length ? 'block' : 'none';
  }
  document.getElementById('akaire-toggle').onclick = function () {
    active = !active;
    this.classList.toggle('on', active);
    document.body.classList.toggle('akaire-active', active);
  };
  document.getElementById('akaire-copy').onclick = function () {
    var md = marks.map(function (m, i) {
      return (i + 1) + '. 「' + (m.near || '(該当テキストなし)') + '」付近' +
        '（位置 x:' + Math.round(m.x) + ' y:' + Math.round(m.y) + ' w:' + Math.round(m.w) + ' h:' + Math.round(m.h) + '） — ' + m.note;
    }).join('\n');
    md = '## 赤入れ指摘 ' + location.pathname + '（' + marks.length + '件）\n' + md;
    navigator.clipboard.writeText(md).then(function () {
      var b = document.getElementById('akaire-copy'); b.textContent = 'コピー済';
      setTimeout(function () { b.textContent = 'コピー'; }, 1200);
    });
  };
  document.addEventListener('mousedown', function (e) {
    if (!active || e.target.closest('#akaire-bar,#akaire-panel')) return;
    startX = e.pageX; startY = e.pageY;
    dragBox = document.createElement('div');
    dragBox.className = 'akaire-mark';
    document.body.appendChild(dragBox);
    e.preventDefault();
  });
  document.addEventListener('mousemove', function (e) {
    if (!dragBox) return;
    var x = Math.min(startX, e.pageX), y = Math.min(startY, e.pageY);
    dragBox.style.cssText = 'left:' + x + 'px;top:' + y + 'px;width:' + Math.abs(e.pageX - startX) + 'px;height:' + Math.abs(e.pageY - startY) + 'px;';
  });
  document.addEventListener('mouseup', function (e) {
    if (!dragBox) return;
    var w = Math.abs(e.pageX - startX), h = Math.abs(e.pageY - startY);
    dragBox.remove(); dragBox = null;
    if (w < 8 || h < 8) return;
    var note = prompt('この箇所への指摘・メモ:');
    if (!note) return;
    marks.push({ x: Math.min(startX, e.pageX), y: Math.min(startY, e.pageY), w: w, h: h, note: note, near: nearestText(startX + w / 2, startY + h / 2) });
    save(); render();
  });
  render();
})();
