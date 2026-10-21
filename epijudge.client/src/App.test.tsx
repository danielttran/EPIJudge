import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { webcrypto } from 'node:crypto';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import App from './App';
import type { Problem, Result } from './workspaceModels';

// Exercise the real App, hooks, and persistence client together. Monaco is an
// external editor surface; its props are represented by an ordinary textarea.
vi.mock('./Editor', () => ({
  ReadOnlyCode: ({ code, label }: { code: string; label: string }) => (
    <pre aria-label={label}>
      <code>{code}</code>
    </pre>
  ),
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
    if (url.startsWith('/api/problems/') && url.includes('/solution?language='))
      return json({
        problemId: url.split('/')[3],
        language: new URL(url, 'http://local').searchParams.get('language'),
        code: `// Reference for ${url.split('/')[3]}`,
        explanation: 'Use the algorithm required by this question contract.',
        timeComplexity: 'O(n).',
        spaceComplexity: 'O(1).',
        attribution: 'Original test reference.',
      });
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
it.each(['csharp', 'javascript', 'python', 'cpp', 'java'])(
  'opens a clean %s starter with its relevant references collapsed',
  async (language) => {
    localStorage.setItem('epi:language', JSON.stringify(language));
    const previous = fetchMock.getMockImplementation()! as (
      url: string,
      options?: RequestInit,
    ) => Promise<Response>;
    const clean = problem('count_bits', 'Count Bits');
    clean.starters = Object.fromEntries(
      ['csharp', 'javascript', 'python', 'cpp', 'java'].map((id) => [
        id,
        {
          signature: id,
          starterCode: id + ' clean callable',
          filename: 'solution',
          runtime: id,
          codeFormat: 'callable-v1',
          references: [{ title: id + ' required API', code: id + ' helper', names: ['Required'] }],
        },
      ]),
    );
    fetchMock.mockImplementation((url: string, options?: RequestInit) =>
      url === '/api/problems' ? Promise.resolve(json([clean])) : previous(url, options),
    );
    const editor = (await loaded()) as HTMLTextAreaElement;
    expect(editor.value).toBe(language + ' clean callable');
    expect((screen.getByRole('combobox', { name: 'Code format' }) as HTMLSelectElement).value).toBe(
      'callable-v1',
    );
    expect(screen.getByText('Provided types and APIs').closest('details')!.open).toBe(false);
    fireEvent.click(screen.getByText('Provided types and APIs'));
    expect(
      (await screen.findByLabelText(language + ' required API provided reference')).textContent,
    ).toBe(language + ' helper');
    expect(fetchMock.mock.calls.some(([, options]) => options?.method === 'PUT')).toBe(false);
  },
);
it('keeps a legacy full-program draft unchanged until an explicit reset adopts the clean starter', async () => {
  const source = 'using System;\r\n// my saved λ code\r\nclass Solution {}';
  const clean = problem('count_bits', 'Count Bits');
  clean.starters!.csharp.codeFormat = 'callable-v1';
  const previous = fetchMock.getMockImplementation()! as (
    url: string,
    options?: RequestInit,
  ) => Promise<Response>;
  fetchMock.mockImplementation((url: string, options?: RequestInit) => {
    if (url === '/api/problems') return Promise.resolve(json([clean]));
    if (url === '/api/practice')
      return Promise.resolve(
        json({
          drafts: [
            {
              problemId: 'count_bits',
              language: 'csharp',
              code: source,
              revision: 4,
              updatedAt: 'now',
            },
          ],
          progress: [],
        }),
      );
    return previous(url, options);
  });
  const editor = (await loaded()) as HTMLTextAreaElement;
  // Textarea normalizes its visible line endings; persistence still carries the original string.
  expect(editor.value).toBe(source.replaceAll('\r\n', '\n'));
  expect((screen.getByRole('combobox', { name: 'Code format' }) as HTMLSelectElement).value).toBe(
    'legacy-v1',
  );
  expect(fetchMock.mock.calls.some(([, options]) => options?.method === 'PUT')).toBe(false);
  vi.stubGlobal(
    'confirm',
    vi.fn(() => true),
  );
  fireEvent.click(screen.getByRole('button', { name: 'Reset to starter code' }));
  expect(editor.value).toBe('csharp starter');
  expect((screen.getByRole('combobox', { name: 'Code format' }) as HTMLSelectElement).value).toBe(
    'callable-v1',
  );
  fireEvent.click(screen.getByRole('button', { name: 'Run Ctrl ↵' }));
  await waitFor(() =>
    expect(fetchMock.mock.calls.some(([url]) => url === '/api/submissions')).toBe(true),
  );
  const body = JSON.parse(
    fetchMock.mock.calls.find(([url]) => url === '/api/submissions')![1]!.body as string,
  );
  expect(body.code).toBe('csharp starter');
  expect(body.codeFormat).toBe('callable-v1');
});
it.each(['legacy-v1', 'callable-v1'] as const)(
  'restores historical %s source together with its execution format',
  async (format) => {
    const previous = fetchMock.getMockImplementation()! as (
      url: string,
      options?: RequestInit,
    ) => Promise<Response>;
    const attempt = {
      id: 'historical-format',
      problemId: 'count_bits',
      language: 'csharp',
      code: 'historical source ' + format,
      codeFormat: format,
      mode: 'submit',
      status: 'Accepted',
      passed: 3,
      total: 3,
      elapsedMs: 1,
      timestamp: '2026-01-01T00:00:00Z',
      sequence: 1,
      result: null,
      legacy: false,
    };
    fetchMock.mockImplementation((url: string, options?: RequestInit) => {
      if (url === '/api/practice/history/historical-format') return Promise.resolve(json(attempt));
      if (url.startsWith('/api/practice/history?')) return Promise.resolve(json([attempt]));
      return previous(url, options);
    });
    const editor = (await loaded()) as HTMLTextAreaElement;
    fireEvent.click(screen.getByRole('button', { name: 'History' }));
    fireEvent.click(await screen.findByRole('button', { name: 'View answer' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Restore to editor' }));
    expect(editor.value).toBe(attempt.code);
    expect((screen.getByRole('combobox', { name: 'Code format' }) as HTMLSelectElement).value).toBe(
      format,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Run Ctrl ↵' }));
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => url === '/api/submissions')).toBe(true),
    );
    const body = JSON.parse(
      fetchMock.mock.calls.find(([url]) => url === '/api/submissions')![1]!.body as string,
    );
    expect(body.code).toBe(attempt.code);
    expect(body.codeFormat).toBe(format);
  },
);
it('shows an archive failure while preserving the conflicted editor instead of discarding it', async () => {
  const previous = fetchMock.getMockImplementation()! as (
    url: string,
    options?: RequestInit,
  ) => Promise<Response>;
  fetchMock.mockImplementation((url: string, options?: RequestInit) =>
    options?.method === 'PUT'
      ? Promise.resolve(
          json(
            {
              draft: {
                problemId: 'count_bits',
                language: 'csharp',
                code: 'remote',
                revision: 9,
                updatedAt: 'now',
              },
            },
            409,
          ),
        )
      : previous(url, options),
  );
  const editor = (await loaded()) as HTMLTextAreaElement;
  fireEvent.change(editor, { target: { value: 'my retained source' } });
  const useSaved = await screen.findByRole('button', { name: 'Use saved version' });
  const setItem = Storage.prototype.setItem;
  const archive = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(function (
    this: Storage,
    key,
    value,
  ) {
    if (key.startsWith('epi:recovered:')) throw new DOMException('Full', 'QuotaExceededError');
    setItem.call(this, key, value);
  });
  fireEvent.click(useSaved);
  expect(await screen.findByText(/Could not preserve this browser copy/)).toBeTruthy();
  expect(editor.value).toBe('my retained source');
  expect(screen.getByRole('button', { name: 'Keep my version' })).toBeTruthy();
  archive.mockRestore();
});
it.each([
  [
    'legacy-v1',
    'callable-v1',
    'public class Solution\n{\n    public int CountBits(int x) { return 0; }\n}',
  ],
  ['callable-v1', 'legacy-v1', 'using System;\nclass CustomSupport { }\npublic class Solution { }'],
] as const)(
  'pastes source verbatim in %s mode and changes execution format only after explicit selection of %s',
  async (initialFormat, targetFormat, pastedCode) => {
    const previous = fetchMock.getMockImplementation()! as (
      url: string,
      options?: RequestInit,
    ) => Promise<Response>;
    const clean = problem('count_bits', 'Count Bits');
    clean.starters!.csharp.codeFormat = 'callable-v1';
    fetchMock.mockImplementation((url: string, options?: RequestInit) => {
      if (url === '/api/problems') return Promise.resolve(json([clean]));
      if (url === '/api/practice')
        return Promise.resolve(
          json({
            drafts: [
              {
                problemId: 'count_bits',
                language: 'csharp',
                code: 'previous saved source',
                codeFormat: initialFormat,
                revision: 7,
                updatedAt: 'now',
              },
            ],
            progress: [],
          }),
        );
      return previous(url, options);
    });
    const editor = (await loaded()) as HTMLTextAreaElement;
    const format = screen.getByRole('combobox', { name: 'Code format' }) as HTMLSelectElement;
    expect(format.value).toBe(initialFormat);
    fireEvent.change(editor, { target: { value: pastedCode } });
    expect(editor.value).toBe(pastedCode);
    expect(format.value).toBe(initialFormat);
    fireEvent.change(format, { target: { value: targetFormat } });
    expect(editor.value).toBe(pastedCode);
    expect(format.value).toBe(targetFormat);
    fireEvent.click(screen.getByRole('button', { name: 'Run Ctrl ↵' }));
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => url === '/api/submissions')).toBe(true),
    );
    const submitted = JSON.parse(
      fetchMock.mock.calls.find(([url]) => url === '/api/submissions')![1]!.body as string,
    );
    expect(submitted.code).toBe(pastedCode);
    expect(submitted.codeFormat).toBe(targetFormat);
    const saved = JSON.parse(
      fetchMock.mock.calls.filter(([, options]) => options?.method === 'PUT').at(-1)![1]!
        .body as string,
    );
    expect(saved.code).toBe(pastedCode);
    expect(saved.codeFormat).toBe(targetFormat);
  },
);
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

it('opens language-specific read-only solutions without overwriting saved drafts or changing the editor language', async () => {
  const editor = (await loaded()) as HTMLTextAreaElement;
  expect(fetchMock.mock.calls.some(([url]) => url.includes('/solution?language='))).toBe(false);
  fireEvent.change(editor, { target: { value: 'my independent C# draft' } });
  await waitFor(() =>
    expect(
      fetchMock.mock.calls.some(
        ([url, options]) => url.endsWith('/count_bits/csharp') && options?.method === 'PUT',
      ),
    ).toBe(true),
  );
  const writes = fetchMock.mock.calls.filter(([, options]) => options?.method === 'PUT').length;
  fireEvent.click(screen.getByRole('tab', { name: 'Solution' }));
  expect(await screen.findByLabelText('C# reference solution code')).toBeTruthy();
  expect(editor.value).toBe('my independent C# draft');
  expect(screen.queryByRole('button', { name: /copy.*editor|replace.*editor/i })).toBeNull();
  fireEvent.change(screen.getByRole('combobox', { name: 'Select programming language' }), {
    target: { value: 'python' },
  });
  expect(editor.value).toBe('python starter');
  expect(await screen.findByText('Python reference solution')).toBeTruthy();
  fireEvent.change(screen.getByRole('combobox', { name: 'Select programming language' }), {
    target: { value: 'csharp' },
  });
  expect(editor.value).toBe('my independent C# draft');
  fireEvent.click(screen.getByRole('tab', { name: 'Problem' }));
  expect(screen.getByRole('heading', { name: '1. Count Bits' })).toBeTruthy();
  expect(fetchMock.mock.calls.filter(([, options]) => options?.method === 'PUT')).toHaveLength(
    writes,
  );
  expect(fetchMock.mock.calls.some(([url]) => url === '/api/submissions')).toBe(false);
});

it('keeps the Solution view on selection changes and loads only the new question answer', async () => {
  const editor = (await loaded()) as HTMLTextAreaElement;
  fireEvent.click(screen.getByRole('tab', { name: 'Solution' }));
  expect(await screen.findByText('// Reference for count_bits')).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Next problem' }));
  expect(await screen.findByText('// Reference for parity')).toBeTruthy();
  expect(screen.queryByText('// Reference for count_bits')).toBeNull();
  expect(screen.getByRole('heading', { name: 'Parity — Solution' })).toBeTruthy();
  expect(editor.value).toBe('csharp starter');
  fireEvent.click(screen.getByRole('button', { name: 'Previous problem' }));
  expect(await screen.findByText('// Reference for count_bits')).toBeTruthy();
  expect(screen.getByRole('tab', { name: 'Solution' }).getAttribute('aria-selected')).toBe('true');
  expect(fetchMock.mock.calls.some(([, options]) => options?.method === 'PUT')).toBe(false);
});

it('supports keyboard tab navigation with associated panels and keeps editor focus separate', async () => {
  const editor = await loaded();
  const description = screen.getByRole('tab', { name: 'Problem' });
  const solution = screen.getByRole('tab', { name: 'Solution' });
  description.focus();
  fireEvent.keyDown(description, { key: 'ArrowRight' });
  expect(document.activeElement).toBe(solution);
  expect(solution.tabIndex).toBe(0);
  expect(description.tabIndex).toBe(-1);
  expect(await screen.findByRole('tabpanel', { name: 'Solution' })).toBeTruthy();
  expect(screen.queryByRole('tabpanel', { name: 'Problem' })).toBeNull();
  fireEvent.keyDown(solution, { key: 'ArrowLeft' });
  expect(document.activeElement).toBe(description);
  expect(screen.getByRole('tabpanel', { name: 'Problem' })).toBeTruthy();
  fireEvent.keyDown(description, { key: 'End' });
  expect(document.activeElement).toBe(solution);
  fireEvent.keyDown(solution, { key: 'Home' });
  expect(document.activeElement).toBe(description);
  fireEvent.keyDown(description, { key: 'x' });
  expect(document.activeElement).toBe(description);
  expect((editor as HTMLTextAreaElement).value).toBe('csharp starter');
});

it('renders independent Interview Cake attribution and a safe explicit source reference', async () => {
  const original = fetchMock.getMockImplementation()! as (
    url: string,
    options?: RequestInit,
  ) => Promise<Response>;
  fetchMock.mockImplementation((url: string, options?: RequestInit) =>
    url === '/api/problems'
      ? Promise.resolve(
          json([
            {
              ...problem('interviewcake_stock-price', 'Apple Stocks'),
              collection: 'interviewcake',
              position: 2,
              sourceAttribution:
                'Independently authored exercise based on the Interview Cake algorithm task. No affiliation.',
              sourceUrl: 'https://www.interviewcake.com/question/csharp/stock-price',
            },
          ]),
        )
      : original(url, options),
  );
  render(<App />);
  const source = await screen.findByRole('link', { name: 'Original task reference' });
  expect(source.getAttribute('href')).toBe(
    'https://www.interviewcake.com/question/csharp/stock-price',
  );
  expect(source.getAttribute('target')).toBe('_blank');
  expect(source.getAttribute('rel')).toBe('noopener noreferrer');
  expect(screen.getByText(/Independently authored exercise/)).toBeTruthy();
  expect(screen.getByRole('heading', { name: 'IC02. Apple Stocks' })).toBeTruthy();
});
