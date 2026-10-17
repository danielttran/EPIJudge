import { lazy, Suspense, useCallback, useEffect, useRef, useState } from 'react';
import {
  Braces,
  Check,
  CheckCircle2,
  ChevronRight,
  Circle,
  Clock3,
  Code2,
  FileCode2,
  FlaskConical,
  History,
  LoaderCircle,
  Play,
  RotateCcw,
  Search,
  Send,
  Terminal,
  XCircle,
} from 'lucide-react';
const CodeEditor = lazy(() => import('./Editor'));

type Problem = {
  id: string;
  title: string;
  topic: string;
  difficulty: string;
  description: string;
  constraints: string[];
  signature: string;
  starterCode: string;
  examples: { input: string; output: string; explanation: string }[];
};
type TestCase = {
  number: number;
  passed: boolean;
  input: string | null;
  expected: string | null;
  actual: string | null;
  error: string | null;
  elapsedMs: number;
  hidden: boolean;
};
type Result = {
  id: string;
  status: string;
  passed: number;
  total: number;
  elapsedMs: number;
  diagnostics: string | null;
  cases: TestCase[];
};
type Attempt = {
  id: string;
  problemId: string;
  mode: string;
  status: string;
  passed: number;
  total: number;
  timestamp: string;
};

function load<T>(key: string, fallback: T): T {
  try {
    return JSON.parse(localStorage.getItem(key) ?? 'null') ?? fallback;
  } catch {
    return fallback;
  }
}
function save(key: string, value: unknown) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* Storage can be unavailable in private browsing. */
  }
}

export default function App() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selected, setSelected] = useState(load('epi:selected', 'count_bits'));
  const [code, setCode] = useState('');
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState('');
  const [loadError, setLoadError] = useState('');
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const [activeMode, setActiveMode] = useState('run');
  const [tab, setTab] = useState<'results' | 'history'>('results');
  const [attempts, setAttempts] = useState<Attempt[]>(load('epi:attempts', []));
  const [solvedIds, setSolvedIds] = useState<string[]>(load('epi:solved', []));
  const [activeCase, setActiveCase] = useState(0);
  const problem = problems.find((item) => item.id === selected);
  const currentAttemptRef = useRef<() => void>(() => {});
  const currentSubmitRef = useRef<() => void>(() => {});
  const solved = new Set(solvedIds);

  useEffect(() => {
    const controller = new AbortController();
    fetch('/api/problems', { signal: controller.signal })
      .then((response) => {
        if (!response.ok)
          throw new Error(
            'The API did not respond. Check that EpiJudge.Web is running on port 5178.',
          );
        return response.json() as Promise<Problem[]>;
      })
      .then((items) => {
        setProblems(items);
        if (!items.some((item) => item.id === selected)) setSelected(items[0]?.id ?? 'count_bits');
      })
      .catch((reason) => {
        if (reason.name !== 'AbortError') setLoadError(reason.message);
      });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    if (!problem) return;
    setCode(load('epi:code:' + problem.id, problem.starterCode));
    setResult(null);
    setError('');
    setActiveCase(0);
    save('epi:selected', problem.id);
  }, [problem?.id]);

  const changeCode = (value: string) => {
    setCode(value);
    if (problem) save('epi:code:' + problem.id, value);
  };
  const execute = async (mode: 'run' | 'submit') => {
    if (!problem || busyRef.current) return;
    busyRef.current = true;
    setBusy(true);
    setActiveMode(mode);
    setError('');
    setResult(null);
    setTab('results');
    setActiveCase(0);
    try {
      const response = await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-EpiJudge-Client': 'local-editor' },
        body: JSON.stringify({ problemId: problem.id, code, mode }),
      });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(
          detail.message ?? detail.detail ?? 'The runner could not complete this request.',
        );
      }
      const next: Result = await response.json();
      setResult(next);
      if (mode === 'submit' && next.status === 'Accepted')
        setSolvedIds((previous) => {
          const updated = [...new Set([...previous, problem.id])];
          save('epi:solved', updated);
          return updated;
        });
      setAttempts((previous) => {
        const updated = [
          {
            id: next.id,
            problemId: problem.id,
            mode,
            status: next.status,
            passed: next.passed,
            total: next.total,
            timestamp: new Date().toISOString(),
          },
          ...previous,
        ].slice(0, 50);
        save('epi:attempts', updated);
        return updated;
      });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Could not reach the local runner.');
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  };
  currentAttemptRef.current = () => {
    void execute('run');
  };
  currentSubmitRef.current = () => {
    void execute('submit');
  };
  const runCommand = useCallback(() => currentAttemptRef.current(), []);
  const submitCommand = useCallback(() => currentSubmitRef.current(), []);
  const shownCase = result?.cases[activeCase];
  const visibleProblems = problems.filter((item) =>
    `${item.title} ${item.topic}`.toLowerCase().includes(query.toLowerCase()),
  );

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="EPI Practice home">
          <span className="brand-mark">
            <Braces size={24} strokeWidth={2.5} />
          </span>
          <span>
            epi<span className="brand-divider">/</span>
            <strong>practice</strong>
          </span>
        </a>
        <span className="topbar-rule" />
        <span className="workspace-label">C# WORKSPACE</span>
        <div className="topbar-right">
          <span className="local-badge">
            <i /> Local development
          </span>
          <span className="avatar">C#</span>
        </div>
      </header>

      <main className="workspace">
        <aside className="sidebar">
          <div className="library-heading">
            <span>
              <Code2 size={17} /> Problem library
            </span>
            <span className="count-chip">{problems.length || 3}</span>
          </div>
          <label className="search-box">
            <Search size={15} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Find a problem…"
              aria-label="Search problems"
            />
          </label>
          <div className="sidebar-label">AVAILABLE EXERCISES</div>
          <nav className="problem-list" aria-label="Problems">
            {visibleProblems.map((item, index) => (
              <button
                key={item.id}
                disabled={busy}
                className={'problem-link ' + (item.id === selected ? 'selected' : '')}
                onClick={() => {
                  setSelected(item.id);
                  setTab('results');
                }}
              >
                <span className={'problem-indicator ' + (solved.has(item.id) ? 'solved' : '')}>
                  {solved.has(item.id) ? <CheckCircle2 size={16} /> : <Circle size={15} />}
                </span>
                <span className="problem-link-text">
                  <strong>
                    {String(problems.indexOf(item) + 1 || index + 1).padStart(2, '0')}. {item.title}
                  </strong>
                  <span>{item.topic}</span>
                </span>
                <ChevronRight size={14} className="problem-arrow" />
              </button>
            ))}
            {problems.length > 0 && visibleProblems.length === 0 && (
              <p className="sidebar-empty">No matching problems.</p>
            )}
          </nav>
          <div className="library-note">
            <span className="tiny-dot" /> Built on the EPI test corpus
            <p>
              3 web-ready exercises.
              <br />
              218 problems in the C# catalog.
            </p>
          </div>
          <div className="progress-card">
            <div>
              <span>Your progress</span>
              <strong>
                {solved.size}
                <small> / {problems.length || 3}</small>
              </strong>
            </div>
            <div className="progress-track">
              <i style={{ width: `${(solved.size / (problems.length || 3)) * 100}%` }} />
            </div>
            <p>One problem at a time.</p>
          </div>
          <div className="sidebar-footer">
            <Braces size={15} />
            <span>React + ASP.NET Core</span>
            <span className="version">v0.1</span>
          </div>
        </aside>

        <section className="problem-pane">
          <div className="pane-heading">
            <span className="active-pane-tab">
              <FileCode2 size={16} /> Description
            </span>
            <span className="muted">EPI COLLECTION</span>
          </div>
          {loadError ? (
            <div className="page-error">
              <XCircle />
              <h2>Couldn’t load the library</h2>
              <p>{loadError}</p>
              <button className="secondary-button" onClick={() => location.reload()}>
                Try again
              </button>
            </div>
          ) : !problem ? (
            <div className="loading-state">
              <LoaderCircle className="spin" /> Loading your workspace…
            </div>
          ) : (
            <article className="problem-description">
              <div className="breadcrumb">
                Practice <ChevronRight size={12} /> {problem.topic}
              </div>
              <h1>{problem.title}</h1>
              <div className="problem-tags">
                <span className={'difficulty ' + problem.difficulty.toLowerCase()}>
                  {problem.difficulty}
                </span>
                <span>{problem.topic}</span>
                {solved.has(problem.id) && (
                  <span className="solved-tag">
                    <Check size={12} /> Solved
                  </span>
                )}
              </div>
              <p className="description-copy">{problem.description}</p>
              <div className="signature-label">YOUR METHOD</div>
              <code className="method-signature">{problem.signature}</code>
              <h2>Examples</h2>
              {problem.examples.map((example, index) => (
                <section className="example" key={index}>
                  <div className="example-number">EXAMPLE {index + 1}</div>
                  <div className="example-code">
                    <div>
                      <span>Input</span>
                      <code>{example.input}</code>
                    </div>
                    <div>
                      <span>Output</span>
                      <code>{example.output}</code>
                    </div>
                  </div>
                  <p>{example.explanation}</p>
                </section>
              ))}
              <h2>Keep in mind</h2>
              <ul className="constraints">
                {problem.constraints.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              <div className="practice-tip">
                <FlaskConical size={18} />
                <p>
                  <strong>Make it work, then make it better.</strong>Run checks 3 visible TSV cases.
                  Submit checks the entire test file.
                </p>
              </div>
              <p className="attribution">
                Practice data from Elements of Programming Interviews Judge. For trusted local use.
              </p>
            </article>
          )}
        </section>

        <section className="coding-pane" aria-label="Code and results">
          <div className="editor-panel">
            <div className="editor-toolbar">
              <span className="editor-file">
                <FileCode2 size={16} /> Solution.cs
                <span className="file-dot" />
              </span>
              <div className="editor-tools">
                <span className="language-badge">
                  C# <small>.NET 10</small>
                </span>
                <button
                  className="icon-button"
                  title="Reset to starter code"
                  aria-label="Reset to starter code"
                  disabled={busy || !problem}
                  onClick={() => {
                    if (
                      problem &&
                      confirm(
                        'Reset this problem to its starter code? Your saved edits will be replaced.',
                      )
                    )
                      changeCode(problem.starterCode);
                  }}
                >
                  <RotateCcw size={15} />
                </button>
              </div>
            </div>
            <div className="editor-container">
              <Suspense fallback={<div className="editor-loading">Preparing your editor…</div>}>
                <CodeEditor
                  code={code}
                  onChange={changeCode}
                  onRun={runCommand}
                  onSubmit={submitCommand}
                  busy={busy}
                />
              </Suspense>
            </div>
            <div className="editor-actions">
              <span>
                <span className="saved-dot" /> Saved in this browser
              </span>
              <div>
                <button
                  className="run-button"
                  disabled={busy || !problem || !code.trim()}
                  onClick={() => void execute('run')}
                >
                  {busy && activeMode === 'run' ? (
                    <LoaderCircle className="spin" size={15} />
                  ) : (
                    <Play size={15} />
                  )}{' '}
                  Run <kbd>Ctrl ↵</kbd>
                </button>
                <button
                  className="submit-button"
                  disabled={busy || !problem || !code.trim()}
                  onClick={() => void execute('submit')}
                >
                  {busy && activeMode === 'submit' ? (
                    <LoaderCircle className="spin" size={15} />
                  ) : (
                    <Send size={15} />
                  )}{' '}
                  Submit
                </button>
              </div>
            </div>
          </div>

          <section className="results-panel" aria-live="polite">
            <div className="results-tabs">
              <button
                className={tab === 'results' ? 'active' : ''}
                onClick={() => setTab('results')}
              >
                <Terminal size={15} /> Test results
              </button>
              <button
                className={tab === 'history' ? 'active' : ''}
                onClick={() => setTab('history')}
              >
                <History size={15} /> History
              </button>
              <span className="results-caption">
                {busy ? 'RUNNER ACTIVE' : 'READY WHEN YOU ARE'}
              </span>
            </div>
            <div className="results-body">
              {tab === 'history' ? (
                <div className="history-list">
                  {attempts.filter((attempt) => attempt.problemId === selected).length === 0 ? (
                    <EmptyState
                      icon={<History size={25} />}
                      title="Your attempts live here"
                      text="Run or submit your code to start a local history."
                    />
                  ) : (
                    attempts
                      .filter((attempt) => attempt.problemId === selected)
                      .map((attempt) => (
                        <div className="history-item" key={attempt.id}>
                          <span className={attempt.status === 'Accepted' ? 'positive' : 'negative'}>
                            {attempt.status === 'Accepted' ? (
                              <CheckCircle2 size={16} />
                            ) : (
                              <XCircle size={16} />
                            )}
                            {attempt.status}
                          </span>
                          <span>
                            {attempt.mode === 'submit' ? 'Submit' : 'Run'} · {attempt.passed}/
                            {attempt.total}
                          </span>
                          <time>
                            {new Date(attempt.timestamp).toLocaleTimeString([], {
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </time>
                        </div>
                      ))
                  )}
                </div>
              ) : busy ? (
                <EmptyState
                  icon={<LoaderCircle className="spin" size={28} />}
                  title="Compiling and running your C#…"
                  text={
                    activeMode === 'submit'
                      ? 'Checking the full EPI test file. This may take a few seconds.'
                      : 'Checking 3 visible cases from the EPI test file.'
                  }
                />
              ) : error ? (
                <div className="runner-error">
                  <XCircle size={21} />
                  <div>
                    <strong>Couldn’t complete this attempt</strong>
                    <p>{error}</p>
                  </div>
                </div>
              ) : !result ? (
                <EmptyState
                  icon={<Terminal size={27} />}
                  title="Let’s see what your code can do"
                  text="Run a few cases, or submit when you’re ready for the full test set."
                />
              ) : (
                <>
                  <div className="result-summary">
                    <div>
                      <span
                        className={
                          'result-status ' +
                          (result.status === 'Accepted' ? 'positive' : 'negative')
                        }
                      >
                        {result.status === 'Accepted' ? (
                          <CheckCircle2 size={20} />
                        ) : (
                          <XCircle size={20} />
                        )}
                        {result.status}
                      </span>
                      <span className="pass-count">
                        {result.passed.toLocaleString()} / {result.total.toLocaleString()} cases
                        passed
                      </span>
                    </div>
                    <span className="runtime">
                      <Clock3 size={13} /> {result.elapsedMs.toFixed(1)} ms
                    </span>
                  </div>
                  {result.diagnostics && <pre className="diagnostics">{result.diagnostics}</pre>}
                  {result.cases.length > 0 && (
                    <>
                      <div className="case-tabs">
                        {result.cases.map((test, index) => (
                          <button
                            className={activeCase === index ? 'selected' : ''}
                            onClick={() => setActiveCase(index)}
                            key={test.number}
                          >
                            <span className={test.passed ? 'case-pass' : 'case-fail'} />{' '}
                            {test.hidden ? 'Hidden ' : 'Case '}
                            {test.number}
                          </button>
                        ))}
                      </div>
                      {shownCase &&
                        (shownCase.hidden ? (
                          <p className="hidden-case-note">
                            This case is hidden. Use Run to inspect visible inputs and compare your
                            output.
                          </p>
                        ) : (
                          <div className="case-details">
                            <div>
                              <span>Input</span>
                              <code>{shownCase.input}</code>
                            </div>
                            <div>
                              <span>Expected</span>
                              <code>{shownCase.expected}</code>
                            </div>
                            <div>
                              <span>Your output</span>
                              <code className={shownCase.passed ? '' : 'negative'}>
                                {shownCase.error ?? shownCase.actual ?? 'No output'}
                              </code>
                            </div>
                          </div>
                        ))}
                    </>
                  )}
                  {result.status === 'Accepted' && activeMode === 'submit' && (
                    <div className="accepted-note">
                      <Check size={16} /> All cases passed. Your progress has been saved.
                    </div>
                  )}
                </>
              )}
            </div>
          </section>
        </section>
      </main>
    </div>
  );
}

function EmptyState({ icon, title, text }: { icon: React.ReactNode; title: string; text: string }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <strong>{title}</strong>
      <p>{text}</p>
    </div>
  );
}
