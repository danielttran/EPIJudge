# Reading and design

The problem library's dropdown contains Coding, Reading & Design, topic filters,
and the four study plans. Each plan is one ordered list with no Review tab.
Other exercises remain accessible outside the plans. Reading & Design includes
all twelve companions; study plans open only the companions assigned to their lists. These are original
study notes and prompts, not copied EPI chapters or a certified edition inventory.

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

## Persistence

The existing SQLite `drafts` table stores each reading document under its lesson
ID and the internal `reading` discriminator. It contains version 1 JSON with
`notes`, `reviewed`, `checkpoints`, and `answers`. Notes are limited to 20,000
characters. The serialized document may use up to 128,000 characters to accommodate
JSON escaping. The existing 40,000-character coding limit is unchanged.

The same 500 ms debounce, optimistic revisions, browser recovery, retry, tab
conflicts, and version 1 answer backups are reused. Reading is never an executable
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
