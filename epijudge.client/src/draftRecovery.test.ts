import { webcrypto } from 'node:crypto';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { DraftRecovery } from './draftRecovery';

beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('crypto', webcrypto);
});
afterEach(() => vi.unstubAllGlobals());

it('clears only the matching code and format while retaining another tab recovery document', () => {
  const legacyKey = 'epi:pending:old:python:count_bits';
  const callableKey = 'epi:pending:new:python:count_bits';
  localStorage.setItem(legacyKey, JSON.stringify({ code: 'same', revision: 1, writtenAt: 1 }));
  localStorage.setItem(
    callableKey,
    JSON.stringify({ code: 'same', codeFormat: 'callable-v1', revision: 1, writtenAt: 2 }),
  );
  const recovery = new DraftRecovery();
  recovery.clear('python:count_bits', 'same', 'legacy-v1');
  expect(localStorage.getItem(legacyKey)).toBeNull();
  expect(localStorage.getItem(callableKey)).not.toBeNull();
  expect(recovery.find('python:count_bits')?.codeFormat).toBe('callable-v1');
  recovery.clear('python:count_bits', 'same', 'callable-v1');
  expect(recovery.find('python:count_bits')).toBeNull();
});
it('keeps legacy recovery strings verbatim and ignores unknown formats', () => {
  const code = 'old program\r\nλ 🐈\r\n';
  localStorage.setItem(
    'epi:pending:old:python:count_bits',
    JSON.stringify({ code, revision: 1, writtenAt: 1 }),
  );
  localStorage.setItem(
    'epi:pending:future:python:count_bits',
    JSON.stringify({ code: 'do not guess', codeFormat: 'future', revision: 2, writtenAt: 2 }),
  );
  expect(new DraftRecovery().find('python:count_bits')?.code).toBe(code);
});
