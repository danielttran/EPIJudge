import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { SolutionPanel } from './SolutionPanel';

vi.mock('./Editor', () => ({
  ReadOnlyCode: ({ code, label }: { code: string; label: string }) => (
    <pre aria-label={label}>
      <code>{code}</code>
    </pre>
  ),
}));

const answer = (problemId: string, code = 'public class Solution { }', language = 'csharp') => ({
  problemId,
  language,
  code,
  explanation: 'Keep a running count while consuming each bit.',
  timeComplexity: 'O(b), where b is the number of set bits.',
  spaceComplexity: 'O(1).',
  attribution: 'Original C# implementation for EPI Practice.',
});
const response = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status });
let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  fetchMock = vi.fn();
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
it('loads only the selected local endpoint and renders selectable code, approach, complexity and attribution', async () => {
  fetchMock.mockResolvedValue(response(answer('count_bits')));
  render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
  expect(screen.getByRole('status').textContent).toContain('Loading C# solution');
  expect(await screen.findByText('C# reference solution')).toBeTruthy();
  expect(fetchMock).toHaveBeenCalledWith('/api/problems/count_bits/solution?language=csharp', {
    signal: expect.any(AbortSignal),
  });
  expect(screen.getByLabelText('C# reference solution code').textContent).toBe(
    answer('count_bits').code,
  );
  expect(screen.getByLabelText('C# reference solution code').tagName).toBe('PRE');
  expect(screen.getByText(answer('count_bits').explanation)).toBeTruthy();
  expect(screen.getByText(answer('count_bits').timeComplexity)).toBeTruthy();
  expect(screen.getByText(answer('count_bits').spaceComplexity)).toBeTruthy();
  expect(screen.getByText(answer('count_bits').attribution)).toBeTruthy();
  expect(screen.queryByRole('textbox')).toBeNull();
  expect(screen.queryByRole('button', { name: /editor/i })).toBeNull();
});
it('shows required references separately and copies only the visible callable implementation', async () => {
  const writeText = vi.fn(async () => {});
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
  fetchMock.mockResolvedValue(
    response({
      ...answer('count_bits', 'public int CountBits(int x) {\n    return 0;\n}'),
      codeFormat: 'callable-v1',
      references: [{ title: 'Required API', code: 'int Helper();', names: ['Helper'] }],
    }),
  );
  render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
  await screen.findByLabelText('C# reference solution code');
  expect(screen.getByText('Provided types and APIs').closest('details')!.open).toBe(false);
  fireEvent.click(screen.getByText('Provided types and APIs'));
  expect((await screen.findByLabelText('Required API provided reference')).textContent).toBe(
    'int Helper();',
  );
  fireEvent.click(screen.getByRole('button', { name: 'Copy code' }));
  await screen.findByText('Code copied.');
  expect(writeText).toHaveBeenCalledWith('public int CountBits(int x) {\n    return 0;\n}');
});
it('treats a missing solution as unavailable without rendering an empty code block', async () => {
  fetchMock.mockResolvedValue(response({}, 404));
  render(<SolutionPanel problemId="unknown" title="Unknown" language="csharp" />);
  expect(await screen.findByText('A C# solution is not available for this question.')).toBeTruthy();
  expect(screen.queryByLabelText('C# reference solution code')).toBeNull();
});
it.each(['http', 'network', 'malformed', 'wrong question', 'wrong language'])(
  'shows a retryable error for %s failure and recovers',
  async (failure) => {
    if (failure === 'http') fetchMock.mockResolvedValueOnce(response({}, 503));
    else if (failure === 'network') fetchMock.mockRejectedValueOnce(new Error('Disconnected'));
    else if (failure === 'malformed') fetchMock.mockResolvedValueOnce(response({}));
    else if (failure === 'wrong question')
      fetchMock.mockResolvedValueOnce(response(answer('parity')));
    else fetchMock.mockResolvedValueOnce(response({ ...answer('count_bits'), language: 'python' }));
    fetchMock.mockResolvedValueOnce(response(answer('count_bits')));
    render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(screen.queryByLabelText('C# reference solution code')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Retry solution' }));
    expect(await screen.findByLabelText('C# reference solution code')).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  },
);
it('aborts the previous selection and ignores its late answer even when the transport ignores abort', async () => {
  let finishFirst!: (result: Response) => void;
  fetchMock.mockImplementationOnce(
    () =>
      new Promise<Response>((resolve) => {
        finishFirst = resolve;
      }),
  );
  fetchMock.mockResolvedValueOnce(response(answer('parity', 'Parity answer')));
  const view = render(
    <SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />,
  );
  const firstSignal = fetchMock.mock.calls[0][1].signal as AbortSignal;
  view.rerender(<SolutionPanel problemId="parity" title="Parity" language="csharp" />);
  expect(firstSignal.aborted).toBe(true);
  expect(await screen.findByLabelText('C# reference solution code')).toBeTruthy();
  await act(async () => {
    finishFirst(response(answer('count_bits', 'Stale answer')));
  });
  expect(screen.getByLabelText('C# reference solution code').textContent).toBe('Parity answer');
  expect(screen.queryByText('Stale answer')).toBeNull();
});
it('clears the previous answer immediately while another question is loading', async () => {
  fetchMock.mockResolvedValueOnce(response(answer('count_bits', 'First answer')));
  fetchMock.mockImplementationOnce(() => new Promise<Response>(() => {}));
  const view = render(
    <SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />,
  );
  await screen.findByText('First answer');
  view.rerender(<SolutionPanel problemId="parity" title="Parity" language="csharp" />);
  expect(screen.queryByText('First answer')).toBeNull();
  expect(screen.getByRole('status').textContent).toContain('Loading');
  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
});
it('aborts loading on unmount and ignores its late rejection', async () => {
  let reject!: (reason: Error) => void;
  fetchMock.mockImplementationOnce(
    () =>
      new Promise<Response>((_, fail) => {
        reject = fail;
      }),
  );
  const view = render(
    <SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />,
  );
  const signal = fetchMock.mock.calls[0][1].signal as AbortSignal;
  view.unmount();
  expect(signal.aborted).toBe(true);
  await act(async () => {
    reject(new Error('late failure'));
  });
  expect(screen.queryByRole('alert')).toBeNull();
});

it.each([
  ['csharp', 'C#'],
  ['javascript', 'JavaScript'],
  ['python', 'Python'],
  ['cpp', 'C++'],
  ['java', 'Java'],
])(
  'loads and labels the %s solution requested by the selected editor language',
  async (language, label) => {
    const code = language + ' algorithm source';
    fetchMock.mockResolvedValue(response(answer('count_bits', code, language)));
    render(<SolutionPanel problemId="count_bits" title="Count Bits" language={language} />);
    expect(await screen.findByLabelText(label + ' reference solution code')).toBeTruthy();
    expect(screen.getByLabelText(label + ' reference solution code').textContent).toBe(code);
    expect(screen.getByText(label + ' reference solution')).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/problems/count_bits/solution?language=' + language,
      {
        signal: expect.any(AbortSignal),
      },
    );
  },
);

it('aborts the previous language and ignores a late answer for the same problem in that language', async () => {
  let finishFirst!: (result: Response) => void;
  fetchMock.mockImplementationOnce(
    () =>
      new Promise<Response>((resolve) => {
        finishFirst = resolve;
      }),
  );
  fetchMock.mockResolvedValueOnce(response(answer('count_bits', 'Python algorithm', 'python')));
  const view = render(
    <SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />,
  );
  const firstSignal = fetchMock.mock.calls[0][1].signal as AbortSignal;
  view.rerender(<SolutionPanel problemId="count_bits" title="Count Bits" language="python" />);
  expect(firstSignal.aborted).toBe(true);
  expect(await screen.findByLabelText('Python reference solution code')).toBeTruthy();
  await act(async () => {
    finishFirst(response(answer('count_bits', 'Stale C# algorithm')));
  });
  expect(screen.getByLabelText('Python reference solution code').textContent).toBe(
    'Python algorithm',
  );
  expect(screen.queryByLabelText('C# reference solution code')).toBeNull();
  expect(screen.queryByText('Stale C# algorithm')).toBeNull();
});

it('clears a visible answer immediately when the editor language changes', async () => {
  fetchMock.mockResolvedValueOnce(response(answer('count_bits', 'C# algorithm')));
  fetchMock.mockImplementationOnce(() => new Promise<Response>(() => {}));
  const view = render(
    <SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />,
  );
  await screen.findByText('C# algorithm');
  view.rerender(<SolutionPanel problemId="count_bits" title="Count Bits" language="java" />);
  expect(screen.queryByText('C# algorithm')).toBeNull();
  expect(screen.getByRole('status').textContent).toContain('Loading Java solution');
});

it('renders authored walkthrough, correctness, complexity and edge cases as separate sections', async () => {
  const rich = {
    ...answer('count_bits'),
    walkthrough: 'For x = 7, clearing the lowest bit visits 7, 6, 4, 0 and counts three bits.',
    correctness:
      'Each iteration removes exactly one set bit; termination at zero counts all set bits.',
    edgeCases: ['Zero returns zero.', 'Negative inputs use their 32-bit representation.'],
  };
  fetchMock.mockResolvedValue(response(rich));
  render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
  await screen.findByLabelText('C# reference solution code');
  for (const name of [
    'Approach',
    'Walkthrough',
    'Implementation',
    'Correctness',
    'Complexity',
    'Edge cases',
  ])
    expect(screen.getByRole('heading', { name })).toBeTruthy();
  expect(screen.getByText(rich.walkthrough)).toBeTruthy();
  expect(screen.getByText(rich.correctness)).toBeTruthy();
  for (const item of rich.edgeCases) expect(screen.getByText(item)).toBeTruthy();
});

it('uses the selected problem example when an optional authored walkthrough is unavailable', async () => {
  fetchMock.mockResolvedValue(
    response({ ...answer('count_bits'), walkthrough: null, correctness: null, edgeCases: null }),
  );
  render(
    <SolutionPanel
      problemId="count_bits"
      title="Count Bits"
      language="csharp"
      example={{ input: 'x = 7', output: '3', explanation: 'All three binary digits are set.' }}
    />,
  );
  expect(await screen.findByText('x = 7')).toBeTruthy();
  expect(screen.getByText('3')).toBeTruthy();
  expect(screen.getByText('All three binary digits are set.')).toBeTruthy();
  expect(screen.queryByRole('heading', { name: 'Correctness' })).toBeNull();
});

it('reports copying only after the clipboard has accepted the exact source', async () => {
  const previous = Object.getOwnPropertyDescriptor(navigator, 'clipboard');
  let complete!: () => void;
  const writeText = vi.fn(
    () =>
      new Promise<void>((resolve) => {
        complete = resolve;
      }),
  );
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
  try {
    fetchMock.mockResolvedValue(response(answer('count_bits')));
    render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
    await screen.findByLabelText('C# reference solution code');
    fireEvent.click(screen.getByRole('button', { name: 'Copy code' }));
    expect(writeText).toHaveBeenCalledWith(answer('count_bits').code);
    expect(screen.queryByText('Code copied.')).toBeNull();
    await act(async () => {
      complete();
    });
    expect(screen.getByRole('status').textContent).toBe('Code copied.');
  } finally {
    if (previous) Object.defineProperty(navigator, 'clipboard', previous);
    else Reflect.deleteProperty(navigator, 'clipboard');
  }
});

it.each(['denied', 'unavailable'])(
  'reports clipboard %s without a copied message or editor writes',
  async (failure) => {
    const previous = Object.getOwnPropertyDescriptor(navigator, 'clipboard');
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value:
        failure === 'denied'
          ? { writeText: vi.fn().mockRejectedValue(new Error('Denied')) }
          : undefined,
    });
    try {
      fetchMock.mockResolvedValue(response(answer('count_bits')));
      render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
      await screen.findByLabelText('C# reference solution code');
      fireEvent.click(screen.getByRole('button', { name: 'Copy code' }));
      expect((await screen.findByRole('alert')).textContent).toContain('Could not copy.');
      expect(screen.queryByText('Code copied.')).toBeNull();
      expect(fetchMock).toHaveBeenCalledTimes(1);
    } finally {
      if (previous) Object.defineProperty(navigator, 'clipboard', previous);
      else Reflect.deleteProperty(navigator, 'clipboard');
    }
  },
);

it('does not show a stale clipboard success after the language has changed', async () => {
  const previous = Object.getOwnPropertyDescriptor(navigator, 'clipboard');
  let complete!: () => void;
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: {
      writeText: () =>
        new Promise<void>((resolve) => {
          complete = resolve;
        }),
    },
  });
  try {
    fetchMock.mockResolvedValueOnce(response(answer('count_bits')));
    fetchMock.mockResolvedValueOnce(response(answer('count_bits', 'Python source', 'python')));
    const view = render(
      <SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />,
    );
    await screen.findByLabelText('C# reference solution code');
    fireEvent.click(screen.getByRole('button', { name: 'Copy code' }));
    view.rerender(<SolutionPanel problemId="count_bits" title="Count Bits" language="python" />);
    await screen.findByLabelText('Python reference solution code');
    await act(async () => {
      complete();
    });
    expect(screen.queryByText('Code copied.')).toBeNull();
    expect(screen.getByLabelText('Python reference solution code').textContent).toBe(
      'Python source',
    );
  } finally {
    if (previous) Object.defineProperty(navigator, 'clipboard', previous);
    else Reflect.deleteProperty(navigator, 'clipboard');
  }
});

it.each([
  { walkthrough: 7 },
  { correctness: false },
  { edgeCases: 'not an array' },
  { edgeCases: [7] },
])(
  'rejects malformed optional explanation metadata %# instead of rendering it as a proof',
  async (badMetadata) => {
    fetchMock.mockResolvedValue(response({ ...answer('count_bits'), ...badMetadata }));
    render(<SolutionPanel problemId="count_bits" title="Count Bits" language="csharp" />);
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(screen.queryByLabelText('C# reference solution code')).toBeNull();
  },
);
