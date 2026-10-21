import { act, cleanup, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { useSubmission } from './useSubmission';

const graded = {
  id: 'a',
  status: 'Accepted',
  passed: 3,
  total: 3,
  elapsedMs: 1,
  diagnostics: null,
  cases: [],
};
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status });
function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((yes) => {
    resolve = yes;
  });
  return { promise, resolve };
}
let fetchMock: ReturnType<typeof vi.fn>;
const options = () => ({
  problemId: 'p',
  language: 'python',
  code: 'exact source',
  practice: { ready: true, flush: vi.fn(async () => {}), refresh: vi.fn(async () => {}) },
  onStarted: vi.fn(),
  onCompleted: vi.fn(),
  onRefreshError: vi.fn(),
});
beforeEach(() => {
  fetchMock = vi.fn(async () => json(graded));
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

it.each(['run', 'submit'] as const)(
  'flushes before %s and sends the exact editor snapshot',
  async (mode) => {
    const config = options();
    const saving = deferred<void>();
    config.practice.flush.mockReturnValueOnce(saving.promise);
    const hook = renderHook(() => useSubmission(config));
    let loading!: Promise<void>;
    act(() => {
      loading = hook.result.current.execute(mode);
    });
    expect(fetchMock).not.toHaveBeenCalled();
    expect(hook.result.current.busy).toBe(true);
    await act(async () => {
      saving.resolve();
      await loading;
    });
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({
      problemId: 'p',
      language: 'python',
      code: 'exact source',
      codeFormat: 'legacy-v1',
      mode,
    });
    expect(hook.result.current.result).toEqual(graded);
    expect(hook.result.current.activeMode).toBe(mode);
    expect(config.onCompleted).toHaveBeenCalledOnce();
    expect(hook.result.current.busy).toBe(false);
  },
);
it('sends callable format with the unchanged visible source snapshot', async () => {
  const config = { ...options(), codeFormat: 'callable-v1' as const };
  const hook = renderHook(() => useSubmission(config));
  await act(async () => {
    await hook.result.current.execute('submit');
  });
  expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({
    problemId: 'p',
    language: 'python',
    code: 'exact source',
    codeFormat: 'callable-v1',
    mode: 'submit',
  });
});
it('blocks execution until drafts are ready and prevents double submissions', async () => {
  const config = options();
  config.practice.ready = false;
  const hook = renderHook(
    ({ ready }) => useSubmission({ ...config, practice: { ...config.practice, ready } }),
    { initialProps: { ready: false } },
  );
  await act(async () => {
    await hook.result.current.execute('run');
  });
  expect(fetchMock).not.toHaveBeenCalled();
  hook.rerender({ ready: true });
  const response = deferred<Response>();
  fetchMock.mockReturnValueOnce(response.promise);
  await act(async () => {
    const first = hook.result.current.execute('run');
    await hook.result.current.execute('submit');
    response.resolve(json(graded));
    await first;
  });
  expect(fetchMock).toHaveBeenCalledOnce();
});
it('does not execute when flushing drafts fails', async () => {
  const config = options();
  config.practice.flush.mockRejectedValueOnce(new Error('conflict'));
  const hook = renderHook(() => useSubmission(config));
  await act(async () => {
    await hook.result.current.execute('submit');
  });
  expect(fetchMock).not.toHaveBeenCalled();
  expect(hook.result.current.error).toBe('conflict');
  expect(hook.result.current.busy).toBe(false);
});
it.each(['http', 'network', 'json'])(
  'reports a %s execution failure and permits retry',
  async (kind) => {
    fetchMock.mockImplementationOnce(() =>
      kind === 'network'
        ? Promise.reject(new Error('offline'))
        : Promise.resolve(kind === 'http' ? json({ message: 'busy' }, 429) : new Response('{')),
    );
    const hook = renderHook(() => useSubmission(options()));
    await act(async () => {
      await hook.result.current.execute('submit');
    });
    expect(hook.result.current.error).not.toBe('');
    expect(hook.result.current.busy).toBe(false);
    await act(async () => {
      await hook.result.current.execute('submit');
    });
    expect(hook.result.current.error).toBe('');
    expect(hook.result.current.result).toEqual(graded);
  },
);
it('keeps the grading result visible when progress refresh fails', async () => {
  const config = options();
  config.practice.refresh.mockRejectedValueOnce(new Error('offline'));
  const hook = renderHook(() => useSubmission(config));
  await act(async () => {
    await hook.result.current.execute('submit');
  });
  expect(hook.result.current.result).toEqual(graded);
  expect(hook.result.current.error).toBe('');
  expect(config.onRefreshError).toHaveBeenCalledOnce();
  expect(config.onCompleted).toHaveBeenCalledOnce();
});
it.each([
  ['detail', 'specific error'],
  ['empty', 'The runner could not complete this request.'],
  ['invalid', 'The runner could not complete this request.'],
  ['non-error', 'Could not reach the local runner.'],
])('handles %s error responses', async (kind, message) => {
  fetchMock.mockImplementationOnce(() =>
    kind === 'non-error'
      ? Promise.reject('offline')
      : Promise.resolve(
          kind === 'invalid'
            ? new Response('{', { status: 503 })
            : json(kind === 'detail' ? { detail: 'specific error' } : {}, 503),
        ),
  );
  const hook = renderHook(() => useSubmission(options()));
  await act(async () => {
    await hook.result.current.execute('submit');
  });
  expect(hook.result.current.error).toBe(message);
});
it('finishes persistence synchronization after unmount without notifying the old UI', async () => {
  const config = options();
  const response = deferred<Response>();
  fetchMock.mockReturnValueOnce(response.promise);
  const hook = renderHook(() => useSubmission(config));
  let loading!: Promise<void>;
  act(() => {
    loading = hook.result.current.execute('submit');
  });
  hook.unmount();
  await act(async () => {
    response.resolve(json(graded));
    await loading;
  });
  expect(config.practice.refresh).toHaveBeenCalledOnce();
  expect(config.onCompleted).not.toHaveBeenCalled();
});
it.each(['problem', 'language'])(
  'does not attach a late result to a different %s',
  async (change) => {
    const config = options();
    const response = deferred<Response>();
    fetchMock.mockReturnValueOnce(response.promise);
    const hook = renderHook((props) => useSubmission(props), { initialProps: config });
    let loading!: Promise<void>;
    act(() => {
      loading = hook.result.current.execute('submit');
    });
    hook.rerender({
      ...config,
      problemId: change === 'problem' ? 'q' : 'p',
      language: change === 'language' ? 'java' : 'python',
    });
    await act(async () => {
      response.resolve(json(graded));
      await loading;
    });
    expect(hook.result.current.result).toBeNull();
    expect(hook.result.current.error).toBe('');
    expect(hook.result.current.busy).toBe(false);
  },
);
