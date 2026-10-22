// Inspect the longest authored solution in each language at real desktop/mobile/200% zoom.
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const {
  chromium,
} = require("../../epijudge.client/node_modules/playwright-core");
const root = path.resolve(__dirname, "../..");
const base = process.argv[2];
if (!base) throw new Error("Pass an isolated local server URL.");
const output = path.join(root, ".epi-runs/clarity-layout");
fs.mkdirSync(output, { recursive: true });
const rows = JSON.parse(
  fs.readFileSync(path.join(root, "solutions/catalog.json")),
);
const languages = {
  csharp: "C#",
  javascript: "JavaScript",
  python: "Python",
  cpp: "C++",
  java: "Java",
};
const length = (r) =>
  [
    r.explanation,
    r.correctness,
    r.walkthrough,
    r.timeComplexity,
    r.spaceComplexity,
    ...r.edgeCases,
  ].join("").length;
const content = (r) =>
  [
    r.explanation,
    r.correctness,
    r.walkthrough,
    r.attribution,
    ...r.edgeCases,
  ].join(" ");
const tokenLength = (r) =>
  Math.max(
    ...content(r)
      .split(/\s+/)
      .map((token) => token.length),
  );
const samples = [
  ...new Map(
    Object.keys(languages)
      .flatMap((language) => {
        const selected = rows.filter((r) => r.language === language);
        return [
          selected.toSorted((a, b) => length(b) - length(a))[0],
          selected.toSorted((a, b) => tokenLength(b) - tokenLength(a))[0],
        ];
      })
      .map((row) => [row.language + "/" + row.problemId, row]),
  ).values(),
];
const report = { passed: false, checks: [], errors: [] };
const options = {
  headless: true,
  executablePath: process.env.CHROMIUM_PATH || "/usr/bin/chromium",
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
};
async function screenshot(page, filename) {
  const session = await page.context().newCDPSession(page);
  const capture = await session.send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  await session.detach();
  const buffer = Buffer.from(capture.data, "base64");
  const viewport = await page.evaluate(() => ({
    width: innerWidth,
    height: innerHeight,
    dpr: devicePixelRatio,
  }));
  assert(
    Math.abs(buffer.readUInt32BE(16) - viewport.width * viewport.dpr) <= 2,
  );
  assert(
    Math.abs(buffer.readUInt32BE(20) - viewport.height * viewport.dpr) <= 2,
  );
  fs.writeFileSync(filename, buffer);
}
(async () => {
  const browser = await chromium.launch(options);
  try {
    for (const profile of [
      { id: "desktop", width: 1440, height: 1000 },
      { id: "mobile", width: 320, height: 740 },
      { id: "zoom200", zoom: 2 },
    ]) {
      let context;
      if (profile.zoom) {
        const dir = fs.mkdtempSync(path.join(output, "zoom-profile-"));
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
      const page = await context.newPage();
      page.on("pageerror", (e) => report.errors.push(String(e)));
      for (const row of samples) {
        await page.goto(base + "/practice?problem=" + row.problemId);
        await page
          .getByRole("combobox", { name: "Select programming language" })
          .selectOption(row.language);
        const contract = page.locator(
          'section[aria-label$="callable contract"]',
        );
        await contract.waitFor();
        assert(
          (await contract.innerText()).includes("What your function must do"),
        );
        assert(
          (await page.locator(".solution-content").count()) === 0,
          "Contract must precede revealing solution",
        );
        await contract.scrollIntoViewIfNeeded();
        await screenshot(
          page,
          path.join(
            output,
            `${profile.id}-${row.language}-${row.problemId}-contract.png`,
          ),
        );
        await page.getByRole("tab", { name: "Solution", exact: true }).click();
        await page
          .getByLabel(languages[row.language] + " reference solution code")
          .waitFor();
        const text = await page.locator(".solution-content").innerText();
        for (const field of [
          "explanation",
          "correctness",
          "walkthrough",
          "timeComplexity",
          "spaceComplexity",
        ])
          assert(
            text.includes(row[field]),
            `${profile.id}/${row.language}: missing ${field}`,
          );
        for (const edge of row.edgeCases) assert(text.includes(edge));
        const cdp = await context.newCDPSession(page);
        const zoom = (await cdp.send("Page.getLayoutMetrics")).cssVisualViewport
          .zoom;
        assert(Math.abs(zoom - (profile.zoom || 1)) < 0.01);
        const overflow = await page.evaluate(() =>
          [
            document.documentElement,
            ...document.querySelectorAll(
              ".solution-content,.solution-explanation,.solution-complexity dd,.solution-edge-cases,.attribution",
            ),
          ]
            .filter((e) => e.scrollWidth > e.clientWidth + 2)
            .map((e) => ({
              tag: e.className || e.tagName,
              width: e.clientWidth,
              scroll: e.scrollWidth,
            })),
        );
        assert.deepEqual(
          overflow,
          [],
          `${profile.id}/${row.language}: clipped reading content`,
        );
        await page
          .locator(".solution-content")
          .evaluate((e) => (e.scrollTop = 0));
        await screenshot(
          page,
          path.join(
            output,
            `${profile.id}-${row.language}-${row.problemId}-approach.png`,
          ),
        );
        await page
          .locator("#solution-correctness-heading")
          .scrollIntoViewIfNeeded();
        await screenshot(
          page,
          path.join(
            output,
            `${profile.id}-${row.language}-${row.problemId}-proof.png`,
          ),
        );
        report.checks.push({
          profile: profile.id,
          language: row.language,
          problemId: row.problemId,
          characters: length(row),
          zoom,
        });
        console.log(
          "PASS " + profile.id + "/" + row.language + "/" + row.problemId,
        );
        await cdp.detach();
      }
      await context.close();
    }
    assert.deepEqual(report.errors, []);
    report.passed = true;
  } catch (e) {
    report.errors.push(String(e.stack || e));
    process.exitCode = 1;
  } finally {
    await browser.close();
    fs.writeFileSync(
      path.join(output, "report.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
  }
})();
