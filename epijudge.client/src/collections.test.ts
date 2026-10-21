import { expect, it } from 'vitest';
import { availableCollections, collectionName, problemNumber } from './collections';
import type { Problem } from './workspaceModels';

const problem = (collection?: string, position?: number) => ({ collection, position }) as Problem;

it('derives collection counts only from questions actually registered in the API', () => {
  const current = [problem(), problem('epi'), problem('blind75', 1)];
  expect(availableCollections(current)).toEqual([
    { id: 'epi', name: 'EPI', count: 2 },
    { id: 'blind75', name: 'Blind 75', count: 1 },
  ]);
  expect(availableCollections(current).some(({ id }) => id === 'interviewcake')).toBe(false);
  expect(availableCollections([])).toEqual([]);
  expect(availableCollections([...current, problem('interviewcake', 1)]).at(-1)).toEqual({
    id: 'interviewcake',
    name: 'Interview Cake',
    count: 1,
  });
});
it('uses stable collection positions for Blind and Interview Cake while retaining EPI numbering', () => {
  expect(problemNumber(problem(), 3)).toBe('4');
  expect(problemNumber(problem('epi'), 3, true)).toBe('04');
  expect(problemNumber(problem('blind75', 75), 250)).toBe('B75');
  expect(problemNumber(problem('interviewcake', 41), 333)).toBe('IC41');
  expect(problemNumber(problem('blind75'), 3)).toBe('B04');
  expect(problemNumber(problem('interviewcake', 0), 0)).toBe('IC01');
});
it('keeps unknown registered collection names distinct from EPI', () => {
  expect(collectionName()).toBe('EPI');
  expect(collectionName('interviewcake')).toBe('Interview Cake');
  expect(collectionName('custom')).toBe('custom');
  expect(availableCollections([problem('custom')])).toEqual([
    { id: 'custom', name: 'custom', count: 1 },
  ]);
  expect(problemNumber(problem('custom'), 11)).toBe('12');
});
