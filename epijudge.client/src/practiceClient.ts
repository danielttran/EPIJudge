import {
  codeFormatOrLegacy,
  type CodeDocument,
  type CodeFormat,
  type Draft,
  type Pending,
  type Progress,
  type CatalogEntry,
} from './practiceModels';
import { DraftRecovery, read, write } from './draftRecovery';
import { request, saveDraft, downloadBackup, importBackup } from './practiceApi';
import { migrateLegacyAnswers } from './legacyMigration';

const languages = ['csharp', 'javascript', 'python', 'cpp', 'java', 'reading'];
const keyFor = (problem: string, language: string) => `${language}:${problem}`;

export class PracticeClient {
  ready = false;
  error = '';
  progress: Record<string, Progress> = {};
  private drafts = new Map<string, Draft>();
  private pending = new Map<string, Pending>();
  private failed = new Set<string>();
  private readonly recovery = new DraftRecovery();
  private timers = new Map<string, ReturnType<typeof setTimeout>>();
  private saving = new Map<string, Promise<void>>();
  private listeners = new Set<() => void>();
  private version = 0;
  private initialization: Promise<void> | null = null;
  private catalog: CatalogEntry[] = [];
  private online = false;
  private refreshVersion = 0;
  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };
  snapshot = () => this.version;
  private emit() {
    this.version++;
    for (const listener of this.listeners) listener();
  }

  initialize(catalog: CatalogEntry[]) {
    if (this.initialization) return this.initialization;
    this.catalog = catalog;
    this.initialization = this.connect().finally(() => {
      this.initialization = null;
    });
    return this.initialization;
  }

  private async connect() {
    try {
      for (const problem of this.catalog)
        for (const language of languages) {
          const key = keyFor(problem.id, language);
          const recovery = this.recovery.find(key);
          if (recovery && !this.pending.has(key)) this.pending.set(key, recovery);
        }
      await migrateLegacyAnswers(this.catalog);
      await this.refresh();
      this.online = true;
      this.error = '';
      for (const key of this.pending.keys()) void this.flushKey(key);
    } catch (reason) {
      this.online = false;
      this.error = reason instanceof Error ? reason.message : 'Saved answers are unavailable.';
      // Legacy browser answers remain usable during an outage; never mark these as server-saved.
      for (const p of this.catalog)
        for (const language of languages) {
          const key = keyFor(p.id, language);
          if (!this.drafts.has(key)) {
            const code =
              read<string | null>(`epi:code:${language}:${p.id}`, null) ??
              (language === 'csharp' ? read<string | null>(`epi:code:${p.id}`, null) : null);
            if (typeof code === 'string')
              this.drafts.set(key, { problemId: p.id, language, code, revision: 0, updatedAt: '' });
          }
        }
    } finally {
      this.ready = true;
      this.emit();
    }
  }

  async refresh() {
    const requestVersion = ++this.refreshVersion;
    const state = await request<{ drafts: Draft[]; progress: Progress[] }>('');
    if (requestVersion !== this.refreshVersion) return;
    for (const draft of state.drafts) {
      const key = keyFor(draft.problemId, draft.language);
      if ((this.drafts.get(key)?.revision ?? -1) <= draft.revision) this.drafts.set(key, draft);
    }
    this.progress = Object.fromEntries(state.progress.map((p) => [p.problemId, p]));
    this.emit();
  }

  codeFor(problem: string, language: string, starter: string) {
    return this.documentFor(problem, language, starter).code;
  }

  documentFor(
    problem: string,
    language: string,
    starter: string,
    starterFormat: CodeFormat = 'legacy-v1',
  ): CodeDocument {
    const key = keyFor(problem, language);
    const saved = this.pending.get(key) ?? this.drafts.get(key);
    return saved
      ? { code: saved.code, codeFormat: codeFormatOrLegacy(saved.codeFormat) }
      : { code: starter, codeFormat: starterFormat };
  }

  edit(problem: string, language: string, code: string, codeFormat?: CodeFormat) {
    const key = keyFor(problem, language);
    const previous = this.pending.get(key);
    const current = previous ?? this.drafts.get(key);
    const pending = {
      code,
      revision: previous?.revision ?? this.drafts.get(key)?.revision ?? 0,
      codeFormat: codeFormat ?? codeFormatOrLegacy(current?.codeFormat),
      conflict: previous?.conflict,
    };
    this.pending.set(key, pending);
    this.recovery.keep(key, pending);
    this.failed.delete(key);
    clearTimeout(this.timers.get(key));
    // Timers are keyed by problem and language, so switching never cancels another draft's save.
    this.timers.set(
      key,
      setTimeout(() => {
        void this.flushKey(key);
      }, 500),
    );
    this.emit();
  }

  status(problem: string, language: string) {
    const key = keyFor(problem, language);
    if (!this.ready) return 'Loading saved answer…';
    if (this.pending.get(key)?.conflict) return 'Save conflict — browser copy kept';
    if (!this.online || this.failed.has(key))
      return this.recovery.unavailable.has(key)
        ? 'Save failed — keep this tab open'
        : 'Save failed — browser copy kept';
    if (this.pending.has(key)) return 'Saving…';
    return 'Saved';
  }

  conflict(problem: string, language: string) {
    return this.pending.get(keyFor(problem, language))?.conflict;
  }
  resolve(problem: string, language: string, useSaved: boolean) {
    const key = keyFor(problem, language);
    const pending = this.pending.get(key);
    if (!pending?.conflict) return;
    const saved = pending.conflict;
    this.drafts.set(key, saved);
    if (useSaved) {
      const recoveredKey = 'epi:recovered:' + key + ':' + Date.now();
      // One atomic storage entry keeps source and its execution contract together.
      // Do not discard the active draft or its recovery record if archiving fails.
      if (
        !write(recoveredKey, {
          code: pending.code,
          codeFormat: codeFormatOrLegacy(pending.codeFormat),
        })
      ) {
        this.error =
          'Could not preserve this browser copy. Your local draft is still open; free browser storage or keep your version.';
        this.emit();
        return;
      }
      this.pending.delete(key);
      this.recovery.clear(key, pending.code, codeFormatOrLegacy(pending.codeFormat));
    } else {
      this.pending.set(key, {
        code: pending.code,
        codeFormat: codeFormatOrLegacy(pending.codeFormat),
        revision: saved.revision,
      });
      this.recovery.keep(key, this.pending.get(key)!);
      void this.flushKey(key);
    }
    this.error = '';
    this.emit();
  }

  private flushKey(key: string): Promise<void> {
    clearTimeout(this.timers.get(key));
    if (this.saving.has(key)) return this.saving.get(key)!;
    if (!this.online || !this.pending.has(key) || this.pending.get(key)?.conflict)
      return Promise.resolve();
    const operation = (async () => {
      while (this.pending.has(key) && !this.pending.get(key)?.conflict) {
        const sent = { ...this.pending.get(key)! };
        const [language, problem] = key.split(':');
        try {
          const result = await saveDraft(problem, language, sent);
          if (!result.saved) {
            const pending = this.pending.get(key)!;
            if (!result.draft) {
              pending.revision = 0;
              this.recovery.keep(key, pending);
              continue;
            }
            pending.conflict = result.draft;
            this.recovery.keep(key, pending);
            this.emit();
            return;
          }
          const draft = result.draft;
          this.drafts.set(key, draft);
          const pending = this.pending.get(key)!;
          if (
            pending.code === sent.code &&
            codeFormatOrLegacy(pending.codeFormat) === codeFormatOrLegacy(sent.codeFormat)
          ) {
            this.pending.delete(key);
            this.recovery.clear(key, sent.code, codeFormatOrLegacy(sent.codeFormat));
          } else {
            pending.revision = draft.revision;
            this.recovery.keep(key, pending);
          }
          this.failed.delete(key);
          this.emit();
        } catch (reason) {
          this.failed.add(key);
          this.error = reason instanceof Error ? reason.message : 'Save failed.';
          this.emit();
          return;
        }
      }
    })();
    this.saving.set(key, operation);
    void operation.finally(() => this.saving.delete(key));
    return operation;
  }

  async flush() {
    if (!this.online) await this.initialize(this.catalog);
    await Promise.all([...this.pending.keys()].map((key) => this.flushKey(key)));
    if (this.pending.size || !this.online)
      throw new Error('Some answers are not saved yet. Resolve any conflict or retry saving.');
    this.error = '';
    this.emit();
  }

  async exportAnswers() {
    await this.flush();
    await downloadBackup();
  }

  async importAnswers(file: File) {
    if (file.size > 64 * 1024 * 1024) throw new Error('The backup is larger than 64 MB.');
    await this.flush();
    await importBackup(await file.text());
    await this.refresh();
  }

  async sync() {
    if (!this.ready) return;
    if (!this.online) {
      await this.initialize(this.catalog);
      return;
    }
    try {
      await this.refresh();
    } catch {
      /* Existing drafts remain available; an edit or Retry save reports save failures. */
    }
  }
}
