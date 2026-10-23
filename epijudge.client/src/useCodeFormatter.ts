import { useEffect, useRef, useState } from 'react';
import type { CodeFormat } from './practiceModels';

export type FormatSnapshot = { code: string; version: number };
type Options = {
  scope: string;
  language: string;
  codeFormat: CodeFormat;
  busy: boolean;
  read(): FormatSnapshot | null;
  apply(code: string, original: FormatSnapshot): void;
};
export function useCodeFormatter(options: Options) {
  const current = useRef(options);
  current.current = options;
  const request = useRef<AbortController | null>(null);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState('');
  useEffect(() => {
    setPending(false);
    setMessage('');
    return () => {
      request.current?.abort();
      request.current = null;
    };
  }, [options.scope, options.busy]);

  async function format() {
    if (request.current || current.current.busy) return;
    const start = current.current;
    const original = start.read();
    if (!original?.code.trim()) {
      setMessage('Enter code to format.');
      return;
    }
    const controller = new AbortController();
    request.current = controller;
    setPending(true);
    setMessage('');
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch('/api/code/format', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-EpiJudge-Client': 'local-editor' },
        body: JSON.stringify({
          language: start.language,
          codeFormat: start.codeFormat,
          code: original.code,
        }),
        signal: controller.signal,
      });
      const result = await response.json();
      if (
        request.current !== controller ||
        current.current.scope !== start.scope ||
        current.current.busy
      )
        return;
      if (controller.signal.aborted) throw new Error('Formatting cancelled.');
      const now = current.current.read();
      if (!now || now.code !== original.code || now.version !== original.version) {
        setMessage('Code changed while formatting. Nothing was replaced.');
        return;
      }
      if (!response.ok) throw new Error(result.message || 'Could not format code.');
      if (typeof result.code !== 'string' || !result.code.trim() || result.code.length > 40000)
        throw new Error('The formatter returned no code.');
      if (result.code === original.code) setMessage('Already formatted.');
      else {
        current.current.apply(result.code, original);
        setMessage('Code formatted. Undo restores your previous code.');
      }
    } catch (error) {
      if (request.current === controller && current.current.scope === start.scope) {
        setMessage(
          controller.signal.aborted
            ? 'Formatting cancelled. Code was not changed.'
            : error instanceof Error
              ? error.message
              : 'Could not format code. Code was not changed.',
        );
      }
    } finally {
      clearTimeout(timer);
      if (request.current === controller) {
        request.current = null;
        setPending(false);
      }
    }
  }
  return { format, pending, message, clearMessage: () => setMessage('') };
}
