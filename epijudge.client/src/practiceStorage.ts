import { useEffect, useSyncExternalStore } from 'react';

type Draft = {
  problemId: string;
  language: string;
  code: string;
  revision: number;
  updatedAt: string;
};
type Pending = { code: string; revision: number; conflict?: Draft; writtenAt?: number };
type Progress = { problemId: string; status: 'solved' | 'attempted'; acceptedLanguages: string[] };
type CatalogEntry = { id: string };
const languages = ['csharp', 'javascript', 'python', 'cpp', 'java'];
const headers = { 'Content-Type': 'application/json', 'X-EpiJudge-Client': 'local-editor' };
const keyFor = (problem: string, language: string) => `${language}:${problem}`;

function read<T>(key: string, fallback: T): T {
  try {
    return JSON.parse(localStorage.getItem(key) ?? 'null') ?? fallback;
  } catch {
    return fallback;
  }
}
function write(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}
async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch('/api/practice' + path, {
    cache: 'no-store',
    signal: AbortSignal.timeout(20_000),
    ...options,
    headers,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(
      detail.message ??
        detail.detail ??
        'Could not reach saved answers. Your browser copy is retained.',
    );
  }
  return response.json();
}

class PracticeClient {
  ready = false;
  error = '';
  progress: Record<string, Progress> = {};
  private drafts = new Map<string, Draft>();
  private pending = new Map<string, Pending>();
  private failed = new Set<string>();
  private recoveryUnavailable = new Set<string>();
  private timers = new Map<string, ReturnType<typeof setTimeout>>();
  private saving = new Map<string, Promise<void>>();
  private listeners = new Set<() => void>();
  private version = 0;
  private initialization: Promise<void> | null = null;
  private catalog: CatalogEntry[] = [];
  private online = false;
  private readonly tabId = crypto.randomUUID();
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

  private recoveryKey(key: string) {
    return `epi:pending:${this.tabId}:${key}`;
  }
  private keepRecovery(key: string, pending: Pending) {
    pending.writtenAt = Date.now();
    if (write(this.recoveryKey(key), pending)) this.recoveryUnavailable.delete(key);
    else this.recoveryUnavailable.add(key);
  }
  private recover(key: string): Pending | null {
    try {
      const copies: Pending[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const storageKey = localStorage.key(i)!;
        if (storageKey.startsWith('epi:pending:') && storageKey.endsWith(':' + key)) {
          const pending = read<Pending | null>(storageKey, null);
          if (pending && typeof pending.code === 'string' && Number.isSafeInteger(pending.revision))
            copies.push(pending);
        }
      }
      return copies.sort((a, b) => (b.writtenAt ?? 0) - (a.writtenAt ?? 0))[0] ?? null;
    } catch {
      return null;
    }
  }
  private clearRecovery(key: string, code: string) {
    try {
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const storageKey = localStorage.key(i)!;
        if (
          storageKey.startsWith('epi:pending:') &&
          storageKey.endsWith(':' + key) &&
          read<Pending | null>(storageKey, null)?.code === code
        )
          localStorage.removeItem(storageKey);
      }
    } catch {
      /* A retained copy is safer than discarding it. */
    }
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
      const drafts: Draft[] = [];
      const known = new Set(this.catalog.map((p) => p.id));
      for (const p of this.catalog)
        for (const language of languages) {
          const code =
            read<string | null>(`epi:code:${language}:${p.id}`, null) ??
            (language === 'csharp' ? read<string | null>(`epi:code:${p.id}`, null) : null);
          if (typeof code === 'string')
            drafts.push({
              problemId: p.id,
              language,
              code,
              revision: 0,
              updatedAt: new Date().toISOString(),
            });
          const key = keyFor(p.id, language);
          const recovery = this.recover(key);
          if (recovery && typeof recovery.code === 'string' && !this.pending.has(key))
            this.pending.set(key, recovery);
        }
      const attempts = read<
        Array<{
          id: string;
          problemId: string;
          mode: string;
          status: string;
          passed: number;
          total: number;
          timestamp: string;
        }>
      >('epi:attempts', [])
        .filter((a) => known.has(a.problemId))
        .map((a) => ({
          ...a,
          id: `legacy:${a.id}`,
          code: null,
          language: null,
          elapsedMs: 0,
          result: null,
          legacy: true,
        }));
      const solvedIds = read<string[]>('epi:solved', []).filter((id) => known.has(id));
      // Content-based IDs remain idempotent even when a full/private browser cannot store a new marker.
      const source = JSON.stringify({
        drafts: drafts.map(({ problemId, language, code }) => ({ problemId, language, code })),
        attempts,
        solvedIds,
      });
      const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(source));
      const migrationId =
        'browser-v1:' +
        [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
      await request('/migrate', {
        method: 'POST',
        body: JSON.stringify({ migrationId, drafts, attempts, solvedIds }),
      });
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
    const key = keyFor(problem, language);
    return this.pending.get(key)?.code ?? this.drafts.get(key)?.code ?? starter;
  }

  edit(problem: string, language: string, code: string) {
    const key = keyFor(problem, language);
    const previous = this.pending.get(key);
    const pending = {
      code,
      revision: previous?.revision ?? this.drafts.get(key)?.revision ?? 0,
      conflict: previous?.conflict,
    };
    this.pending.set(key, pending);
    this.keepRecovery(key, pending);
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
      return this.recoveryUnavailable.has(key)
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
      write('epi:recovered:' + key + ':' + Date.now(), pending.code);
      this.pending.delete(key);
      this.clearRecovery(key, pending.code);
    } else {
      this.pending.set(key, { code: pending.code, revision: saved.revision });
      this.keepRecovery(key, this.pending.get(key)!);
      void this.flushKey(key);
    }
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
          const response = await fetch(
            `/api/practice/drafts/${encodeURIComponent(problem)}/${language}`,
            {
              method: 'PUT',
              signal: AbortSignal.timeout(15_000),
              headers,
              body: JSON.stringify({ code: sent.code, revision: sent.revision }),
            },
          );
          if (response.status === 409) {
            const detail = await response.json();
            const pending = this.pending.get(key)!;
            if (!detail.draft) {
              pending.revision = 0;
              this.keepRecovery(key, pending);
              continue;
            }
            pending.conflict = detail.draft;
            this.keepRecovery(key, pending);
            this.emit();
            return;
          }
          if (!response.ok)
            throw new Error('Could not save your answer. Retry saving before closing this tab.');
          const draft: Draft = await response.json();
          this.drafts.set(key, draft);
          const pending = this.pending.get(key)!;
          if (pending.code === sent.code) {
            this.pending.delete(key);
            this.clearRecovery(key, sent.code);
          } else {
            pending.revision = draft.revision;
            this.keepRecovery(key, pending);
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
    const response = await fetch('/api/practice/export', {
      cache: 'no-store',
      signal: AbortSignal.timeout(60_000),
    });
    if (!response.ok) throw new Error('Could not export saved answers.');
    const url = URL.createObjectURL(await response.blob());
    const link = document.createElement('a');
    link.href = url;
    link.download = 'epi-answers-' + new Date().toISOString().slice(0, 10) + '.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async importAnswers(file: File) {
    if (file.size > 64 * 1024 * 1024) throw new Error('The backup is larger than 64 MB.');
    await this.flush();
    const text = await file.text();
    JSON.parse(text);
    await request('/import', { method: 'POST', body: text, signal: AbortSignal.timeout(120_000) });
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

const client = new PracticeClient();
export function usePractice(catalog: CatalogEntry[]) {
  useSyncExternalStore(client.subscribe, client.snapshot);
  useEffect(() => {
    if (!catalog.length) return;
    void client.initialize(catalog);
    const focus = () => {
      void client.sync();
    };
    const visibility = () => {
      if (document.visibilityState === 'hidden') void client.flush().catch(() => {});
    };
    window.addEventListener('focus', focus);
    document.addEventListener('visibilitychange', visibility);
    return () => {
      window.removeEventListener('focus', focus);
      document.removeEventListener('visibilitychange', visibility);
    };
  }, [catalog, client]);
  return client;
}
