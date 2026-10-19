import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { useSubmissionHistory } from './useSubmissionHistory';
import type { Attempt } from './workspaceModels';

const attempt = (id: string, problemId = 'p', sequence = 1) =>
  ({ id, problemId, sequence, code: id }) as Attempt;
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status });
function deferred() {
  let resolve!: (value: Response) => void;
  const promise = new Promise<Response>((yes) => {
    resolve = yes;
  });
  return { promise, resolve };
}
let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  fetchMock = vi.fn(async () => json([]));
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
const mount = (id = 'p') =>
  renderHook(
    ({ problemId, language, ready, version }) =>
      useSubmissionHistory(problemId, language, ready, version),
    { initialProps: { problemId: id, language: 'python', ready: true, version: 0 } },
  );

it('waits for practice initialization and reloads when history changes', async () => {
  const hook = renderHook(
    ({ ready, version }) => useSubmissionHistory('p', 'python', ready, version),
    { initialProps: { ready: false, version: 0 } },
  );
  expect(fetchMock).not.toHaveBeenCalled();
  hook.rerender({ ready: true, version: 0 });
  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
  hook.rerender({ ready: true, version: 1 });
  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
});
it('ignores an old initial-history response after switching problems even if abort is ignored', async () => {
  const old = deferred();
  fetchMock.mockReturnValueOnce(old.promise).mockResolvedValueOnce(json([attempt('new', 'q')]));
  const hook = mount();
  hook.rerender({ problemId: 'q', language: 'python', ready: true, version: 0 });
  await waitFor(() => expect(hook.result.current.attempts[0]?.id).toBe('new'));
  await act(async () => old.resolve(json([attempt('old')])));
  expect(hook.result.current.attempts.map((a) => a.id)).toEqual(['new']);
});
it.each(['problem', 'language'])(
  'ignores a pending detail response after changing %s',
  async (change) => {
    const hook = mount();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledOnce());
    const old = deferred();
    fetchMock.mockReturnValueOnce(old.promise);
    let loading!: Promise<void>;
    act(() => {
      loading = hook.result.current.viewAnswer(attempt('old'));
    });
    hook.rerender({
      problemId: change === 'problem' ? 'q' : 'p',
      language: change === 'language' ? 'java' : 'python',
      ready: true,
      version: 0,
    });
    await act(async () => {
      old.resolve(json(attempt('old')));
      await loading;
    });
    expect(hook.result.current.viewedAttempt).toBeNull();
  },
);
it('shows the most recently opened answer when responses arrive out of order', async () => {
  const hook = mount();
  await waitFor(() => expect(fetchMock).toHaveBeenCalledOnce());
  const old = deferred();
  fetchMock.mockReturnValueOnce(old.promise).mockResolvedValueOnce(json(attempt('new')));
  let loading!: Promise<void>;
  act(() => {
    loading = hook.result.current.viewAnswer(attempt('old'));
  });
  await act(async () => {
    await hook.result.current.viewAnswer(attempt('new'));
  });
  await act(async () => {
    old.resolve(json(attempt('old')));
    await loading;
  });
  expect(hook.result.current.viewedAttempt?.id).toBe('new');
});
it('closing an answer also invalidates a pending detail request', async () => {
  const hook = mount();
  await waitFor(() => expect(fetchMock).toHaveBeenCalledOnce());
  const old = deferred();
  fetchMock.mockReturnValueOnce(old.promise);
  let loading!: Promise<void>;
  act(() => {
    loading = hook.result.current.viewAnswer(attempt('old'));
    hook.result.current.closeAnswer();
  });
  await act(async () => {
    old.resolve(json(attempt('old')));
    await loading;
  });
  expect(hook.result.current.viewedAttempt).toBeNull();
});
it('ignores an older-page response after switching problems', async () => {
  fetchMock.mockResolvedValueOnce(
    json(Array.from({ length: 50 }, (_, i) => attempt('a' + i, 'p', 100 - i))),
  );
  const hook = mount();
  await waitFor(() => expect(hook.result.current.hasMoreHistory).toBe(true));
  const old = deferred();
  fetchMock.mockReturnValueOnce(old.promise).mockResolvedValueOnce(json([attempt('new', 'q')]));
  let loading!: Promise<void>;
  act(() => {
    loading = hook.result.current.loadOlder();
  });
  hook.rerender({ problemId: 'q', language: 'python', ready: true, version: 0 });
  await waitFor(() => expect(hook.result.current.attempts[0]?.id).toBe('new'));
  await act(async () => {
    old.resolve(json([attempt('old')]));
    await loading;
  });
  expect(hook.result.current.attempts.map((a) => a.id)).toEqual(['new']);
});
it('prevents duplicate pagination requests and deduplicates overlapping pages', async () => {
  const first = Array.from({ length: 50 }, (_, i) => attempt('a' + i, 'p', 100 - i));
  fetchMock.mockResolvedValueOnce(json(first));
  const hook = mount();
  await waitFor(() => expect(hook.result.current.hasMoreHistory).toBe(true));
  const page = deferred();
  fetchMock.mockReturnValueOnce(page.promise);
  await act(async () => {
    const loading = hook.result.current.loadOlder();
    await hook.result.current.loadOlder();
    page.resolve(json([first[49], attempt('older')]));
    await loading;
  });
  expect(fetchMock).toHaveBeenCalledTimes(2);
  expect(fetchMock.mock.calls[1][0]).toContain('before=51');
  expect(hook.result.current.attempts).toHaveLength(51);
  expect(hook.result.current.hasMoreHistory).toBe(false);
});
it.each(['initial', 'detail', 'older'])('reports %s errors and permits retry', async (kind) => {
  fetchMock.mockResolvedValueOnce(
    kind === 'initial'
      ? json({}, 503)
      : json(Array.from({ length: 50 }, (_, i) => attempt('a' + i))),
  );
  const hook = mount();
  await waitFor(() => expect(fetchMock).toHaveBeenCalledOnce());
  if (kind !== 'initial') {
    await waitFor(() => expect(hook.result.current.hasMoreHistory).toBe(true));
    fetchMock.mockResolvedValueOnce(json({}, 503));
    await act(async () => {
      await (kind === 'detail'
        ? hook.result.current.viewAnswer(attempt('a'))
        : hook.result.current.loadOlder());
    });
  }
  await waitFor(() => expect(hook.result.current.historyError).toContain('Could not'));
  hook.rerender({ problemId: 'p', language: 'python', ready: true, version: 1 });
  await waitFor(() => expect(hook.result.current.historyError).toBe(''));
});
it('aborts requests on unmount without reporting an error', async () => {
  const pending = deferred();
  fetchMock.mockReturnValueOnce(pending.promise);
  const hook = mount();
  const signal = fetchMock.mock.calls[0][1].signal as AbortSignal;
  hook.unmount();
  expect(signal.aborted).toBe(true);
  await act(async () => pending.resolve(json([attempt('late')])));
});
