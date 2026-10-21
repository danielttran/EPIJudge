// Real Chromium layout acceptance: geometry, hit targets, focus and rendered evidence.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { chromium } = require("../epijudge.client/node_modules/playwright-core");
const base = process.argv[2];
if (!base) throw new Error("Pass an isolated local server URL.");
const root = path.resolve(__dirname, "..");
const folder = path.join(root, ".epi-runs/learn-layout");
fs.mkdirSync(folder, { recursive: true });
const profiles = [
  { id: "desktop", width: 1440, height: 1000 },
  { id: "tablet", width: 820, height: 1180 },
  { id: "phone320", width: 320, height: 740 },
  { id: "zoom200", width: 1440, height: 1000, zoom: 2 },
];
const report = {
  passed: false,
  profiles: [],
  states: [],
  checks: [],
  failures: [],
  pageErrors: [],
  externalRequests: [],
};
const browserOptions = {
  headless: true,
  ...(process.env.CHROMIUM_PATH
    ? { executablePath: process.env.CHROMIUM_PATH }
    : { channel: "chromium" }),
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
};
function check(ok, message, detail) {
  report.checks.push({ passed: Boolean(ok), message });
  if (!ok) {
    report.failures.push({ message, detail });
    console.log("FAIL layout " + message + " " + JSON.stringify(detail));
  }
}
async function until(predicate, message) {
  const deadline = Date.now() + 25000;
  while (Date.now() < deadline) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Timed out: " + message);
}
async function evidence(page, profile, state) {
  const file = path.join(folder, profile + "-" + state + ".png");
  // Capture the complete native surface. Playwright's CSS-sized clip crops
  // screenshots to the top-left quarter when Chromium has native 200% zoom.
  const session = await page.context().newCDPSession(page);
  const capture = await session.send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  await session.detach();
  const buffer = Buffer.from(capture.data, "base64");
  fs.writeFileSync(file, buffer);
  const viewport = await page.evaluate(() => ({
    width: innerWidth,
    height: innerHeight,
    dpr: devicePixelRatio,
  }));
  const pixels = {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20),
  };
  check(
    Math.abs(pixels.width - viewport.width * viewport.dpr) <= 2 &&
      Math.abs(pixels.height - viewport.height * viewport.dpr) <= 2,
    profile + "/" + state + ": screenshot covers the full native viewport",
    { pixels, viewport },
  );
  report.states.push({
    profile,
    state,
    pixels,
    viewport,
    screenshot: path.relative(root, file),
    sha256: crypto
      .createHash("sha256")
      .update(fs.readFileSync(file))
      .digest("hex"),
  });
}
async function top(page) {
  await page.evaluate(() => {
    window.scrollTo(0, 0);
    document.querySelector("main")?.scrollTo(0, 0);
  });
}
async function geometry(page, label) {
  const result = await page.evaluate(() => {
    const visible = (element) => {
      const style = getComputedStyle(element),
        r = element.getBoundingClientRect();
      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        r.width > 0 &&
        r.height > 0
      );
    };
    const findings = [];
    const main = document.querySelector("main");
    if (document.documentElement.scrollWidth > innerWidth + 1)
      findings.push([
        "page horizontal overflow",
        document.documentElement.scrollWidth,
        innerWidth,
      ]);
    if (main && main.scrollWidth > main.clientWidth + 1)
      findings.push([
        "main horizontal overflow",
        main.scrollWidth,
        main.clientWidth,
      ]);
    for (const element of document.querySelectorAll(
      ".learn-card h3, .learn-card-source, .learn-breadcrumb, .learn-related strong, .learn-pagination a, .learn-intro h1, .learn-article-grid h1, .learn-article-grid h2, .solution-code-heading h2, .section-navigation, .pane-heading, .topbar-actions",
    )) {
      if (!visible(element)) continue;
      const r = element.getBoundingClientRect(),
        style = getComputedStyle(element);
      if (r.left < -1 || r.right > innerWidth + 1)
        findings.push([
          "text/control outside viewport",
          element.className || element.tagName,
          r.left,
          r.right,
        ]);
      if (element.scrollWidth > element.clientWidth + 2)
        findings.push(["clipped text", element.textContent.slice(0, 80)]);
      const card = element.closest(".learn-card");
      if (card && r.right > card.getBoundingClientRect().right + 1)
        findings.push(["text escapes card", element.textContent.slice(0, 80)]);
    }
    const article = document.querySelector(
      ".learn-article-grid > .reading-pane",
    );
    const aside = document.querySelector(".learn-article-sidebar");
    if (article && aside) {
      const a = article.getBoundingClientRect(),
        b = aside.getBoundingClientRect(),
        body = article.querySelector(".reading-body").getBoundingClientRect();
      if (a.bottom < body.bottom - 1)
        findings.push(["article text escapes panel", a.bottom, body.bottom]);
      if (matchMedia("(max-width: 800px)").matches) {
        if (b.top < a.bottom - 1)
          findings.push(["stacked sidebar overlaps article", a.bottom, b.top]);
      } else if (a.right > b.left + 1)
        findings.push(["sidebar overlaps article column", a.right, b.left]);
    }
    const header = document.querySelector(".topbar");
    if (header) {
      const groups = [...header.children].filter(visible);
      for (let i = 0; i < groups.length; i++)
        for (let j = i + 1; j < groups.length; j++) {
          const a = groups[i].getBoundingClientRect(),
            b = groups[j].getBoundingClientRect();
          if (
            Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 &&
            Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2
          )
            findings.push([
              "header groups overlap",
              groups[i].className,
              groups[j].className,
            ]);
        }
    }
    const editor = document.querySelector(
      ".coding-pane .editor-container .monaco-editor",
    );
    if (editor) {
      const r = editor.getBoundingClientRect();
      const renderedCode = [
        ...editor.querySelectorAll(".view-lines .view-line"),
      ]
        .map((line) => line.textContent)
        .join("")
        .trim();
      if (r.height < 120 || r.width < 100 || !renderedCode)
        findings.push([
          "main code editor collapsed or has no rendered code",
          r.width,
          r.height,
          renderedCode,
        ]);
    }
    return findings;
  });
  check(
    result.length === 0,
    label + ": no unintended overlap, clipping or page overflow",
    result,
  );
}
async function hitTargets(page, label) {
  const modal = page.locator("dialog[open]");
  const container = (await modal.count()) ? modal : page.locator("body");
  const controls = container
    .locator("a[href], button, input, select, textarea, summary")
    .filter({ visible: true });
  let tested = 0;
  for (let i = 0; i < (await controls.count()); i++) {
    const control = controls.nth(i);
    if (
      (await control.isDisabled()) ||
      (await control.evaluate((element) =>
        Boolean(element.closest(".monaco-editor")),
      ))
    )
      continue;
    await control.scrollIntoViewIfNeeded();
    const finding = await control.evaluate((element) => {
      const r = element.getBoundingClientRect();
      const x = Math.max(0, Math.min(innerWidth - 1, r.left + r.width / 2));
      const y = Math.max(0, Math.min(innerHeight - 1, r.top + r.height / 2));
      const hit = document.elementFromPoint(x, y);
      return {
        okay: Boolean(hit && (element === hit || element.contains(hit))),
        label:
          element.getAttribute("aria-label") ||
          element.textContent.trim().slice(0, 60) ||
          element.tagName,
        hit: hit?.tagName + "." + hit?.className,
      };
    });
    tested++;
    check(
      finding.okay,
      label + ": reachable hit target " + finding.label,
      finding,
    );
  }
  check(tested > 0, label + ": interactive targets inspected", { tested });
}
async function keyboard(page, label) {
  const modal = page.locator("dialog[open]");
  if (await modal.count()) {
    await modal.getByRole("button").first().focus();
    for (let i = 0; i < 8; i++) await page.keyboard.press("Tab");
    check(
      await modal.evaluate((element) =>
        element.contains(document.activeElement),
      ),
      label + ": keyboard focus remains inside modal",
    );
    return;
  }
  const target = page.getByRole("link", { name: "Learn", exact: true }).first();
  await target.focus();
  for (let i = 0; i < 8; i++) await page.keyboard.press("Tab");
  const focus = await page.evaluate(() => {
    const element = document.activeElement,
      editor = element.closest(".monaco-editor"),
      r = (editor ?? element).getBoundingClientRect(),
      style = getComputedStyle(element);
    let left = Math.max(0, r.left),
      right = Math.min(innerWidth, r.right),
      top = Math.max(0, r.top),
      bottom = Math.min(innerHeight, r.bottom);
    if (editor)
      for (
        let parent = editor.parentElement;
        parent;
        parent = parent.parentElement
      ) {
        const box = parent.getBoundingClientRect(),
          clipping = getComputedStyle(parent);
        if (clipping.overflowX !== "visible") {
          left = Math.max(left, box.left);
          right = Math.min(right, box.right);
        }
        if (clipping.overflowY !== "visible") {
          top = Math.max(top, box.top);
          bottom = Math.min(bottom, box.bottom);
        }
      }
    const hit = document.elementFromPoint(
      (left + right) / 2,
      (top + bottom) / 2,
    );
    return {
      tag: element.tagName,
      text:
        element.getAttribute("aria-label") || element.textContent.slice(0, 50),
      visible: editor
        ? right - left >= 24 && bottom - top >= 24
        : r.width > 0 &&
          r.height > 0 &&
          r.top >= -1 &&
          r.bottom <= innerHeight + 1,
      focusIndicator:
        style.outlineStyle !== "none" || style.boxShadow !== "none",
      hit: Boolean(
        hit &&
          ((editor ?? element) === hit || (editor ?? element).contains(hit)),
      ),
      virtualEditorInput: Boolean(editor),
    };
  });
  check(
    focus.tag !== "BODY" &&
      focus.visible &&
      focus.hit &&
      (focus.focusIndicator || focus.virtualEditorInput),
    label + ": keyboard focus scrolls into reach",
    focus,
  );
  if (await page.locator(".learn-index, .learn-article-page").count()) {
    const expected = await page.evaluate(() => {
      const elements = [
        ...document.querySelectorAll(
          "a[href], button, input, select, textarea, summary",
        ),
      ].filter((element) => {
        const r = element.getBoundingClientRect(),
          style = getComputedStyle(element);
        if (
          !r.width ||
          !r.height ||
          style.visibility === "hidden" ||
          element.matches(":disabled")
        )
          return false;
        if (element.matches('input[type="radio"]')) {
          const group = [
            ...document.querySelectorAll('input[type="radio"]'),
          ].filter((radio) => radio.name === element.name);
          return element === (group.find((radio) => radio.checked) ?? group[0]);
        }
        return true;
      });
      elements.forEach((element, index) =>
        element.setAttribute("data-layout-focus-id", String(index)),
      );
      return elements.map((element) => ({
        id: element.getAttribute("data-layout-focus-id"),
        text:
          element.getAttribute("aria-label") ||
          element.textContent.trim().slice(0, 60) ||
          element.tagName,
      }));
    });
    await target.focus();
    const visited = new Set();
    for (let i = 0; i < expected.length + 3; i++) {
      const id = await page.evaluate(() =>
        document.activeElement.getAttribute("data-layout-focus-id"),
      );
      if (id !== null) visited.add(id);
      await page.keyboard.press("Tab");
    }
    const missing = expected.filter((element) => !visited.has(element.id));
    check(
      !missing.length,
      label + ": all reading controls reached in sequential Tab traversal",
      { missing, expected: expected.length, reached: visited.size },
    );
  }
}
(async () => {
  let browser;
  try {
    browser = await chromium.launch(browserOptions);
    for (const profile of profiles) {
      let context;
      if (profile.zoom) {
        const directory = fs.mkdtempSync(path.join(folder, "zoom-profile-"));
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
          ...browserOptions,
          viewport: null,
          args: [...browserOptions.args, "--window-size=1440,1000"],
        });
      } else
        context = await browser.newContext({
          viewport: { width: profile.width, height: profile.height },
        });
      const page = await context.newPage();
      page.on("pageerror", (error) =>
        report.pageErrors.push({ profile: profile.id, error: String(error) }),
      );
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
      const go = async (href) => {
        await page.goto(base + href);
        await page.locator("h1").first().waitFor();
      };
      const inspect = async (name, { hits = true, focusSelector } = {}) => {
        await top(page);
        if (focusSelector)
          await page.locator(focusSelector).first().scrollIntoViewIfNeeded();
        await geometry(page, profile.id + "/" + name);
        await evidence(page, profile.id, name);
        if (hits) await hitTargets(page, profile.id + "/" + name);
        await keyboard(page, profile.id + "/" + name);
      };
      let releaseLoading;
      try {
        await go("/learn");
        const session = await context.newCDPSession(page);
        const zoom = (await session.send("Page.getLayoutMetrics"))
          .cssVisualViewport.zoom;
        const metrics = await page.evaluate(() => ({
          width: innerWidth,
          height: innerHeight,
          dpr: devicePixelRatio,
          outerWidth,
          outerHeight,
        }));
        report.profiles.push({
          ...profile,
          measured: metrics,
          nativeZoom: zoom,
        });
        check(
          Math.abs(zoom - (profile.zoom ?? 1)) < 0.01,
          profile.id + ": verified native browser zoom",
          { zoom, metrics },
        );
        await inspect("index");
        await page
          .getByRole("searchbox")
          .fill("no matching layout query <long search>");
        await page
          .getByRole("heading", { name: "No matching articles" })
          .waitFor();
        await inspect("empty-search", { focusSelector: ".learn-empty" });
        await go("/learn");
        await page
          .locator(".learn-card h3")
          .first()
          .evaluate(
            (element) =>
              (element.textContent =
                "A deliberately long article title with useful normal wrapping and anUnbrokenTokenThatStillMustRemainReadableWithoutClippingOrCoveringControls"),
          );
        await inspect("long-card-title", {
          focusSelector: ".learn-card:first-child",
        });
        await go("/learn/reading-normalization");
        await inspect("article-long-title");
        await page
          .locator(".learn-article-grid h1")
          .evaluate(
            (element) =>
              (element.textContent =
                "A longer technical article heading with anUnbrokenIdentifierThatNeedsToWrapWithoutOverflowAtNarrowWidths"),
          );
        await page
          .locator('.learn-breadcrumb [aria-current="page"]')
          .evaluate(
            (element) =>
              (element.textContent =
                "AnUnbrokenBreadcrumbTitleThatMustNotStretchTheArticlePageBeyondItsViewport"),
          );
        await inspect("article-title-stress");
        await go("/learn/reading-shared-state");
        await page.getByText("Need a starting point?").click();
        await page.getByRole("button", { name: "Step A (read)" }).click();
        await page.locator("fieldset").waitFor();
        await until(
          async () => !(await page.locator("fieldset").isDisabled()),
          "reading readiness",
        );
        await page.getByRole("radio").first().check();
        await inspect("article-expanded", {
          focusSelector: ".reading-interaction",
        });
        await page
          .locator(".reading-body details[open]")
          .scrollIntoViewIfNeeded();
        await geometry(page, profile.id + "/expanded-scroll");
        await evidence(page, profile.id, "expanded-scroll");
        await page
          .getByRole("link", { name: "Your notes & checkpoints" })
          .click();
        await page
          .getByRole("textbox", { name: "Your notes and design response" })
          .focus();
        check(
          await page
            .getByRole("textbox", { name: "Your notes and design response" })
            .evaluate((element) => {
              const r = element.getBoundingClientRect();
              return r.top >= 0 && r.top < innerHeight;
            }),
          profile.id + ": notes reachable by keyboard/anchor",
        );
        await evidence(page, profile.id, "notes-focus");
        const loadingGate = new Promise((resolve) => {
          releaseLoading = resolve;
        });
        await page.route("**/api/problems", async (route) => {
          await loadingGate;
          await route.continue();
        });
        await go("/learn/reading-parent-pointer-lca");
        await page.getByText("Loading local practice…").waitFor();
        await inspect("article-loading", {
          hits: false,
          focusSelector: ".learn-article-sidebar",
        });
        releaseLoading();
        await page.locator(".learn-related").first().waitFor();
        await page.unroute("**/api/problems");
        await page.route("**/api/problems", (route) =>
          route.fulfill({ status: 503, body: "{}" }),
        );
        await go("/learn/reading-parent-pointer-lca");
        await page
          .getByRole("heading", { name: "Couldn’t load the library" })
          .waitFor();
        await inspect("article-error", { focusSelector: ".page-error" });
        await page.unroute("**/api/problems");
        await go("/learn/missing");
        await inspect("missing-article");
        await go("/practice?problem=lowest_common_ancestor");
        await page.locator(".coding-pane .monaco-editor").waitFor();
        await until(
          async () =>
            await page
              .getByRole("button", { name: /^Run(?:\s|$)/ })
              .isEnabled(),
          "Practice ready",
        );
        await inspect("practice-problem");
        await page
          .locator(".coding-pane .provided-code-reference > summary")
          .click();
        await page
          .locator(".coding-pane .provided-reference-code .monaco-editor")
          .first()
          .waitFor();
        await inspect("practice-helper-expanded", {
          focusSelector: ".coding-pane .provided-code-reference",
        });
        await page
          .getByRole("button", { name: "History", exact: true })
          .click();
        await page
          .locator(".results-panel:not(.collapsed) .results-body")
          .waitFor();
        await inspect("practice-history-expanded", {
          focusSelector: ".results-panel",
        });
        await page.getByRole("button", { name: "Collapse results" }).click();
        await page
          .locator(".coding-pane .provided-code-reference > summary")
          .click();
        await page.getByRole("tab", { name: "Solution", exact: true }).click();
        await page
          .getByRole("combobox", { name: "Select programming language" })
          .selectOption("javascript");
        await page.getByLabel("JavaScript reference solution code").waitFor();
        await inspect("practice-solution", {
          focusSelector: ".solution-code-heading",
        });
        await page.getByRole("button", { name: "Toggle problem list" }).click();
        await page.getByRole("dialog", { name: "Problem library" }).waitFor();
        await page
          .getByRole("textbox", { name: "Search problems" })
          .fill("a very long search with no matching local problems");
        await inspect("practice-library");
        await page.getByRole("button", { name: "Close problem list" }).click();
      } catch (error) {
        report.failures.push({
          profile: profile.id,
          error: String(error.stack ?? error),
        });
        await evidence(page, profile.id, "unexpected-error");
      } finally {
        releaseLoading?.();
        await page.unrouteAll({ behavior: "wait" });
        await context.close();
        console.log(
          "Completed layout profile " +
            profile.id +
            ": " +
            report.states.filter((state) => state.profile === profile.id)
              .length +
            " states; " +
            report.failures.length +
            " cumulative failures",
        );
      }
    }
    check(
      report.pageErrors.length === 0 && report.externalRequests.length === 0,
      "no page errors or external assets",
      { errors: report.pageErrors, external: report.externalRequests },
    );
    report.passed = report.failures.length === 0;
  } finally {
    fs.writeFileSync(
      path.join(root, ".epi-runs/learn-layout.json"),
      JSON.stringify(report, null, 2) + "\n",
    );
    if (browser) await browser.close();
  }
  console.log(
    JSON.stringify(
      {
        passed: report.passed,
        profiles: report.profiles,
        states: report.states.length,
        checks: report.checks.length,
        failures: report.failures.length,
      },
      null,
      2,
    ),
  );
  if (!report.passed) process.exitCode = 1;
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
