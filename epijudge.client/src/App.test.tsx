import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { webcrypto } from 'node:crypto';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import App from './App';
import type { Problem, Result } from './workspaceModels';

// Exercise the real App, hooks, and persistence client together. Monaco is an
// external editor surface; its props are represented by an ordinary textarea.
vi.mock('./Editor', () => ({
  default: ({
    code,
    onChange,
    busy,
  }: {
    code: string;
    onChange(value: string): void;
    busy: boolean;
  }) => (
    <textarea
      aria-label="Test code editor"
      value={code}
      disabled={busy}
      onChange={(e) => onChange(e.target.value)}
    />
  ),
}));
const problem = (id: string, title: string): Problem => ({
  id,
  title,
  topic: 'Bits',
  difficulty: 'Unrated',
  description: 'A test exercise.',
  constraints: ['Return a count.'],
  signature: 'Count()',
  starterCode: 'C# starter',
  testCount: 3,
  examples: [],
  starters: Object.fromEntries(
    ['csharp', 'javascript', 'python', 'cpp', 'java'].map((language) => [
      language,
      {
        signature: language,
        starterCode: language + ' starter',
        filename: 'solution',
        runtime: language,
      },
    ]),
  ),
});
const graded: Result = {
  id: 'a',
  status: 'Accepted',
  passed: 3,
  total: 3,
  elapsedMs: 1,
  diagnostics: null,
  cases: [],
};
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status });
let fetchMock: ReturnType<typeof vi.fn>;
let progress: Array<{ problemId: string; status: string; acceptedLanguages: string[] }>;
let grade: Result;
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('crypto', webcrypto);
  progress = [];
  grade = graded;
  Object.defineProperty(HTMLDialogElement.prototype, 'showModal', {
    configurable: true,
    value: function (this: HTMLDialogElement) {
      this.open = true;
    },
  });
  Object.defineProperty(HTMLDialogElement.prototype, 'close', {
    configurable: true,
    value: function (this: HTMLDialogElement) {
      this.open = false;
    },
  });
  fetchMock = vi.fn(async (url: string, options?: RequestInit) => {
    if (url === '/api/problems')
      return json([problem('count_bits', 'Count Bits'), problem('parity', 'Parity')]);
    if (url === '/api/practice') return json({ drafts: [], progress });
    if (url.startsWith('/api/practice/history')) return json([]);
    if (options?.method === 'PUT') {
      const body = JSON.parse(options.body as string);
      return json({
        problemId: url.split('/').at(-2),
        language: url.split('/').at(-1),
        ...body,
        revision: body.revision + 1,
        updatedAt: 'now',
      });
    }
    if (url === '/api/submissions') {
      const body = JSON.parse(options!.body as string);
      progress = [
        {
          problemId: body.problemId,
          status: body.mode === 'submit' && grade.status === 'Accepted' ? 'solved' : 'attempted',
          acceptedLanguages: [],
        },
      ];
      return json(grade);
    }
    return json({});
  });
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
async function loaded() {
  render(<App />);
  const editor = await screen.findByRole('textbox', { name: 'Test code editor' });
  await waitFor(() => expect((editor as HTMLTextAreaElement).disabled).toBe(false));
  return editor;
}
it('loads the workspace, switches problem/language, and restores a per-language draft', async () => {
  const editor = await loaded();
  expect((editor as HTMLTextAreaElement).value).toBe('csharp starter');
  fireEvent.change(editor, { target: { value: 'my C# answer' } });
  fireEvent.change(screen.getByRole('combobox', { name: 'Select programming language' }), {
    target: { value: 'python' },
  });
  expect((editor as HTMLTextAreaElement).value).toBe('python starter');
  fireEvent.change(screen.getByRole('combobox', { name: 'Select programming language' }), {
    target: { value: 'csharp' },
  });
  expect((editor as HTMLTextAreaElement).value).toBe('my C# answer');
  fireEvent.click(screen.getByRole('button', { name: 'Toggle problem list' }));
  const dialog = screen.getByRole('dialog');
  fireEvent.click(within(dialog).getByRole('button', { name: '02. Parity — Not started' }));
  expect(await screen.findByRole('heading', { name: '2. Parity' })).toBeTruthy();
  // Flush explicitly before teardown so this test leaves no autosave timer behind.
  fireEvent.click(screen.getByRole('button', { name: 'Run Ctrl ↵' }));
  await waitFor(() =>
    expect(fetchMock.mock.calls.some(([url]) => url === '/api/submissions')).toBe(true),
  );
  await waitFor(() =>
    expect((screen.getByRole('button', { name: 'Submit' }) as HTMLButtonElement).disabled).toBe(
      false,
    ),
  );
});
it('opens reading from the filter, saves work, and retains the selection after remount', async () => {
  await loaded();
  fireEvent.click(screen.getByRole('button', { name: 'Toggle problem list' }));
  fireEvent.change(screen.getByRole('combobox', { name: 'Filter by topic or study plan' }), {
    target: { value: 'kind:reading' },
  });
  fireEvent.click(screen.getByRole('button', { name: /R01.*Reading companion/ }));
  const notes = screen.getByRole('textbox', { name: 'Your notes and design response' });
  expect(screen.queryByRole('button', { name: 'Submit' })).toBeNull();
  fireEvent.change(notes, { target: { value: 'A node is identified by its object identity.' } });
  fireEvent.click(screen.getByRole('button', { name: 'Mark reviewed' }));
  await waitFor(() =>
    expect(
      fetchMock.mock.calls.some(
        ([url, options]) =>
          url.endsWith('/reading-parent-pointer-lca/reading') && options?.method === 'PUT',
      ),
    ).toBe(true),
  );
  const call = fetchMock.mock.calls.find(([url]) =>
    url.endsWith('/reading-parent-pointer-lca/reading'),
  )!;
  const saved = {
    problemId: 'reading-parent-pointer-lca',
    language: 'reading',
    ...JSON.parse(call[1]!.body as string),
    revision: 1,
    updatedAt: 'now',
  };
  const previousFetch = fetchMock.getMockImplementation()! as (
    url: string,
    options?: RequestInit,
  ) => Promise<Response>;
  fetchMock.mockImplementation((url: string, options?: RequestInit) =>
    url === '/api/practice'
      ? Promise.resolve(json({ drafts: [saved], progress: [] }))
      : previousFetch(url, options),
  );
  cleanup();
  render(<App />);
  await waitFor(() =>
    expect(
      (
        screen.getByRole('textbox', {
          name: 'Your notes and design response',
        }) as HTMLTextAreaElement
      ).value,
    ).toContain('object identity'),
  );
  expect(screen.getByRole('button', { name: 'Undo review' })).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Toggle problem list' }));
  expect(screen.getByRole('button', { name: /R01.*reviewed/ }).classList.contains('reviewed')).toBe(
    true,
  );
  fireEvent.click(screen.getByRole('button', { name: /R02.*Reading companion/ }));
  expect(
    (screen.getByRole('textbox', { name: 'Your notes and design response' }) as HTMLTextAreaElement)
      .value,
  ).toBe('');
  fireEvent.click(screen.getByRole('button', { name: 'Previous problem' }));
  expect(
    (screen.getByRole('textbox', { name: 'Your notes and design response' }) as HTMLTextAreaElement)
      .value,
  ).toContain('object identity');
}, 15_000);
it.each([
  ['submit', 'Accepted', 'solved'],
  ['submit', 'Wrong answer', 'attempted'],
  ['run', 'Accepted', 'attempted'],
])('updates the nav after %s returns %s', async (mode, status, expected) => {
  grade = { ...graded, status, passed: status === 'Accepted' ? 3 : 0 };
  await loaded();
  fireEvent.click(
    screen.getByRole('button', { name: mode === 'submit' ? 'Submit' : 'Run Ctrl ↵' }),
  );
  await waitFor(() =>
    expect(fetchMock.mock.calls.some(([url]) => url === '/api/submissions')).toBe(true),
  );
  await waitFor(() =>
    expect((screen.getByRole('button', { name: 'Submit' }) as HTMLButtonElement).disabled).toBe(
      false,
    ),
  );
  fireEvent.click(screen.getByRole('button', { name: 'Toggle problem list' }));
  const row = screen.getByRole('button', { name: `01. Count Bits — ${expected}` });
  expect(row.classList.contains(expected)).toBe(true);
});
it.each(['count_bits', 'reading-shared-state'])(
  'shows catalog failures for %s instead of staying on Loading workspace',
  async (selected) => {
    localStorage.setItem('epi:selected', JSON.stringify(selected));
    fetchMock.mockResolvedValueOnce(json({}, 503));
    render(<App />);
    expect(await screen.findByRole('heading', { name: 'Couldn’t load the library' })).toBeTruthy();
  },
);
it('remembers the selected plan and steps through coding and reading in guide order', async () => {
  await loaded();
  fireEvent.click(screen.getByRole('button', { name: 'Toggle problem list' }));
  fireEvent.change(screen.getByRole('combobox', { name: 'Filter by topic or study plan' }), {
    target: { value: 'plan:3-days' },
  });
  expect(JSON.parse(localStorage.getItem('epi:libraryFilter')!)).toBe('plan:3-days');
  fireEvent.click(screen.getByRole('button', { name: 'Close problem list' }));
  // Count Bits is a bootcamp outside this plan. Next enters the plan at parity.
  fireEvent.click(screen.getByRole('button', { name: 'Next problem' }));
  expect(await screen.findByRole('heading', { name: '2. Parity' })).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Next problem' }));
  expect(
    await screen.findByRole('heading', { name: 'Shared state and interleavings' }),
  ).toBeTruthy();
  expect(screen.queryByRole('button', { name: 'Submit' })).toBeNull();
});

it('discards the retired tab preference and keeps navigation in the single plan list', async () => {
  localStorage.setItem('epi:studyPhase', JSON.stringify('Review'));
  localStorage.setItem('epi:libraryFilter', JSON.stringify('plan:3-days'));
  const storedAnswer = 'Unrelated saved answer';
  localStorage.setItem('epi:code:python:parity', JSON.stringify(storedAnswer));
  await loaded();
  expect(localStorage.getItem('epi:studyPhase')).toBeNull();
  expect(JSON.parse(localStorage.getItem('epi:code:python:parity')!)).toBe(storedAnswer);
  fireEvent.click(screen.getByRole('button', { name: 'Toggle problem list' }));
  const rows = within(screen.getByRole('navigation', { name: 'Problems' })).getAllByRole('button');
  expect(rows).toHaveLength(18);
  expect(screen.queryByRole('group', { name: 'Study plan workload' })).toBeNull();
  expect(screen.queryByRole('button', { name: /9.4/ })).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: 'Close problem list' }));
  fireEvent.click(screen.getByRole('button', { name: 'Next problem' }));
  expect(await screen.findByRole('heading', { name: '2. Parity' })).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Next problem' }));
  expect(
    await screen.findByRole('heading', { name: 'Shared state and interleavings' }),
  ).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Next problem' }));
  expect(
    await screen.findByRole('heading', { name: 'Design a constrained journey planner' }),
  ).toBeTruthy();
  expect((screen.getByRole('button', { name: 'Next problem' }) as HTMLButtonElement).disabled).toBe(
    true,
  );
});
