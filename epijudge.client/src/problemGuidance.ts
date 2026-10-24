import catalog from './problemGuidance.json';

export type ProblemGuidance = { tags: string[]; hints: string[] };
const guidance: Record<string, ProblemGuidance> = catalog;

export function guidanceFor(problemId: string): ProblemGuidance | undefined {
  return Object.hasOwn(guidance, problemId) ? guidance[problemId] : undefined;
}

export function patternTags(problemId: string): string[] {
  return guidanceFor(problemId)?.tags ?? [];
}

export function availablePatterns(problems: { id: string }[]): string[] {
  return [...new Set(problems.flatMap((problem) => patternTags(problem.id)))].sort();
}
