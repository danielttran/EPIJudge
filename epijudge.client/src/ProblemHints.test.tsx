import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, it } from 'vitest';
import { ProblemHints } from './ProblemHints';
import { availablePatterns, guidanceFor, patternTags } from './problemGuidance';
import { libraryEntries } from './studyPlans';
import type { Problem } from './workspaceModels';
import solutions from '../../solutions/catalog.json';
import catalog from './problemGuidance.json';

afterEach(cleanup);
it('covers every actual problem exactly once with nonempty tags and staged hints', () => {
  const ids = [...new Set(solutions.map((row) => row.problemId))].sort();
  expect(Object.keys(catalog).sort()).toEqual(ids);
  for (const id of ids) {
    const entry = guidanceFor(id)!;
    expect(entry.tags.length, id).toBeGreaterThan(0);
    expect(new Set(entry.tags).size, id).toBe(entry.tags.length);
    expect(entry.hints, id).toHaveLength(2);
    expect(entry.hints[0], id).not.toBe(entry.hints[1]);
    for (const text of [...entry.tags, ...entry.hints]) {
      expect(text.trim(), id).toBe(text);
      expect(text.length, id).toBeGreaterThan(0);
      expect(text, id).not.toMatch(/TODO|TBD|undefined|```/);
    }
    expect(entry.hints[1], id).toMatch(/[.!?]$/);
  }
});
it('hides hints initially, reveals progressively, and can hide everything again', () => {
  render(<ProblemHints problemId="count_bits" />);
  const hints = guidanceFor('count_bits')!.hints;
  expect(screen.queryByText(hints[0])).toBeNull();
  expect(screen.queryByText(hints[1])).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal first hint' }));
  expect(screen.getByText(hints[0])).toBeTruthy();
  expect(screen.queryByText(hints[1])).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal next hint' }));
  expect(screen.getByText(hints[1])).toBeTruthy();
  expect(screen.queryByRole('button', { name: /Reveal/ })).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: 'Hide hints' }));
  expect(screen.queryByText(hints[1])).toBeNull();
  expect(screen.getByRole('button', { name: 'Reveal first hint' })).toBeTruthy();
});
it('resets revealed content on keyed problem navigation and handles unknown IDs', () => {
  const view = render(<ProblemHints key="count_bits" problemId="count_bits" />);
  fireEvent.click(screen.getByRole('button', { name: 'Reveal first hint' }));
  view.rerender(<ProblemHints key="two_sum" problemId="two_sum" />);
  expect(screen.getByRole('button', { name: 'Reveal first hint' })).toBeTruthy();
  expect(screen.queryByText(guidanceFor('count_bits')!.hints[0])).toBeNull();
  view.rerender(<ProblemHints key="missing" problemId="missing" />);
  expect(screen.queryByRole('region')).toBeNull();
  expect(guidanceFor('__proto__')).toBeUndefined();
});
it('filters and searches by exact reviewed pattern without losing collection behavior', () => {
  const problems = [
    { id: 'count_bits', title: 'Count Bits', topic: 'Primitive types', collection: 'epi' },
    { id: 'two_sum', title: 'Two Sum', topic: 'Arrays', collection: 'epi' },
    { id: 'blind75_two_sum', title: 'Two Sum', topic: 'Arrays', collection: 'blind75' },
  ] as Problem[];
  expect(availablePatterns(problems)).toEqual([
    'Bit manipulation',
    'Hashing and counting',
    'Two pointers',
  ]);
  expect(libraryEntries(problems, 'pattern:Two pointers').map((e) => e.problem?.id)).toEqual([
    'two_sum',
  ]);
  expect(libraryEntries(problems, '', 'hashing').map((e) => e.problem?.id)).toEqual([
    'blind75_two_sum',
  ]);
  expect(libraryEntries(problems, 'collection:blind75', 'hashing')).toHaveLength(1);
  expect(libraryEntries(problems, 'pattern:unknown')).toHaveLength(0);
  expect(patternTags('unknown')).toEqual([]);
});
