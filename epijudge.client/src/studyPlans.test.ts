import { expect, it } from 'vitest';
import { libraryEntries, selectedStudyPlan, STUDY_PLANS } from './studyPlans';
import guide from './studyGuide.json';
import rawCatalog from '../../EpiJudge.Runner/catalog.json';
import type { Problem } from './workspaceModels';

// The three hand-maintained entries are combined with the generated catalog by the API.
const problems = [
  ...rawCatalog.map((p) => ({ id: p.Id, title: p.Title, topic: p.Topic })),
  { id: 'count_bits', title: 'Count Bits', topic: 'Primitive types' },
  { id: 'two_sum', title: 'Two Sum', topic: 'Arrays' },
  { id: 'anagrams', title: 'Anagrams', topic: 'Hash tables' },
] as Problem[];

it('maps every runnable guide entry to an existing catalog identity', () => {
  const ids = new Set(problems.map((p) => p.id));
  for (const column of guide.columns)
    for (const entry of column) {
      if (entry.problemId)
        expect(ids.has(entry.problemId), `${entry.number}: ${entry.problemId}`).toBe(true);
      else expect(entry.reason).not.toBe('');
    }
});
it.each([
  ['3-days', 18, 16],
  ['7-days', 41, 36],
  ['1-month', 65, 58],
  ['4-months', 92, 82],
])('keeps %s as one focused list', (id, total, runnable) => {
  const entries = libraryEntries(problems, `plan:${id}`);
  expect(entries).toHaveLength(total as number);
  expect(entries.filter((e) => e.problem)).toHaveLength(runnable as number);
  expect(new Set(entries.map((e) => e.number)).size).toBe(entries.length);
});
it('preserves priority, chapter, and within-cell order without adding the next column', () => {
  const entries = libraryEntries([...problems].reverse(), 'plan:3-days');
  expect(entries.slice(0, 5).map((e) => e.number)).toEqual(['4.1', '5.1', '5.6', '6.1', '7.1']);
  expect(entries.at(-1)?.number).toBe('20.13');
  expect(entries.some((e) => e.number === '4.7')).toBe(false);
});
it.each(STUDY_PLANS)('includes only the assigned columns for $id', (plan) => {
  const entries = libraryEntries(problems, `plan:${plan.id}`);
  const expected = [
    ...new Set(
      guide.columns
        .slice(0, plan.scenario)
        .flatMap((column) => column.map((entry) => entry.number)),
    ),
  ];
  expect(entries.map((entry) => entry.number)).toEqual(expected);
  expect(entries.every((entry) => entry.column! < plan.scenario)).toBe(true);
});
it('deduplicates an exercise assigned in more than one column', () => {
  const entries = libraryEntries(problems, 'plan:1-month').filter((e) => e.number === '12.5');
  expect(entries).toHaveLength(1);
  expect(entries[0].column).toBe(1);
});
it.each([
  ['6.7', 'phone_number_mnemonic'],
  ['6.8', 'look_and_say'],
  ['6.11', 'snake_string'],
  ['9.11', 'tree_with_parent_inorder'],
  ['9.12', 'tree_from_preorder_inorder'],
  ['9.16', 'tree_right_sibling'],
  ['15.2', 'n_queens'],
  ['15.3', 'permutations'],
  ['15.4', 'power_set'],
  ['15.6', 'enumerate_balanced_parentheses'],
  ['15.9', 'sudoku_solve'],
  ['15.10', 'gray_code'],
  ['11.10', 'find_missing_and_duplicate'],
  ['18.2', 'painting'],
])('resolves reference %s by identity rather than the older index', (number, id) => {
  expect(guide.columns.flat().find((entry) => entry.number === number)?.problemId).toBe(id);
  expect(libraryEntries(problems, 'kind:coding').some((entry) => entry.problem?.id === id)).toBe(
    true,
  );
});
it('keeps distinct missing LCA tasks visible instead of substituting the root-based LCA task', () => {
  const entries = libraryEntries(problems, 'plan:4-months');
  for (const number of ['9.4', '12.4']) {
    const entry = entries.find((e) => e.number === number)!;
    expect(entry.problem).toBeUndefined();
    expect(entry.reason).toContain('separate graded entry');
  }
});
it('preserves plan order through search and matches book numbers', () => {
  const all = libraryEntries(problems, 'plan:4-months');
  const searched = libraryEntries(problems, 'plan:4-months', 'array');
  expect(searched.map((e) => e.number)).toEqual(
    all
      .filter((e) => `${e.title} ${e.topic} ${e.problem?.id ?? ''}`.toLowerCase().includes('array'))
      .map((e) => e.number),
  );
  expect(libraryEntries(problems, 'plan:4-months', '9.12').map((e) => e.number)).toEqual(['9.12']);
});
it('retains the original all-topics ordering and topic/search filters', () => {
  expect(libraryEntries(problems, 'kind:coding').map((e) => e.problem?.id)).toEqual(
    problems.map((p) => p.id),
  );
  expect(libraryEntries(problems, 'Arrays').every((e) => e.topic === 'Arrays')).toBe(true);
  expect(libraryEntries(problems, '', 'not-a-real-problem')).toEqual([]);
  expect(selectedStudyPlan('Arrays')).toBeUndefined();
});

it('keeps excluded exercises and all reading companions available outside study plans', () => {
  const plan = libraryEntries(problems, 'plan:3-days');
  expect(plan.some((entry) => entry.number === '4.7')).toBe(false);
  const excluded = guide.columns[1].find((entry) => entry.number === '4.7')!;
  expect(
    libraryEntries(problems, '').some((entry) => entry.problem?.id === excluded.problemId),
  ).toBe(true);
  const companions = libraryEntries(problems, 'kind:reading');
  expect(companions).toHaveLength(12);
  for (const reference of guide.columns.flat().filter((entry) => !entry.problemId))
    expect(
      companions.some((entry) => entry.lesson?.bookReferences.includes(reference.number)),
    ).toBe(true);
  expect(libraryEntries(problems, '').filter((entry) => entry.lesson)).toHaveLength(12);
});

it('keeps Blind 75 separate, ordered, searchable, and distinct from similar EPI titles', () => {
  const blind = [
    {
      id: 'blind75_two_sum',
      title: 'Two Sum',
      topic: 'Arrays',
      collection: 'blind75',
      position: 1,
    },
    {
      id: 'blind75_combination_sum',
      title: 'Combination Sum',
      topic: 'Arrays',
      collection: 'blind75',
      position: 9,
    },
    {
      id: 'blind75_combination_sum_iv',
      title: 'Combination Sum IV',
      topic: 'Dynamic Programming',
      collection: 'blind75',
      position: 70,
    },
  ] as Problem[];
  const combined = [...problems, ...blind];
  expect(libraryEntries(combined, 'collection:epi').map((e) => e.problem?.id)).toEqual(
    problems.map((p) => p.id),
  );
  const entries = libraryEntries(combined, 'collection:blind75');
  expect(entries.map((e) => e.problem?.id)).toEqual(blind.map((p) => p.id));
  expect(entries.map((e) => e.number)).toEqual(['B01', 'B09', 'B70']);
  expect(entries.every((e) => !e.lesson)).toBe(true);
  expect(
    libraryEntries(combined, 'collection:blind75', 'COMBINATION').map((e) => e.number),
  ).toEqual(['B09', 'B70']);
  expect(libraryEntries(combined, 'collection:blind75', 'missing query')).toEqual([]);
  expect(libraryEntries(combined, 'plan:3-days').map((e) => e.number)).toEqual(
    libraryEntries(problems, 'plan:3-days').map((e) => e.number),
  );
  expect(new Set(libraryEntries(combined, '').map((e) => e.number)).size).toBe(
    libraryEntries(combined, '').length,
  );
});
