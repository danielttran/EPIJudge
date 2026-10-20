import guide from './studyGuide.json';
import type { Problem } from './workspaceModels';
import { READING_LESSONS, type ReadingLesson } from './reading/readingLessons';

export const STUDY_PLANS = [
  { id: '3-days', label: '3 days — Hackathon', scenario: 1 },
  { id: '7-days', label: '7 days — Finals cram', scenario: 2 },
  { id: '1-month', label: '1 month — Term project', scenario: 3 },
  { id: '4-months', label: '4 months — Algorithms class', scenario: 4 },
] as const;

export type LibraryEntry = {
  problem?: Problem;
  lesson?: ReadingLesson;
  number: string;
  title: string;
  topic: string;
  column?: number;
  reason?: string;
};

export function selectedStudyPlan(filter: string) {
  return STUDY_PLANS.find((plan) => filter === `plan:${plan.id}`);
}

export function libraryEntries(problems: Problem[], filter: string, query = ''): LibraryEntry[] {
  const plan = selectedStudyPlan(filter);
  const byId = new Map(problems.map((problem) => [problem.id, problem]));
  let entries: LibraryEntry[];
  if (plan) {
    const seen = new Set<string>();
    entries = [];
    for (let column = 0; column < plan.scenario; column++) {
      for (const item of guide.columns[column]) {
        if (seen.has(item.number)) continue;
        seen.add(item.number);
        const problem = item.problemId ? byId.get(item.problemId) : undefined;
        entries.push({
          ...item,
          problem,
          lesson: problem
            ? undefined
            : READING_LESSONS.find((lesson) => lesson.bookReferences.includes(item.number)),
          column,
          reason: problem
            ? undefined
            : 'reason' in item
              ? item.reason
              : 'This book exercise is not available in the current catalog.',
        });
      }
    }
  } else {
    entries = problems.flatMap((problem, index) =>
      !filter ||
      filter === 'kind:coding' ||
      (filter.startsWith('collection:') && (problem.collection ?? 'epi') === filter.slice(11)) ||
      problem.topic === filter
        ? [
            {
              problem,
              number:
                problem.collection === 'blind75'
                  ? `B${String(problem.position).padStart(2, '0')}`
                  : String(index + 1).padStart(2, '0'),
              title: problem.title,
              topic: problem.topic,
            },
          ]
        : [],
    );
    entries.push(
      ...READING_LESSONS.flatMap((lesson, index) =>
        !filter || filter === 'kind:reading' || lesson.topic === filter
          ? [
              {
                lesson,
                number: `R${String(index + 1).padStart(2, '0')}`,
                title: lesson.title,
                topic: lesson.topic,
              },
            ]
          : [],
      ),
    );
  }
  const search = query.trim().toLowerCase();
  return entries.filter((item) =>
    `${item.number} ${item.title} ${item.topic} ${item.problem?.id ?? ''}`
      .toLowerCase()
      .includes(search),
  );
}
