import { webcrypto } from 'node:crypto';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { migrateLegacyAnswers } from './legacyMigration';

beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('crypto', webcrypto);
});
afterEach(() => vi.unstubAllGlobals());
const valid = {
  id: 'a',
  problemId: 'p',
  mode: 'submit',
  status: 'Accepted',
  passed: 3,
  total: 3,
  timestamp: '2026-01-01T00:00:00Z',
};
it.each(
  [
    null,
    {},
    'wrong type',
    3,
    [null, {}, { ...valid, passed: -1 }, { ...valid, total: 0 }, { ...valid, timestamp: 'bad' }],
  ].map((value) => [value]),
)('ignores malformed legacy records (%j) without deleting original data', async (value) => {
  const source = JSON.stringify(value);
  localStorage.setItem('epi:attempts', source);
  localStorage.setItem('epi:solved', source);
  const fetchMock = vi.fn(async (_url: string, _options: RequestInit) => new Response('{}'));
  vi.stubGlobal('fetch', fetchMock);
  await migrateLegacyAnswers([{ id: 'p' }]);
  const body = JSON.parse(fetchMock.mock.calls[0][1].body as string);
  expect(body.attempts).toEqual([]);
  expect(body.solvedIds).toEqual([]);
  expect(localStorage.getItem('epi:attempts')).toBe(source);
});
it('prefers language-specific C# over the older key and preserves empty drafts', async () => {
  localStorage.setItem('epi:code:p', JSON.stringify('old'));
  localStorage.setItem('epi:code:csharp:p', JSON.stringify(''));
  localStorage.setItem('epi:code:python:p', JSON.stringify('python code'));
  const fetchMock = vi.fn(async (_url: string, _options: RequestInit) => new Response('{}'));
  vi.stubGlobal('fetch', fetchMock);
  await migrateLegacyAnswers([{ id: 'p' }]);
  const body = JSON.parse(fetchMock.mock.calls[0][1].body as string);
  expect(body.drafts.map((d: { language: string; code: string }) => [d.language, d.code])).toEqual([
    ['csharp', ''],
    ['python', 'python code'],
  ]);
});
it('changes migration identity only when recoverable content changes', async () => {
  const fetchMock = vi.fn(async (_url: string, _options: RequestInit) => new Response('{}'));
  vi.stubGlobal('fetch', fetchMock);
  localStorage.setItem('epi:attempts', JSON.stringify([valid]));
  await migrateLegacyAnswers([{ id: 'p' }]);
  await migrateLegacyAnswers([{ id: 'p' }]);
  localStorage.setItem('epi:code:java:p', JSON.stringify('new source'));
  await migrateLegacyAnswers([{ id: 'p' }]);
  const ids = fetchMock.mock.calls.map(
    ([, options]) => JSON.parse(options.body as string).migrationId,
  );
  expect(ids[0]).toBe(ids[1]);
  expect(ids[2]).not.toBe(ids[1]);
});
