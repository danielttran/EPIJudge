const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("../epijudge.client/node_modules/playwright-core");
const base = process.argv[2];
if (!base) throw new Error("Pass an isolated local server URL.");
const root = path.resolve(__dirname, "..");
const ctciPath = path.join(root, "ctci6/catalog.json");
const ctciCount = fs.existsSync(ctciPath)
  ? JSON.parse(fs.readFileSync(ctciPath, "utf8")).length
  : 0;
const inventory = require("../epijudge.client/src/reading/learnInventory.json");
const folder = path.join(root, ".epi-runs/learn-views");
fs.mkdirSync(folder, { recursive: true });
const report = {
  passed: false,
  checks: [],
  articles: [],
  screenshots: [],
  externalRequests: [],
  pageErrors: [],
};
const check = (ok, label) => {
  assert.ok(ok, label);
  report.checks.push(label);
  console.log("PASS Learn " + label);
};
const pauseUntil = async (predicate, label) => {
  const end = Date.now() + 20000;
  while (Date.now() < end) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Timed out: " + label);
};
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
    permissions: ["clipboard-read", "clipboard-write"],
  });
  const page = await context.newPage();
  page.on("pageerror", (error) => report.pageErrors.push(String(error)));
  await context.route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (
      ["http:", "https:"].includes(url.protocol) &&
      url.origin !== new URL(base).origin
    ) {
      report.externalRequests.push(url.href);
      return route.abort();
    }
    return route.continue();
  });
  const api = async (endpoint) => {
    const response = await context.request.get(base + endpoint);
    assert.equal(response.status(), 200);
    return response.json();
  };
  const snapshot = async () => {
    const state = await api("/api/practice/export");
    return JSON.stringify({
      drafts: state.drafts
        .map((d) => [d.problemId, d.language, d.code, d.codeFormat])
        .sort(),
      attempts: state.attempts.map((a) => a.id).sort(),
      solved: state.solvedIds,
    });
  };
  const screenshot = async (name) => {
    const file = path.join(folder, name + ".png");
    await page.screenshot({ path: file });
    report.screenshots.push(path.relative(root, file));
  };
  try {
    const problems = await api("/api/problems");
    check(
      problems.length === 334 + ctciCount &&
        problems.filter((p) => p.collection === "interviewcake").length === 41,
      "the original coding bank and every registered CtCI exercise remain in Practice",
    );
    await page.goto(base + "/learn");
    await page.getByRole("heading", { name: "Learn", exact: true }).waitFor();
    check(
      (await page.locator(".learn-card").count()) === 12,
      "index contains exactly12 unique local article cards",
    );
    check(
      (await page
        .getByRole("navigation", { name: "Learn topics" })
        .getByRole("link")
        .count()) === 4,
      "only three populated categories plus All topics appear",
    );
    check(
      (await page
        .getByRole("option", { name: "Interview Cake", exact: true })
        .count()) === 0,
      "no invented Interview Cake article source",
    );
    await screenshot("learn-index-desktop");
    await page.getByRole("link", { name: /Trees & Graphs/ }).focus();
    await page.keyboard.press("Enter");
    await pauseUntil(
      async () => (await page.locator(".learn-card").count()) === 2,
      "keyboard topic selection",
    );
    check(
      new URL(page.url()).searchParams.get("topic") === "trees-graphs",
      "keyboard topic navigation updates canonical filter URL",
    );
    const inlineScripts = await page.locator("script:not([src])").count();
    await page.getByRole("searchbox").fill("no matching article <script>");
    await page.getByRole("heading", { name: "No matching articles" }).waitFor();
    check(
      (await page.locator("script:not([src])").count()) === inlineScripts,
      "search text renders safely",
    );
    await page.getByRole("link", { name: "Clear filters" }).click();
    await page.getByRole("searchbox").fill("Foundations");
    await pauseUntil(
      async () => (await page.locator(".learn-card").count()) === 4,
      "displayed topic search",
    );
    check(true, "search finds articles by their displayed topic name");
    await page.getByRole("searchbox").fill("");
    await page
      .getByRole("combobox", { name: "Source", exact: true })
      .selectOption("other");
    check(
      (await page.locator(".learn-card").count()) === 12,
      "actual source filter retains all matching articles",
    );
    await page.goBack();
    await pauseUntil(
      () => new URL(page.url()).searchParams.get("source") === null,
      "back restores source filter",
    );
    await page.goForward();
    await pauseUntil(
      () => new URL(page.url()).searchParams.get("source") === "other",
      "forward restores source filter",
    );
    check(true, "back and forward restore index filters");
    const untouched = await snapshot();
    for (const article of inventory.articles) {
      const response = await page.goto(base + "/learn/" + article.id);
      check(
        response.status() === 200,
        article.id + " deep link served locally",
      );
      await page
        .getByRole("heading", { name: article.title, exact: true })
        .waitFor();
      check(
        (await page
          .getByRole("navigation", { name: "On this page" })
          .getByRole("link")
          .count()) === 4,
        article.id + " four valid table-of-contents entries",
      );
      for (const href of await page
        .getByRole("navigation", { name: "On this page" })
        .getByRole("link")
        .evaluateAll((items) => items.map((item) => item.getAttribute("href"))))
        check(
          (await page.locator(href).count()) === 1,
          article.id + " ToC target " + href,
        );
      for (const target of article.relatedProblems) {
        await page
          .locator(
            '.learn-article-sidebar a[href="/practice?problem=' +
              target.id +
              '"]',
          )
          .waitFor();
        check(
          (await page
            .locator(
              '.learn-article-sidebar a[href="/practice?problem=' +
                target.id +
                '"]',
            )
            .count()) === 1,
          article.id + " verified related practice " + target.id,
        );
      }
      check(
        (await page
          .getByRole("tab", { name: "Solution", exact: true })
          .count()) === 0 &&
          (await page
            .getByRole("button", { name: "Submit", exact: true })
            .count()) === 0,
        article.id + " is reading rather than a fake runnable problem",
      );
      report.articles.push(article.id);
    }
    check(
      (await snapshot()) === untouched,
      "reading every article creates no drafts, attempts, or coding progress",
    );
    await page.goto(base + "/learn/reading-parent-pointer-lca");
    await page
      .getByRole("heading", { name: "LCA with parent pointers", exact: true })
      .waitFor();
    await page.locator(".learn-related").first().waitFor();
    await screenshot("learn-article-desktop");
    await page
      .getByRole("navigation", { name: "On this page" })
      .getByRole("link", { name: "Core idea" })
      .click();
    check(
      new URL(page.url()).hash === "#section-core-idea",
      "ToC anchors navigate to original article sections",
    );
    await page
      .getByRole("textbox", { name: "Your notes and design response" })
      .fill("Preserved Learn notes Ω 😀");
    await page.getByRole("button", { name: "Mark reviewed" }).click();
    await pauseUntil(
      async () =>
        (await api("/api/practice")).drafts.some(
          (d) =>
            d.problemId === "reading-parent-pointer-lca" &&
            JSON.parse(d.code).notes === "Preserved Learn notes Ω 😀" &&
            JSON.parse(d.code).reviewed,
        ),
      "reading saved",
    );
    await page.getByRole("link", { name: /Next article/ }).click();
    await page.getByRole("link", { name: /Previous article/ }).click();
    check(
      (await page
        .getByRole("textbox", { name: "Your notes and design response" })
        .inputValue()) === "Preserved Learn notes Ω 😀",
      "previous/next retain reading notes and review state",
    );
    await page
      .locator(
        '.learn-article-sidebar a[href="/practice?problem=lowest_common_ancestor"]',
      )
      .click();
    await page
      .locator(".coding-pane .monaco-editor textarea.inputarea")
      .waitFor();
    check(
      new URL(page.url()).searchParams.get("problem") ===
        "lowest_common_ancestor",
      "related practice opens actual local question",
    );
    const draft = "// Learn navigation draft Ω\npublic class Solution {}";
    const editor = page.locator(
      ".coding-pane .editor-container .monaco-editor",
    );
    await editor.click();
    await page.keyboard.press("Control+KeyA");
    await page.keyboard.insertText(draft);
    await pauseUntil(
      async () =>
        (await api("/api/practice")).drafts.some(
          (d) =>
            d.problemId === "lowest_common_ancestor" &&
            d.language === "csharp" &&
            d.code === draft,
        ),
      "coding draft saved",
    );
    await page.getByRole("tab", { name: "Solution", exact: true }).click();
    await page.getByLabel("C# reference solution code").waitFor();
    await page.getByRole("link", { name: "Learn", exact: true }).click();
    await page.getByRole("link", { name: "Practice", exact: true }).click();
    await page
      .locator(".coding-pane .monaco-editor textarea.inputarea")
      .waitFor();
    check(
      (await api("/api/practice")).drafts.some(
        (d) =>
          d.problemId === "lowest_common_ancestor" &&
          d.code === draft &&
          d.codeFormat === "callable-v1",
      ),
      "Learn/Practice and Solution navigation preserve exact coding draft and format",
    );
    await page.getByRole("tab", { name: "Problem", exact: true }).click();
    check(
      (await page
        .getByRole("navigation", { name: "Related reading" })
        .getByRole("link")
        .count()) === 2,
      "Practice only links to the two genuinely related local articles",
    );
    await page.evaluate(() =>
      localStorage.setItem(
        "epi:selected",
        JSON.stringify("reading-parent-pointer-lca"),
      ),
    );
    await page.goto(base + "/");
    await page.waitForURL("**/learn/reading-parent-pointer-lca");
    await pauseUntil(
      async () =>
        (await page
          .getByRole("textbox", { name: "Your notes and design response" })
          .inputValue()) === "Preserved Learn notes Ω 😀",
      "legacy reading notes hydration",
    );
    check(
      (await page
        .getByRole("textbox", { name: "Your notes and design response" })
        .inputValue()) === "Preserved Learn notes Ω 😀",
      "old root selection redirects without losing reading notes",
    );
    await page.goto(base + "/reading/reading-shared-state");
    await page.waitForURL("**/learn/reading-shared-state");
    check(
      (await page.getByRole("button", { name: "Step A (read)" }).count()) === 1,
      "legacy reading route redirects and simulator remains functional",
    );
    await page.getByRole("button", { name: "Step A (read)" }).click();
    check(
      (await page.getByRole("button", { name: "Step A (compute)" }).count()) ===
        1,
      "existing concurrency simulator still advances",
    );
    for (const route of [
      "/learn/missing",
      "/learn/%E0%A4%A",
      "/practice?problem=missing",
      "/practice/missing",
      "/unknown",
    ]) {
      await page.goto(base + route);
      await page.locator('.learn-empty[role="alert"]').waitFor();
      check(
        (await page.getByRole("link", { name: "Browse Learn" }).count()) === 1,
        "safe missing route " + route,
      );
    }
    const backup = await api("/api/practice/export");
    const beforeRestore = await snapshot();
    for (let i = 0; i < 2; i++) {
      const restored = await context.request.post(
        base + "/api/practice/import",
        { headers: { "X-EpiJudge-Client": "local-editor" }, data: backup },
      );
      assert.equal(restored.status(), 200);
    }
    check(
      (await snapshot()) === beforeRestore,
      "idempotent backup restoration retains reading and coding work",
    );
    await page.setViewportSize({ width: 390, height: 844 });
    for (const [route, name] of [
      ["/learn", "learn-index-mobile"],
      ["/learn/reading-parent-pointer-lca", "learn-article-mobile"],
    ]) {
      await page.goto(base + route);
      await page.locator("h1").waitFor();
      if (route !== "/learn") {
        await page.locator(".learn-related").first().waitFor();
        check(
          await page.evaluate(() => {
            const article = document.querySelector(
              ".learn-article-grid > .reading-pane",
            );
            const body = article.querySelector(".reading-body");
            const sidebar = document.querySelector(".learn-article-sidebar");
            return (
              article.getBoundingClientRect().bottom >=
                body.getBoundingClientRect().bottom - 1 &&
              sidebar.getBoundingClientRect().top >=
                article.getBoundingClientRect().bottom
            );
          }),
          "mobile article has natural height and no vertical overlap",
        );
      }
      await screenshot(name);
      check(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth + 1,
        ),
        "mobile no horizontal overflow " + route,
      );
    }
    await page.route("**/api/problems", (route) =>
      route.fulfill({ status: 503, body: "{}" }),
    );
    await page.goto(base + "/learn/reading-parent-pointer-lca");
    await page
      .getByRole("heading", { name: "Couldn’t load the library" })
      .waitFor();
    check(
      (await page
        .getByRole("heading", { name: "LCA with parent pointers", exact: true })
        .count()) === 1 && (await page.locator(".learn-related").count()) === 0,
      "local reading remains available on API failure without broken practice links",
    );
    check(
      report.pageErrors.length === 0 && report.externalRequests.length === 0,
      "zero page errors and no external asset requests",
    );
    report.passed = true;
  } catch (error) {
    report.error = String(error.stack ?? error);
    await page.screenshot({ path: path.join(folder, "failure.png") });
    throw error;
  } finally {
    fs.writeFileSync(
      path.join(root, ".epi-runs/learn-browser.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
