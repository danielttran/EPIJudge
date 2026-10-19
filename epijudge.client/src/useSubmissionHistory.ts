import { useEffect, useRef, useState } from 'react';
import type { Attempt } from './workspaceModels';

async function get<T>(path: string, signal: AbortSignal, message: string): Promise<T> {
  const response = await fetch('/api/practice/history' + path, { cache: 'no-store', signal });
  if (!response.ok) throw new Error(message);
  return response.json();
}

export function useSubmissionHistory(
  problemId: string | undefined,
  language: string,
  ready: boolean,
  version: number,
) {
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [historyError, setHistoryError] = useState('');
  const [hasMoreHistory, setHasMoreHistory] = useState(false);
  const [viewedAttempt, setViewedAttempt] = useState<Attempt | null>(null);
  const scope = `${problemId}:${language}:${ready}:${version}`;
  // Update during render: even an already-resolved response must not commit to
  // the new selection in the interval before effect cleanup runs.
  const currentScope = useRef(scope);
  currentScope.current = scope;
  const requests = useRef(new Set<AbortController>());
  const detailVersion = useRef(0);
  const loadingOlder = useRef(false);

  useEffect(() => {
    setAttempts([]);
    setViewedAttempt(null);
    setHistoryError('');
    setHasMoreHistory(false);
    loadingOlder.current = false;
    const controller = new AbortController();
    requests.current.add(controller);
    if (problemId && ready) {
      void get<Attempt[]>(
        `?problemId=${encodeURIComponent(problemId)}`,
        controller.signal,
        'Could not load saved history.',
      )
        .then((items) => {
          if (controller.signal.aborted || currentScope.current !== scope) return;
          setAttempts(items);
          setHasMoreHistory(items.length === 50);
        })
        .catch((reason) => {
          if (!controller.signal.aborted && currentScope.current === scope)
            setHistoryError(reason.message);
        })
        .finally(() => requests.current.delete(controller));
    }
    const active = requests.current;
    return () => {
      for (const request of active) request.abort();
      active.clear();
    };
  }, [scope, problemId, ready]);

  async function viewAnswer(attempt: Attempt) {
    const requestVersion = ++detailVersion.current;
    const controller = new AbortController();
    requests.current.add(controller);
    try {
      const answer = await get<Attempt>(
        '/' + encodeURIComponent(attempt.id),
        controller.signal,
        'Could not open saved answer.',
      );
      if (
        !controller.signal.aborted &&
        currentScope.current === scope &&
        requestVersion === detailVersion.current
      ) {
        setViewedAttempt(answer);
        setHistoryError('');
      }
    } catch (reason) {
      if (
        !controller.signal.aborted &&
        currentScope.current === scope &&
        requestVersion === detailVersion.current
      )
        setHistoryError(reason instanceof Error ? reason.message : 'Could not open answer.');
    } finally {
      requests.current.delete(controller);
    }
  }

  async function loadOlder() {
    if (!problemId || !attempts.length || loadingOlder.current || !hasMoreHistory) return;
    loadingOlder.current = true;
    const controller = new AbortController();
    requests.current.add(controller);
    try {
      const older = await get<Attempt[]>(
        `?problemId=${encodeURIComponent(problemId)}&before=${attempts[attempts.length - 1].sequence}`,
        controller.signal,
        'Could not load older attempts.',
      );
      if (controller.signal.aborted || currentScope.current !== scope) return;
      setAttempts((previous) => [
        ...previous,
        ...older.filter((a) => !previous.some((p) => p.id === a.id)),
      ]);
      setHasMoreHistory(older.length === 50);
      setHistoryError('');
    } catch (reason) {
      if (!controller.signal.aborted && currentScope.current === scope)
        setHistoryError(reason instanceof Error ? reason.message : 'Could not load history.');
    } finally {
      requests.current.delete(controller);
      if (currentScope.current === scope) loadingOlder.current = false;
    }
  }
  return {
    attempts,
    historyError,
    hasMoreHistory,
    viewedAttempt,
    viewAnswer,
    loadOlder,
    closeAnswer: () => {
      detailVersion.current++;
      setViewedAttempt(null);
    },
  };
}
