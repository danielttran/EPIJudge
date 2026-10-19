import { CheckCircle2, History, XCircle } from 'lucide-react';
import type { Attempt } from './workspaceModels';
import type { useSubmissionHistory } from './useSubmissionHistory';
import { EmptyState } from './EmptyState';

type Props = {
  history: ReturnType<typeof useSubmissionHistory>;
  busy: boolean;
  onRetry(): void;
  onRestore(attempt: Attempt): void;
};
export function HistoryPanel({ history, busy, onRetry, onRestore }: Props) {
  const {
    attempts,
    historyError,
    hasMoreHistory,
    viewedAttempt,
    viewAnswer,
    loadOlder,
    closeAnswer,
  } = history;
  return (
    <div className="history-list">
      {historyError && (
        <p className="save-warning">
          {historyError}
          <button onClick={() => onRetry()}>Retry history</button>
        </p>
      )}
      {viewedAttempt && (
        <div className="saved-answer">
          <div>
            <strong>
              {viewedAttempt.language ?? 'Legacy'} · {viewedAttempt.status}
            </strong>
            <button onClick={() => closeAnswer()}>Close answer</button>
          </div>
          <p>
            {new Date(viewedAttempt.timestamp).toLocaleString()} · {viewedAttempt.passed}/
            {viewedAttempt.total} cases · {viewedAttempt.elapsedMs.toFixed(1)} ms
          </p>
          {viewedAttempt.code !== null ? (
            <>
              <pre tabIndex={0} aria-label="Saved answer code">
                {viewedAttempt.code}
              </pre>
              <button
                disabled={busy}
                onClick={() => {
                  if (!viewedAttempt.language || viewedAttempt.code === null) return;
                  onRestore(viewedAttempt);
                  closeAnswer();
                }}
              >
                Restore to editor
              </button>
            </>
          ) : (
            <p>
              This legacy entry contains only a result summary. Its original code was not saved.
            </p>
          )}
          {viewedAttempt.result?.diagnostics && <pre>{viewedAttempt.result.diagnostics}</pre>}
        </div>
      )}
      {hasMoreHistory && (
        <button className="history-more" onClick={() => void loadOlder()}>
          Load older attempts
        </button>
      )}
      {attempts.length === 0 ? (
        <EmptyState
          icon={<History size={25} />}
          title="Your attempts live here"
          text="Run or submit your code to start a local history."
        />
      ) : (
        attempts.map((attempt) => (
          <div className="history-item" key={attempt.id}>
            <span className={attempt.status === 'Accepted' ? 'positive' : 'negative'}>
              {attempt.status === 'Accepted' ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
              {attempt.status}
            </span>
            <span>
              {attempt.language ?? 'Legacy'} · {attempt.mode === 'submit' ? 'Submit' : 'Run'} ·{' '}
              {attempt.passed}/{attempt.total}
            </span>
            <button onClick={() => void viewAnswer(attempt)}>
              {attempt.legacy ? 'Legacy summary' : 'View answer'}
            </button>
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
  );
}
