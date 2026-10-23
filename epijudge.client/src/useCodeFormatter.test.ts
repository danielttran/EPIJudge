import { act, renderHook } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { useCodeFormatter } from './useCodeFormatter';

const json = (code: string) => new Response(JSON.stringify({ code }));
function deferred() {
  let resolve!: (value: Response) => void;
  const promise = new Promise<Response>((done) => (resolve = done));
  return { promise, resolve };
}
function setup(language = 'javascript') {
  let snapshot = { code: 'unformatted source', version: 1 };
  const apply = vi.fn((code: string) => {
    snapshot = { code, version: snapshot.version + 1 };
  });
  const options = {
    scope: 'count_bits:' + language,
    language,
    codeFormat: 'callable-v1' as const,
    busy: false,
    read: () => snapshot,
    apply,
  };
  const hook = renderHook((p) => useCodeFormatter(p), { initialProps: options });
  return {
    hook,
    options,
    apply,
    edit: (code = 'new draft') => {
      snapshot = { code, version: snapshot.version + 1 };
    },
    read: () => snapshot,
  };
}
afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});
it.each(['csharp', 'javascript', 'python', 'cpp', 'java'])(
  'requests local formatting for %s and applies only a successful result',
  async (language) => {
    const fetcher = vi.fn(async (_url: string, _options: RequestInit) => json('formatted source'));
    vi.stubGlobal('fetch', fetcher);
    const { hook, apply } = setup(language);
    await act(() => hook.result.current.format());
    expect(fetcher.mock.calls[0][0]).toBe('/api/code/format');
    expect(JSON.parse(fetcher.mock.calls[0][1].body as string).language).toBe(language);
    expect(apply).toHaveBeenCalledOnce();
    expect(hook.result.current.message).toContain('Undo');
  },
);
it('coalesces repeated clicks while a request is pending', async () => {
  const next = deferred();
  const fetcher = vi.fn(() => next.promise);
  vi.stubGlobal('fetch', fetcher);
  const { hook } = setup();
  let running: Promise<void>;
  act(() => {
    running = hook.result.current.format();
    void hook.result.current.format();
  });
  expect(fetcher).toHaveBeenCalledOnce();
  await act(async () => {
    next.resolve(json('formatted'));
    await running;
  });
});
it.each(['edit', 'edit-and-undo', 'problem', 'language', 'code-format', 'busy', 'unmount'])(
  'discards stale results after %s',
  async (change) => {
    const next = deferred();
    vi.stubGlobal('fetch', () => next.promise);
    const { hook, options, apply, edit } = setup();
    let running: Promise<void>;
    act(() => {
      running = hook.result.current.format();
    });
    if (change === 'edit') edit();
    if (change === 'edit-and-undo') {
      edit();
      edit('unformatted source');
    }
    if (change === 'problem' || change === 'language' || change === 'code-format')
      hook.rerender({ ...options, scope: change });
    if (change === 'busy') hook.rerender({ ...options, busy: true });
    if (change === 'unmount') hook.unmount();
    await act(async () => {
      next.resolve(json('formatted'));
      await running;
    });
    expect(apply).not.toHaveBeenCalled();
  },
);
it.each([400, 503])('leaves invalid/incomplete code untouched on HTTP %s', async (status) => {
  vi.stubGlobal(
    'fetch',
    async () => new Response(JSON.stringify({ message: 'Cannot format this code.' }), { status }),
  );
  const { hook, apply, read } = setup();
  await act(() => hook.result.current.format());
  expect(apply).not.toHaveBeenCalled();
  expect(read().code).toBe('unformatted source');
  expect(hook.result.current.message).toBe('Cannot format this code.');
});
it('does not create an undo edit for an already formatted document', async () => {
  vi.stubGlobal('fetch', async () => json('unformatted source'));
  const { hook, apply } = setup();
  await act(() => hook.result.current.format());
  expect(apply).not.toHaveBeenCalled();
  expect(hook.result.current.message).toBe('Already formatted.');
});
it('does not apply a late response even when a transport ignores timeout cancellation', async () => {
  vi.useFakeTimers();
  const next = deferred();
  vi.stubGlobal('fetch', () => next.promise);
  const { hook, apply } = setup();
  let running: Promise<void>;
  act(() => {
    running = hook.result.current.format();
  });
  act(() => vi.advanceTimersByTime(15000));
  await act(async () => {
    next.resolve(json('late source'));
    await running;
  });
  expect(apply).not.toHaveBeenCalled();
  expect(hook.result.current.message).toContain('cancelled');
});
it('keeps source on network and malformed-response errors', async () => {
  vi.stubGlobal('fetch', async () => {
    throw new Error('Offline');
  });
  const { hook, apply } = setup();
  await act(() => hook.result.current.format());
  expect(apply).not.toHaveBeenCalled();
  expect(hook.result.current.message).toContain('Offline');
  vi.stubGlobal('fetch', async () => json(''));
  await act(() => hook.result.current.format());
  expect(apply).not.toHaveBeenCalled();
});

it('does not let an old completion clear a newer request or replace its document', async () => {
  const first = deferred(),
    second = deferred();
  vi.stubGlobal(
    'fetch',
    vi.fn().mockReturnValueOnce(first.promise).mockReturnValueOnce(second.promise),
  );
  const { hook, options, apply } = setup();
  let a: Promise<void>, b: Promise<void>;
  act(() => {
    a = hook.result.current.format();
  });
  hook.rerender({ ...options, scope: 'parity:javascript' });
  act(() => {
    b = hook.result.current.format();
  });
  await act(async () => {
    first.resolve(json('stale'));
    await a;
  });
  expect(hook.result.current.pending).toBe(true);
  expect(apply).not.toHaveBeenCalled();
  await act(async () => {
    second.resolve(json('new document formatted'));
    await b;
  });
  expect(apply).toHaveBeenCalledOnce();
  expect(hook.result.current.pending).toBe(false);
});
it('does not request formatting for an empty or busy document', async () => {
  const fetcher = vi.fn();
  vi.stubGlobal('fetch', fetcher);
  const { hook, edit, options } = setup();
  edit('  ');
  await act(() => hook.result.current.format());
  expect(hook.result.current.message).toBe('Enter code to format.');
  hook.rerender({ ...options, busy: true });
  await act(() => hook.result.current.format());
  expect(fetcher).not.toHaveBeenCalled();
});

it('clears stale diagnostics when the editor reports an edit', async () => {
  vi.stubGlobal(
    'fetch',
    async () => new Response(JSON.stringify({ message: 'Invalid syntax' }), { status: 400 }),
  );
  const { hook } = setup();
  await act(() => hook.result.current.format());
  expect(hook.result.current.message).toBe('Invalid syntax');
  act(() => hook.result.current.clearMessage());
  expect(hook.result.current.message).toBe('');
});
