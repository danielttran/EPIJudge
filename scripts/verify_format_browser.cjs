// Real local formatter + Monaco undo/draft/race checks, and five-language color audit.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("../epijudge.client/node_modules/playwright-core");
const {
  inspect,
  options,
  report,
  check,
  fingerprints,
} = require("./verify_theme_browser.cjs");
const base = process.argv[2];
const output = path.resolve(__dirname, "../.epi-runs/code-formatting");
fs.mkdirSync(output, { recursive: true });
const examples = {
  csharp:
    'public class Solution{public int F(int x){/* comment */string s="text  stays";return x+2;}}',
  javascript: 'function f(x){/* comment */const s="text  stays";return x+2}',
  python: 'def f( x ):\n # comment\n s="text  stays"\n return x+2',
  cpp: 'int f(int x){/* comment */const char* s="text  stays";return x+2;}',
  java: 'public static int f(int x){/* comment */String s="text  stays";return x+2;}',
};
const labels = {
  csharp: "C#",
  javascript: "JavaScript",
  python: "Python",
  cpp: "C++",
  java: "Java",
};
const invalid = {
  csharp: "class X { int F( }",
  javascript: "function f( {",
  python: "def f(:",
  cpp: "int f( {",
  java: "static int f( {",
};
(async () => {
  const browser = await chromium.launch(options);
  let context;
  try {
    for (const profile of [
      { id: "desktop", width: 1440, height: 1000 },
      { id: "mobile", width: 320, height: 740 },
      { id: "zoom200", zoom: 2 },
    ]) {
      if (profile.zoom) {
        const dir = fs.mkdtempSync(path.join(output, "zoom-"));
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
      await context.grantPermissions(["clipboard-read", "clipboard-write"], {
        origin: base,
      });
      const page = await context.newPage();
      page.on("pageerror", (e) => report.errors.push(String(e)));
      await page.route("**/api/problems", async (route) => {
        const response = await route.fetch();
        const problems = await response.json();
        const sample = problems.find((p) => p.id === "count_bits");
        sample.description += " Long text stress: " + "unbroken".repeat(70);
        sample.examples[0].input += " " + "long_input_".repeat(70);
        await route.fulfill({ response, json: problems });
      });
      await page.goto(base + "/practice?problem=count_bits");
      const headers = { "X-EpiJudge-Client": "local-editor" };
      const beforeFormatting = await (
        await page.request.get(base + "/api/practice")
      ).json();
      for (const [language, code] of Object.entries(examples)) {
        const formatted = await page.request.post(base + "/api/code/format", {
          headers,
          data: { language, code, codeFormat: "callable-v1" },
        });
        check(
          formatted.status() === 200,
          language + " HTTP formatting available",
        );
      }
      assert.deepEqual(
        await (await page.request.get(base + "/api/practice")).json(),
        beforeFormatting,
        "format endpoint never saves drafts or attempts",
      );
      check(
        (
          await page.request.post(base + "/api/code/format", {
            data: {
              language: "python",
              code: "x=1",
              codeFormat: "callable-v1",
            },
          })
        ).status() === 403,
        "format requires same-app header",
      );
      for (const body of [
        { language: "ruby", code: "x=1", codeFormat: "callable-v1" },
        { language: "python", code: "x=1", codeFormat: "other" },
        {
          language: "python",
          code: "x".repeat(40001),
          codeFormat: "callable-v1",
        },
      ])
        check(
          (
            await page.request.post(base + "/api/code/format", {
              headers,
              data: body,
            })
          ).status() === 400,
          "invalid format request rejected",
        );

      const editor = page.locator(
        ".coding-pane .monaco-editor textarea.inputarea",
      );
      const button = page.getByRole("button", {
        name: "Format code",
        exact: true,
      });
      const paste = async (code) => {
        await editor.focus();
        await page.keyboard.press("Control+A");
        await page.evaluate(
          (text) => navigator.clipboard.writeText(text),
          code,
        );
        await page.keyboard.press("Control+V");
      };
      const saved = async (code) => {
        await page.waitForFunction(async (wanted) => {
          const state = await (await fetch("/api/practice")).json();
          return state.drafts.some((d) => d.code === wanted);
        }, code);
      };
      for (const theme of ["light", "dark"]) {
        if ((await page.locator("html").getAttribute("data-theme")) !== theme)
          await page
            .getByRole("button", { name: "Dark mode", exact: true })
            .click();
        for (const language of Object.keys(examples)) {
          await page
            .getByRole("combobox", { name: "Select programming language" })
            .selectOption(language);
          await editor.waitFor();
          const source = examples[language];
          await paste(source);
          await saved(source);
          const requested = page.waitForResponse((r) =>
            r.url().endsWith("/api/code/format"),
          );
          await button.click();
          const response = await requested;
          check(
            response.status() === 200,
            language + " uses real local formatter",
          );
          const formatted = (await response.json()).code;
          await page
            .getByText("Code formatted. Undo restores your previous code.", {
              exact: true,
            })
            .waitFor();
          await saved(formatted);
          await editor.focus();
          await page.keyboard.press("Control+Z");
          await saved(source);
          check(true, language + " undo restores exact original draft");
          await page.keyboard.press("Control+Y");
          await saved(formatted);
          check(true, language + " redo restores formatting");
          await page.locator(".format-toolbar").scrollIntoViewIfNeeded();
          await inspect(
            page,
            `format-${theme}-${profile.id}-${language}-editor`,
          );
          // Caret, line numbers, selection, and a long line remain readable inside Monaco.
          await editor.focus();
          await page.keyboard.press("Control+A");
          await page
            .locator(".coding-pane .monaco-editor .selected-text")
            .first()
            .waitFor({ state: "attached" });
          check(true, language + " selection renders");
          const colors = await page.evaluate(() => {
            const rgba = (color) => color.match(/[\d.]+/g).map(Number);
            const luminance = (rgb) =>
              rgb
                .slice(0, 3)
                .map((v) => {
                  v /= 255;
                  return v <= 0.04045
                    ? v / 12.92
                    : ((v + 0.055) / 1.055) ** 2.4;
                })
                .reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
            const ratio = (a, b) => {
              const values = [luminance(rgba(a)), luminance(rgba(b))].sort(
                (a, b) => b - a,
              );
              return (values[0] + 0.05) / (values[1] + 0.05);
            };
            const editor = document.querySelector(
              ".coding-pane .monaco-editor",
            );
            const background = getComputedStyle(
              editor.querySelector(".monaco-editor-background"),
            ).backgroundColor;
            const selection = getComputedStyle(
              editor.querySelector(".selected-text"),
            ).backgroundColor;
            const lowTokens = [...editor.querySelectorAll(".view-line span")]
              .filter(
                (el) =>
                  el.textContent.trim() &&
                  ratio(getComputedStyle(el).color, selection) < 4.48,
              )
              .map((el) => ({
                text: el.textContent,
                color: getComputedStyle(el).color,
              }));
            const lowNumbers = [...editor.querySelectorAll(".line-numbers")]
              .filter(
                (el) =>
                  el.textContent.trim() &&
                  ratio(getComputedStyle(el).color, background) < 4.48,
              )
              .map((el) => getComputedStyle(el).color);
            const cursor = getComputedStyle(editor.querySelector(".cursor"));
            return {
              lowTokens,
              lowNumbers,
              caret: ratio(cursor.backgroundColor, background),
            };
          });
          assert.deepEqual(
            colors.lowTokens,
            [],
            language + " selected syntax text contrast",
          );
          assert.deepEqual(
            colors.lowNumbers,
            [],
            language + " line-number contrast",
          );
          check(colors.caret >= 3, language + " caret contrast");
          await page.keyboard.press("ArrowRight");
          await paste(invalid[language]);
          const failed = page.waitForResponse((r) =>
            r.url().endsWith("/api/code/format"),
          );
          await button.click();
          check(
            (await failed).status() === 400,
            language + " incomplete syntax rejected",
          );
          await saved(invalid[language]);
          await page
            .locator(".format-message")
            .filter({ hasText: /syntax|Line/ })
            .waitFor();
          await inspect(
            page,
            `format-${theme}-${profile.id}-${language}-error`,
          );
          await paste(
            source +
              "\n" +
              (language === "python" ? "# " : "// ") +
              "long_text_".repeat(80),
          );
          await page
            .getByRole("tab", { name: "Solution", exact: true })
            .click();
          const reference = page.getByLabel(
            labels[language] + " reference solution code",
          );
          await reference.waitFor();
          await reference.evaluate((el) => {
            const panel = el.closest(".solution-content");
            panel.scrollTop +=
              el.getBoundingClientRect().top -
              panel.getBoundingClientRect().top -
              8;
          });
          await inspect(
            page,
            `format-${theme}-${profile.id}-${language}-reference`,
          );
          await page.getByRole("tab", { name: "Problem", exact: true }).click();
          await page
            .locator(".problem-description")
            .evaluate((el) => (el.scrollTop = 0));
          await inspect(
            page,
            `format-${theme}-${profile.id}-${language}-description`,
          );
        }
      }
      // Deliberately delay a response: typing and switching must invalidate it.
      await page
        .getByRole("combobox", { name: "Select programming language" })
        .selectOption("javascript");
      let release;
      const held = new Promise((resolve) => (release = resolve));
      let started;
      const ready = new Promise((resolve) => (started = resolve));
      let calls = 0;
      await page.route("**/api/code/format", async (route) => {
        calls++;
        started();
        await held;
        await route.fulfill({
          json: { code: "function staleReplacement() {}\n" },
        });
      });
      await paste(examples.javascript);
      await button.click();
      await ready;
      check(
        await page
          .getByRole("button", { name: "Formatting…", exact: true })
          .isDisabled(),
        "repeated clicks disabled",
      );
      await paste("function newerDraft(){return 9;}");
      release();
      await page
        .getByText("Code changed while formatting. Nothing was replaced.", {
          exact: true,
        })
        .waitFor();
      await saved("function newerDraft(){return 9;}");
      check(calls === 1, "one request while pending");
      await page.unroute("**/api/code/format");
      for (const change of ["language", "problem"]) {
        let finish, begin;
        const held = new Promise((resolve) => (finish = resolve)),
          ready = new Promise((resolve) => (begin = resolve));
        await page.route("**/api/code/format", async (route) => {
          begin();
          await held;
          await route
            .fulfill({ json: { code: "function staleReplacement() {}\n" } })
            .catch(() => {});
        });
        await paste(examples.javascript);
        await button.click();
        await ready;
        if (change === "language")
          await page
            .getByRole("combobox", { name: "Select programming language" })
            .selectOption("python");
        else
          await page.evaluate(() => {
            history.pushState(null, "", "/practice?problem=parity");
            dispatchEvent(new PopStateEvent("popstate"));
          });
        await page
          .getByRole("button", { name: "Format code", exact: true })
          .waitFor();
        const before = await page
          .locator(".coding-pane .view-lines")
          .innerText();
        finish();
        await page.waitForTimeout(250);
        assert.equal(
          await page.locator(".coding-pane .view-lines").innerText(),
          before,
          "switching " + change + " rejects stale formatting",
        );
        await page.unroute("**/api/code/format");
        await page.evaluate(() => {
          history.pushState(null, "", "/practice?problem=count_bits");
          dispatchEvent(new PopStateEvent("popstate"));
        });
        await page
          .getByRole("combobox", { name: "Select programming language" })
          .selectOption("javascript");
        check(true, "switching " + change + " preserves the active document");
      }

      await context.close();
      context = null;
    }
    check(report.errors.length === 0, "no page errors");
    assert.deepEqual(
      fingerprints(),
      report.inputHashes,
      "final source fingerprints unchanged",
    );
    report.passed = true;
  } catch (error) {
    report.failure = String(error);
    throw error;
  } finally {
    if (context) await context.close();
    await browser.close();
    fs.writeFileSync(
      path.join(output, "report.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
