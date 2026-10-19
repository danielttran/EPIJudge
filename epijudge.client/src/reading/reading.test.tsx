import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { PracticeClient } from '../practiceClient';
import { ReadingWorkspace } from './ReadingWorkspace';
import { EMPTY_READING_JSON, parseReading, READING_LESSONS } from './readingLessons';
import { initialRace, stepRace } from './raceSimulation';
import { RaceSimulator } from './RaceSimulator';

afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.unstubAllGlobals();
});
it('rejects malformed reading documents and keeps valid Unicode notes', () => {
  for (const code of [
    'bad',
    'null',
    '{}',
    '{"version":2}',
    JSON.stringify({ ...parseReading(EMPTY_READING_JSON), notes: 'x'.repeat(20001) }),
    JSON.stringify({ ...parseReading(EMPTY_READING_JSON), answers: { quiz: -1 } }),
  ])
    expect(parseReading(code).notes).toBe('');
  expect(
    parseReading(JSON.stringify({ ...parseReading(EMPTY_READING_JSON), notes: 'λ 😀\nnotes' }))
      .notes,
  ).toBe('λ 😀\nnotes');
});
it('demonstrates a lost update and protects the complete increment with a lock', () => {
  let state = initialRace();
  for (const thread of [0, 1, 0, 1, 0, 1]) state = stepRace(state, thread, false);
  expect(state.counter).toBe(1);
  expect(stepRace(state, 0, false)).toBe(state);
  expect(stepRace(state, 3, false)).toBe(state);
  state = stepRace(initialRace(), 0, true);
  const blocked = stepRace(state, 1, true);
  expect(blocked.stages).toEqual([1, 0]);
  expect(blocked.log.at(-1)).toContain('waits');
  for (const thread of [0, 0, 1, 1, 1]) state = stepRace(state, thread, true);
  expect(state.counter).toBe(2);
});
it('resets the interactive simulator when lock policy changes', () => {
  render(<RaceSimulator />);
  fireEvent.click(screen.getByRole('button', { name: 'Step A (read)' }));
  fireEvent.click(screen.getByRole('button', { name: 'Step A (compute)' }));
  fireEvent.click(screen.getByRole('button', { name: 'Step A (write)' }));
  expect(screen.getByRole('status').textContent).toContain('1');
  fireEvent.click(screen.getByRole('checkbox'));
  expect(screen.getByRole('status').textContent).toContain('0');
  fireEvent.click(screen.getByRole('button', { name: 'Reset simulation' }));
  expect(screen.getByRole('button', { name: 'Step A (read)' })).toBeTruthy();
});
it('recovers an offline reading edit and offers both choices for a conflicting save', async () => {
  const lesson = READING_LESSONS[0];
  const local = JSON.stringify({ ...parseReading(EMPTY_READING_JSON), notes: 'offline notes' });
  const remote = JSON.stringify({ ...parseReading(EMPTY_READING_JSON), notes: 'other tab' });
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => {
      throw new Error('Offline');
    }),
  );
  const offline = new PracticeClient();
  await offline.initialize([{ id: lesson.id }]);
  offline.edit(lesson.id, 'reading', local);
  await offline.flush().catch(() => {});
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, options?: RequestInit) => {
      if (options?.method === 'PUT')
        return new Response(
          JSON.stringify({
            draft: {
              problemId: lesson.id,
              language: 'reading',
              code: remote,
              revision: 3,
              updatedAt: 'now',
            },
          }),
          { status: 409 },
        );
      return new Response(
        JSON.stringify(url === '/api/practice' ? { drafts: [], progress: [] } : {}),
      );
    }),
  );
  const recovered = new PracticeClient();
  await recovered.initialize([{ id: lesson.id }]);
  await waitFor(() => expect(recovered.conflict(lesson.id, 'reading')).toBeTruthy());
  const view = render(<ReadingWorkspace lesson={lesson} practice={recovered} />);
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('offline notes');
  expect(screen.getByRole('button', { name: 'Keep my version' })).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Use saved version' }));
  view.rerender(<ReadingWorkspace lesson={lesson} practice={recovered} />);
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('other tab');
});
it('autosaves notes, checkpoints, quiz answers, and review status, restoring them after reconnect', async () => {
  const lesson = READING_LESSONS[0];
  let saved: unknown[] = [];
  const fetchMock = vi.fn(async (url: string, options?: RequestInit) => {
    if (options?.method === 'PUT') {
      const body = JSON.parse(options.body as string);
      const draft = {
        problemId: lesson.id,
        language: 'reading',
        code: body.code,
        revision: body.revision + 1,
        updatedAt: '2026-10-19T00:00:00Z',
      };
      saved = [draft];
      return new Response(JSON.stringify(draft));
    }
    return new Response(
      JSON.stringify(url === '/api/practice' ? { drafts: saved, progress: [] } : {}),
    );
  });
  vi.stubGlobal('fetch', fetchMock);
  const practice = new PracticeClient();
  await practice.initialize([{ id: lesson.id }]);
  const view = render(<ReadingWorkspace lesson={lesson} practice={practice} />);
  const redraw = () => view.rerender(<ReadingWorkspace lesson={lesson} practice={practice} />);
  fireEvent.change(screen.getByRole('textbox', { name: 'Your notes and design response' }), {
    target: { value: 'Compare identities, not values. λ' },
  });
  redraw();
  fireEvent.click(screen.getByRole('checkbox', { name: lesson.checkpoints[0].label }));
  redraw();
  fireEvent.click(
    screen.getByRole('radio', { name: lesson.quizzes[0].options[lesson.quizzes[0].correctIndex] }),
  );
  redraw();
  expect(screen.getByText(/Correct\./)).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Mark reviewed' }));
  redraw();
  await practice.flush();
  expect(practice.progress).toEqual({});
  const restored = new PracticeClient();
  await restored.initialize([{ id: lesson.id }]);
  view.rerender(<ReadingWorkspace lesson={lesson} practice={restored} />);
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toContain('λ');
  expect(
    (screen.getByRole('checkbox', { name: lesson.checkpoints[0].label }) as HTMLInputElement)
      .checked,
  ).toBe(true);
  expect(screen.getByRole('button', { name: 'Undo review' })).toBeTruthy();
  expect(parseReading(restored.codeFor(lesson.id, 'reading', EMPTY_READING_JSON)).reviewed).toBe(
    true,
  );
  fireEvent.click(screen.getByRole('button', { name: 'Undo review' }));
  await restored.flush();
  await waitFor(() =>
    expect(parseReading(restored.codeFor(lesson.id, 'reading', EMPTY_READING_JSON)).reviewed).toBe(
      false,
    ),
  );
});
it('renders every lesson as HTML with no external raw-HTML execution', () => {
  const practice = new PracticeClient();
  practice.ready = true;
  for (const lesson of READING_LESSONS) {
    const view = render(
      <ReadingWorkspace
        lesson={{
          ...lesson,
          body:
            lesson.body + '\n<script>alert(1)</script>\n<a href="javascript:alert(1)">unsafe</a>',
        }}
        practice={practice}
      />,
    );
    expect(screen.getByRole('heading', { name: lesson.title })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Core idea' })).toBeTruthy();
    expect(view.container.querySelector('script')).toBeNull();
    expect(view.container.querySelector('a[href^="javascript:"]')).toBeNull();
    view.unmount();
  }
});
