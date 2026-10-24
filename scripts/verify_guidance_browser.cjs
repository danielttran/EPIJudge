// Real built application, isolated practice profile; no mocked APIs or grading.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('../epijudge.client/node_modules/playwright-core');
const catalog = require('../epijudge.client/src/problemGuidance.json');
const base = process.argv[2];
if (!base) throw new Error('Pass the isolated server URL.');
const output = path.resolve(__dirname, '../.epi-runs/guidance-audit');
fs.mkdirSync(output, { recursive: true });
const report = { passed: false, checks: 0, renderedProblems: 0, scenes: [], errors: [] };
function check(value, label) { assert(value, label); report.checks++; }
(async () => {
  const browser = await chromium.launch({
    ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : { channel: 'chromium' }),
    headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();
    page.on('pageerror', error => report.errors.push(error.message));
    await page.goto(base + '/practice?problem=count_bits');
    await page.locator('#hints-count_bits').waitFor({ state: 'attached' });
    const response = await context.request.get(base + '/api/problems');
    check(response.ok(), 'live problem catalog');
    const problems = await response.json();
    check(JSON.stringify(problems.map(p => p.id).sort()) === JSON.stringify(Object.keys(catalog).sort()), 'exact live-bank guidance coverage');
    const go = async id => {
      await page.evaluate(id => {
        history.pushState(null, '', '/practice?problem=' + encodeURIComponent(id));
        dispatchEvent(new PopStateEvent('popstate'));
      }, id);
      await page.getByRole('tab', { name: 'Problem', exact: true }).click();
      await page.locator('[id="hints-' + id + '"]').waitFor({ state: 'attached' });
    };
    for (const problem of problems) {
      await go(problem.id);
      const entry = catalog[problem.id];
      const hints = page.getByRole('region', { name: 'Problem hints', exact: true });
      check(await hints.locator('details').count() === 0, problem.id + ' initially hidden');
      check(await hints.evaluate(el => el.parentElement.lastElementChild === el), problem.id + ' at statement bottom');
      check(JSON.stringify(await page.locator('.pattern-tag').allTextContents()) === JSON.stringify(entry.tags), problem.id + ' tags');
      await hints.getByRole('button', { name: 'Reveal first hint' }).click();
      check(await hints.locator('details').count() === 1, problem.id + ' only first revealed');
      check(await hints.locator('summary').first().evaluate(el => el === document.activeElement), problem.id + ' first hint receives focus');
      await hints.getByRole('button', { name: 'Reveal next hint' }).click();
      check(JSON.stringify(await hints.locator('details p').allTextContents()) === JSON.stringify(entry.hints), problem.id + ' exact hints');
      check(await hints.locator('summary').nth(1).evaluate(el => el === document.activeElement), problem.id + ' second hint receives focus');
      report.renderedProblems++;
    }
    const representatives = ['count_bits', 'two_sum', 'blind75_two_sum', 'interviewcake_stock-price', 'ctci6_15_4', 'ctci6_10_6'];
    for (const theme of ['dark', 'light']) {
      const toggle = page.getByRole('button', { name: 'Dark mode' });
      if ((await toggle.getAttribute('aria-pressed') === 'true') !== (theme === 'dark')) await toggle.click();
      for (const width of [320, 768, 1440]) {
        await page.setViewportSize({ width, height: 1000 });
        for (const id of representatives) {
          await go(id);
          const hints = page.getByRole('region', { name: 'Problem hints', exact: true });
          // Returning to the same problem without navigation need not reset hints.
          if (await hints.getByRole('button', { name: 'Hide hints' }).count()) await hints.getByRole('button', { name: 'Hide hints' }).click();
          await hints.getByRole('button', { name: 'Reveal first hint' }).click();
          await hints.getByRole('button', { name: 'Reveal next hint' }).click();
          await hints.scrollIntoViewIfNeeded();
          check(await hints.evaluate(el => el.scrollWidth <= el.clientWidth + 1), `${theme}/${width}/${id} hint wrapping`);
          check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${theme}/${width}/${id} no page overflow`);
          await hints.locator('summary').first().focus();
          await page.keyboard.press('Enter');
          check(await hints.locator('details').first().getAttribute('open') === null, 'keyboard collapse');
          await page.keyboard.press('Enter');
          check(await hints.locator('details').first().getAttribute('open') !== null, 'keyboard expand');
          report.scenes.push({ theme, width, id });
          if (id === 'ctci6_15_4') await page.screenshot({ path: path.join(output, `${theme}-${width}-hints.png`) });
          await page.getByRole('tab', { name: 'Solution', exact: true }).click();
          check(await page.getByRole('region', { name: 'Problem hints' }).count() === 0, 'hints not in solution view');
        }
      }
    }
    await page.setViewportSize({ width: 1440, height: 1000 });
    await go('count_bits');
    const editor = page.locator('.coding-pane .monaco-editor textarea.inputarea');
    await editor.focus();
    await page.keyboard.press('Control+A');
    await page.keyboard.insertText('// retained practice draft');
    const draft = await page.locator('.coding-pane .view-lines').innerText();
    await page.getByRole('button', { name: 'Reveal first hint' }).click();
    for (const language of ['csharp', 'javascript', 'python', 'cpp', 'java']) {
      await page.getByRole('tab', { name: 'Solution', exact: true }).click();
      await page.getByLabel('Solution language', { exact: true }).selectOption(language);
      await page.getByRole('tab', { name: 'Problem', exact: true }).click();
      check(await page.locator('.coding-pane .view-lines').innerText() === draft, 'hint/solution language preserves draft ' + language);
    }
    await page.getByRole('button', { name: 'Toggle problem list' }).click();
    const library = page.getByRole('dialog', { name: 'Problem library' });
    await library.getByLabel('Filter by topic or study plan').selectOption('pattern:Two pointers');
    const expected = problems.filter(p => catalog[p.id].tags.includes('Two pointers'));
    check(await library.locator('.problem-link').count() === expected.length, 'pattern filter exact count');
    await library.getByLabel('Search problems').fill('two pointers');
    check(await library.locator('.problem-link').count() === expected.length, 'pattern search matches tags');
    for (const theme of ['light', 'dark']) {
      await page.evaluate(theme => { document.documentElement.dataset.theme = theme; }, theme);
      for (const width of [320, 768, 1440]) {
        await page.setViewportSize({ width, height: 1000 });
        check(await library.locator('.problem-link').evaluateAll(rows => rows.every((row, index) => {
          const r = row.getBoundingClientRect();
          const label = row.querySelector('.problem-link-text').getBoundingClientRect();
          const next = rows[index + 1]?.getBoundingClientRect();
          return label.top >= r.top && label.bottom <= r.bottom && (!next || r.bottom <= next.top + 1);
        })), `${theme}/${width} library labels fit their rows without overlap`);
        check(await library.evaluate(el => el.scrollWidth <= el.clientWidth + 1), `${theme}/${width} library fits horizontally`);
        await page.screenshot({ path: path.join(output, `${theme}-${width}-pattern-library.png`) });
      }
    }
    await library.getByRole('button', { name: 'Close problem list' }).click();
    // Browser history must not expose another problem's hint state.
    await go('two_sum');
    await page.getByRole('button', { name: 'Reveal first hint' }).click();
    await go('blind75_two_sum');
    await page.goBack();
    await page.locator('#hints-two_sum').waitFor();
    check(await page.locator('#hints-two_sum details').count() === 0, 'Back resets problem hints');
    await page.goForward();
    await page.locator('#hints-blind75_two_sum').waitFor();
    check(await page.locator('#hints-blind75_two_sum details').count() === 0, 'Forward resets problem hints');
    await page.getByRole('button', { name: 'Reveal first hint' }).click();
    await page.getByRole('button', { name: 'Reveal next hint' }).click();
    await page.getByRole('button', { name: 'Hide hints' }).click();
    check(await page.getByRole('button', { name: 'Reveal first hint' }).evaluate(el => el === document.activeElement), 'Hide restores keyboard focus');

    await page.getByRole('button', { name: 'Toggle problem list' }).click();
    await library.getByLabel('Search problems').fill('');
    for (const tag of [...new Set(Object.values(catalog).flatMap(entry => entry.tags))]) {
      await library.getByLabel('Filter by topic or study plan').selectOption('pattern:' + tag);
      check(await library.locator('.problem-link').count() === problems.filter(p => catalog[p.id].tags.includes(tag)).length, 'exact filter ' + tag);
    }
    await library.getByLabel('Filter by topic or study plan').selectOption('');
    check(await library.locator('.problem-link').evaluateAll(rows => rows.every(row => {
      const id = row.getAttribute('aria-describedby');
      const label = id && document.getElementById(id);
      return label && label.textContent.trim().length > 0;
    })), 'all pattern labels accessible to assistive technology');
    for (const theme of ['light', 'dark']) {
      await page.evaluate(theme => { document.documentElement.dataset.theme = theme; }, theme);
      for (const width of [320, 768, 1440]) {
        await page.setViewportSize({ width, height: 640 });
        check(await library.locator('.problem-link').evaluateAll(rows => rows.every((row, index) => {
          const r = row.getBoundingClientRect();
          const label = row.querySelector('.problem-link-text').getBoundingClientRect();
          const next = rows[index + 1]?.getBoundingClientRect();
          return label.top >= r.top && label.bottom <= r.bottom + 1 && label.left >= r.left && label.right <= r.right + 1 && (!next || r.bottom <= next.top + 1);
        })), `${theme}/${width} all-bank library row bounds`);
        check(await library.locator('.library-patterns').evaluateAll(labels => labels.every(el => parseFloat(getComputedStyle(el).fontSize) >= 12)), 'pattern labels at least 12px');
        await page.screenshot({ path: path.join(output, `${theme}-${width}-all-patterns.png`) });
      }
    }
    await library.getByRole('button', { name: 'Close problem list' }).click();
    // Emulate a 200% zoomed desktop through CSS zoom plus a reduced viewport.
    await page.setViewportSize({ width: 768, height: 640 });
    await page.evaluate(() => { document.documentElement.style.zoom = '2'; });
    await go('ctci6_17_23');
    await page.getByRole('button', { name: 'Reveal first hint' }).click();
    await page.getByRole('button', { name: 'Reveal next hint' }).click();
    const zoomHints = page.locator('#hints-ctci6_17_23');
    check(await zoomHints.evaluate(el => el.scrollWidth <= el.clientWidth + 1), 'zoomed hints wrap');
    await page.getByRole('button', { name: 'Hide hints' }).click();
    check(await page.getByRole('button', { name: 'Reveal first hint' }).isVisible(), 'zoomed controls operable');
    await page.evaluate(() => { document.documentElement.style.zoom = ''; });
    check(report.errors.length === 0, 'no browser runtime errors');
    report.passed = true;
    console.log(JSON.stringify(report, null, 2));
  } finally {
    fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2));
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
