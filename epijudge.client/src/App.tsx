import { useCallback, useEffect, useRef, useState } from 'react';
import CodeEditor from './Editor';
import { ProblemLibrary } from './ProblemLibrary';
import { HistoryPanel } from './HistoryPanel';
import { EmptyState } from './EmptyState';
import {
  Braces,
  Code2,
  Check,
  CheckCircle2,
  ChevronRight,
  ChevronLeft,
  ChevronDown,
  ChevronUp,
  PanelLeft,
  Clock3,
  FileCode2,
  FlaskConical,
  History,
  LoaderCircle,
  Play,
  RotateCcw,
  Send,
  Terminal,
  XCircle,
} from 'lucide-react';
import { ErrorBoundary } from './ErrorBoundary';
import { usePractice } from './practiceStorage';

import { LANGUAGES, getStarterCode, getSignature, type Problem } from './workspaceModels';
import { useSubmissionHistory } from './useSubmissionHistory';
import { useSubmission } from './useSubmission';

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
  const libraryTrigger = useRef<HTMLButtonElement>(null);
  const [language, setLanguage] = useState<string>(() => load('epi:language', 'csharp'));
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selected, setSelected] = useState(load('epi:selected', 'count_bits'));
  const practice = usePractice(problems);
  const [storageNotice, setStorageNotice] = useState('');
  const [syncWarning, setSyncWarning] = useState('');
  const [historyVersion, setHistoryVersion] = useState(0);
  const [loadError, setLoadError] = useState('');
  const [tab, setTab] = useState<'results' | 'history'>('results');
  const [activeCase, setActiveCase] = useState(0);
  const problem = problems.find((item) => item.id === selected);
  const currentAttemptRef = useRef<() => void>(() => {});
  const currentSubmitRef = useRef<() => void>(() => {});
  const solved = new Set(
    Object.values(practice.progress)
      .filter((p) => p.status === 'solved')
      .map((p) => p.problemId),
  );
  const code = problem
    ? practice.codeFor(problem.id, language, getStarterCode(problem, language))
    : '';
  const saveStatus = problem ? practice.status(problem.id, language) : 'Loading saved answer…';
  const saveConflict = problem ? practice.conflict(problem.id, language) : undefined;

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
    setActiveCase(0);
    save('epi:selected', problem.id);
  }, [problem?.id, language]);

  const handleLanguageChange = (newLang: string) => {
    setLanguage(newLang);
    save('epi:language', newLang);
  };

  const history = useSubmissionHistory(problem?.id, language, practice.ready, historyVersion);

  const changeCode = (value: string) => {
    if (problem) practice.edit(problem.id, language, value);
  };
  const storageAction = async (action: () => Promise<unknown>, message = '') => {
    try {
      await action();
      setStorageNotice(message);
    } catch (reason) {
      setStorageNotice(
        reason instanceof Error ? reason.message : 'Could not access saved answers.',
      );
    }
  };
  const { result, error, busy, activeMode, execute } = useSubmission({
    problemId: problem?.id,
    language,
    code,
    practice,
    onStarted: () => {
      setSyncWarning('');
      setResultsOpen(true);
      setTab('results');
      setActiveCase(0);
    },
    onCompleted: () => setHistoryVersion((value) => value + 1),
    onRefreshError: (message) => setSyncWarning(message),
  });
  currentAttemptRef.current = () => {
    void execute('run');
  };
  currentSubmitRef.current = () => {
    void execute('submit');
  };
  const runCommand = useCallback(() => currentAttemptRef.current(), []);
  const submitCommand = useCallback(() => currentSubmitRef.current(), []);
  const shownCase = result?.cases[activeCase];

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
            disabled={busy || !practice.ready || !problem || !code.trim()}
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
            disabled={busy || !practice.ready || !problem || !code.trim()}
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
            <i /> Local profile
          </span>
          <span className="avatar">{currentLang.shortLabel}</span>
        </div>
      </header>

      <main className="workspace">
        <ProblemLibrary
          open={libraryOpen}
          problems={problems}
          selected={selected}
          busy={busy}
          practice={practice}
          storageNotice={storageNotice}
          onClose={() => {
            setLibraryOpen(false);
            libraryTrigger.current?.focus();
          }}
          onSelect={(id) => {
            setSelected(id);
            setTab('results');
          }}
          onExport={() => storageAction(() => practice.exportAnswers(), 'Answers exported.')}
          onImport={(file) =>
            storageAction(async () => {
              await practice.importAnswers(file);
              setHistoryVersion((value) => value + 1);
            }, 'Imported answers and history. Existing drafts were kept.')
          }
        />

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
                {!solved.has(problem.id) &&
                  practice.progress[problem.id]?.status === 'attempted' && (
                    <span className="attempted-tag">
                      <Clock3 size={12} /> Attempted
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
                  disabled={busy || !practice.ready || !problem}
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
                  disabled={busy || !practice.ready}
                  aria-label="Select programming language"
                >
                  {LANGUAGES.map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>
              <span>Autosaved on this computer</span>
            </div>
            {syncWarning && (
              <div className="save-warning" role="status">
                <span>{syncWarning}</span>
                <button
                  onClick={async () => {
                    try {
                      await practice.refresh();
                      setHistoryVersion((value) => value + 1);
                      setSyncWarning('');
                    } catch {
                      setSyncWarning(
                        'Could not refresh progress. Your graded answer is still saved.',
                      );
                    }
                  }}
                >
                  Retry synchronization
                </button>
              </div>
            )}
            {(practice.error || saveConflict) && (
              <div className="save-warning" role="status">
                <span>
                  {saveConflict
                    ? 'This answer changed in another tab. Choose which version to keep.'
                    : practice.error}
                </span>
                {saveConflict && problem ? (
                  <>
                    <button onClick={() => practice.resolve(problem.id, language, true)}>
                      Use saved version
                    </button>
                    <button onClick={() => practice.resolve(problem.id, language, false)}>
                      Keep my version
                    </button>
                  </>
                ) : (
                  <button onClick={() => void storageAction(() => practice.flush())}>
                    Retry save
                  </button>
                )}
              </div>
            )}
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
                  busy={busy || !practice.ready}
                  language={currentLang.monacoLang}
                />
              </ErrorBoundary>
            </div>
            <div className="editor-actions">
              <span>
                <span className={'saved-dot ' + (saveStatus === 'Saved' ? 'saved' : 'pending')} />{' '}
                <span role="status">{saveStatus}</span>
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
                <HistoryPanel
                  history={history}
                  busy={busy}
                  onRetry={() => setHistoryVersion((value) => value + 1)}
                  onRestore={(answer) => {
                    if (!answer.language || answer.code === null) return;
                    handleLanguageChange(answer.language);
                    practice.edit(answer.problemId, answer.language, answer.code);
                  }}
                />
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
