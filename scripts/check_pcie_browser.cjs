#!/usr/bin/env node
/* Run against a saved Jekyll build. No requests leave the local test server.
   node scripts/check_pcie_browser.cjs --root BUILD --output QA [--chapters 7,8,9]
   Optional PCIE_PLAYWRIGHT_PATH and PCIE_BROWSER select a local runtime. */
const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require(process.env.PCIE_PLAYWRIGHT_PATH || 'playwright');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => {
  if (v.startsWith('--')) a.push([v.slice(2), all[i + 1]]);
  return a;
}, []));
if (!args.root || !args.output) throw new Error('--root and --output are required');
const root = path.resolve(args.root), output = path.resolve(args.output);
fs.mkdirSync(output, { recursive: true });
const chapters = args.chapters ? args.chapters.split(',').map(Number) : [7, 8, 9];
const completed = fs.readdirSync(path.join(root,'DOCS','pcie-course')).map(name => /^chapter-(\d+)\.html$/.exec(name)).filter(Boolean).map(match => Number(match[1]));
if (chapters.some(n => !Number.isInteger(n) || !completed.includes(n))) throw new Error('Expected completed chapter numbers from the supplied build');
const server = http.createServer((req, res) => {
  let requested = decodeURIComponent(req.url.split('?')[0]);
  let file = path.resolve(root, '.' + requested);
  if (file !== root && !file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  if (requested.endsWith('/')) file = path.join(file, 'index.html');
  fs.readFile(file, (error, data) => {
    if (error) { res.writeHead(404).end(); return; }
    const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml' };
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    res.end(data);
  });
});

(async () => {
  let browser;
  const results = [];
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const origin = 'http://127.0.0.1:' + server.address().port;
    browser = await chromium.launch({ headless: true, ...(process.env.PCIE_BROWSER ? { executablePath: process.env.PCIE_BROWSER } : {}) });
    for (const chapter of chapters) {
      const cases = [];
      for (const [device, width, height] of [['desktop',1440,1000],['tablet',834,1194],['landscape',1194,834],['phone',390,844]])
        for (const theme of ['light','dark']) cases.push({ chapter, device, width, height, theme, edition: 'tutorial', url: `/DOCS/pcie-course/chapter-${chapter}.html` });
      for (const [edition, device, width, height] of [['zh-tw','desktop',1440,1000],['zh-tw','tablet',834,1194],['en','desktop',1440,1000],['en','phone',390,844]])
        for (const theme of ['light','dark']) cases.push({ chapter, device, width, height, theme, edition, url: `/pcie/chapter-${chapter}-${edition}/` });
      for (const c of cases) {
        const page = await browser.newPage({ viewport: { width: c.width, height: c.height }, colorScheme: c.theme, reducedMotion: 'reduce', javaScriptEnabled: c.edition !== 'tutorial' });
        await page.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
        const result = { case: c, failures: [] };
        const response = await page.goto(origin + c.url, { waitUntil: 'domcontentloaded' });
        if (response.status() !== 200) result.failures.push('HTTP ' + response.status());
        if (c.edition !== 'tutorial') await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), c.theme);
        const scope = c.edition === 'tutorial' ? '.lesson' : '.pcie-article';
        const base = await page.locator(scope).evaluate(el => ({
          overflow: document.documentElement.scrollWidth - innerWidth,
          diagrams: el.querySelectorAll('svg').length,
          blackSvgText: [...el.querySelectorAll('svg text')].filter(t => getComputedStyle(t).fill === 'rgb(0, 0, 0)').map(t => t.textContent),
          clippedText: [...el.querySelectorAll('svg text')].filter(t => {
            const b = t.getBBox(), v = t.ownerSVGElement.viewBox.baseVal;
            return b.x < -1 || b.y < -1 || b.x + b.width > v.width + 1 || b.y + b.height > v.height + 1;
          }).map(t => t.textContent),
          shortControls: [...el.querySelectorAll('a,summary,.walk-label')].filter(t => !t.closest('svg') && t.getBoundingClientRect().height > 0 && t.getBoundingClientRect().height < 43.9).map(t => t.textContent.trim().slice(0,80)),
        }));
        if (base.overflow > 1) result.failures.push('Page overflow: ' + base.overflow);
        if (!base.diagrams) result.failures.push('No core diagram');
        if (base.clippedText.length) result.failures.push({ clippedText: base.clippedText });
        if (c.theme === 'dark' && base.blackSvgText.length) result.failures.push({ darkText: base.blackSvgText });
        if (base.shortControls.length) result.failures.push({ shortControls: base.shortControls });
        const walks = page.locator(scope + ' .guided-walk');
        result.walks = await walks.count();
        if (c.edition === 'tutorial' && !result.walks) result.failures.push('Revised tutorial has no guided diagram');
        for (let w = 0; w < result.walks; w++) {
          const walk = walks.nth(w);
          const radios = walk.locator('input.walk-choice');
          for (let step = 0; step < await radios.count(); step++) {
            const radio = radios.nth(step), id = await radio.getAttribute('id');
            await walk.locator(`label[for="${id}"]`).click();
            if (!await radio.isChecked()) result.failures.push(`Walk ${w} step ${step + 1} did not select`);
            const visibility = await walk.evaluate(el => [...el.querySelectorAll('.walk-step,.walk-node')].every(n => {
              const style = getComputedStyle(n);
              return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity) > 0.5;
            }));
            if (!visibility) result.failures.push(`Walk ${w} hides content at step ${step + 1}`);
            const highlights = await walk.evaluate((el, number) => {
              const active = el.querySelector(`.walk-step[data-walk-step="${number}"]`);
              const other = [...el.querySelectorAll('.walk-step')].find(e => e !== active);
              const targets = [...el.querySelectorAll(`.walk-node[data-walk-steps~="${number}"]`)];
              return (!other || getComputedStyle(active).borderTopColor !== getComputedStyle(other).borderTopColor)
                && targets.length > 0 && targets.every(e => getComputedStyle(e).getPropertyValue('--walk-active-weight').trim() === '750');
            }, String(step + 1));
            if (!highlights) result.failures.push(`Walk ${w}: CSS highlight missing at step ${step + 1}`);
          }
          await radios.first().focus();
          if (await radios.count() > 1) {
            await page.keyboard.press('ArrowRight');
            if (!await radios.nth(1).isChecked()) result.failures.push(`Walk ${w}: keyboard step selection failed`);
          }
          const component = walk.locator('.walk-component-links a').first();
          if (await component.count()) {
            const href = await component.getAttribute('href');
            await component.click();
            if (!(await page.locator(href).count())) result.failures.push('Component target missing');
            const details = page.locator(href).locator('details');
            await details.locator('summary').click();
            if (!await details.evaluate(e => e.open)) result.failures.push('Component background did not open');
          }
        }
        const source = page.locator(scope + ' details.source-note').first();
        if (await source.count()) {
          await source.locator('summary').click();
          if (!await source.evaluate(e => e.open)) result.failures.push('Source did not open');
        }
        if (([0,7,8,9,13].includes(chapter) && ['desktop','phone'].includes(c.device)) || result.failures.length) {
          const diagram = page.locator(scope + ' .diagram').first();
          if (await diagram.count()) await diagram.scrollIntoViewIfNeeded();
          await page.screenshot({ path: path.join(output, `ch${chapter}-${c.edition}-${c.device}-${c.theme}.png`), animations: 'disabled' });
        }
        if (c.edition === 'tutorial' && c.device === 'desktop' && c.theme === 'light') {
          await page.emulateMedia({ media: 'print' });
          const hidden = await page.locator(scope).evaluate(el => [...el.querySelectorAll('.walk-step')].some(n => getComputedStyle(n).display === 'none'));
          if (hidden) result.failures.push('Print hides explanation');
        }
        results.push(result);
        await page.close();
      }
      console.log(`Chapter ${chapter}: ${results.filter(r => r.case.chapter === chapter && r.failures.length).length} failed cases / ${cases.length}`);
    }
  } finally {
    fs.writeFileSync(path.join(output, 'browser-results.json'), JSON.stringify(results, null, 2));
    if (browser) await browser.close();
    server.close();
  }
  const failures = results.filter(r => r.failures.length);
  console.log(JSON.stringify({ cases: results.length, failures }, null, 2));
  if (failures.length) process.exitCode = 1;
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });
