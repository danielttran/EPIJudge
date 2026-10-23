// Solution reading preferences must never mutate the executable draft scope.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { chromium } = require("../epijudge.client/node_modules/playwright-core");
const {
  inspect,
  options,
  report,
  check,
  fingerprints,
} = require("./verify_theme_browser.cjs");
const base = process.argv[2];
if (!base) throw new Error("Pass an isolated local server URL.");
const problemId = process.argv[3] || "count_bits";
const output = path.resolve(__dirname, "../.epi-runs/solution-language" + (process.argv[3] ? "-" + problemId : ""));
fs.mkdirSync(output, { recursive: true });
const ownHash = () =>
  crypto.createHash("sha256").update(fs.readFileSync(__filename)).digest("hex");
const languages = [
  ["csharp", "C#"],
  ["javascript", "JavaScript"],
  ["python", "Python"],
  ["cpp", "C++"],
  ["java", "Java"],
];

async function main() {
  const browser = await chromium.launch(options);
  let context;
  report.inputHashes = {
    ...fingerprints(),
    "scripts/verify_solution_language_browser.cjs": ownHash(),
  };
  try {
    for (const profile of [
      { id: "desktop", width: 1440, height: 1000 },
      { id: "mobile", width: 320, height: 740 },
      { id: "zoom200", zoom: 2 },
    ]) {
      if (profile.zoom) {
        const directory = fs.mkdtempSync(path.join(output, "zoom-"));
        fs.mkdirSync(path.join(directory, "Default"));
        fs.writeFileSync(
          path.join(directory, "Default/Preferences"),
          JSON.stringify({
            partition: {
              default_zoom_level: { x: Math.log(2) / Math.log(1.2) },
            },
          }),
        );
        context = await chromium.launchPersistentContext(directory, {
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
      page.on("pageerror", (error) => report.errors.push(String(error)));
      await page.goto(base + "/practice?problem=" + problemId);
      if (problemId.startsWith("ctci6_")) {
        await page.getByRole("button", { name: "Toggle problem list" }).click();
        await page.getByRole("combobox", { name: "Filter by topic or study plan" }).selectOption("collection:ctci6");
        const expected = (await (await page.request.get(base + "/api/problems")).json()).filter(p => p.collection === "ctci6");
        check(await page.locator("#problem-library .problem-link").count() === expected.length, profile.id + " CtCI registered count");
        await page.getByRole("button", { name: /^C8\.11\. Coins/ }).scrollIntoViewIfNeeded();
        await inspect(page, "ctci-library-" + profile.id, true);
        await page.getByRole("button", { name: "Close problem list" }).click();
      }
      await page
        .getByRole("combobox", { name: "Select programming language" })
        .selectOption("csharp");
      const editor = page.locator(
        ".coding-pane .monaco-editor textarea.inputarea",
      );
      await editor.waitFor();
      await editor.focus();
      await page.keyboard.press("Control+A");
      const draft =
        "public int CountBits(int x) { return 999; } // protected draft Ω";
      await page.evaluate((text) => navigator.clipboard.writeText(text), draft);
      const saved = page.waitForResponse(
        (response) =>
          response.request().method() === "PUT" &&
          response.url().includes("/" + problemId + "/csharp"),
      );
      await page.keyboard.press("Control+V");
      await saved;
      const before = await (
        await page.request.get(base + "/api/practice")
      ).json();
      const cdp = await context.newCDPSession(page);
      const zoom = (await cdp.send("Page.getLayoutMetrics")).cssVisualViewport
        .zoom;
      await cdp.detach();
      check(
        Math.abs(zoom - (profile.zoom || 1)) < 0.01,
        profile.id + " native browser zoom",
      );
      await page.getByRole("tab", { name: "Solution", exact: true }).click();
      const selector = page.getByRole("combobox", {
        name: "Solution language",
      });
      await selector.waitFor();
      check(
        (await selector.locator("option").count()) === 5,
        profile.id + " five supported choices",
      );
      for (const theme of ["light", "dark"]) {
        if ((await page.locator("html").getAttribute("data-theme")) !== theme)
          await page
            .getByRole("button", { name: "Dark mode", exact: true })
            .click();
        for (const [language, label] of languages) {
          await selector.selectOption(language);
          await selector.focus();
          const code = page.getByLabel(label + " reference solution code", {
            exact: true,
          });
          await code.waitFor();
          const solution = await (
            await page.request.get(
              base + "/api/problems/" + problemId + "/solution?language=" + language,
            )
          ).json();
          assert.equal(
            await page.locator(".solution-approach").textContent(),
            solution.explanation,
            "matching language reasoning",
          );
          if (solution.walkthrough)
            await page
              .getByRole("region", { name: "Walkthrough", exact: true })
              .getByText(solution.walkthrough, { exact: true })
              .waitFor({ state: "attached" });
          check(
            (await page
              .getByRole("combobox", { name: "Select programming language" })
              .inputValue()) === "csharp",
            profile.id + " editor language remains independent",
          );
          check(
            await selector.evaluate((el) => document.activeElement === el),
            profile.id + " selector focus retained after answer load",
          );
          await selector.scrollIntoViewIfNeeded();
          await inspect(
            page,
            "solution-picker-" + problemId + "-" + profile.id + "-" + theme + "-" + language,
          );
          if (problemId.startsWith("ctci6_")) {
            const reference=page.locator("#solution-panel .provided-code-reference");
            if (await reference.count()) {
              await reference.locator("summary").click();
              await reference.locator(".provided-reference-code").first().scrollIntoViewIfNeeded();
              await inspect(page, "ctci-provided-"+profile.id+"-"+theme+"-"+language);
              await reference.locator("summary").click();
            }
          }
        }
      }
      await selector.focus();
      await page.keyboard.press("Home");
      await page.keyboard.press("ArrowDown");
      await page.keyboard.press("Enter");
      check(
        (await selector.inputValue()) === "javascript",
        profile.id + " native keyboard selection",
      );
      await page
        .getByLabel("JavaScript reference solution code", { exact: true })
        .waitFor();
      await page.reload();
      await page.getByRole("tab", { name: "Solution", exact: true }).click();
      await page
        .getByLabel("JavaScript reference solution code", { exact: true })
        .waitFor();
      check(
        (await selector.inputValue()) === "javascript",
        profile.id + " solution choice survives reload",
      );
      await editor.focus();
      await page.keyboard.press("Control+A");
      await page.keyboard.press("Control+C");
      assert.equal(
        await page.evaluate(() => navigator.clipboard.readText()),
        draft,
        profile.id + " executable draft survives solution switching and reload",
      );
      assert.deepEqual(
        await (await page.request.get(base + "/api/practice")).json(),
        before,
        "solution switching leaves stored drafts and progress unchanged",
      );
      await context.close();
      context = null;
    }
    assert.deepEqual(report.errors, [], "no browser application errors");
    report.passed = true;
  } finally {
    fs.writeFileSync(
      path.join(output, "report.json"),
      JSON.stringify(report, null, 2),
    );
    if (context) await context.close();
    await browser.close();
  }
  console.log(
    JSON.stringify({
      passed: report.passed,
      scenes: report.scenes.length,
      checks: report.checks.length,
      errors: report.errors,
    }),
  );
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
