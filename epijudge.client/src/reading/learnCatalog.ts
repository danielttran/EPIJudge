import inventory from './learnInventory.json';
import { READING_LESSONS } from './readingLessons';
import type { Problem } from '../workspaceModels';

export const LEARN_TOPICS = [
  {
    id: 'foundations',
    title: 'Foundations',
    description: 'Reason about shared state, coordination, and scheduling.',
  },
  { id: 'arrays-strings', title: 'Arrays & Strings', description: 'Work with sequences and text.' },
  { id: 'hashing', title: 'Hashing', description: 'Organize fast lookups and membership.' },
  {
    id: 'trees-graphs',
    title: 'Trees & Graphs',
    description: 'Explore relationships, paths, and ancestors.',
  },
  {
    id: 'recursion-dp',
    title: 'Recursion & Dynamic Programming',
    description: 'Break problems into smaller subproblems.',
  },
  {
    id: 'system-design',
    title: 'System Design',
    description: 'Define contracts, weigh tradeoffs, and plan for failure.',
  },
  {
    id: 'language-concepts',
    title: 'Language Concepts',
    description: 'Understand language behavior and execution.',
  },
] as const;

export const LEARN_ARTICLES = inventory.articles.map((item) => {
  const lesson = READING_LESSONS.find((candidate) => candidate.id === item.id);
  if (!lesson || typeof lesson.body !== 'string')
    throw new Error('Missing reading content: ' + item.id);
  return { ...item, lesson };
});
export type LearnArticle = (typeof LEARN_ARTICLES)[number];
export const availableLearnTopics = LEARN_TOPICS.filter((topic) =>
  LEARN_ARTICLES.some((article) => article.topicId === topic.id),
);
export const learnArticleById = (id: string) => LEARN_ARTICLES.find((article) => article.id === id);
export const learnHref = (id: string) => '/learn/' + encodeURIComponent(id);
export const practiceHref = (id: string) => '/practice?problem=' + encodeURIComponent(id);
export const headingId = (text: string) =>
  'section-' +
  text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
export const articleHeadings = (body: string) =>
  [...body.matchAll(/^## (.+)$/gm)].map((match) => ({ title: match[1], id: headingId(match[1]) }));
export const relatedArticles = (problemId: string) =>
  LEARN_ARTICLES.filter((article) =>
    article.relatedProblems.some((problem) => problem.id === problemId),
  );
export const relatedProblems = (article: LearnArticle, problems: Problem[]) =>
  article.relatedProblems.flatMap((relation) => {
    const problem = problems.find((candidate) => candidate.id === relation.id);
    return problem ? [{ problem, reason: relation.reason }] : [];
  });

export function filterArticles(topic: string, source: string, query: string) {
  const search = query.trim().toLocaleLowerCase();
  return LEARN_ARTICLES.filter(
    (article) =>
      (!topic || article.topicId === topic) &&
      (!source || article.sourceId === source) &&
      `${article.title} ${article.description} ${article.originalTopic} ${LEARN_TOPICS.find((item) => item.id === article.topicId)?.title ?? ''} ${article.sourceLabel} ${article.lesson.body}`
        .toLocaleLowerCase()
        .includes(search),
  );
}
