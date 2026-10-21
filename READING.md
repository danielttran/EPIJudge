# Learn

The top navigation separates **Learn** from **Practice**. Learn contains all twelve
local companions: four concurrency articles in Foundations, two in Trees & Graphs,
and six in System Design. Empty categories are hidden. Search includes article
titles, summaries, topics, and body text; source and topic filters compose in the URL.
All available readings are original EPI study companions. No Interview Cake article
bodies are stored here; its 41 coding tasks stay in Practice. External further-reading
references are links rather than imported articles. These are original
study notes and prompts, not copied EPI chapters or a certified edition inventory.

The article page includes a breadcrumb, table of contents, verified related coding
links, previous/next articles, and the original notes and interactions. Practice has
small related-reading links only where an explicit conceptual relation is recorded.
Related articles do not substitute for a question's Solution tab. The four existing
study plans retain their ordered coding/reading lists; reading items open Learn,
with study-plan stepping available while that plan is selected. Standalone book-only
items retain their existing placement and unavailable status.

## Inventory and addresses

The complete [inventory/mapping](epijudge.client/src/reading/learnInventory.json)
records every stable ID, original and current topic, source labels/URLs, body hash,
word count, estimated duration, and justified related-problem IDs. No body was copied
or rewritten for this move. Duration is the existing body word count divided by
200 words/minute, rounded up to at least one minute; it excludes exercises and notes.

`/learn` is the index; `/learn/reading-...` addresses an article. Topic, source, and
search state use `topic`, `source`, and `q` query parameters. `/practice?problem=...`
addresses a coding problem. Browser back/forward and direct links restore these
states. The old root workspace had no distinct article URL: existing saved reading
selections at `/` redirect to the corresponding Learn article. The compatibility
form `/reading/reading-...` redirects within the app as well. IDs and storage keys
are unchanged. Missing items show a useful unavailable page rather than opening
an unrelated exercise. Reading URLs are SPA routes served by the existing fallback.

## Authoring

1. Add a stable `reading-...` ID in
   `epijudge.client/src/reading/content/lessons.json` and a matching `.md` file.
   Keep IDs and checkpoint/quiz IDs stable to preserve saved work.
2. Supply a title, topic, verified book references where available, checkpoints,
   quiz options and a zero-based correct index, prompts, and optional source links.
   Do not invent edition-specific page numbers or present inferred titles as exact.
3. Markdown renders through `react-markdown`. Raw HTML is skipped; there is no
   arbitrary script/MDX execution. Interactive features are explicit React components.
4. The `race` simulation is registered in `ReadingWorkspace.tsx`. Additional
   simulations should be small components with testable state transitions.
5. Build the backend after changing metadata: it embeds the same manifest for
   validation. Frontend-only Markdown edits do not require a schema change.
6. Add or update the Learn mapping and its body hash, word count, and duration.
   Related IDs must exist in the runnable catalog and include a specific reason;
   do not infer interchangeable contracts from similar titles. Run the inventory
   audit to detect missing, duplicate, or unmapped bodies.

## Persistence

The existing SQLite `drafts` table stores each reading document under its lesson
ID and the internal `reading` discriminator. It contains version 1 JSON with
`notes`, `reviewed`, `checkpoints`, and `answers`. Notes are limited to 20,000
characters. The serialized document may use up to 128,000 characters to accommodate
JSON escaping. The existing 40,000-character coding limit is unchanged.

The same 500 ms debounce, optimistic revisions, browser recovery, retry, tab
conflicts, and answer backups are reused. Current version 2 exports and legacy
version 1 imports keep the existing reading discriminator and coding formats. Reading is never an executable
language, accepted submission, or legacy solved ID. No database migration or new
storage service is necessary. On a new machine, use the normal repository setup
and import an exported answer backup to transfer personal notes; cloning alone
does not transfer the local database. Older app versions that do not know reading
IDs will reject backups containing them, so update before importing.

Reviewed is a reversible manual assessment, independent of checkpoint and quiz
completion. A reading companion does not add a missing automated grader.

## Verification

Run `./Test.ps1` from the repository root; add `-Coverage` for coverage. The tests
exercise Markdown rendering, safe links/HTML handling, notes and review autosave,
navigation and reloads, SQLite persistence and backup round-trips, malformed
document rejection, and lost updates with and without a lock.

`python scripts/verify_learn_inventory.py` audits all twelve mappings and unchanged
bodies, source labels, word counts, durations, section anchors, and related targets,
alongside the 218/75/41 runnable inventory. After building the website, run
`python scripts/verify_learn_http.py --dll EpiJudge.Web/bin/Release/net10.0/EpiJudge.Web.dll --browser`
for an isolated profile with real desktop/mobile Chromium, all article deep links,
search/filter history, keyboard navigation, legacy redirects, notes, drafts, backup
restoration, missing/API-error states, and offline assets. The Solutions workflow
runs these checks and retains reports and screenshots. No archived course import
or external article content is needed.
