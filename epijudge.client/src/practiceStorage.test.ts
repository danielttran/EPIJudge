import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { webcrypto } from 'node:crypto';
import { PracticeClient } from './practiceStorage';

const draft = (code = 'saved', revision = 1, problemId = 'count_bits', language = 'python') => ({
  code,
  revision,
  problemId,
  language,
  updatedAt: '2026-01-01T00:00:00Z',
});
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status });
function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason: unknown) => void;
  const promise = new Promise<T>((yes, no) => {
    resolve = yes;
    reject = no;
  });
  return { promise, resolve, reject };
}
let serverDrafts: ReturnType<typeof draft>[];
let writes: Array<{ url: string; code: string; revision: number }>;
let fetchMock: ReturnType<typeof vi.fn>;
async function connected() {
  const client = new PracticeClient();
  await client.initialize([{ id: 'count_bits' }, { id: 'parity' }]);
  return client;
}
beforeEach(() => {
  localStorage.clear();
  vi.useFakeTimers();
  vi.stubGlobal('crypto', webcrypto);
  serverDrafts = [];
  writes = [];
  fetchMock = vi.fn(async (url: string, options?: RequestInit) => {
    if (options?.method === 'PUT') {
      const body = JSON.parse(options.body as string);
      writes.push({ url, ...body });
      const [, language, problemId] = url.match(/drafts\/([^/]+)\/([^/]+)$/) ?? [];
      return json({
        ...draft(body.code, body.revision + 1, language, problemId),
        codeFormat: body.codeFormat ?? 'legacy-v1',
      });
    }
    if (url === '/api/practice') return json({ drafts: serverDrafts, progress: [] });
    return json({ imported: true });
  });
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe('draft saving', () => {
  it('chooses source and format together without converting legacy drafts', async () => {
    serverDrafts = [draft('legacy full program')];
    const client = await connected();
    expect(client.documentFor('count_bits', 'python', 'clean starter', 'callable-v1')).toEqual({
      code: 'legacy full program',
      codeFormat: 'legacy-v1',
    });
    expect(client.documentFor('parity', 'python', 'clean starter', 'callable-v1')).toEqual({
      code: 'clean starter',
      codeFormat: 'callable-v1',
    });
    client.edit('count_bits', 'python', 'same visible text', 'callable-v1');
    await client.flush();
    expect(client.documentFor('count_bits', 'python', 'unused')).toEqual({
      code: 'same visible text',
      codeFormat: 'callable-v1',
    });
    client.edit('count_bits', 'python', 'same visible text', 'legacy-v1');
    await client.flush();
    expect(client.documentFor('count_bits', 'python', 'unused').codeFormat).toBe('legacy-v1');
    expect(writes).toHaveLength(2);
  });
  it('does not acknowledge a newer format-only edit when an older save completes', async () => {
    const client = await connected();
    const response = deferred<Response>();
    fetchMock.mockImplementationOnce(() => response.promise);
    client.edit('count_bits', 'python', 'unchanged', 'legacy-v1');
    const saving = client.flush();
    client.edit('count_bits', 'python', 'unchanged', 'callable-v1');
    response.resolve(json({ ...draft('unchanged'), codeFormat: 'legacy-v1' }));
    await saving;
    expect(client.documentFor('count_bits', 'python', '').codeFormat).toBe('callable-v1');
    const lastWrite = fetchMock.mock.calls
      .filter(([, options]) => options?.method === 'PUT')
      .at(-1)!;
    expect(JSON.parse(lastWrite[1].body).codeFormat).toBe('callable-v1');
    expect(JSON.parse(lastWrite[1].body).revision).toBe(1);
  });
  it('never adopts a remote callable format for an older legacy recovery document', async () => {
    localStorage.setItem(
      'epi:pending:old:python:count_bits',
      JSON.stringify({ code: 'old recovered program', revision: 0 }),
    );
    serverDrafts = [Object.assign(draft('remote callable', 7), { codeFormat: 'callable-v1' })];
    const response = deferred<Response>();
    const previous = fetchMock.getMockImplementation()! as (
      url: string,
      options?: RequestInit,
    ) => Promise<Response>;
    let held = false;
    fetchMock.mockImplementation((url: string, options?: RequestInit) => {
      if (options?.method === 'PUT' && !held) {
        held = true;
        return response.promise;
      }
      return previous(url, options);
    });
    const client = await connected();
    client.edit('count_bits', 'python', 'edited recovered program');
    expect(client.documentFor('count_bits', 'python', '').codeFormat).toBe('legacy-v1');
    response.resolve(json({ ...draft('old recovered program', 8), codeFormat: 'legacy-v1' }));
    await client.flush();
    expect(client.documentFor('count_bits', 'python', '')).toEqual({
      code: 'edited recovered program',
      codeFormat: 'legacy-v1',
    });
  });
  it.each([true, false])(
    'retains the chosen code format when resolving a conflict (saved=%s)',
    async (useSaved) => {
      const client = await connected();
      client.edit('count_bits', 'python', 'local full program', 'legacy-v1');
      fetchMock.mockResolvedValueOnce(
        json({ draft: { ...draft('remote callable', 8), codeFormat: 'callable-v1' } }, 409),
      );
      await expect(client.flush()).rejects.toThrow();
      client.resolve('count_bits', 'python', useSaved);
      await client.flush();
      expect(client.documentFor('count_bits', 'python', '')).toEqual({
        code: useSaved ? 'remote callable' : 'local full program',
        codeFormat: useSaved ? 'callable-v1' : 'legacy-v1',
      });
      if (useSaved) {
        const key = Object.keys(localStorage).find((key) => key.startsWith('epi:recovered:'))!;
        expect(JSON.parse(localStorage.getItem(key)!)).toEqual({
          code: 'local full program',
          codeFormat: 'legacy-v1',
        });
      }
    },
  );
  it.each(['legacy-v1', 'callable-v1'] as const)(
    'retains the active %s draft and original recovery when archiving hits quota',
    async (format) => {
      const source = 'local source\r\nλ 🐈';
      const client = await connected();
      client.edit('count_bits', 'python', source, format);
      fetchMock.mockResolvedValueOnce(
        json({ draft: { ...draft('remote source', 8), codeFormat: 'legacy-v1' } }, 409),
      );
      await expect(client.flush()).rejects.toThrow();
      const recoveryKey = Object.keys(localStorage).find((key) => key.startsWith('epi:pending:'))!;
      const setItem = Storage.prototype.setItem;
      const archive = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(function (
        this: Storage,
        key,
        value,
      ) {
        if (key.startsWith('epi:recovered:')) throw new DOMException('Full', 'QuotaExceededError');
        setItem.call(this, key, value);
      });
      client.resolve('count_bits', 'python', true);
      expect(client.documentFor('count_bits', 'python', '')).toEqual({
        code: source,
        codeFormat: format,
      });
      expect(client.conflict('count_bits', 'python')?.code).toBe('remote source');
      expect(client.error).toContain('Your local draft is still open');
      expect(JSON.parse(localStorage.getItem(recoveryKey)!)).toEqual(
        expect.objectContaining({ code: source, codeFormat: format }),
      );
      expect(Object.keys(localStorage).some((key) => key.startsWith('epi:recovered:'))).toBe(false);
      archive.mockRestore();
      client.resolve('count_bits', 'python', true);
      await client.flush();
      expect(client.documentFor('count_bits', 'python', '')).toEqual({
        code: 'remote source',
        codeFormat: 'legacy-v1',
      });
      expect(localStorage.getItem(recoveryKey)).toBeNull();
      const savedKey = Object.keys(localStorage).find((key) => key.startsWith('epi:recovered:'))!;
      expect(JSON.parse(localStorage.getItem(savedKey)!)).toEqual({
        code: source,
        codeFormat: format,
      });
      expect(client.error).toBe('');
    },
  );
  it('archives source and format in one write rather than risking a partial two-key backup', async () => {
    const client = await connected();
    client.edit('count_bits', 'python', 'local callable', 'callable-v1');
    fetchMock.mockResolvedValueOnce(json({ draft: draft('remote source', 8) }, 409));
    await expect(client.flush()).rejects.toThrow();
    const setItem = Storage.prototype.setItem;
    let archiveWrites = 0;
    const archive = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(function (
      this: Storage,
      key,
      value,
    ) {
      if (key.startsWith('epi:recovered:') && ++archiveWrites > 1)
        throw new DOMException('Second write failed', 'QuotaExceededError');
      setItem.call(this, key, value);
    });
    client.resolve('count_bits', 'python', true);
    expect(archiveWrites).toBe(1);
    const key = Object.keys(localStorage).find((key) => key.startsWith('epi:recovered:'))!;
    expect(JSON.parse(localStorage.getItem(key)!)).toEqual({
      code: 'local callable',
      codeFormat: 'callable-v1',
    });
    expect(client.documentFor('count_bits', 'python', '').code).toBe('remote source');
    archive.mockRestore();
  });
  it('uses a starter only when no answer exists, preserving an empty answer', async () => {
    serverDrafts = [draft('')];
    const client = await connected();
    expect(client.codeFor('count_bits', 'python', 'starter')).toBe('');
    expect(client.codeFor('parity', 'python', 'starter')).toBe('starter');
  });
  it('debounces typing and saves the latest text once', async () => {
    const client = await connected();
    client.edit('count_bits', 'python', 'first');
    await vi.advanceTimersByTimeAsync(400);
    client.edit('count_bits', 'python', 'latest');
    await vi.advanceTimersByTimeAsync(499);
    expect(writes).toHaveLength(0);
    expect(client.status('count_bits', 'python')).toBe('Saving…');
    await vi.advanceTimersByTimeAsync(1);
    expect(writes.map((w) => w.code)).toEqual(['latest']);
    expect(client.status('count_bits', 'python')).toBe('Saved');
    expect(localStorage.length).toBe(0);
  });
  it.each(['csharp', 'javascript', 'python', 'cpp', 'java'])(
    'saves %s separately from other problems and languages',
    async (language) => {
      const client = await connected();
      client.edit('count_bits', language, 'one');
      client.edit('parity', language, 'two');
      await client.flush();
      expect(writes.map((w) => w.url)).toEqual([
        `/api/practice/drafts/count_bits/${language}`,
        `/api/practice/drafts/parity/${language}`,
      ]);
      expect(client.codeFor('count_bits', language, '')).toBe('one');
      expect(client.codeFor('parity', language, '')).toBe('two');
    },
  );
  it('serializes edits arriving while a save is in flight using the returned revision', async () => {
    const client = await connected();
    const pending = deferred<Response>();
    fetchMock.mockImplementationOnce(() => pending.promise);
    client.edit('count_bits', 'python', 'first');
    const flushing = client.flush();
    client.edit('count_bits', 'python', 'second');
    pending.resolve(json(draft('first', 7)));
    await flushing;
    expect(writes).toEqual([expect.objectContaining({ code: 'second', revision: 7 })]);
    expect(client.codeFor('count_bits', 'python', '')).toBe('second');
  });
  it('coalesces simultaneous flush calls instead of sending duplicate writes', async () => {
    const client = await connected();
    const pending = deferred<Response>();
    fetchMock.mockImplementationOnce(() => pending.promise);
    client.edit('count_bits', 'python', 'answer');
    const a = client.flush(),
      b = client.flush();
    pending.resolve(json(draft('answer')));
    await Promise.all([a, b]);
    expect(fetchMock.mock.calls.filter(([, options]) => options?.method === 'PUT')).toHaveLength(1);
  });
  it.each(['network', 'http', 'json'])(
    'retains recovery after a %s failure and supports retry',
    async (failure) => {
      const client = await connected();
      fetchMock.mockImplementationOnce(() =>
        failure === 'network'
          ? Promise.reject(new Error('offline'))
          : Promise.resolve(failure === 'http' ? json({}, 503) : new Response('invalid')),
      );
      client.edit('count_bits', 'python', 'precious answer');
      await expect(client.flush()).rejects.toThrow('not saved');
      expect(client.status('count_bits', 'python')).toBe('Save failed — browser copy kept');
      expect(client.codeFor('count_bits', 'python', '')).toBe('precious answer');
      expect(localStorage.getItem(localStorage.key(0)!)).toContain('precious answer');
      await client.flush();
      expect(client.status('count_bits', 'python')).toBe('Saved');
    },
  );
  it('warns explicitly when neither server nor browser storage can save', async () => {
    const client = await connected();
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('full');
    });
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    client.edit('count_bits', 'python', 'keep open');
    await expect(client.flush()).rejects.toThrow();
    expect(client.status('count_bits', 'python')).toBe('Save failed — keep this tab open');
  });
  it('saves other drafts even when one language fails', async () => {
    const client = await connected();
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    client.edit('count_bits', 'python', 'unsaved');
    client.edit('count_bits', 'java', 'saved');
    await expect(client.flush()).rejects.toThrow();
    expect(client.status('count_bits', 'python')).toContain('Save failed');
    expect(client.status('count_bits', 'java')).toBe('Saved');
    expect(client.codeFor('count_bits', 'python', '')).toBe('unsaved');
  });
  it('preserves the latest edit when a conflict arrives during typing', async () => {
    const client = await connected();
    const response = deferred<Response>();
    fetchMock.mockReturnValueOnce(response.promise);
    client.edit('count_bits', 'python', 'first');
    const flushing = client.flush();
    client.edit('count_bits', 'python', 'latest');
    response.resolve(json({ draft: draft('other tab', 9) }, 409));
    await expect(flushing).rejects.toThrow();
    expect(client.codeFor('count_bits', 'python', '')).toBe('latest');
    client.resolve('count_bits', 'python', false);
    await client.flush();
    expect(writes[0]).toEqual(expect.objectContaining({ code: 'latest', revision: 9 }));
  });
  it.each([true, false])(
    'resolves a revision conflict using saved=%s without silently overwriting',
    async (useSaved) => {
      const client = await connected();
      fetchMock.mockResolvedValueOnce(json({ draft: draft('other tab', 8) }, 409));
      client.edit('count_bits', 'python', 'my answer');
      await expect(client.flush()).rejects.toThrow();
      expect(client.conflict('count_bits', 'python')?.revision).toBe(8);
      expect(client.codeFor('count_bits', 'python', '')).toBe('my answer');
      client.resolve('count_bits', 'python', useSaved);
      await client.flush();
      expect(client.codeFor('count_bits', 'python', '')).toBe(useSaved ? 'other tab' : 'my answer');
      if (!useSaved) expect(writes[0].revision).toBe(8);
      else
        expect(Object.keys(localStorage).some((key) => key.startsWith('epi:recovered:'))).toBe(
          true,
        );
    },
  );
  it('retries revision zero when the conflicting server draft no longer exists', async () => {
    serverDrafts = [draft('old', 10)];
    const client = await connected();
    fetchMock.mockResolvedValueOnce(json({ draft: null }, 409));
    client.edit('count_bits', 'python', 'new');
    await client.flush();
    expect(writes[0].revision).toBe(0);
  });
});

describe('initialization, recovery and synchronization', () => {
  it('shares one initialization request across concurrent callers', async () => {
    const client = new PracticeClient();
    await Promise.all([
      client.initialize([{ id: 'count_bits' }]),
      client.initialize([{ id: 'count_bits' }]),
    ]);
    expect(fetchMock.mock.calls.filter(([url]) => url.endsWith('/migrate'))).toHaveLength(1);
  });
  it('restores the newest recovery copy after reload and leaves other tab edits intact', async () => {
    localStorage.setItem(
      'epi:pending:old:python:count_bits',
      JSON.stringify({ code: 'old', revision: 0, writtenAt: 1 }),
    );
    localStorage.setItem(
      'epi:pending:new:python:count_bits',
      JSON.stringify({ code: 'new', revision: 0, writtenAt: 2 }),
    );
    const client = await connected();
    await client.flush();
    expect(client.codeFor('count_bits', 'python', '')).toBe('new');
    expect(localStorage.getItem('epi:pending:old:python:count_bits')).toContain('old');
  });
  it('ignores malformed recovery records', async () => {
    localStorage.setItem('epi:pending:broken:python:count_bits', '{');
    localStorage.setItem(
      'epi:pending:wrong:python:count_bits',
      JSON.stringify({ code: 3, revision: 'x' }),
    );
    localStorage.setItem(
      'epi:pending:negative:python:count_bits',
      JSON.stringify({ code: 'bad revision', revision: -1 }),
    );
    const client = await connected();
    expect(client.codeFor('count_bits', 'python', 'starter')).toBe('starter');
  });
  it('keeps legacy answers usable offline and reconnects on explicit retry', async () => {
    localStorage.setItem('epi:code:count_bits', JSON.stringify('legacy answer'));
    fetchMock.mockRejectedValueOnce(new Error('offline'));
    const client = await connected();
    expect(client.ready).toBe(true);
    expect(client.codeFor('count_bits', 'csharp', '')).toBe('legacy answer');
    expect(client.status('count_bits', 'csharp')).toContain('Save failed');
    await client.flush();
    expect(client.status('count_bits', 'csharp')).toBe('Saved');
  });
  it('filters legacy unknown problems and generates a repeatable migration id', async () => {
    localStorage.setItem('epi:solved', JSON.stringify(['count_bits', 'unknown']));
    localStorage.setItem(
      'epi:attempts',
      JSON.stringify([
        {
          id: 'a',
          problemId: 'count_bits',
          mode: 'submit',
          status: 'Accepted',
          passed: 1,
          total: 1,
          timestamp: '2026-01-01T00:00:00Z',
        },
        { id: 'b', problemId: 'unknown' },
      ]),
    );
    const client = await connected();
    await client.initialize([{ id: 'count_bits' }, { id: 'parity' }]);
    const migrations = fetchMock.mock.calls
      .filter(([url]) => url.endsWith('/migrate'))
      .map(([, options]) => JSON.parse(options.body));
    expect(migrations[0].migrationId).toBe(migrations[1].migrationId);
    expect(migrations[0].solvedIds).toEqual(['count_bits']);
    expect(migrations[0].attempts).toEqual([
      expect.objectContaining({ id: 'legacy:a', language: null, code: null, legacy: true }),
    ]);
  });
  it('ignores stale refresh responses and never rolls a saved revision backward', async () => {
    const client = await connected();
    const slow = deferred<Response>();
    fetchMock.mockImplementationOnce(() => slow.promise);
    const first = client.refresh();
    serverDrafts = [draft('new', 8)];
    await client.refresh();
    slow.resolve(json({ drafts: [draft('stale', 2)], progress: [] }));
    await first;
    expect(client.codeFor('count_bits', 'python', '')).toBe('new');
    serverDrafts = [draft('older', 1)];
    await client.refresh();
    expect(client.codeFor('count_bits', 'python', '')).toBe('new');
  });
  it('does not replace pending local edits during a refresh', async () => {
    const client = await connected();
    client.edit('count_bits', 'python', 'local');
    serverDrafts = [draft('remote', 4)];
    await client.refresh();
    expect(client.codeFor('count_bits', 'python', '')).toBe('local');
  });
  it('notifies subscribers and stops notifying after unsubscribe', async () => {
    const client = await connected();
    const listener = vi.fn();
    const unsubscribe = client.subscribe(listener);
    const before = client.snapshot();
    client.edit('count_bits', 'python', 'one');
    expect(listener).toHaveBeenCalledOnce();
    expect(client.snapshot()).toBeGreaterThan(before);
    unsubscribe();
    client.edit('count_bits', 'python', 'two');
    expect(listener).toHaveBeenCalledOnce();
  });
  it('rejects oversized or malformed imports before sending an import request', async () => {
    const client = await connected();
    await expect(client.importAnswers({ size: 65 * 1024 * 1024 } as File)).rejects.toThrow('64 MB');
    await expect(
      client.importAnswers({ size: 1, text: async () => '{' } as File),
    ).rejects.toThrow();
    expect(fetchMock.mock.calls.some(([url]) => url.endsWith('/import'))).toBe(false);
  });
});
