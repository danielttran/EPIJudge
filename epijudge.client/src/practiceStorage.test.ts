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
      return json(draft(body.code, body.revision + 1, language, problemId));
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
