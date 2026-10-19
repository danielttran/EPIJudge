import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { ProblemLibrary } from './ProblemLibrary';
import { HistoryPanel } from './HistoryPanel';
import { PracticeClient } from './practiceClient';
import type { Attempt, Problem } from './workspaceModels';
import type { useSubmissionHistory } from './useSubmissionHistory';

const problems = [
  { id: 'bits', title: 'Count Bits', topic: 'Bits' },
  { id: 'parity', title: 'Parity', topic: 'Bits' },
  { id: 'anagrams', title: 'Anagrams', topic: 'Strings' },
] as Problem[];
beforeEach(() => {
  // jsdom has no top-layer dialog implementation; emulate only its open/close API.
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
});
afterEach(cleanup);
function library(open = true) {
  const practice = new PracticeClient();
  practice.ready = true;
  practice.progress = {
    bits: { problemId: 'bits', status: 'solved', acceptedLanguages: ['python'] },
    parity: { problemId: 'parity', status: 'attempted', acceptedLanguages: [] },
  };
  const props = {
    open,
    problems,
    selected: 'bits',
    busy: false,
    practice,
    storageNotice: '',
    filter: '',
    onFilterChange: vi.fn((value: string) => {
      props.filter = value;
      view.rerender(<ProblemLibrary {...props} />);
    }),
    onClose: vi.fn(),
    onSelect: vi.fn(),
    onExport: vi.fn(async () => {}),
    onImport: vi.fn(async (_file: File) => {}),
  };
  const view = render(<ProblemLibrary {...props} />);
  return { props, ...view };
}
it('opens and closes the drawer using the native dialog lifecycle', () => {
  const { props, rerender } = library(false);
  const dialog = screen.getByRole('dialog', { hidden: true }) as HTMLDialogElement;
  expect(dialog.open).toBe(false);
  rerender(<ProblemLibrary {...props} open />);
  expect(dialog.open).toBe(true);
  fireEvent.click(screen.getByRole('button', { name: 'Close problem list' }));
  expect(props.onClose).toHaveBeenCalledOnce();
  rerender(<ProblemLibrary {...props} open={false} />);
  expect(dialog.open).toBe(false);
});
it('renders solved and attempted problem markers, filters the list, and selects a problem', () => {
  const { props } = library();
  const solved = screen.getByRole('button', { name: '01. Count Bits — solved' });
  const attempted = screen.getByRole('button', { name: '02. Parity — attempted' });
  expect(solved.classList.contains('solved')).toBe(true);
  expect(attempted.classList.contains('attempted')).toBe(true);
  expect(solved.getAttribute('aria-current')).toBe('page');
  fireEvent.change(screen.getByRole('textbox', { name: 'Search problems' }), {
    target: { value: 'ana' },
  });
  expect(screen.queryByRole('button', { name: '01. Count Bits — solved' })).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: '03. Anagrams — Not started' }));
  expect(props.onSelect).toHaveBeenCalledWith('anagrams');
  expect(props.onClose).toHaveBeenCalledOnce();
  fireEvent.change(screen.getByRole('combobox', { name: 'Filter by topic or study plan' }), {
    target: { value: 'Bits' },
  });
  expect(screen.getByText('No matching problems.')).toBeTruthy();
});
it('offers all four plans, uses guide order, and opens reading companions', () => {
  const { props } = library();
  const select = screen.getByRole('combobox', { name: 'Filter by topic or study plan' });
  for (const name of [
    '3 days — Hackathon',
    '7 days — Finals cram',
    '1 month — Term project',
    '4 months — Algorithms class',
  ])
    expect(screen.getByRole('option', { name })).toBeTruthy();
  fireEvent.change(select, { target: { value: 'plan:3-days' } });
  expect(props.onFilterChange).toHaveBeenCalledWith('plan:3-days');
  const buttons = screen.getByRole('navigation', { name: 'Problems' }).querySelectorAll('button');
  expect(buttons[0].textContent).toContain('4.1. Computing the parity');
  expect(buttons[0].disabled).toBe(false);
  expect(buttons).toHaveLength(18);
  expect(screen.queryByRole('group', { name: 'Study plan workload' })).toBeNull();
  expect(screen.queryByRole('button', { name: /^Review/ })).toBeNull();
  expect(screen.queryByRole('button', { name: /9.4/ })).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: /19.3.*Reading companion/ }));
  expect(props.onSelect).toHaveBeenCalledWith('reading-shared-state');
  expect(screen.getByText(/Follow this list in order/)).toBeTruthy();
  expect(screen.getByRole('dialog').textContent).not.toMatch(/2019/);
});
it('disables problem selection and import while grading, and invokes backup actions', async () => {
  const { props, rerender } = library();
  fireEvent.click(screen.getByRole('button', { name: 'Export answers' }));
  expect(props.onExport).toHaveBeenCalledOnce();
  const file = new File(['{}'], 'backup.json', { type: 'application/json' });
  fireEvent.change(screen.getByLabelText('Import answers file'), { target: { files: [file] } });
  await waitFor(() => expect(props.onImport).toHaveBeenCalledWith(file));
  rerender(<ProblemLibrary {...props} busy />);
  expect(
    (screen.getByRole('button', { name: 'Import answers' }) as HTMLButtonElement).disabled,
  ).toBe(true);
  expect(
    (screen.getByRole('button', { name: '02. Parity — attempted' }) as HTMLButtonElement).disabled,
  ).toBe(true);
});
const attempt = {
  id: 'a',
  problemId: 'bits',
  language: 'python',
  code: 'saved source',
  mode: 'submit',
  status: 'Accepted',
  passed: 3,
  total: 3,
  elapsedMs: 1,
  timestamp: '2026-01-01T00:00:00Z',
  legacy: false,
  sequence: 1,
  result: null,
} as Attempt;
function history(viewedAttempt: Attempt | null = null) {
  const state = {
    attempts: [attempt],
    historyError: '',
    hasMoreHistory: true,
    viewedAttempt,
    viewAnswer: vi.fn(async (_a: Attempt) => {}),
    loadOlder: vi.fn(async () => {}),
    closeAnswer: vi.fn(),
  } satisfies ReturnType<typeof useSubmissionHistory>;
  const props = { history: state, busy: false, onRetry: vi.fn(), onRestore: vi.fn() };
  return { props, ...render(<HistoryPanel {...props} />) };
}
it('opens historical answers, paginates, and restores the exact saved snapshot', () => {
  const { props } = history(attempt);
  expect(screen.getByLabelText('Saved answer code').textContent).toBe('saved source');
  fireEvent.click(screen.getByRole('button', { name: 'View answer' }));
  expect(props.history.viewAnswer).toHaveBeenCalledWith(attempt);
  fireEvent.click(screen.getByRole('button', { name: 'Load older attempts' }));
  expect(props.history.loadOlder).toHaveBeenCalledOnce();
  fireEvent.click(screen.getByRole('button', { name: 'Restore to editor' }));
  expect(props.onRestore).toHaveBeenCalledWith(attempt);
  expect(props.history.closeAnswer).toHaveBeenCalledOnce();
});
it('explains legacy summaries and prevents restoring source that was never saved', () => {
  history({ ...attempt, language: null, code: null, legacy: true });
  expect(screen.getByText(/original code was not saved/)).toBeTruthy();
  expect(screen.queryByRole('button', { name: 'Restore to editor' })).toBeNull();
});
it('shows retry and empty-history states', () => {
  const { props, rerender } = history();
  rerender(
    <HistoryPanel
      {...props}
      history={{ ...props.history, attempts: [], historyError: 'offline' }}
    />,
  );
  expect(screen.getByText('Your attempts live here')).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Retry history' }));
  expect(props.onRetry).toHaveBeenCalledOnce();
});
