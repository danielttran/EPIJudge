import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { READING_LESSONS, readingLessonById } from './reading/readingLessons';
import { LearnIndex } from './reading/LearnIndex';
import { LearnArticle } from './reading/LearnArticle';
import { learnArticleById, learnHref, practiceHref, relatedArticles } from './reading/learnCatalog';
import { AppLink, appRoute, navigateApp, useAppRoute } from './appNavigation';
import CodeEditor from './Editor';
import { setTheme, useTheme } from './theme';
import { ProblemLibrary } from './ProblemLibrary';
import { HistoryPanel } from './HistoryPanel';
import { EmptyState } from './EmptyState';
import { SolutionPanel } from './SolutionPanel';
import { ProblemHints } from './ProblemHints';
import { patternTags } from './problemGuidance';
import { LanguageSelect } from './LanguageSelect';
import { libraryEntries } from './studyPlans';
import { collectionName, problemNumber } from './collections';
import {
  Braces,
  Sun,
  Moon,
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

import {
  LANGUAGES,
  getStarterCode,
  getStarterFormat,
  getCodeReferences,
  getSignature,
  type Problem,
} from './workspaceModels';
import type { CodeFormat } from './practiceModels';
import { CodeReferences } from './CodeReferences';
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
  const theme = useTheme();
  const route = useAppRoute();
  const isLearn = route.section === 'learn';
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [resultsOpen, setResultsOpen] = useState(false);
  const libraryTrigger = useRef<HTMLButtonElement>(null);
  const [language, setLanguage] = useState<string>(() => load('epi:language', 'csharp'));
  const [solutionLanguage, setSolutionLanguage] = useState<string | null>(() => {
    const saved = load<unknown>('epi:solution-language', null);
    return LANGUAGES.some((item) => item.id === saved) ? (saved as string) : null;
  });
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selected, setSelected] = useState(
    () => appRoute().problemId || load('epi:selected', 'count_bits'),
  );
  const [libraryFilter, setLibraryFilter] = useState(() => load('epi:libraryFilter', ''));
  const practiceCatalog = useMemo(
    () => (problems.length ? [...problems, ...READING_LESSONS.map(({ id }) => ({ id }))] : []),
    [problems],
  );
  const practice = usePractice(practiceCatalog);
  const [storageNotice, setStorageNotice] = useState('');
  const [syncWarning, setSyncWarning] = useState('');
  const [historyVersion, setHistoryVersion] = useState(0);
  const [loadError, setLoadError] = useState('');
  const [tab, setTab] = useState<'results' | 'history'>('results');
  const [problemTab, setProblemTab] = useState<'description' | 'solution'>('description');
  const descriptionTab = useRef<HTMLButtonElement>(null);
  const solutionTab = useRef<HTMLButtonElement>(null);
  const [activeCase, setActiveCase] = useState(0);
  const problem = problems.find((item) => item.id === selected);
  const lesson = readingLessonById(selected);
  const article = learnArticleById(route.articleId);
  const navigation = libraryEntries(problems, libraryFilter)
    .map((entry) => entry.problem ?? entry.lesson)
    .filter((entry) => entry !== undefined);
  const navigationIndex = navigation.findIndex((item) => item.id === selected);
  const currentAttemptRef = useRef<() => void>(() => {});
  const currentSubmitRef = useRef<() => void>(() => {});
  const solved = new Set(
    Object.values(practice.progress)
      .filter((p) => p.status === 'solved')
      .map((p) => p.problemId),
  );
  const document = problem
    ? practice.documentFor(
        problem.id,
        language,
        getStarterCode(problem, language),
        getStarterFormat(problem, language),
      )
    : { code: '', codeFormat: 'legacy-v1' as const };
  const { code, codeFormat } = document;
  const saveStatus = problem ? practice.status(problem.id, language) : 'Loading saved answer…';
  const saveConflict = problem ? practice.conflict(problem.id, language) : undefined;

  useEffect(() => {
    if (problem && !isLearn) save('epi:lastPractice', problem.id);
  }, [problem?.id, isLearn]);

  const selectEntry = (id: string) => {
    setSelected(id);
    if (!readingLessonById(id)) save('epi:lastPractice', id);
    navigateApp(readingLessonById(id) ? learnHref(id) : practiceHref(id));
  };

  useEffect(() => {
    if (route.section === 'practice' && route.problemId) setSelected(route.problemId);
    else if (route.section === 'practice' && readingLessonById(selected))
      setSelected(load('epi:lastPractice', 'count_bits'));
    else if (route.section === 'learn' && article) setSelected(article.id);
  }, [route.section, route.problemId, article]);

  useEffect(() => {
    // Old reading selections had no distinct route. Keep their stable IDs and
    // storage keys and give their existing entry point a canonical Learn URL.
    const url = new URL(window.location.href);
    const legacy =
      url.searchParams.get('lesson') || url.searchParams.get('problem') || url.hash.slice(1);
    const oldLesson = readingLessonById(legacy || selected);
    if (libraryFilter === 'kind:reading') {
      setLibraryFilter('');
      save('epi:libraryFilter', '');
    }
    if (url.pathname.split('/')[1] === 'reading' && article)
      navigateApp(learnHref(article.id) + url.hash, true);
    else if (url.pathname === '/' && oldLesson && !route.unknownPath)
      navigateApp(learnHref(oldLesson.id), true);
    else if (
      route.section === 'practice' &&
      !route.problemId &&
      !route.unknownPath &&
      libraryFilter === 'kind:reading'
    ) {
      navigateApp('/learn', true);
    }
  }, []);

  const currentLang = LANGUAGES.find((l) => l.id === language) ?? LANGUAGES[0];

  useEffect(() => {
    try {
      localStorage.removeItem('epi:studyPhase');
    } catch {
      /* Storage may be unavailable. */
    }
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
        if (
          !items.some((item) => item.id === selected) &&
          !readingLessonById(selected) &&
          !appRoute().problemId
        )
          setSelected(items[0]?.id ?? 'count_bits');
      })
      .catch((reason) => {
        if (reason.name !== 'AbortError') setLoadError(reason.message);
      });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    setActiveCase(0);
    save('epi:selected', selected);
  }, [selected, language]);

  const handleLanguageChange = (newLang: string) => {
    setLanguage(newLang);
    save('epi:language', newLang);
  };

  const history = useSubmissionHistory(problem?.id, language, practice.ready, historyVersion);

  const changeCode = (value: string) => {
    if (problem) practice.edit(problem.id, language, value, codeFormat);
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
    codeFormat,
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
        <button
          className="theme-toggle"
          type="button"
          aria-label="Dark mode"
          aria-pressed={theme === 'dark'}
          title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          {theme === 'dark' ? <Moon size={18} /> : <Sun size={18} />}
        </button>
        <AppLink
          className="brand"
          href="/practice"
          aria-label="EPI Practice home"
          onClick={(event) => {
            if (busy) event.preventDefault();
          }}
        >
          <span className="brand-mark">
            <Braces size={24} strokeWidth={2.5} />
          </span>
          <span>
            epi<span className="brand-divider">/</span>
            <strong>{isLearn ? 'learn' : 'practice'}</strong>
          </span>
        </AppLink>
        <nav className="section-navigation" aria-label="Main navigation">
          <AppLink
            href="/learn"
            aria-current={isLearn ? 'page' : undefined}
            aria-disabled={busy}
            onClick={(event) => {
              if (busy) event.preventDefault();
            }}
          >
            Learn
          </AppLink>
          <AppLink
            href={practiceHref(problem?.id ?? load('epi:lastPractice', 'count_bits'))}
            aria-current={!isLearn ? 'page' : undefined}
            aria-disabled={busy}
            onClick={(event) => {
              if (busy) event.preventDefault();
            }}
          >
            Practice
          </AppLink>
        </nav>
        {!route.unknownPath && (!isLearn || (article && libraryFilter.startsWith('plan:'))) && (
          <>
            <span className="topbar-rule" />
            <button
              ref={libraryTrigger}
              className="library-toggle"
              aria-label={isLearn ? 'Toggle study plan' : 'Toggle problem list'}
              aria-expanded={libraryOpen}
              aria-controls="problem-library"
              onClick={() => setLibraryOpen(true)}
            >
              <PanelLeft size={18} /> <span>{isLearn ? 'Study plan' : 'Problem list'}</span>
            </button>
            <div className="problem-stepping">
              <button
                className="icon-button"
                aria-label={isLearn ? 'Previous study-plan item' : 'Previous problem'}
                disabled={busy || navigationIndex <= 0}
                onClick={() => selectEntry(navigation[navigationIndex - 1].id)}
              >
                <ChevronLeft size={18} />
              </button>
              <button
                className="icon-button"
                aria-label={isLearn ? 'Next study-plan item' : 'Next problem'}
                disabled={busy || !navigation.length || navigationIndex === navigation.length - 1}
                onClick={() => selectEntry(navigation[navigationIndex + 1].id)}
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </>
        )}
        {!isLearn && !route.unknownPath && !lesson && (
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
        )}
        <div className="topbar-right">
          <span className="local-badge">
            <i /> Local profile
          </span>
          <span className="avatar">{isLearn ? 'Read' : currentLang.shortLabel}</span>
        </div>
      </header>

      <main className={'workspace' + (isLearn || route.unknownPath ? ' learn-workspace' : '')}>
        <ProblemLibrary
          open={libraryOpen && (!isLearn || libraryFilter.startsWith('plan:'))}
          problems={problems}
          selected={selected}
          busy={busy}
          practice={practice}
          storageNotice={storageNotice}
          filter={libraryFilter}
          onFilterChange={(value) => {
            setLibraryFilter(value);
            save('epi:libraryFilter', value);
          }}
          onClose={() => {
            setLibraryOpen(false);
            libraryTrigger.current?.focus();
          }}
          onSelect={(id) => {
            selectEntry(id);
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

        {route.unknownPath ||
        (isLearn && route.articleId && !article) ||
        (!isLearn && route.problemId && problems.length > 0 && !problem) ? (
          <section className="learn-empty" role="alert">
            <h1>{isLearn ? 'Article not found' : 'Page not found'}</h1>
            <p>This address does not identify an available local item.</p>
            <AppLink href="/learn">Browse Learn</AppLink>
            <AppLink href="/practice">Return to Practice</AppLink>
          </section>
        ) : isLearn ? (
          article ? (
            <LearnArticle
              article={article}
              practice={practice}
              problems={problems}
              catalogError={loadError}
            />
          ) : (
            <LearnIndex route={route} />
          )
        ) : (
          <>
            <section className="problem-pane">
              <div className="pane-heading">
                <div
                  className="problem-tabs"
                  role="tablist"
                  aria-label="Question content"
                  onKeyDown={(event) => {
                    if (!problem || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key))
                      return;
                    event.preventDefault();
                    const next =
                      event.key === 'Home'
                        ? 'description'
                        : event.key === 'End'
                          ? 'solution'
                          : problemTab === 'description'
                            ? 'solution'
                            : 'description';
                    setProblemTab(next);
                    (next === 'description' ? descriptionTab : solutionTab).current?.focus();
                  }}
                >
                  <button
                    ref={descriptionTab}
                    id="description-tab"
                    role="tab"
                    type="button"
                    className="problem-content-tab"
                    aria-selected={problemTab === 'description'}
                    aria-controls="description-panel"
                    tabIndex={problemTab === 'description' ? 0 : -1}
                    disabled={!problem}
                    onClick={() => setProblemTab('description')}
                  >
                    <FileCode2 size={16} /> Problem
                  </button>
                  <button
                    ref={solutionTab}
                    id="solution-tab"
                    role="tab"
                    type="button"
                    className="problem-content-tab"
                    aria-selected={problemTab === 'solution'}
                    aria-controls="solution-panel"
                    tabIndex={problemTab === 'solution' ? 0 : -1}
                    disabled={!problem}
                    onClick={() => setProblemTab('solution')}
                  >
                    <Code2 size={16} /> Solution
                  </button>
                </div>
                <span className="muted">
                  {collectionName(problem?.collection).toUpperCase()} COLLECTION
                </span>
              </div>
              <div
                id="description-panel"
                role="tabpanel"
                aria-labelledby="description-tab"
                className="problem-tab-panel"
                hidden={problemTab !== 'description'}
              >
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
                      {problemNumber(problem, problems.indexOf(problem))}. {problem.title}
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
                    {patternTags(problem.id).length > 0 && (
                      <div
                        className="pattern-tags"
                        aria-label="Problem patterns"
                        title="Tags describe a supported approach; other valid approaches may exist."
                      >
                        <span className="pattern-label">Patterns</span>
                        {patternTags(problem.id).map((tag) => (
                          <span className="pattern-tag" key={tag}>
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                    <p className="description-copy">{problem.description}</p>
                    {relatedArticles(problem.id).length > 0 && (
                      <nav className="related-reading" aria-label="Related reading">
                        <span>Related reading</span>
                        {relatedArticles(problem.id).map((reading) => (
                          <AppLink
                            key={reading.id}
                            href={learnHref(reading.id)}
                            onClick={(event) => {
                              if (busy) event.preventDefault();
                            }}
                          >
                            {reading.title}
                          </AppLink>
                        ))}
                      </nav>
                    )}
                    {problem.sourceAttribution && (
                      <p className="source-attribution">
                        {problem.sourceAttribution}{' '}
                        {problem.sourceUrl?.startsWith(
                          'https://www.interviewcake.com/question/',
                        ) && (
                          <a href={problem.sourceUrl} target="_blank" rel="noopener noreferrer">
                            Original task reference
                          </a>
                        )}
                      </p>
                    )}
                    {problem.diagram && (
                      <figure className="problem-diagram">
                        <img src={problem.diagram} alt={problem.diagramAlt ?? ''} />
                        <figcaption>{problem.diagramAlt}</figcaption>
                      </figure>
                    )}
                    <div className="signature-label">
                      YOUR {currentLang.shortLabel.toUpperCase()} API
                    </div>
                    <code className="method-signature">{getSignature(problem, language)}</code>
                    {!!problem.starters?.[language]?.contract?.length && (
                      <section aria-label={`${currentLang.shortLabel} callable contract`}>
                        <h2>What your function must do</h2>
                        <ul className="constraints">
                          {problem.starters[language].contract.map((line) => (
                            <li key={line}>{line}</li>
                          ))}
                        </ul>
                      </section>
                    )}
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
                    {(problem.collection ?? 'epi') === 'epi' &&
                      (language === 'cpp' || language === 'java') && (
                        <p className="practice-tip">
                          Implement the displayed {currentLang.shortLabel} callable. Required types
                          are available in the reference panel. Examples may show a wrapper’s
                          observed result; follow the callable contract for return values and
                          mutations.
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
                        <strong>Make it work, then make it better.</strong>Run checks three visible
                        cases. Submit checks the full problem corpus.
                      </p>
                    </div>
                    <p className="attribution">
                      {(problem.collection ?? 'epi') === 'epi'
                        ? 'Practice data from Elements of Programming Interviews Judge. For trusted local use.'
                        : `Original ${collectionName(problem.collection)} statements, test corpora, and local illustrations. For trusted local use.`}
                    </p>
                    <ProblemHints key={problem.id} problemId={problem.id} />
                  </article>
                )}
              </div>
              <div
                id="solution-panel"
                role="tabpanel"
                aria-labelledby="solution-tab"
                className="problem-tab-panel"
                hidden={problemTab !== 'solution'}
              >
                {problem && problemTab === 'solution' && (
                  <SolutionPanel
                    problemId={problem.id}
                    title={problem.title}
                    language={solutionLanguage ?? currentLang.id}
                    onLanguageChange={(value) => {
                      setSolutionLanguage(value);
                      save('epi:solution-language', value);
                    }}
                    example={problem.examples[0]}
                  />
                )}
              </div>
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
                          practice.edit(
                            problem.id,
                            language,
                            getStarterCode(problem, language),
                            getStarterFormat(problem, language),
                          );
                      }}
                    >
                      <RotateCcw size={15} />
                    </button>
                  </div>
                </div>
                <div className="editor-language-row">
                  {' '}
                  <LanguageSelect
                    value={language}
                    onChange={handleLanguageChange}
                    disabled={busy || !practice.ready}
                    label="Select programming language"
                  />
                  <select
                    className="code-format-select"
                    aria-label="Code format"
                    value={codeFormat}
                    disabled={busy || !practice.ready || !problem}
                    onChange={(event) => {
                      if (problem)
                        practice.edit(problem.id, language, code, event.target.value as CodeFormat);
                    }}
                  >
                    <option value="callable-v1">Function / class</option>
                    <option value="legacy-v1">Full program (compatibility)</option>
                  </select>
                  <span>Autosaved on this computer</span>
                </div>
                {codeFormat === 'legacy-v1' && (
                  <p className="code-format-notice">
                    Full program mode keeps your saved code unchanged. Choose Function / class when
                    pasting code from a Solution tab.
                  </p>
                )}
                {problem && (
                  <CodeReferences
                    key={`${problem.id}:${language}`}
                    references={getCodeReferences(problem, language)}
                    language={language}
                  />
                )}
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
                        ? practice.error ||
                          'This answer changed in another tab. Choose which version to keep.'
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
                      <div
                        className="editor-loading"
                        style={{ flexDirection: 'column', gap: '12px' }}
                      >
                        <p style={{ color: 'var(--danger)', margin: 0 }}>
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
                      scope={problem?.id}
                      codeFormat={codeFormat}
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
                    <span
                      className={'saved-dot ' + (saveStatus === 'Saved' ? 'saved' : 'pending')}
                    />{' '}
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
                        practice.edit(
                          answer.problemId,
                          answer.language,
                          answer.code,
                          answer.codeFormat ?? 'legacy-v1',
                        );
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
                      {result.diagnostics && (
                        <pre className="diagnostics">{result.diagnostics}</pre>
                      )}
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
                                This case is hidden. Use Run to inspect visible inputs and compare
                                your output.
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
                                      (shownCase.passed &&
                                      (language === 'cpp' || language === 'java')
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
          </>
        )}
      </main>
    </div>
  );
}
