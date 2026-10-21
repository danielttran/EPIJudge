// Actual Chromium/Monaco acceptance for clean callable code and legacy drafts.
const fs = require("node:fs");
const scriptSource = fs.readFileSync(__filename, "utf8");
const path = require("node:path");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const { chromium } = require("../../epijudge.client/node_modules/playwright-core");

const root = path.resolve(__dirname, "../..");
const base = process.argv[2];
if (!base) throw new Error("Pass the isolated local server URL.");
const artifacts = path.join(root, ".epi-runs");
const screenshots = path.join(artifacts, "code-cleanup-after");
fs.mkdirSync(screenshots, { recursive: true });
const catalogSource = fs.readFileSync(path.join(root, "workspace-code/catalog.json"), "utf8");
const entries = JSON.parse(catalogSource).entries;
const byScope = new Map(entries.map((entry) => [entry.problemId + ":" + entry.language, entry]));
const languages = ["csharp", "javascript", "python", "cpp", "java"];
const languageNames = {
  csharp: "C#",
  javascript: "JavaScript",
  python: "Python",
  cpp: "C++",
  java: "Java",
};
const subjects = {
  simple: "interviewcake_stock-price",
  tree: "interviewcake_balanced-binary-tree",
  list: "interviewcake_delete-node",
  graph: "interviewcake_graph-coloring",
  stateful: "interviewcake_temperature-tracker",
  filesystem: "interviewcake_find-duplicate-files",
  random: "interviewcake_simulate-5-sided-die",
  geometry: "interviewcake_rectangular-love",
};
const checks = [];
const external = [];
const pageErrors = [];
const requests = [];
const report = { passed: false, checks, views: [], externalRequests: external, pageErrors };
const sha = (text) => crypto.createHash("sha256").update(text).digest("hex");
const escape = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const normalizeEol = (text) => text.replace(/\r\n/g, "\n");
function pass(label) {
  checks.push(label);
  console.log("PASS callable browser " + label);
}
async function until(predicate, label) {
  const deadline = Date.now() + 25000;
  while (Date.now() < deadline) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Timed out: " + label);
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}),
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    permissions: ["clipboard-read", "clipboard-write"],
    acceptDownloads: true,
  });
  const page = await context.newPage();
  page.on("pageerror", (error) => pageErrors.push(String(error)));
  page.on("request", (request) => requests.push({ url: request.url(), method: request.method() }));
  await context.route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (["http:", "https:"].includes(url.protocol) && url.origin !== new URL(base).origin) {
      external.push(url.href);
      return route.abort();
    }
    return route.continue();
  });
  const language = page.getByRole("combobox", { name: "Select programming language" });
  const format = page.getByRole("combobox", { name: "Code format", exact: true });
  const problemTab = page.getByRole("tab", { name: "Problem", exact: true });
  const solutionTab = page.getByRole("tab", { name: "Solution", exact: true });
  const mainEditor = page.locator(".coding-pane .editor-container .monaco-editor");
  const mainInput = mainEditor.locator("textarea.inputarea");
  const solutionCode = page.locator(".solution-code");
  const writes = () =>
    requests.filter((request) => ["PUT", "POST", "PATCH", "DELETE"].includes(request.method))
      .length;
  async function api(endpoint, method = "GET", body) {
    const response = await page.request.fetch(base + endpoint, {
      method,
      headers: { "Content-Type": "application/json", "X-EpiJudge-Client": "local-editor" },
      ...(body === undefined ? {} : { data: body }),
    });
    assert.equal(response.status(), 200, method + " " + endpoint);
    return response.json();
  }
  const exportState = () => api("/api/practice/export");
  async function copiedEditor() {
    await mainInput.focus();
    await page.keyboard.press("Control+A");
    await page.keyboard.press("Control+C");
    const text = await page.evaluate(() => navigator.clipboard.readText());
    await page.keyboard.press("Control+Home");
    return text;
  }
  async function assertEditor(expected, expectedFormat = "callable-v1") {
    await until(
      async () =>
        (await mainEditor.count()) === 1 &&
        (await format.inputValue()) === expectedFormat &&
        normalizeEol(await copiedEditor()) === normalizeEol(expected),
      "exact editor code and format",
    );
  }
  async function select(problem, selectedLanguage) {
    await page.getByRole("button", { name: "Toggle problem list" }).click();
    await page
      .getByRole("combobox", { name: "Filter by topic or study plan" })
      .selectOption("collection:" + problem.collection);
    await page
      .getByRole("button", { name: new RegExp("\\. " + escape(problem.title) + " —") })
      .click();
    await problemTab.click();
    await language.selectOption(selectedLanguage);
  }
  async function checkReferences(container, expected, screenshotPrefix) {
    const details = container.locator(".provided-code-reference");
    assert.equal(await details.count(), expected.references.length ? 1 : 0);
    if (!expected.references.length) return;
    assert.equal(
      await details.getAttribute("open"),
      null,
      "references begin collapsed after selection",
    );
    await details.locator("summary").click();
    for (const reference of expected.references) {
      await details.getByRole("heading", { name: reference.title, exact: true }).waitFor();
      const input = details.getByRole("textbox", {
        name: reference.title + " provided reference",
        exact: true,
      });
      await input.waitFor();
      assert.equal(await input.evaluate((element) => element.readOnly), true);
    }
    assert.equal(await details.locator("textarea.inputarea").count(), expected.references.length);
    if (screenshotPrefix) {
      await page.screenshot({
        path: path.join(screenshots, screenshotPrefix + "-references.png"),
        fullPage: true,
      });
    }
    await details.locator("summary").click();
  }
  async function assertSolution(problem, expected) {
    await solutionTab.click();
    await page.getByRole("heading", { name: problem.title + " — Solution", exact: true }).waitFor();
    await until(
      async () =>
        (await solutionCode.locator("textarea.inputarea").count()) === 1 &&
        (await solutionCode.locator("textarea.inputarea").getAttribute("aria-label")) ===
          languageNames[expected.language] + " reference solution code",
      "selected-language solution model",
    );
    assert.equal(
      await solutionCode.locator("textarea.inputarea").evaluate((element) => element.readOnly),
      true,
    );
    await page.getByRole("button", { name: "Copy code", exact: true }).click();
    await page.getByText("Code copied.", { exact: true }).waitFor();
    assert.equal(await page.evaluate(() => navigator.clipboard.readText()), expected.solutionCode);
    assert.equal(await format.inputValue(), "callable-v1");
  }
  async function waitDraft(problemId, selectedLanguage, code, codeFormat) {
    await until(
      async () =>
        (await exportState()).drafts.some(
          (draft) =>
            draft.problemId === problemId &&
            draft.language === selectedLanguage &&
            draft.code === code &&
            draft.codeFormat === codeFormat,
        ),
      "saved draft " + problemId + "/" + selectedLanguage + "/" + codeFormat,
    );
  }
  try {
    const problems = await api("/api/problems");
    const byId = new Map(problems.map((problem) => [problem.id, problem]));
    const untouchedLegacy = "// browser unchanged legacy Ω\r\nmodule.exports = {};\r\n";
    await api("/api/practice/drafts/parity/javascript", "PUT", {
      code: untouchedLegacy,
      revision: 0,
    });
    const legacyDraft = (await exportState()).drafts.find(
      (draft) => draft.problemId === "count_bits" && draft.language === "javascript",
    );
    assert.ok(
      legacyDraft && legacyDraft.codeFormat === "legacy-v1",
      "HTTP setup provides old source",
    );
    await page.goto(base, { waitUntil: "networkidle" });
    await language.waitFor();
    await select(byId.get("count_bits"), "javascript");
    await assertEditor(legacyDraft.code, "legacy-v1");
    const mixedBefore = await exportState();
    const beforeWrites = writes();
    const legacySolution = byScope.get("count_bits:javascript");
    await solutionTab.click();
    await page.getByRole("button", { name: "Copy code", exact: true }).click();
    await page.getByText("Code copied.", { exact: true }).waitFor();
    assert.equal(
      await page.evaluate(() => navigator.clipboard.readText()),
      legacySolution.solutionCode,
    );
    await problemTab.click();
    await assertEditor(legacyDraft.code, "legacy-v1");
    assert.deepEqual(await exportState(), mixedBefore);
    assert.equal(writes(), beforeWrites);
    pass("viewing/copying clean solutions preserves old CRLF/Unicode drafts and legacy format");

    for (const [category, problemId] of Object.entries(subjects)) {
      const problem = byId.get(problemId);
      for (const selectedLanguage of languages) {
        const expected = byScope.get(problemId + ":" + selectedLanguage);
        await select(problem, selectedLanguage);
        await assertEditor(expected.starterCode);
        const prefix =
          category === "simple"
            ? "apple-stocks-" + selectedLanguage
            : category + "-" + selectedLanguage;
        await checkReferences(
          page.locator(".coding-pane"),
          expected,
          selectedLanguage === "csharp" && expected.references.length ? prefix + "-starter" : null,
        );
        const starterPath = path.join(screenshots, prefix + "-starter-after.png");
        await page.screenshot({ path: starterPath, fullPage: true });
        report.views.push({
          problemId,
          language: selectedLanguage,
          category,
          role: "starter",
          codeSha256: sha(expected.starterCode),
          references: expected.references.map((reference) => reference.names).flat(),
          screenshot: starterPath,
        });
        await assertSolution(problem, expected);
        await checkReferences(
          page.getByRole("tabpanel", { name: "Solution", exact: true }),
          expected,
          selectedLanguage === "csharp" && expected.references.length ? prefix + "-solution" : null,
        );
        const solutionPath = path.join(screenshots, prefix + "-solution-after.png");
        await page.screenshot({ path: solutionPath, fullPage: true });
        report.views.push({
          problemId,
          language: selectedLanguage,
          category,
          role: "solution",
          codeSha256: sha(expected.solutionCode),
          references: expected.references.map((reference) => reference.names).flat(),
          screenshot: solutionPath,
        });
        await problemTab.click();
        await assertEditor(expected.starterCode);
      }
      pass(
        category +
          " starter and solution render cleanly in all five languages with exact copied source",
      );
    }
    assert.equal(report.views.length, 80);
    assert.deepEqual(await exportState(), mixedBefore);
    assert.equal(writes(), beforeWrites);
    pass(
      "all 80 representative views are read-only with respect to drafts/history and preserve selection formats",
    );

    const apple = byId.get(subjects.simple);
    await select(apple, "javascript");
    const draftText =
      "// browser callable draft preserved Δ\n" +
      byScope.get(subjects.simple + ":javascript").starterCode;
    await mainInput.focus();
    await page.keyboard.press("Control+A");
    await page.evaluate((text) => navigator.clipboard.writeText(text), draftText);
    await page.keyboard.press("Control+V");
    await waitDraft(apple.id, "javascript", draftText, "callable-v1");
    await language.selectOption("python");
    await assertEditor(byScope.get(apple.id + ":python").starterCode);
    await language.selectOption("javascript");
    await assertEditor(draftText);
    await page.reload({ waitUntil: "networkidle" });
    await assertEditor(draftText);
    pass("new callable draft and its format survive language switching and reload");

    const beforeFormat = (await exportState()).drafts.find(
      (draft) => draft.problemId === apple.id && draft.language === "javascript",
    );
    await format.selectOption("legacy-v1");
    await waitDraft(apple.id, "javascript", draftText, "legacy-v1");
    const afterFormat = (await exportState()).drafts.find(
      (draft) => draft.problemId === apple.id && draft.language === "javascript",
    );
    assert.ok(afterFormat.revision > beforeFormat.revision);
    await format.selectOption("callable-v1");
    await waitDraft(apple.id, "javascript", draftText, "callable-v1");
    pass("explicit compatibility choice changes only format and autosaves a distinct revision");

    const legacyProgram = fs.readFileSync(
      path.join(root, "solutions/javascript/" + apple.id + ".js"),
      "utf8",
    );
    const acceptedLegacy = await api("/api/submissions", "POST", {
      problemId: apple.id,
      language: "javascript",
      code: legacyProgram,
      mode: "run",
    });
    const acceptedCallable = await api("/api/submissions", "POST", {
      problemId: apple.id,
      language: "javascript",
      code: byScope.get(apple.id + ":javascript").solutionCode,
      mode: "run",
      codeFormat: "callable-v1",
    });
    assert.equal(acceptedLegacy.status, "Accepted");
    assert.equal(acceptedCallable.status, "Accepted");
    await page.reload({ waitUntil: "networkidle" });
    await page.getByRole("button", { name: "History", exact: true }).click();
    await page.getByRole("button", { name: "View answer", exact: true }).first().click();
    await page.getByRole("button", { name: "Restore to editor", exact: true }).click();
    await waitDraft(
      apple.id,
      "javascript",
      byScope.get(apple.id + ":javascript").solutionCode,
      "callable-v1",
    );
    await assertEditor(byScope.get(apple.id + ":javascript").solutionCode);
    await page.getByRole("button", { name: "View answer", exact: true }).nth(1).click();
    await page.getByRole("button", { name: "Restore to editor", exact: true }).click();
    await waitDraft(apple.id, "javascript", legacyProgram, "legacy-v1");
    await assertEditor(legacyProgram, "legacy-v1");
    pass("history restoration retains the exact callable or legacy source format");

    await select(byId.get("count_bits"), "javascript");
    await assertEditor(legacyDraft.code, "legacy-v1");
    page.once("dialog", (dialog) => dialog.accept());
    await page.getByRole("button", { name: "Reset to starter code", exact: true }).click();
    await waitDraft(
      "count_bits",
      "javascript",
      byScope.get("count_bits:javascript").starterCode,
      "callable-v1",
    );
    await assertEditor(byScope.get("count_bits:javascript").starterCode);
    assert.ok(
      (await exportState()).drafts.some(
        (draft) =>
          draft.problemId === "parity" &&
          draft.language === "javascript" &&
          draft.code === untouchedLegacy &&
          draft.codeFormat === "legacy-v1",
      ),
    );
    pass(
      "explicit reset adopts the clean callable starter while unrelated old drafts remain byte-preserved",
    );

    await select(byId.get(subjects.tree), "csharp");
    const selectedTree = byScope.get(subjects.tree + ":csharp");
    const solutionUrl = base + "/api/problems/" + subjects.tree + "/solution?language=csharp";
    await context.route(solutionUrl, (route) =>
      route.fulfill({
        status: 503,
        contentType: "application/json",
        body: '{"message":"unavailable"}',
      }),
    );
    const beforeFailure = await exportState();
    await solutionTab.click();
    await page
      .getByRole("tabpanel", { name: "Solution", exact: true })
      .getByRole("alert")
      .waitFor();
    await context.unroute(solutionUrl);
    await page.getByRole("button", { name: "Retry solution", exact: true }).click();
    await assertSolution(byId.get(subjects.tree), selectedTree);
    await problemTab.click();
    await assertEditor(selectedTree.starterCode);
    assert.deepEqual(await exportState(), beforeFailure);
    pass(
      "solution loading failure/retry cannot replace code or silently fall back to a full program",
    );

    const localDiagrams = problems
      .filter((problem) => problem.diagram)
      .map((problem) => problem.diagram);
    await page.evaluate(async (diagrams) => {
      for (const source of diagrams) {
        const image = new Image();
        image.src = source;
        await image.decode();
        if (!image.naturalWidth) throw new Error("Empty local diagram " + source);
      }
    }, localDiagrams);
    assert.equal(localDiagrams.length, 38);
    pass("all 38 local diagrams decode with external origins blocked");

    await page.setViewportSize({ width: 430, height: 900 });
    await solutionTab.click();
    await page
      .getByRole("heading", { name: byId.get(subjects.tree).title + " — Solution", exact: true })
      .waitFor();
    assert.ok(
      await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1),
    );
    const mobilePath = path.join(screenshots, "tree-csharp-mobile-after.png");
    await page.screenshot({ path: mobilePath, fullPage: true });
    assert.equal(await solutionTab.getAttribute("aria-selected"), "true");
    await page.setViewportSize({ width: 1440, height: 1000 });
    pass("clean solution and code-format controls fit a narrow viewport without page overflow");

    const backupBefore = await exportState();
    await page.getByRole("button", { name: "Toggle problem list" }).click();
    const download = page.waitForEvent("download");
    await page.getByRole("button", { name: "Export answers", exact: true }).click();
    const downloaded = await download;
    const backup = JSON.parse(fs.readFileSync(await downloaded.path(), "utf8"));
    assert.equal(backup.version, 2);
    assert.deepEqual(backup, backupBefore);
    assert.ok(backup.drafts.some((draft) => draft.codeFormat === "legacy-v1"));
    assert.ok(backup.drafts.some((draft) => draft.codeFormat === "callable-v1"));
    await page.getByLabel("Import answers file").setInputFiles({
      name: "mixed-callable-legacy.json",
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify(backup)),
    });
    await until(
      async () => /Imported answers/.test(await page.locator("dialog").innerText()),
      "mixed backup import",
    );
    const afterImport = await exportState();
    const preserved = (state) =>
      state.drafts
        .map((draft) => [draft.problemId, draft.language, draft.code, draft.codeFormat])
        .sort();
    assert.deepEqual(preserved(afterImport), preserved(backupBefore));
    assert.deepEqual(afterImport.attempts, backupBefore.attempts);
    pass("real UI export/import round-trips mixed legacy/callable source without duplication");
    assert.deepEqual(external, []);
    assert.deepEqual(pageErrors, []);
    report.passed = true;
  } catch (error) {
    report.error = String(error.stack || error);
    await page
      .screenshot({ path: path.join(screenshots, "failure.png"), fullPage: true })
      .catch(() => {});
    throw error;
  } finally {
    report.scriptSha256 = sha(scriptSource);
    report.catalogSha256 = sha(catalogSource);
    fs.writeFileSync(
      path.join(artifacts, "callable-browser.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
