import { useEffect, useRef, useState } from 'react';
import { Check, Copy, LoaderCircle } from 'lucide-react';
import { ReadOnlyCode } from './Editor';

const LANGUAGE_NAMES: Record<string, string> = {
  csharp: 'C#',
  javascript: 'JavaScript',
  python: 'Python',
  cpp: 'C++',
  java: 'Java',
};

type Solution = {
  problemId: string;
  language: string;
  code: string;
  explanation: string;
  timeComplexity: string;
  spaceComplexity: string;
  attribution: string;
  walkthrough?: string | null;
  correctness?: string | null;
  edgeCases?: string[] | null;
};
type State =
  | { scope: string; status: 'loading' }
  | { scope: string; status: 'unavailable' }
  | { scope: string; status: 'error'; message: string }
  | { scope: string; status: 'ready'; solution: Solution };

function isSolution(value: unknown, problemId: string, language: string): value is Solution {
  if (!value || typeof value !== 'object') return false;
  const solution = value as Partial<Solution>;
  return (
    solution.problemId === problemId &&
    solution.language === language &&
    Object.hasOwn(LANGUAGE_NAMES, language) &&
    (solution.walkthrough == null || typeof solution.walkthrough === 'string') &&
    (solution.correctness == null || typeof solution.correctness === 'string') &&
    (solution.edgeCases == null ||
      (Array.isArray(solution.edgeCases) &&
        solution.edgeCases.every((item) => typeof item === 'string'))) &&
    ['code', 'explanation', 'timeComplexity', 'spaceComplexity', 'attribution'].every(
      (key) =>
        typeof (solution as Record<string, unknown>)[key] === 'string' &&
        ((solution as Record<string, unknown>)[key] as string).trim().length > 0,
    )
  );
}

// This component has no editor or practice-storage callbacks. Reading an answer
// cannot replace a draft, submit code, or mark the problem as solved.
export function SolutionPanel({
  problemId,
  title,
  language,
  example,
}: {
  problemId: string;
  title: string;
  language: string;
  example?: { input: string; output: string; explanation: string };
}) {
  const scope = `${problemId}:${language}`;
  const languageName = LANGUAGE_NAMES[language] ?? language;
  const [attempt, setAttempt] = useState(0);
  const [copyStatus, setCopyStatus] = useState<{
    source: string;
    status: 'copied' | 'error';
  } | null>(null);
  const currentSource = useRef('');
  const copyRequest = useRef(0);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  const [state, setState] = useState<State>({ scope, status: 'loading' });

  useEffect(() => {
    const controller = new AbortController();
    setState({ scope, status: 'loading' });
    fetch(
      `/api/problems/${encodeURIComponent(problemId)}/solution?language=${encodeURIComponent(language)}`,
      {
        signal: controller.signal,
      },
    )
      .then(async (response) => {
        if (controller.signal.aborted) return;
        if (response.status === 404) {
          setState({ scope, status: 'unavailable' });
          return;
        }
        if (!response.ok) throw new Error('The local server could not load this solution.');
        const solution: unknown = await response.json();
        if (controller.signal.aborted) return;
        if (!isSolution(solution, problemId, language))
          throw new Error('The local server returned an incomplete solution.');
        setState({ scope, status: 'ready', solution });
      })
      .catch((reason: unknown) => {
        if (controller.signal.aborted) return;
        setState({
          scope,
          status: 'error',
          message: reason instanceof Error ? reason.message : 'Could not load this solution.',
        });
      });
    return () => controller.abort();
  }, [problemId, language, scope, attempt]);

  // Never show a previous question's answer while the new effect is starting.
  const visible: State = state.scope === scope ? state : { scope, status: 'loading' };
  const sourceKey = visible.status === 'ready' ? scope + ':' + visible.solution.code : '';
  currentSource.current = sourceKey;
  const copyState = copyStatus?.source === sourceKey ? copyStatus.status : null;
  async function copyCode() {
    if (visible.status !== 'ready') return;
    const source = sourceKey;
    const request = ++copyRequest.current;
    setCopyStatus(null);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(visible.solution.code);
      if (mounted.current && currentSource.current === source && copyRequest.current === request)
        setCopyStatus({ source, status: 'copied' });
    } catch {
      if (mounted.current && currentSource.current === source && copyRequest.current === request)
        setCopyStatus({ source, status: 'error' });
    }
  }
  return (
    <article className="solution-content">
      <h1>{title} — Solution</h1>
      {visible.status === 'loading' ? (
        <p className="solution-status" role="status">
          <LoaderCircle className="spin" size={16} /> Loading {languageName} solution…
        </p>
      ) : visible.status === 'unavailable' ? (
        <p role="status">A {languageName} solution is not available for this question.</p>
      ) : visible.status === 'error' ? (
        <div className="solution-error" role="alert">
          <p>{visible.message}</p>
          <button className="secondary-button" onClick={() => setAttempt((value) => value + 1)}>
            Retry solution
          </button>
        </div>
      ) : (
        <>
          <p className="solution-language">{languageName} reference solution</p>
          <h2>Approach</h2>
          <p className="solution-explanation solution-approach">{visible.solution.explanation}</p>
          {(visible.solution.walkthrough || example) && (
            <section aria-labelledby="solution-walkthrough-heading">
              <h2 id="solution-walkthrough-heading">Walkthrough</h2>
              {visible.solution.walkthrough ? (
                <p className="solution-explanation">{visible.solution.walkthrough}</p>
              ) : example ? (
                <div className="example-code solution-walkthrough">
                  <p>
                    <strong>Input</strong> <code>{example.input}</code>
                  </p>
                  <p>
                    <strong>Expected result</strong> <code>{example.output}</code>
                  </p>
                  <p>{example.explanation}</p>
                </div>
              ) : null}
            </section>
          )}
          <section aria-labelledby="solution-implementation-heading">
            <div className="solution-code-heading">
              <h2 id="solution-implementation-heading">Implementation</h2>
              <button type="button" className="solution-copy" onClick={() => void copyCode()}>
                {copyState === 'copied' ? <Check size={14} /> : <Copy size={14} />} Copy code
              </button>
            </div>
            {copyState === 'copied' && (
              <p className="solution-copy-status" role="status">
                Code copied.
              </p>
            )}
            {copyState === 'error' && (
              <p className="solution-copy-status" role="alert">
                Could not copy. Select the code and copy it manually.
              </p>
            )}
            <ReadOnlyCode
              code={visible.solution.code}
              language={language}
              label={`${languageName} reference solution code`}
            />
          </section>
          {visible.solution.correctness && (
            <section aria-labelledby="solution-correctness-heading">
              <h2 id="solution-correctness-heading">Correctness</h2>
              <p className="solution-explanation">{visible.solution.correctness}</p>
            </section>
          )}
          <section aria-labelledby="solution-complexity-heading">
            <h2 id="solution-complexity-heading">Complexity</h2>
            <dl className="solution-complexity">
              <div>
                <dt>Time</dt>
                <dd>{visible.solution.timeComplexity}</dd>
              </div>
              <div>
                <dt>Extra space</dt>
                <dd>{visible.solution.spaceComplexity}</dd>
              </div>
            </dl>
          </section>
          {visible.solution.edgeCases && visible.solution.edgeCases.length > 0 && (
            <section aria-labelledby="solution-edge-cases-heading">
              <h2 id="solution-edge-cases-heading">Edge cases</h2>
              <ul className="solution-edge-cases">
                {visible.solution.edgeCases.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </section>
          )}
          <p className="attribution">{visible.solution.attribution}</p>
        </>
      )}
    </article>
  );
}
