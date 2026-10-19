import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { webcrypto } from 'node:crypto';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { PracticeClient, usePractice } from './practiceStorage';
import { DraftRecovery, read, write } from './draftRecovery';
import { request } from './practiceApi';

const json = (value: unknown, status = 200) => new Response(JSON.stringify(value), { status });
let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('crypto', webcrypto);
  fetchMock = vi.fn(async (url: string, options?: RequestInit) =>
    options?.method === 'PUT'
      ? json({
          problemId: 'p',
          language: 'python',
          ...JSON.parse(options.body as string),
          revision: 1,
          updatedAt: 'now',
        })
      : url === '/api/practice'
        ? json({ drafts: [], progress: [] })
        : json({}),
  );
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

it('initializes only after a catalog exists and isolates separate mounted workspaces', async () => {
  const empty: Array<{ id: string }> = [];
  const hook = renderHook(({ catalog }) => usePractice(catalog), {
    initialProps: { catalog: empty },
  });
  expect(fetchMock).not.toHaveBeenCalled();
  hook.rerender({ catalog: [{ id: 'p' }] });
  await waitFor(() => expect(hook.result.current.ready).toBe(true));
  act(() => hook.result.current.edit('p', 'python', 'local draft'));
  const second = renderHook(() => usePractice(empty));
  expect(second.result.current).not.toBe(hook.result.current);
  expect(second.result.current.codeFor('p', 'python', 'starter')).toBe('starter');
  await act(async () => hook.result.current.flush());
});
it('refreshes on focus, flushes when hidden, and removes listeners on unmount', async () => {
  const catalog = [{ id: 'p' }];
  const hook = renderHook(() => usePractice(catalog));
  await waitFor(() => expect(hook.result.current.ready).toBe(true));
  const refresh = vi.spyOn(hook.result.current, 'sync');
  act(() => window.dispatchEvent(new Event('focus')));
  expect(refresh).toHaveBeenCalledOnce();
  const flush = vi.spyOn(hook.result.current, 'flush');
  vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('hidden');
  await act(async () => {
    document.dispatchEvent(new Event('visibilitychange'));
  });
  expect(flush).toHaveBeenCalledOnce();
  hook.unmount();
  window.dispatchEvent(new Event('focus'));
  document.dispatchEvent(new Event('visibilitychange'));
  expect(refresh).toHaveBeenCalledOnce();
  expect(flush).toHaveBeenCalledOnce();
});
it('sync is safe before initialization, reconnects offline, and retains answers on refresh failure', async () => {
  const client = new PracticeClient();
  await client.sync();
  expect(fetchMock).not.toHaveBeenCalled();
  fetchMock.mockRejectedValueOnce(new Error('offline'));
  await client.initialize([{ id: 'p' }]);
  await client.sync();
  expect(client.status('p', 'python')).toBe('Saved');
  fetchMock.mockRejectedValueOnce(new Error('offline again'));
  await client.sync();
  expect(client.ready).toBe(true);
});
it('export flushes pending edits, downloads a JSON backup, and releases its object URL', async () => {
  vi.useFakeTimers();
  const client = new PracticeClient();
  await client.initialize([{ id: 'p' }]);
  const create = vi.fn(() => 'blob:backup'),
    revoke = vi.fn();
  vi.stubGlobal('URL', Object.assign(URL, { createObjectURL: create, revokeObjectURL: revoke }));
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});
  client.edit('p', 'python', 'answer');
  await client.exportAnswers();
  const urls = fetchMock.mock.calls.map(([url]) => url);
  expect(urls.indexOf('/api/practice/drafts/p/python')).toBeLessThan(
    urls.indexOf('/api/practice/export'),
  );
  expect(click).toHaveBeenCalledOnce();
  expect(create).toHaveBeenCalledOnce();
  await vi.advanceTimersByTimeAsync(1000);
  expect(revoke).toHaveBeenCalledWith('blob:backup');
});
it('reports export failure without starting a download', async () => {
  const client = new PracticeClient();
  await client.initialize([{ id: 'p' }]);
  fetchMock.mockResolvedValueOnce(json({}, 503));
  await expect(client.exportAnswers()).rejects.toThrow('export');
});
it('imports valid JSON after flushing and refreshes the merged server state', async () => {
  const client = new PracticeClient();
  await client.initialize([{ id: 'p' }]);
  const text = '{"version":1,"drafts":[],"attempts":[],"solvedIds":[]}';
  await client.importAnswers({ size: text.length, text: async () => text } as File);
  expect(fetchMock.mock.calls.find(([url]) => url === '/api/practice/import')?.[1].body).toBe(text);
  expect(fetchMock.mock.calls.at(-1)?.[0]).toBe('/api/practice');
});
it.each(['message', 'detail', 'invalid'])('surfaces API errors from %s responses', async (kind) => {
  fetchMock.mockResolvedValueOnce(
    kind === 'invalid'
      ? new Response('{', { status: 503 })
      : json({ [kind]: 'specific failure' }, 503),
  );
  await expect(request('')).rejects.toThrow(
    kind === 'invalid' ? 'browser copy is retained' : 'specific failure',
  );
});
it('recovery read/write gracefully handles unavailable storage and invalid JSON', () => {
  localStorage.setItem('broken', '{');
  expect(read('broken', 'fallback')).toBe('fallback');
  vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
    throw new Error('blocked');
  });
  expect(read('missing', 'fallback')).toBe('fallback');
  vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    throw new Error('blocked');
  });
  expect(write('key', {})).toBe(false);
});
it('recovery cleanup removes matching code only and tolerates blocked storage', () => {
  const recovery = new DraftRecovery();
  recovery.keep('python:p', { code: 'new', revision: 0 });
  localStorage.setItem(
    'epi:pending:other:python:p',
    JSON.stringify({ code: 'other tab', revision: 0 }),
  );
  recovery.clear('python:p', 'new');
  expect(recovery.find('python:p')?.code).toBe('other tab');
  vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => {
    throw new Error('blocked');
  });
  expect(() => recovery.clear('python:p', 'other tab')).not.toThrow();
  vi.spyOn(Storage.prototype, 'key').mockImplementation(() => {
    throw new Error('blocked');
  });
  expect(recovery.find('python:p')).toBeNull();
});
