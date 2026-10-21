import Markdown from 'react-markdown';
import type { PracticeClient } from '../practiceClient';
import {
  EMPTY_READING_JSON,
  parseReading,
  type ReadingDocument,
  type ReadingLesson,
} from './readingLessons';
import { RaceSimulator } from './RaceSimulator';
import { headingId } from './learnCatalog';

export function ReadingWorkspace({
  lesson,
  practice,
  catalogError = '',
}: {
  lesson: ReadingLesson;
  practice: PracticeClient;
  catalogError?: string;
}) {
  const document = parseReading(practice.codeFor(lesson.id, 'reading', EMPTY_READING_JSON));
  const update = (patch: Partial<ReadingDocument>) =>
    practice.edit(lesson.id, 'reading', JSON.stringify({ ...document, ...patch }));
  const conflict = practice.conflict(lesson.id, 'reading');
  return (
    <>
      <section className="problem-pane reading-pane" aria-label="Reading lesson">
        <div className="pane-heading">
          <span>Learn</span>
          <span>ORIGINAL COMPANION</span>
        </div>
        <article className="reading-body">
          <p className="breadcrumb">
            {lesson.topic} · Book reference {lesson.bookReferences.join(', ')}
          </p>
          <h1>{lesson.title}</h1>
          <p className="reading-attribution">
            Original study companion. Consult your EPI book for the full exercise. Reference numbers
            follow the community study-guide transcription; exact edition titles and pages are
            unverified.
          </p>
          <Markdown
            skipHtml
            components={{
              h2: ({ children }) => (
                <h2 id={headingId(String(children))} tabIndex={-1}>
                  {children}
                </h2>
              ),
              a: ({ children, ...props }) => (
                <a {...props} target="_blank" rel="noopener noreferrer">
                  {children}
                </a>
              ),
            }}
          >
            {lesson.body}
          </Markdown>
          {lesson.hints.map((hint, index) => (
            <details key={index}>
              <summary>Need a starting point?</summary>
              <p>{hint}</p>
            </details>
          ))}
          {lesson.simulation === 'race' && <RaceSimulator />}
          {lesson.sources.length > 0 && (
            <>
              <h2>Further reading</h2>
              <ul>
                {lesson.sources.map((source) => (
                  <li key={source}>
                    <a href={source} target="_blank" rel="noopener noreferrer">
                      {new URL(source).hostname}
                    </a>
                  </li>
                ))}
              </ul>
            </>
          )}
        </article>
      </section>
      <section className="problem-pane reading-pane" aria-label="Reading notes and checkpoints">
        <div className="pane-heading">
          <span>Your study workspace</span>
          <span role="status">{practice.status(lesson.id, 'reading')}</span>
        </div>
        <div className="reading-body">
          {catalogError && (
            <div className="page-error" role="alert">
              <h2>Couldn’t load the library</h2>
              <p>{catalogError}</p>
              <button className="secondary-button" onClick={() => location.reload()}>
                Try again
              </button>
            </div>
          )}
          {(practice.error || conflict) && (
            <div className="save-warning" role="alert">
              <p>
                {conflict
                  ? 'This lesson changed in another tab. Choose which version to keep.'
                  : practice.error}
              </p>
              {conflict ? (
                <>
                  <button onClick={() => practice.resolve(lesson.id, 'reading', true)}>
                    Use saved version
                  </button>
                  <button onClick={() => practice.resolve(lesson.id, 'reading', false)}>
                    Keep my version
                  </button>
                </>
              ) : (
                <button onClick={() => void practice.flush().catch(() => {})}>Retry save</button>
              )}
            </div>
          )}
          <fieldset disabled={!practice.ready}>
            <legend>Check your understanding</legend>
            {lesson.checkpoints.map((checkpoint) => (
              <label className="reading-checkpoint" key={checkpoint.id}>
                <input
                  type="checkbox"
                  checked={document.checkpoints.includes(checkpoint.id)}
                  onChange={(event) =>
                    update({
                      checkpoints: event.target.checked
                        ? [...document.checkpoints, checkpoint.id]
                        : document.checkpoints.filter((id) => id !== checkpoint.id),
                    })
                  }
                />
                {checkpoint.label}
              </label>
            ))}
            {lesson.quizzes.map((quiz) => (
              <section className="reading-interaction" key={quiz.id}>
                <h2>{quiz.prompt}</h2>
                {quiz.options.map((option, index) => (
                  <label className="reading-checkpoint" key={option}>
                    <input
                      type="radio"
                      name={`${lesson.id}-${quiz.id}`}
                      checked={document.answers[quiz.id] === index}
                      onChange={() =>
                        update({ answers: { ...document.answers, [quiz.id]: index } })
                      }
                    />
                    {option}
                  </label>
                ))}
                {document.answers[quiz.id] !== undefined && (
                  <p role="status">
                    {document.answers[quiz.id] === quiz.correctIndex ? 'Correct. ' : 'Try again. '}
                    {quiz.explanation}
                  </p>
                )}
              </section>
            ))}
            <label className="reading-notes-label" htmlFor="reading-notes">
              Your notes and design response
            </label>
            <textarea
              id="reading-notes"
              className="reading-notes"
              maxLength={20_000}
              value={document.notes}
              onChange={(event) => update({ notes: event.target.value })}
              placeholder="Assumptions, worked examples, tradeoffs, and tests…"
            />
            <p className="muted">
              {document.notes.length.toLocaleString()} / 20,000 characters · Autosaved on this
              computer. Included in Export answers.
            </p>
            <button
              className={'secondary-button' + (document.reviewed ? ' reviewed' : '')}
              onClick={() => update({ reviewed: !document.reviewed })}
            >
              {document.reviewed ? 'Undo review' : 'Mark reviewed'}
            </button>
            <p className="reading-attribution">
              Reviewed is your self-assessment. Coding acceptance is tracked separately.
            </p>
          </fieldset>
        </div>
      </section>
    </>
  );
}
