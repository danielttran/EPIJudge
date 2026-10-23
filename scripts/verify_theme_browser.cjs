// Run against an isolated EPIJudge server; no algorithm corpus is rerun.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { chromium } = require("../epijudge.client/node_modules/playwright-core");
const base = process.argv[2];
if (!base) throw new Error("Pass an isolated local server URL.");
const folder = path.resolve(__dirname, "../.epi-runs/theme-layout");
fs.mkdirSync(folder, { recursive: true });
const options = {
  headless: true,
  ...(process.env.CHROMIUM_PATH
    ? { executablePath: process.env.CHROMIUM_PATH }
    : { channel: "chromium" }),
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
};
const report = { passed: false, scenes: [], errors: [], checks: [] };
const inputPaths = [
  "epijudge.client/index.html",
  "epijudge.client/public/theme.js",
  "epijudge.client/src/theme.ts",
  "epijudge.client/src/App.tsx",
  "epijudge.client/src/SolutionPanel.tsx",
  "epijudge.client/src/LanguageSelect.tsx",
  "epijudge.client/src/CodeReferences.tsx",
  "epijudge.client/src/collections.ts",
  "EpiJudge.Runner/CtciCatalog.cs",
  "ctci6/catalog.json",
  "ctci6/practice/catalog.json",
  "workspace-code/catalog.json",
  "epijudge.client/src/Editor.tsx",
  "epijudge.client/src/ErrorBoundary.tsx",
  "epijudge.client/src/styles.css",
  "scripts/verify_theme_browser.cjs",
  "scripts/verify_format_browser.cjs",
  "epijudge.client/src/useCodeFormatter.ts",
  "EpiJudge.Runner/CodeFormatter.cs",
  "EpiJudge.Runner/EpiJudge.Runner.csproj",
  "EpiJudge.Web/Program.cs",
  "scripts/code_workspace/formatter.py",
];
const fingerprints = () =>
  Object.fromEntries(
    inputPaths.map((file) => [
      file,
      crypto
        .createHash("sha256")
        .update(fs.readFileSync(path.resolve(__dirname, "..", file)))
        .digest("hex"),
    ]),
  );
report.inputHashes = fingerprints();
const check = (value, label) => {
  assert(value, label);
  report.checks.push(label);
};
async function inspect(page, id, dialog = false) {
  // Existing button hover transitions also interpolate when theme variables change.
  await page.waitForTimeout(200);
  const details = await page.evaluate(
    ({ dialog }) => {
      const visibleRect = (el) => {
        const r = el.getBoundingClientRect();
        const box = {
          left: Math.max(0, r.left),
          right: Math.min(innerWidth, r.right),
          top: Math.max(0, r.top),
          bottom: Math.min(innerHeight, r.bottom),
        };
        for (
          let parent = el.parentElement;
          parent;
          parent = parent.parentElement
        ) {
          const style = getComputedStyle(parent),
            bounds = parent.getBoundingClientRect();
          if (/auto|scroll|hidden|clip/.test(style.overflowY)) {
            box.top = Math.max(box.top, bounds.top);
            box.bottom = Math.min(box.bottom, bounds.bottom);
          }
          if (/auto|scroll|hidden|clip/.test(style.overflowX)) {
            box.left = Math.max(box.left, bounds.left);
            box.right = Math.min(box.right, bounds.right);
          }
        }
        return box;
      };
      const shown = (el) => {
        const r = visibleRect(el),
          s = getComputedStyle(el);
        return (
          r.right - r.left > 1 &&
          r.bottom - r.top > 1 &&
          s.visibility !== "hidden" &&
          s.display !== "none"
        );
      };
      const controls = [
        ...document.querySelectorAll(
          dialog
            ? "dialog[open] button,dialog[open] input,dialog[open] select"
            : ".topbar button,.topbar a,.format-toolbar button,.editor-language-row select,.editor-toolbar button",
        ),
      ].filter(shown);
      const clipped = controls
        .filter((el) => {
          const r = el.getBoundingClientRect();
          return r.left < 0 || r.right > innerWidth + 1;
        })
        .map((el) => el.getAttribute("aria-label") || el.textContent);
      const covered = controls
        .filter((el) => {
          const r = el.getBoundingClientRect();
          const visible = visibleRect(el);
          const hit = document.elementFromPoint(
            (visible.left + visible.right) / 2,
            (visible.top + visible.bottom) / 2,
          );
          return !el.contains(hit);
        })
        .map((el) => el.getAttribute("aria-label") || el.textContent);
      function rgb(s) {
        return s.match(/[\d.]+/g).map(Number);
      }
      function luminance(c) {
        return c
          .slice(0, 3)
          .map((x) => {
            x /= 255;
            return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4;
          })
          .reduce((v, x, i) => v + x * [0.2126, 0.7152, 0.0722][i], 0);
      }
      const contrast = [];
      const scope = dialog
        ? document.querySelector("dialog[open]")
        : document.body;
      for (const el of scope.querySelectorAll("*")) {
        if (
          !shown(el) ||
          el.closest(
            '[disabled], [aria-hidden="true"], svg, .monaco-editor .margin',
          )
        )
          continue;
        const text = [...el.childNodes]
          .filter((n) => n.nodeType === 3)
          .map((n) => n.textContent)
          .join("")
          .trim();
        if (!text) continue;
        const style = getComputedStyle(el);
        let bg = [0, 0, 0, 0];
        for (let p = el; p; p = p.parentElement) {
          const c = rgb(getComputedStyle(p).backgroundColor);
          const a = c[3] ?? 1;
          const k = (1 - bg[3]) * a;
          for (let i = 0; i < 3; i++) bg[i] += c[i] * k;
          bg[3] += k;
          if (bg[3] > 0.999) break;
        }
        const fg = rgb(style.color);
        const a = fg[3] ?? 1;
        for (let i = 0; i < 3; i++) fg[i] = fg[i] * a + bg[i] * (1 - a);
        const ls = [luminance(fg), luminance(bg)].sort((a, b) => b - a);
        const ratio = (ls[0] + 0.05) / (ls[1] + 0.05);
        const large =
          parseFloat(style.fontSize) >= 24 ||
          (parseFloat(style.fontSize) >= 18.66 && +style.fontWeight >= 700);
        if (ratio < (large ? 3 : 4.5) - 0.02)
          contrast.push({
            text: text.slice(0, 70),
            ratio: +ratio.toFixed(2),
            color: style.color,
            bg: bg.slice(0, 3),
            class: el.className,
          });
      }
      return {
        overflow: document.documentElement.scrollWidth > innerWidth + 2,
        clipped,
        covered,
        contrast,
        theme: document.documentElement.dataset.theme,
        width: innerWidth,
      };
    },
    { dialog },
  );
  check(!details.overflow, id + " no document overflow");
  assert.deepEqual(details.clipped, [], id + " clipped controls");
  assert.deepEqual(details.covered, [], id + " covered controls");
  assert.deepEqual(details.contrast, [], id + " text contrast");
  const cdp = await page.context().newCDPSession(page);
  const shot = await cdp.send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  await cdp.detach();
  fs.writeFileSync(
    path.join(folder, id + ".png"),
    Buffer.from(shot.data, "base64"),
  );
  report.scenes.push({ id, ...details });
  console.log("PASS theme " + id);
}
async function main() {
  const browser = await chromium.launch(options);
  let context;
  try {
    // Block the React bundle: the independent bootstrap must already select the theme.
    for (const theme of ["light", "dark"]) {
      context = await browser.newContext({ colorScheme: theme });
      const page = await context.newPage();
      await page.route("**/assets/*.js", (route) => route.abort());
      await page.goto(base + "/practice");
      check(
        (await page.locator("html").getAttribute("data-theme")) === theme,
        "pre-React system " + theme,
      );
      await context.close();
      context = null;
    }
    // Exercise keyboard activation, persistence, live system changes and cross-tab sync.
    context = await browser.newContext({ colorScheme: "light" });
    let page = await context.newPage();
    await page.goto(base + "/practice?problem=count_bits");
    const toggle = page.getByRole("button", { name: "Dark mode", exact: true });
    await toggle.waitFor();
    await toggle.focus();
    await page.keyboard.press("Space");
    check(
      (await toggle.getAttribute("aria-pressed")) === "true",
      "keyboard Space switches to dark",
    );
    await page.reload();
    await toggle.waitFor();
    check(
      (await toggle.getAttribute("aria-pressed")) === "true",
      "dark preference survives reload",
    );
    await page.emulateMedia({ colorScheme: "light" });
    check(
      (await toggle.getAttribute("aria-pressed")) === "true",
      "explicit choice overrides system",
    );
    const second = await context.newPage();
    await second.goto(base + "/learn");
    await second
      .getByRole("button", { name: "Dark mode", exact: true })
      .click();
    await page.waitForFunction(
      () => document.documentElement.dataset.theme === "light",
    );
    check(true, "choice synchronizes across open tabs");
    await page.evaluate(() => localStorage.removeItem("epi:theme"));
    await page.reload();
    await toggle.waitFor();
    await page.emulateMedia({ colorScheme: "dark" });
    await page.waitForFunction(
      () => document.documentElement.dataset.theme === "dark",
    );
    check(
      true,
      "without an explicit preference live system changes are followed",
    );
    await context.close();
    context = null;
    for (const profile of [
      { id: "desktop", width: 1440, height: 1000 },
      { id: "mobile", width: 320, height: 740 },
      { id: "zoom200", zoom: 2 },
    ]) {
      if (profile.zoom) {
        const dir = fs.mkdtempSync(path.join(folder, "zoom-"));
        fs.mkdirSync(path.join(dir, "Default"));
        fs.writeFileSync(
          path.join(dir, "Default/Preferences"),
          JSON.stringify({
            partition: {
              default_zoom_level: { x: Math.log(2) / Math.log(1.2) },
            },
          }),
        );
        context = await chromium.launchPersistentContext(dir, {
          ...options,
          viewport: null,
          args: [...options.args, "--window-size=1440,1000"],
        });
      } else
        context = await browser.newContext({
          viewport: { width: profile.width, height: profile.height },
        });
      context.setDefaultTimeout(25000);
      page = await context.newPage();
      page.on("pageerror", (error) => report.errors.push(String(error)));
      await page.goto(base + "/practice?problem=count_bits");
      await page
        .getByRole("combobox", { name: "Select programming language" })
        .selectOption("javascript");
      const response = await page.request.get(
        base + "/api/problems/count_bits/solution?language=javascript",
      );
      const solution = await response.json();
      const editor = page.locator(
        ".coding-pane .monaco-editor textarea.inputarea",
      );
      await editor.waitFor();
      await context.grantPermissions(["clipboard-read", "clipboard-write"], {
        origin: base,
      });
      const edit = async (code) => {
        await editor.focus();
        await page.keyboard.press("Control+A");
        await page.evaluate(
          (text) => navigator.clipboard.writeText(text),
          code,
        );
        await page.keyboard.press("Control+V");
      };
      const run = async (status) => {
        await page.getByRole("button", { name: "Run", exact: true }).click();
        await page
          .locator(".result-status")
          .filter({ hasText: status })
          .waitFor();
      };
      await edit(solution.code);
      await run("Accepted");
      const session = await context.newCDPSession(page);
      const zoom = (await session.send("Page.getLayoutMetrics"))
        .cssVisualViewport.zoom;
      await session.detach();
      check(
        Math.abs(zoom - (profile.zoom || 1)) < 0.01,
        profile.id + " native browser zoom",
      );
      for (const theme of ["light", "dark"]) {
        if ((await page.locator("html").getAttribute("data-theme")) !== theme)
          await page
            .getByRole("button", { name: "Dark mode", exact: true })
            .click();
        await page.getByRole("tab", { name: "Problem", exact: true }).click();
        await page.evaluate(() => window.scrollTo(0, 0));
        await page
          .locator(".problem-description")
          .evaluate((el) => (el.scrollTop = 0));
        await inspect(page, `${theme}-${profile.id}-practice`);
        await page.locator(".results-panel").scrollIntoViewIfNeeded();
        await inspect(page, `${theme}-${profile.id}-results`);
        await edit("function countBits(x) { return -1; }");
        await run("Wrong answer");
        await page.locator(".results-panel").scrollIntoViewIfNeeded();
        await inspect(page, `${theme}-${profile.id}-failure`);
        await edit(solution.code);
        await run("Accepted");
        await page.getByRole("tab", { name: "Solution", exact: true }).click();
        await page.getByLabel("JavaScript reference solution code").waitFor();
        await page
          .locator(".solution-content")
          .evaluate((el) => (el.scrollTop = el.scrollHeight));
        await inspect(page, `${theme}-${profile.id}-solution`);
        await page
          .getByLabel("JavaScript reference solution code")
          .evaluate((el) => {
            const panel = el.closest(".solution-content");
            panel.scrollTop +=
              el.getBoundingClientRect().top -
              panel.getBoundingClientRect().top -
              8;
          });
        await inspect(page, `${theme}-${profile.id}-reference-code`);
        await page.getByRole("button", { name: "Toggle problem list" }).click();
        await inspect(page, `${theme}-${profile.id}-dialog`, true);
        await page.getByRole("button", { name: "Close problem list" }).click();
        await page.getByRole("link", { name: "Learn", exact: true }).click();
        await page
          .getByRole("heading", { name: "Learn", exact: true })
          .waitFor();
        await inspect(page, `${theme}-${profile.id}-learn`);
        await page
          .getByRole("link", { name: /LCA with parent pointers/ })
          .click();
        await page.locator(".learn-article-grid").waitFor();
        await inspect(page, `${theme}-${profile.id}-reading`);
        await page.getByRole("link", { name: "Practice", exact: true }).click();
        await editor.waitFor();
        check(
          (await page.locator(".coding-pane .view-lines").innerText()).includes(
            "countBits",
          ),
          "theme/navigation preserves executable draft",
        );
        if (profile.id === "desktop") {
          for (const [language, label] of [
            ["csharp", "C#"],
            ["python", "Python"],
            ["cpp", "C++"],
            ["java", "Java"],
          ]) {
            await page
              .getByRole("combobox", { name: "Select programming language" })
              .selectOption(language);
            await page
              .getByRole("tab", { name: "Solution", exact: true })
              .click();
            await page.getByLabel(label + " reference solution code").waitFor();
            await page
              .getByLabel(label + " reference solution code")
              .evaluate((el) => {
                const panel = el.closest(".solution-content");
                panel.scrollTop +=
                  el.getBoundingClientRect().top -
                  panel.getBoundingClientRect().top -
                  8;
              });
            await inspect(page, `${theme}-desktop-${language}-reference-code`);
          }
          await page
            .getByRole("combobox", { name: "Select programming language" })
            .selectOption("javascript");
          await page.getByRole("tab", { name: "Problem", exact: true }).click();
        }
        // Reloading/navigating clears the displayed result; execute only this tiny example again.
        if (theme === "light") {
          await page.getByRole("button", { name: "Run", exact: true }).click();
          await page
            .locator(".result-status")
            .filter({ hasText: "Accepted" })
            .waitFor();
        }
      }
      await context.close();
      context = null;
    }
    check(report.errors.length === 0, "no browser errors");
    assert.deepEqual(
      fingerprints(),
      report.inputHashes,
      "inputs stayed unchanged during acceptance",
    );
    report.passed = true;
  } catch (error) {
    report.failure = String(error);
    throw error;
  } finally {
    if (context) await context.close();
    await browser.close();
    fs.writeFileSync(
      path.join(folder, "report.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
  }
}
if (require.main === module)
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });

module.exports = { inspect, options, report, check, fingerprints };
