import { useCallback, useEffect, useRef, useState } from 'react';
import CodeEditor from './Editor';
import {
  Braces,
  Check,
  CheckCircle2,
  ChevronRight,
  ChevronLeft,
  ChevronDown,
  ChevronUp,
  PanelLeft,
  X,
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
import { ErrorBoundary } from './ErrorBoundary';

type Problem = {
  id: string;
  title: string;
  topic: string;
  difficulty: string;
  description: string;
  constraints: string[];
  signature: string;
  testCount: number;
  starterCode: string;
  jsSignature?: string;
  jsStarterCode?: string;
  pySignature?: string;
  pyStarterCode?: string;
  starters?: Record<
    string,
    { signature: string; starterCode: string; filename: string; runtime: string }
  >;
  examples: { input: string; output: string; explanation: string }[];
};

type LanguageConfig = {
  id: string;
  shortLabel: string;
  label: string;
  runtime: string;
  filename: string;
  monacoLang: string;
};

const LANGUAGES: LanguageConfig[] = [
  {
    id: 'csharp',
    shortLabel: 'C#',
    label: 'C# (.NET 10)',
    runtime: 'C# .NET 10',
    filename: 'Solution.cs',
    monacoLang: 'csharp',
  },
  {
    id: 'javascript',
    shortLabel: 'JS',
    label: 'JavaScript (Node.js 24)',
    runtime: 'JavaScript Node.js 24',
    filename: 'solution.js',
    monacoLang: 'javascript',
  },
  {
    id: 'python',
    shortLabel: 'PY',
    label: 'Python (Python 3.14)',
    runtime: 'Python 3.14',
    filename: 'solution.py',
    monacoLang: 'python',
  },
  {
    id: 'cpp',
    shortLabel: 'C++',
    label: 'C++ (C++17)',
    runtime: 'C++17',
    filename: 'solution.cpp',
    monacoLang: 'cpp',
  },
  {
    id: 'java',
    shortLabel: 'JAVA',
    label: 'Java (JDK 21)',
    runtime: 'Java 21',
    filename: 'Solution.java',
    monacoLang: 'java',
  },
];

function getStarterCode(p: Problem, lang: string): string {
  if (p.starters?.[lang]) return p.starters[lang].starterCode;
  if (lang === 'python') {
    return p.starters?.python?.starterCode || p.pyStarterCode || p.starterCode;
  }
  if (lang === 'javascript') {
    return p.starters?.javascript?.starterCode || p.jsStarterCode || p.starterCode;
  }
  return p.starters?.csharp?.starterCode || p.starterCode;
}

function getSignature(p: Problem, lang: string): string {
  if (p.starters?.[lang]) return p.starters[lang].signature;
  if (lang === 'python') {
    return p.starters?.python?.signature || p.pySignature || p.signature;
  }
  if (lang === 'javascript') {
    return p.starters?.javascript?.signature || p.jsSignature || p.signature;
  }
  return p.starters?.csharp?.signature || p.signature;
}

function getStoredCode(p: Problem, lang: string): string {
  const scoped = load<string | null>('epi:code:' + lang + ':' + p.id, null);
  if (scoped !== null) return scoped;
  if (lang === 'csharp') {
    const legacy = load<string | null>('epi:code:' + p.id, null);
    if (legacy !== null) return legacy;
  }
  return getStarterCode(p, lang);
}
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
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [resultsOpen, setResultsOpen] = useState(false);
  const libraryDialog = useRef<HTMLDialogElement>(null);
  const libraryTrigger = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (libraryOpen) libraryDialog.current?.showModal();
    else libraryDialog.current?.close();
  }, [libraryOpen]);
  const [language, setLanguage] = useState<string>(() => load('epi:language', 'csharp'));
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selected, setSelected] = useState(load('epi:selected', 'count_bits'));
  const [code, setCode] = useState('');
  const [query, setQuery] = useState('');
  const [topic, setTopic] = useState('');
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

  const currentLang = LANGUAGES.find((l) => l.id === language) ?? LANGUAGES[0];

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
    setCode(getStoredCode(problem, language));
    setResult(null);
    setError('');
    setActiveCase(0);
    save('epi:selected', problem.id);
  }, [problem?.id, language]);

  const handleLanguageChange = (newLang: string) => {
    setLanguage(newLang);
    save('epi:language', newLang);
  };

  const changeCode = (value: string) => {
    setCode(value);
    if (problem) save(`epi:code:${language}:${problem.id}`, value);
  };
  const execute = async (mode: 'run' | 'submit') => {
    if (!problem || busyRef.current) return;
    busyRef.current = true;
    setBusy(true);
    setResultsOpen(true);
    setActiveMode(mode);
    setError('');
    setResult(null);
    setTab('results');
    setActiveCase(0);
    try {
      const response = await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-EpiJudge-Client': 'local-editor' },
        body: JSON.stringify({ problemId: problem.id, code, mode, language }),
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
  const visibleProblems = problems.filter(
    (item) =>
      (!topic || item.topic === topic) &&
      `${item.title} ${item.topic} ${item.id}`.toLowerCase().includes(query.toLowerCase()),
  );
  const topics = [...new Set(problems.map((item) => item.topic))].sort();
  const solvedCount = problems.filter((item) => solved.has(item.id)).length;

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
        <button
          ref={libraryTrigger}
          className="library-toggle"
          aria-label="Toggle problem list"
          aria-expanded={libraryOpen}
          aria-controls="problem-library"
          onClick={() => setLibraryOpen(true)}
        >
          <PanelLeft size={18} /> <span>Problem list</span>
        </button>
        <div className="problem-stepping">
          <button
            className="icon-button"
            aria-label="Previous problem"
            disabled={busy || !problem || problems.indexOf(problem) === 0}
            onClick={() =>
              setSelected(problems[problems.findIndex((p) => p.id === selected) - 1].id)
            }
          >
            <ChevronLeft size={18} />
          </button>
          <button
            className="icon-button"
            aria-label="Next problem"
            disabled={busy || !problem || problems.indexOf(problem) === problems.length - 1}
            onClick={() =>
              setSelected(problems[problems.findIndex((p) => p.id === selected) + 1].id)
            }
          >
            <ChevronRight size={18} />
          </button>
        </div>
        <div className="topbar-actions">
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
        <div className="topbar-right">
          <span className="local-badge">
            <i /> Local development
          </span>
          <span className="avatar">{currentLang.shortLabel}</span>
        </div>
      </header>

      <main className="workspace">
        <dialog
          ref={libraryDialog}
          id="problem-library"
          className="library-dialog"
          aria-label="Problem library"
          onClose={() => {
            setLibraryOpen(false);
            libraryTrigger.current?.focus();
          }}
          onClick={(event) => {
            if (event.target === event.currentTarget) setLibraryOpen(false);
          }}
        >
          <aside className="sidebar">
            <div className="library-heading">
              <span>
                <Code2 size={17} /> Problem library
              </span>
              <span className="count-chip">{problems.length}</span>
              <button
                className="icon-button"
                aria-label="Close problem list"
                onClick={() => setLibraryOpen(false)}
              >
                <X size={20} />
              </button>
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
            <select
              className="topic-filter"
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
              aria-label="Filter by topic"
            >
              <option value="">All topics</option>
              {topics.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
            <div className="sidebar-label">{visibleProblems.length} EXERCISES</div>
            <nav className="problem-list" aria-label="Problems">
              {visibleProblems.map((item, index) => (
                <button
                  key={item.id}
                  disabled={busy}
                  className={'problem-link ' + (item.id === selected ? 'selected' : '')}
                  title={item.title + ' · ' + item.topic}
                  aria-current={item.id === selected ? 'page' : undefined}
                  onClick={() => {
                    setSelected(item.id);
                    setTab('results');
                    setLibraryOpen(false);
                  }}
                >
                  <span className={'problem-indicator ' + (solved.has(item.id) ? 'solved' : '')}>
                    {solved.has(item.id) ? <CheckCircle2 size={16} /> : <Circle size={15} />}
                  </span>
                  <span className="problem-link-text">
                    <strong>
                      {String(problems.indexOf(item) + 1 || index + 1).padStart(2, '0')}.{' '}
                      {item.title}
                    </strong>
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
                All {problems.length} repository exercises available in C#, JavaScript, Python, C++,
                and Java.
              </p>
            </div>
            <div className="progress-card">
              <div>
                <span>Your progress</span>
                <strong>
                  {solvedCount}
                  <small> / {problems.length}</small>
                </strong>
              </div>
              <div className="progress-track">
                <i style={{ width: `${(solvedCount / Math.max(1, problems.length)) * 100}%` }} />
              </div>
              <p>One problem at a time.</p>
            </div>
            <div className="sidebar-footer">
              <Braces size={15} />
              <span>React + ASP.NET Core</span>
              <span className="version">v0.1</span>
            </div>
          </aside>
        </dialog>

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
              <h1>
                {problems.indexOf(problem) + 1}. {problem.title}
              </h1>
              <div className="problem-tags">
                <span className={'difficulty ' + problem.difficulty.toLowerCase()}>
                  {problem.difficulty}
                </span>
                <span>{problem.topic}</span>
                {typeof problem.testCount === 'number' && (
                  <span>{problem.testCount.toLocaleString()} test cases</span>
                )}
                {solved.has(problem.id) && (
                  <span className="solved-tag">
                    <Check size={12} /> Solved
                  </span>
                )}
              </div>
              <p className="description-copy">{problem.description}</p>
              <div className="signature-label">YOUR {currentLang.shortLabel.toUpperCase()} API</div>
              <code className="method-signature">{getSignature(problem, language)}</code>
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
                      <span>Expected result</span>
                      <code>{example.output}</code>
                    </div>
                  </div>
                  <p>{example.explanation}</p>
                </section>
              ))}
              <h2>Keep in mind</h2>
              {(language === 'cpp' || language === 'java') && (
                <p className="practice-tip">
                  Implement the TODO methods in the supplied {currentLang.shortLabel} file. Keep its
                  class names, wrappers, and main function. These languages use the original EPI
                  types; follow the supplied code where it differs from the C# types below.
                </p>
              )}
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
                <Code2 size={16} /> Code
                <span className="file-dot" />
              </span>
              <div className="editor-tools">
                <span className="language-badge">
                  {currentLang.label} <small>{currentLang.runtime}</small>
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
                        `Reset this problem to its ${currentLang.label} starter code? Your saved edits will be replaced.`,
                      )
                    )
                      changeCode(getStarterCode(problem, language));
                  }}
                >
                  <RotateCcw size={15} />
                </button>
              </div>
            </div>
            <div className="editor-language-row">
              {' '}
              <div className="language-selector-wrapper">
                <select
                  className="language-select"
                  value={language}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                  disabled={busy}
                  aria-label="Select programming language"
                >
                  {LANGUAGES.map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>
              <span>Saved in this browser</span>
            </div>
            <div className="editor-container">
              <ErrorBoundary
                fallback={(err, reset) => (
                  <div className="editor-loading" style={{ flexDirection: 'column', gap: '12px' }}>
                    <p style={{ color: '#fca5a5', margin: 0 }}>
                      Couldn’t open the editor. Your saved code is safe.
                    </p>
                    <small>{err.message}</small>
                    <button type="button" className="secondary-button" onClick={() => reset()}>
                      Retry loading editor
                    </button>
                  </div>
                )}
              >
                <CodeEditor
                  code={code}
                  onChange={changeCode}
                  onRun={runCommand}
                  onSubmit={submitCommand}
                  busy={busy}
                  language={currentLang.monacoLang}
                />
              </ErrorBoundary>
            </div>
            <div className="editor-actions">
              <span>
                <span className="saved-dot" /> Saved in this browser
              </span>
            </div>
          </div>

          <section
            className={'results-panel' + (resultsOpen ? '' : ' collapsed')}
            aria-live="polite"
          >
            <div className="results-tabs">
              <button
                className={tab === 'results' ? 'active' : ''}
                onClick={() => {
                  setTab('results');
                  setResultsOpen(true);
                }}
              >
                <Terminal size={15} /> Test results
              </button>
              <button
                className={tab === 'history' ? 'active' : ''}
                onClick={() => {
                  setTab('history');
                  setResultsOpen(true);
                }}
              >
                <History size={15} /> History
              </button>
              <span className="results-caption">
                {busy ? 'RUNNER ACTIVE' : 'READY WHEN YOU ARE'}
              </span>
              <button
                className="results-toggle"
                aria-label={resultsOpen ? 'Collapse results' : 'Expand results'}
                aria-expanded={resultsOpen}
                aria-controls="test-results-body"
                onClick={() => setResultsOpen((value) => !value)}
              >
                {resultsOpen ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
              </button>
            </div>
            <div className="results-body" id="test-results-body">
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
                  title={`Compiling and running your ${currentLang.shortLabel}…`}
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
                                {shownCase.error ||
                                  shownCase.actual ||
                                  (shownCase.passed && (language === 'cpp' || language === 'java')
                                    ? 'Accepted by the problem validator'
                                    : 'No output')}
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
