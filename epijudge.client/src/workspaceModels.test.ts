import { expect, it } from 'vitest';
import { getSignature, getStarterCode, LANGUAGES, type Problem } from './workspaceModels';

const legacy = {
  starterCode: 'C# source',
  signature: 'C# signature',
  jsStarterCode: 'JS source',
  jsSignature: 'JS signature',
  pyStarterCode: 'Python source',
  pySignature: 'Python signature',
} as Problem;
it.each(LANGUAGES)('selects the catalog-provided $id starter and signature', ({ id }) => {
  const problem = {
    ...legacy,
    starters: {
      [id]: {
        starterCode: id + ' source',
        signature: id + ' signature',
        filename: 'solution',
        runtime: id,
      },
    },
  };
  expect(getStarterCode(problem, id)).toBe(id + ' source');
  expect(getSignature(problem, id)).toBe(id + ' signature');
});
it.each([
  ['csharp', 'C#'],
  ['javascript', 'JS'],
  ['python', 'Python'],
])('reads legacy %s starters', (id, prefix) => {
  expect(getStarterCode(legacy, id)).toBe(prefix + ' source');
  expect(getSignature(legacy, id)).toBe(prefix + ' signature');
});
it.each(['javascript', 'python', 'unknown'])(
  'falls back to the original starter for %s when no language version exists',
  (id) => {
    const problem = { starterCode: 'original', signature: 'signature' } as Problem;
    expect(getStarterCode(problem, id)).toBe('original');
    expect(getSignature(problem, id)).toBe('signature');
  },
);
