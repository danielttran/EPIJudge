// Real Chromium, Monaco, local solution API and isolated persisted drafts.
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const { chromium } = require("../epijudge.client/node_modules/playwright-core");
const base = process.argv[2];
if (!base) throw Error("Pass the isolated local server URL.");
const root = path.resolve(__dirname, "..");
const artifacts = path.join(root, ".epi-runs");
fs.mkdirSync(artifacts, { recursive: true });
const checks = [];
const external = [];
const errors = [];
const requests = [];
const verifiedScopes = new Map();
const report = {
  passed: false,
  checks,
  externalRequests: external,
  pageErrors: errors,
};
const LANGUAGE_NAMES = {
  csharp: "C#",
  javascript: "JavaScript",
  python: "Python",
  cpp: "C++",
  java: "Java",
};
const LANGUAGES = Object.keys(LANGUAGE_NAMES);
function pass(label) {
  checks.push(label);
  console.log("PASS solutions browser " + label);
}
async function until(predicate, label) {
  const end = Date.now() + 20000;
  while (Date.now() < end) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw Error("Timed out: " + label);
}
(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROMIUM_PATH
      ? { executablePath: process.env.CHROMIUM_PATH }
      : {}),
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    acceptDownloads: true,
    permissions: ["clipboard-read", "clipboard-write"],
  });
  const page = await context.newPage();
  page.on("pageerror", (error) => errors.push(String(error)));
  page.on("request", (request) =>
    requests.push({ url: request.url(), method: request.method() }),
  );
  await context.route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (
      ["http:", "https:"].includes(url.protocol) &&
      url.origin !== new URL(base).origin
    ) {
      external.push(url.href);
      return route.abort();
    }
    return route.continue();
  });
  const endpoint = (id, lang) =>
    base + "/api/problems/" + id + "/solution?language=" + lang;
  const solutionTab = page.getByRole("tab", { name: "Solution", exact: true });
  const descriptionTab = page.getByRole("tab", {
    name: "Problem",
    exact: true,
  });
  const code = page.locator(".solution-code");
  const language = page.getByRole("combobox", {
    name: "Select programming language",
  });
  const editor = page.locator(".coding-pane .monaco-editor textarea.inputarea");
  const editorText = async () =>
    (
      await page.locator(".coding-pane .monaco-editor .view-lines").innerText()
    ).replace(/\s+/g, " ");
  const exportState = async () => {
    const response = await page.request.get(base + "/api/practice/export");
    assert.equal(response.status(), 200);
    return response.json();
  };
  const answer = async (id, lang) => {
    const response = await page.request.get(endpoint(id, lang));
    assert.equal(response.status(), 200);
    return response.json();
  };
  const saved = async (id, lang, draft) =>
    until(
      async () => {
        const state = await exportState();
        return state.drafts.some(
          (d) => d.problemId === id && d.language === lang && d.code === draft,
        );
      },
      "draft " + id + "/" + lang,
    );
  const edit = async (draft) => {
    await editor.focus();
    await page.keyboard.press("Control+A");
    await page.keyboard.insertText(draft);
  };
  const prepareDrafts = async (id) => {
    for (const lang of LANGUAGES) {
      const draft =
        (lang === "python" ? "#" : "//") +
        " solution-tab retained " +
        id +
        " " +
        lang;
      await language.selectOption(lang);
      await edit(draft);
      await saved(id, lang, draft);
    }
  };
  const select = async (collection, name) => {
    await page.getByRole("button", { name: "Toggle problem list" }).click();
    await page
      .getByRole("combobox", { name: "Filter by topic or study plan" })
      .selectOption("collection:" + collection);
    await page.getByRole("button", { name }).click();
  };
  const assertAnswer = async (expected) => {
    assert.equal(expected.codeFormat, "callable-v1");
    assert.ok(Array.isArray(expected.references));
    await until(
      async () =>
        (await code.count()) === 1 &&
        (await code
          .locator("textarea.inputarea")
          .getAttribute("aria-label")) ===
          LANGUAGE_NAMES[expected.language] + " reference solution code",
      expected.problemId + "/" + expected.language + " read-only editor",
    );
    assert.equal(await solutionTab.getAttribute("aria-selected"), "true");
    assert.equal(await language.inputValue(), expected.language);
    assert.equal(
      await page
        .getByText(LANGUAGE_NAMES[expected.language] + " reference solution", {
          exact: true,
        })
        .count(),
      1,
    );
    assert.ok(
      (await page.locator(".solution-approach").innerText()).includes(
        expected.explanation,
      ),
    );
    assert.ok(
      (await page.locator(".solution-complexity").innerText()).includes(
        expected.timeComplexity,
      ),
    );
    assert.ok(
      (await page.locator(".solution-complexity").innerText()).includes(
        expected.spaceComplexity,
      ),
    );
    assert.equal(
      await code
        .locator("textarea.inputarea")
        .evaluate((input) => input.readOnly),
      true,
    );
    assert.equal(
      await page
        .getByRole("button", { name: /copy.*editor|replace.*editor/i })
        .count(),
      0,
    );
    await page.getByRole("button", { name: "Copy code", exact: true }).click();
    await page.getByText("Code copied.", { exact: true }).waitFor();
    assert.equal(
      await page.evaluate(() => navigator.clipboard.readText()),
      expected.code,
    );
    verifiedScopes.set(expected.problemId + ":" + expected.language, {
      problemId: expected.problemId,
      language: expected.language,
      codeFormat: expected.codeFormat,
      codeSha256: crypto
        .createHash("sha256")
        .update(expected.code)
        .digest("hex"),
    });
  };
  try {
    await page.goto(base, { waitUntil: "networkidle" });
    await language.waitFor();
    await until(async () => (await editor.count()) === 1, "Monaco ready");
    assert.equal(
      requests.filter((r) => r.url.includes("/solution?language=")).length,
      0,
    );
    await select("epi", /^01\. Count Bits/);
    await prepareDrafts("count_bits");
    const epi = await answer("count_bits", "java");
    const beforeViews = await exportState();
    assert.equal(beforeViews.version, 2);
    assert.ok(
      beforeViews.drafts.every((draft) =>
        ["legacy-v1", "callable-v1"].includes(draft.codeFormat),
      ),
    );
    const writesBefore = requests.filter((r) =>
      ["PUT", "POST", "DELETE", "PATCH"].includes(r.method),
    ).length;
    await solutionTab.click();
    await assertAnswer(epi);
    for (const lang of LANGUAGES) {
      await language.selectOption(lang);
      await until(
        async () =>
          (await editorText()).includes("retained count_bits " + lang),
        "retained EPI " + lang,
      );
      await assertAnswer(await answer("count_bits", lang));
    }
    assert.ok((await editorText()).includes("retained count_bits java"));
    assert.equal(await language.inputValue(), "java");
    await descriptionTab.focus();
    await page.keyboard.press("End");
    assert.equal(
      await solutionTab.evaluate((node) => document.activeElement === node),
      true,
    );
    await page.keyboard.press("ArrowLeft");
    assert.equal(
      await descriptionTab.evaluate((node) => document.activeElement === node),
      true,
    );
    assert.equal(
      await page
        .getByRole("tabpanel", { name: "Problem", exact: true })
        .isVisible(),
      true,
    );
    await page.keyboard.press("ArrowRight");
    await assertAnswer(epi);
    // assertAnswer exercises Copy, which intentionally moves focus off the tabs.
    await solutionTab.focus();
    await page.keyboard.press("Home");
    assert.equal(
      await descriptionTab.evaluate((node) => document.activeElement === node),
      true,
    );
    await solutionTab.click();
    await assertAnswer(epi);
    assert.deepEqual(await exportState(), beforeViews);
    assert.equal(
      requests.filter((r) =>
        ["PUT", "POST", "DELETE", "PATCH"].includes(r.method),
      ).length,
      writesBefore,
    );
    const leftBounds = await page.locator(".problem-pane").boundingBox();
    const rightBounds = await page.locator(".coding-pane").boundingBox();
    assert.ok(
      leftBounds &&
        rightBounds &&
        Math.abs(leftBounds.width - rightBounds.width) <= 3,
    );
    assert.ok((await code.locator(".line-numbers").count()) > 0);
    const tokenClasses = await code
      .locator('.view-line span[class*="mtk"]')
      .evaluateAll((tokens) => [
        ...new Set(tokens.map((token) => token.className)),
      ]);
    assert.ok(
      tokenClasses.length >= 2,
      "Local grammar provides distinct syntax token styles",
    );
    await code.locator("textarea.inputarea").focus();
    await page.keyboard.press("Control+A");
    await page.keyboard.insertText("readonly replacement must not appear");
    assert.equal(
      (await code.innerText()).includes("readonly replacement must not appear"),
      false,
    );
    await assertAnswer(epi);
    await page.locator(".solution-content").evaluate((article) => {
      article.scrollTop = 0;
    });
    await page.screenshot({
      path: path.join(artifacts, "solutions-browser-epi.png"),
      fullPage: true,
    });
    pass(
      "all five EPI solutions, explanations, complexity and keyboard tabs preserve real Monaco drafts",
    );

    await page
      .getByRole("button", { name: "Next problem", exact: true })
      .click();
    await assertAnswer(await answer("two_sum", "java"));
    assert.equal(
      await page
        .getByRole("heading", { name: "Two Sum — Solution", exact: true })
        .isVisible(),
      true,
    );
    await page
      .getByRole("button", { name: "Previous problem", exact: true })
      .click();
    await assertAnswer(epi);
    assert.ok((await editorText()).includes("retained count_bits java"));
    assert.deepEqual(await exportState(), beforeViews);
    pass(
      "selection changes retain the Solution tab and load the matching question without changing drafts",
    );

    await select("interviewcake", /^IC02\. Apple Stocks/);
    await prepareDrafts("interviewcake_stock-price");
    const cakeDrafts = await exportState();
    for (const lang of LANGUAGES) {
      await language.selectOption(lang);
      await until(
        async () =>
          (await editorText()).includes(
            "retained interviewcake_stock-price " + lang,
          ),
        "retained Interview Cake " + lang,
      );
      await assertAnswer(await answer("interviewcake_stock-price", lang));
      if (lang === "csharp") {
        await page
          .getByRole("heading", { name: "Correctness", exact: true })
          .waitFor();
        await page
          .getByRole("heading", { name: "Edge cases", exact: true })
          .waitFor();
      }
    }
    assert.deepEqual(await exportState(), cakeDrafts);
    await descriptionTab.click();
    const source = page.getByRole("link", {
      name: "Original task reference",
      exact: true,
    });
    assert.ok(
      (await source.getAttribute("href")).startsWith(
        "https://www.interviewcake.com/question/csharp/stock-price",
      ),
    );
    assert.equal(await source.getAttribute("rel"), "noopener noreferrer");
    await solutionTab.click();
    await page.screenshot({
      path: path.join(artifacts, "solutions-browser-interviewcake.png"),
      fullPage: true,
    });
    pass(
      "all 41 Interview Cake tasks are separately filterable and five selected-language solutions preserve their drafts",
    );

    await select("blind75", /^B01\. Two Sum/);
    await prepareDrafts("blind75_two_sum");
    const blind = await answer("blind75_two_sum", "java");
    await assertAnswer(blind);
    const allDrafts = await exportState();
    const stableWrites = requests.filter((r) =>
      ["PUT", "POST", "DELETE", "PATCH"].includes(r.method),
    ).length;
    for (const lang of LANGUAGES) {
      await language.selectOption(lang);
      await until(
        async () =>
          (await editorText()).includes("retained blind75_two_sum " + lang),
        "retained " + lang,
      );
      await assertAnswer(await answer("blind75_two_sum", lang));
    }
    assert.deepEqual(await exportState(), allDrafts);
    assert.equal(
      requests.filter((r) =>
        ["PUT", "POST", "DELETE", "PATCH"].includes(r.method),
      ).length,
      stableWrites,
    );
    assert.notEqual(epi.code, blind.code);
    pass(
      "all five Blind solutions use their own contract and preserve independent language drafts",
    );

    const blindPattern = endpoint("blind75_two_sum", "java");
    await descriptionTab.click();
    await context.route(blindPattern, (route) =>
      route.fulfill({
        status: 503,
        contentType: "application/json",
        body: "{}",
      }),
    );
    await solutionTab.click();
    await page
      .getByRole("tabpanel", { name: "Solution", exact: true })
      .getByRole("alert")
      .waitFor();
    await context.unroute(blindPattern);
    await page
      .getByRole("button", { name: "Retry solution", exact: true })
      .click();
    await assertAnswer(blind);
    pass(
      "local solution HTTP failure displays a retry and recovers to the exact answer",
    );

    await descriptionTab.click();
    await context.route(blindPattern, (route) =>
      route.fulfill({
        status: 404,
        contentType: "application/json",
        body: "{}",
      }),
    );
    await solutionTab.click();
    await page
      .getByText("A Java solution is not available for this question.", {
        exact: true,
      })
      .waitFor();
    assert.equal(await code.count(), 0);
    await context.unroute(blindPattern);
    await descriptionTab.click();
    await solutionTab.click();
    await assertAnswer(blind);
    pass(
      "unavailable answer is explicit and never replaces the editor with an empty answer",
    );

    await descriptionTab.click();
    await context.route(blindPattern, (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ ...blind, problemId: "wrong-question" }),
      }),
    );
    await solutionTab.click();
    await page
      .getByRole("tabpanel", { name: "Solution", exact: true })
      .getByRole("alert")
      .waitFor();
    assert.equal(await code.count(), 0);
    await context.unroute(blindPattern);
    await page
      .getByRole("button", { name: "Retry solution", exact: true })
      .click();
    await assertAnswer(blind);
    pass("mismatched answer payload fails safely and can be retried");

    await descriptionTab.click();
    let delayedRoute;
    await context.route(blindPattern, (route) => {
      delayedRoute = route;
    });
    await solutionTab.click();
    await until(async () => Boolean(delayedRoute), "delayed solution request");
    await page
      .getByRole("button", { name: "Next problem", exact: true })
      .click();
    const second = await answer("blind75_contains_duplicate", "java");
    await assertAnswer(second);
    await delayedRoute
      .fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(blind),
      })
      .catch(() => {});
    await context.unroute(blindPattern);
    await assertAnswer(second);
    await page
      .getByRole("button", { name: "Previous problem", exact: true })
      .click();
    await assertAnswer(blind);
    assert.deepEqual(await exportState(), allDrafts);
    assert.equal(
      requests.filter((r) =>
        ["PUT", "POST", "DELETE", "PATCH"].includes(r.method),
      ).length,
      stableWrites,
    );
    pass(
      "late answers from an aborted selection never overwrite the selected answer or stored drafts",
    );

    await descriptionTab.click();
    let delayedLanguageRoute;
    await context.route(blindPattern, (route) => {
      delayedLanguageRoute = route;
    });
    await solutionTab.click();
    await until(
      async () => Boolean(delayedLanguageRoute),
      "delayed Java solution request",
    );
    await language.selectOption("python");
    const pythonAnswer = await answer("blind75_two_sum", "python");
    await assertAnswer(pythonAnswer);
    await delayedLanguageRoute
      .fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(blind),
      })
      .catch(() => {});
    await context.unroute(blindPattern);
    await assertAnswer(pythonAnswer);
    await language.selectOption("java");
    await assertAnswer(blind);
    assert.deepEqual(await exportState(), allDrafts);
    assert.equal(
      requests.filter((r) =>
        ["PUT", "POST", "DELETE", "PATCH"].includes(r.method),
      ).length,
      stableWrites,
    );
    pass(
      "late solutions from a previous editor language cannot replace the selected-language answer or drafts",
    );

    await page.evaluate(() => {
      window.__solutionClipboardWrite = navigator.clipboard.writeText.bind(
        navigator.clipboard,
      );
      Object.defineProperty(navigator.clipboard, "writeText", {
        configurable: true,
        value: () =>
          Promise.reject(
            new DOMException("Clipboard denied", "NotAllowedError"),
          ),
      });
    });
    await page.getByRole("button", { name: "Copy code", exact: true }).click();
    await page
      .getByText("Could not copy. Select the code and copy it manually.", {
        exact: true,
      })
      .waitFor();
    assert.equal(
      await page.getByText("Code copied.", { exact: true }).count(),
      0,
    );
    await page.evaluate(() => {
      Object.defineProperty(navigator.clipboard, "writeText", {
        configurable: true,
        value: window.__solutionClipboardWrite,
      });
      delete window.__solutionClipboardWrite;
    });
    await assertAnswer(blind);
    assert.deepEqual(await exportState(), allDrafts);
    pass(
      "Copy uses the exact selected source and clipboard failure never reports success or changes the editor",
    );

    const catalog = await (
      await page.request.get(base + "/api/problems")
    ).json();
    const diagrams = catalog.filter((p) => p.diagram).map((p) => p.diagram);
    assert.equal(
      catalog.filter((p) => p.collection === "blind75" && p.diagram).length,
      35,
    );
    assert.equal(
      catalog.filter((p) => p.collection === "interviewcake" && p.diagram)
        .length,
      3,
    );
    assert.equal(diagrams.length, 38);
    await page.evaluate(async (images) => {
      for (const source of images) {
        const image = new Image();
        image.src = source;
        await image.decode();
        if (!image.naturalWidth) throw Error("Empty local diagram " + source);
      }
    }, diagrams);
    assert.deepEqual(external, []);
    assert.deepEqual(errors, []);
    await page.screenshot({
      path: path.join(artifacts, "solutions-browser.png"),
      fullPage: true,
    });
    pass(
      "solution UI, Monaco, and all 38 local diagrams work with external origins blocked",
    );

    await page.setViewportSize({ width: 390, height: 844 });
    await assertAnswer(blind);
    const panelBounds = await page
      .getByRole("tabpanel", { name: "Solution", exact: true })
      .boundingBox();
    assert.ok(
      panelBounds &&
        panelBounds.x >= 0 &&
        panelBounds.x + panelBounds.width <= 391,
    );
    assert.equal(await solutionTab.isVisible(), true);
    await page.screenshot({
      path: path.join(artifacts, "solutions-browser-mobile.png"),
      fullPage: true,
    });
    await page.locator(".solution-content").evaluate((article) => {
      article.scrollTop =
        article.querySelector(".solution-code").offsetTop - article.offsetTop;
    });
    const codeBounds = await code.boundingBox();
    assert.ok(
      codeBounds &&
        codeBounds.y < panelBounds.y + panelBounds.height &&
        codeBounds.y + codeBounds.height > panelBounds.y,
    );
    assert.equal(
      await code
        .locator("textarea.inputarea")
        .evaluate((input) => input.readOnly),
      true,
    );
    assert.equal(await descriptionTab.isVisible(), true);
    assert.equal(await solutionTab.isVisible(), true);
    await page.screenshot({
      path: path.join(artifacts, "solutions-browser-mobile-code.png"),
      fullPage: true,
    });
    await page.setViewportSize({ width: 1440, height: 1000 });
    pass(
      "Solution tab and code panel fit a narrow viewport without changing the draft",
    );

    await page.getByRole("button", { name: "Toggle problem list" }).click();
    const download = page.waitForEvent("download");
    await page
      .getByRole("button", { name: "Export answers", exact: true })
      .click();
    const downloaded = await download;
    const backup = JSON.parse(fs.readFileSync(await downloaded.path(), "utf8"));
    assert.equal(backup.version, 2);
    assert.deepEqual(backup, allDrafts);
    await page.getByLabel("Import answers file").setInputFiles({
      name: "solutions-retained.json",
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify(backup)),
    });
    await until(
      async () =>
        /Imported answers/.test(await page.locator("dialog").innerText()),
      "backup import",
    );
    assert.deepEqual(await exportState(), allDrafts);
    await page.getByRole("button", { name: "Close problem list" }).click();
    await assertAnswer(blind);
    pass(
      "backup export and idempotent restoration preserve existing answers after reading solutions",
    );

    await page.getByRole("button", { name: "Toggle problem list" }).click();
    await page
      .getByRole("combobox", { name: "Filter by topic or study plan" })
      .selectOption("kind:reading");
    await page.getByRole("button", { name: /R01.*Reading companion/ }).click();
    assert.equal(await solutionTab.count(), 0);
    assert.equal(
      await page.getByRole("button", { name: "Submit", exact: true }).count(),
      0,
    );
    assert.equal(
      await page
        .getByRole("textbox", { name: "Your notes and design response" })
        .isVisible(),
      true,
    );
    assert.deepEqual(await exportState(), allDrafts);
    pass(
      "existing reading companions retain their notes workflow and are not mislabeled as executable solutions",
    );

    assert.equal(
      requests.filter((r) => r.url.endsWith("/api/submissions")).length,
      0,
    );
    assert.deepEqual(external, []);
    assert.deepEqual(errors, []);
    report.passed = true;
    report.verifiedSolutionScopes = [...verifiedScopes.values()];
    report.readOnlyViewsCreatedSubmissions = false;
  } catch (error) {
    report.error = String(error.stack || error);
    await page
      .screenshot({
        path: path.join(artifacts, "solutions-browser-failure.png"),
        fullPage: true,
      })
      .catch(() => {});
    fs.writeFileSync(
      path.join(artifacts, "solutions-browser-failure.txt"),
      await page
        .locator("body")
        .innerText()
        .catch(() => "Page unavailable"),
    );
    throw error;
  } finally {
    fs.writeFileSync(
      path.join(artifacts, "solutions-browser.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
