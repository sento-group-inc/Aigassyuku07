// 使い方: node scripts/check-lp.js <LPのパスかURL> [撮影先=./lp-check]
// 初回だけ: npm i --prefix "$TMPDIR/lp-check" playwright-core && npx --prefix "$TMPDIR/lp-check" playwright-core install chromium
// 実行:     NODE_PATH="$TMPDIR/lp-check/node_modules" node scripts/check-lp.js workspaces/<商品名>/site/index.html
// PC(1440px)とスマホ(375px)で最後までスクロールして撮影し、採点の前に機械で分かる不備を出す。
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path');
const [src, outDir = 'lp-check'] = process.argv.slice(2);
if (!src) { console.error('usage: node check-lp.js <lp.html|url> [outDir]'); process.exit(2); }
const url = /^https?:/.test(src) ? src : 'file://' + path.resolve(src);
fs.mkdirSync(outDir, { recursive: true });

async function scrollThrough(p) {
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h; y += 400) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(120); }
  await p.waitForTimeout(800);
}

async function inspect(b, name, viewport, reducedMotion = 'no-preference') {
  const ctx = await b.newContext({ viewport, reducedMotion });
  const p = await ctx.newPage();
  const errors = [];
  p.on('pageerror', e => errors.push(e.message));
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  p.on('requestfailed', r => errors.push('failed: ' + r.url()));
  await p.addInitScript(() => {
    window.__lcp = 0; window.__cls = 0;
    new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
  });
  await p.goto(url, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1200);
  if (reducedMotion === 'no-preference') await p.screenshot({ path: path.join(outDir, `${name}_firstview.png`) });
  await scrollThrough(p);
  const r = await p.evaluate(() => {
    const visible = e => { const s = getComputedStyle(e), b = e.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && b.width > 0 && b.height > 0; };
    const texts = [...document.querySelectorAll('body *')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && visible(e));
    const tiny = texts.filter(e => parseFloat(getComputedStyle(e).fontSize) < 12).map(e => e.textContent.trim().slice(0, 30));
    const hiddenText = texts.filter(e => parseFloat(getComputedStyle(e).opacity) === 0).map(e => e.textContent.trim().slice(0, 30));
    const imgs = [...document.images];
    return {
      hscroll: document.documentElement.scrollWidth > innerWidth + 1,
      h1: document.querySelectorAll('h1').length,
      tinyText: tiny.slice(0, 10), tinyCount: tiny.length,
      hiddenAfterScroll: hiddenText.slice(0, 10), hiddenCount: hiddenText.length,
      imgNoAlt: imgs.filter(i => !i.hasAttribute('alt')).length,
      imgBroken: imgs.filter(i => i.complete && i.naturalWidth === 0).length,
      lcpMs: Math.round(window.__lcp), cls: +window.__cls.toFixed(3),
    };
  });
  await p.evaluate(() => scrollTo(0, 0));
  await p.keyboard.press('Tab');
  r.focusVisible = await p.evaluate(() => {
    const e = document.activeElement; if (!e || e === document.body) return false;
    const s = getComputedStyle(e);
    return (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || s.boxShadow !== 'none';
  });
  if (reducedMotion === 'no-preference') await p.screenshot({ path: path.join(outDir, `${name}_full.png`), fullPage: true });
  await ctx.close();
  return { ...r, errors };
}

(async () => {
  const b = await chromium.launch();
  const pc = await inspect(b, 'pc', { width: 1440, height: 900 });
  const mobile = await inspect(b, 'mobile', { width: 375, height: 812 });
  const reduced = await inspect(b, 'reduced', { width: 1440, height: 900 }, 'reduce');
  await b.close();
  const problems = [];
  for (const [n, r] of [['pc', pc], ['mobile', mobile]]) {
    if (r.hscroll) problems.push(`${n}: 横スクロールが出る`);
    if (r.h1 !== 1) problems.push(`${n}: h1 が ${r.h1} 個（1個にする）`);
    if (r.tinyCount) problems.push(`${n}: 12px未満の文字が ${r.tinyCount} か所`);
    if (r.hiddenCount) problems.push(`${n}: 最後までスクロールしても見えない文字が ${r.hiddenCount} か所`);
    if (r.imgNoAlt) problems.push(`${n}: alt の無い画像が ${r.imgNoAlt} 枚`);
    if (r.imgBroken) problems.push(`${n}: 読み込めない画像が ${r.imgBroken} 枚`);
    if (r.errors.length) problems.push(`${n}: エラー ${r.errors.length} 件`);
    if (r.cls >= 0.1) problems.push(`${n}: レイアウトのずれ CLS ${r.cls}（0.1未満にする）`);
    if (r.lcpMs > 2500) problems.push(`${n}: 主要な表示まで ${r.lcpMs}ms（2500ms以内にする）`);
    if (!r.focusVisible) problems.push(`${n}: Tab で最初に移った要素にフォーカスの表示が無い`);
  }
  if (reduced.hiddenCount) problems.push(`動きを減らす設定で見えない文字が ${reduced.hiddenCount} か所`);
  const ok = problems.length === 0;
  console.log(JSON.stringify({ ok, problems, pc, mobile, reducedMotion: { hiddenCount: reduced.hiddenCount }, screenshots: path.resolve(outDir) }, null, 1));
  process.exit(ok ? 0 : 1);
})();
