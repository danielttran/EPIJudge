import type { Draft, CatalogEntry } from './practiceModels';
import { read } from './draftRecovery';
import { request } from './practiceApi';

const languages = ['csharp', 'javascript', 'python', 'cpp', 'java'];

type LegacyAttempt = {
  id: string;
  problemId: string;
  mode: 'run' | 'submit';
  status: string;
  passed: number;
  total: number;
  timestamp: string;
};
function validAttempt(value: unknown): value is LegacyAttempt {
  if (!value || typeof value !== 'object') return false;
  const a = value as Partial<LegacyAttempt>;
  return (
    typeof a.id === 'string' &&
    a.id.length > 0 &&
    typeof a.problemId === 'string' &&
    (a.mode === 'run' || a.mode === 'submit') &&
    typeof a.status === 'string' &&
    a.status.length > 0 &&
    Number.isSafeInteger(a.passed) &&
    Number.isSafeInteger(a.total) &&
    a.passed! >= 0 &&
    a.total! >= a.passed! &&
    typeof a.timestamp === 'string' &&
    Number.isFinite(Date.parse(a.timestamp))
  );
}

export async function migrateLegacyAnswers(catalog: CatalogEntry[]) {
  const drafts: Draft[] = [];
  const known = new Set(catalog.map((p) => p.id));
  for (const p of catalog)
    for (const language of languages) {
      const code =
        read<string | null>(`epi:code:${language}:${p.id}`, null) ??
        (language === 'csharp' ? read<string | null>(`epi:code:${p.id}`, null) : null);
      if (typeof code === 'string')
        drafts.push({
          problemId: p.id,
          language,
          code,
          revision: 0,
          updatedAt: new Date().toISOString(),
        });
    }
  const oldAttempts = read<unknown>('epi:attempts', []);
  const attempts = (Array.isArray(oldAttempts) ? oldAttempts : [])
    .filter(validAttempt)
    .filter((a) => known.has(a.problemId))
    .map((a) => ({
      ...a,
      id: `legacy:${a.id}`,
      code: null,
      language: null,
      elapsedMs: 0,
      result: null,
      legacy: true,
    }));
  const oldSolved = read<unknown>('epi:solved', []);
  const solvedIds = (Array.isArray(oldSolved) ? oldSolved : []).filter(
    (id): id is string => typeof id === 'string' && known.has(id),
  );
  // Content-based IDs remain idempotent even when a full/private browser cannot store a new marker.
  const source = JSON.stringify({
    drafts: drafts.map(({ problemId, language, code }) => ({ problemId, language, code })),
    attempts,
    solvedIds,
  });
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(source));
  const migrationId =
    'browser-v1:' +
    [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
  return request('/migrate', {
    method: 'POST',
    body: JSON.stringify({ migrationId, drafts, attempts, solvedIds }),
  });
}
