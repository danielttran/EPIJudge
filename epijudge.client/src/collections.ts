import type { Problem } from './workspaceModels';

const PRESENTATION: Record<string, { name: string; prefix: string }> = {
  epi: { name: 'EPI', prefix: '' },
  blind75: { name: 'Blind 75', prefix: 'B' },
  interviewcake: { name: 'Interview Cake', prefix: 'IC' },
  ctci6: { name: 'CtCI 6th Edition', prefix: 'C' },
};

export function collectionName(collection = 'epi') {
  return PRESENTATION[collection]?.name ?? collection;
}

export function availableCollections(problems: Problem[]) {
  const counts = new Map<string, number>();
  for (const problem of problems) {
    const id = problem.collection ?? 'epi';
    counts.set(id, (counts.get(id) ?? 0) + 1);
  }
  return [...counts].map(([id, count]) => ({ id, name: collectionName(id), count }));
}

export function problemNumber(problem: Problem, index: number, padded = false) {
  if (problem.collection === 'ctci6') {
    const reference = /^ctci6_(\d+)_(\d+)$/.exec(problem.id);
    if (reference) return `C${reference[1]}.${reference[2]}`;
  }
  const prefix = PRESENTATION[problem.collection ?? 'epi']?.prefix;
  if (prefix) {
    const position = problem.position && problem.position > 0 ? problem.position : index + 1;
    return prefix + String(position).padStart(2, '0');
  }
  return padded ? String(index + 1).padStart(2, '0') : String(index + 1);
}
