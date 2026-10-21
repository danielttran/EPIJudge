import { useEffect, useRef, useState } from 'react';
import type { Result } from './workspaceModels';
import type { CodeFormat } from './practiceModels';

type Options = {
  problemId?: string;
  language: string;
  code: string;
  codeFormat?: CodeFormat;
  practice: { ready: boolean; flush(): Promise<void>; refresh(): Promise<void> };
  onStarted(): void;
  onCompleted(): void;
  onRefreshError(message: string): void;
};

export function useSubmission(options: Options) {
  const { problemId, language, code, practice } = options;
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [activeMode, setActiveMode] = useState<'run' | 'submit'>('run');
  const busyRef = useRef(false);
  const scope = `${problemId}:${language}`;
  const currentScope = useRef(scope);
  currentScope.current = scope;
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  useEffect(() => {
    setResult(null);
    setError('');
  }, [scope]);

  async function execute(mode: 'run' | 'submit') {
    if (!problemId || busyRef.current || !practice.ready) return;
    busyRef.current = true;
    setBusy(true);
    setActiveMode(mode);
    setError('');
    setResult(null);
    options.onStarted();
    const isCurrent = () => mounted.current && currentScope.current === scope;
    try {
      await practice.flush();
      const response = await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-EpiJudge-Client': 'local-editor' },
        body: JSON.stringify({
          problemId,
          code,
          mode,
          language,
          codeFormat: options.codeFormat ?? 'legacy-v1',
        }),
      });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(
          detail.message ?? detail.detail ?? 'The runner could not complete this request.',
        );
      }
      const next: Result = await response.json();
      if (isCurrent()) setResult(next);
      // Grading already succeeded. A failed progress refresh must not turn an
      // accepted submission into an execution error or hide its result.
      try {
        await practice.refresh();
      } catch {
        if (mounted.current)
          options.onRefreshError(
            'Answer graded and saved. Could not refresh progress; retry synchronization.',
          );
      }
      if (mounted.current) options.onCompleted();
    } catch (reason) {
      if (isCurrent())
        setError(reason instanceof Error ? reason.message : 'Could not reach the local runner.');
    } finally {
      busyRef.current = false;
      if (mounted.current) setBusy(false);
    }
  }
  return { result, error, busy, activeMode, execute };
}
