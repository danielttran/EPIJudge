import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { createHash } from 'node:crypto';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { AppLink, appRoute, navigateApp } from '../appNavigation';
import { PracticeClient } from '../practiceClient';
import { LearnIndex } from './LearnIndex';
import { LearnArticle } from './LearnArticle';
import {
  LEARN_ARTICLES,
  LEARN_TOPICS,
  availableLearnTopics,
  filterArticles,
  relatedArticles,
  relatedProblems,
  articleHeadings,
  headingId,
  learnHref,
  practiceHref,
} from './learnCatalog';
import { READING_LESSONS } from './readingLessons';

beforeEach(() => window.history.replaceState(null, '', '/learn'));
afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.restoreAllMocks();
});

it('maps every existing body exactly once with verified source, duration, and storage IDs', () => {
  expect(LEARN_ARTICLES).toHaveLength(12);
  expect(new Set(LEARN_ARTICLES.map((article) => article.id)).size).toBe(12);
  expect(LEARN_ARTICLES.map((article) => article.id)).toEqual(
    READING_LESSONS.map((lesson) => lesson.id),
  );
  for (const article of LEARN_ARTICLES) {
    expect(createHash('sha256').update(article.lesson.body).digest('hex')).toBe(article.bodySha256);
    const words = article.lesson.body.trim().split(/\s+/).length;
    expect(article.wordCount).toBe(words);
    expect(article.readingMinutes).toBe(Math.max(1, Math.ceil(words / 200)));
    expect(article.sourceUrls).toEqual(article.lesson.sources);
    expect(article.sourceLabel).toBe('EPI study companion');
    expect(article.sourceId).toBe('other');
    expect(LEARN_TOPICS.some((topic) => topic.id === article.topicId)).toBe(true);
    const headings = articleHeadings(article.lesson.body);
    expect(headings).toHaveLength(4);
    expect(new Set(headings.map((heading) => heading.id)).size).toBe(4);
  }
  expect(availableLearnTopics.map((topic) => topic.id)).toEqual([
    'foundations',
    'trees-graphs',
    'system-design',
  ]);
});

it('retains all 334 runnable questions and only links to real, explicitly mapped exercises', () => {
  const root = existsSync(resolve(process.cwd(), 'EpiJudge.Runner/catalog.json'))
    ? process.cwd()
    : resolve(process.cwd(), '..');
  const epi = JSON.parse(readFileSync(resolve(root, 'EpiJudge.Runner/catalog.json'), 'utf8'));
  const blind = JSON.parse(readFileSync(resolve(root, 'blind75/catalog.json'), 'utf8'));
  const cake = JSON.parse(readFileSync(resolve(root, 'interviewcake/catalog.json'), 'utf8'));
  expect([epi.length, blind.length, cake.length]).toEqual([215, 75, 41]);
  const solutions = JSON.parse(
    readFileSync(resolve(root, 'solutions/catalog.json'), 'utf8'),
  ) as Array<{ problemId: string; language: string; collection: string }>;
  const current = solutions.filter((item) => item.language === 'csharp');
  expect(
    ['epi', 'blind75', 'interviewcake'].map(
      (name) => current.filter((item) => item.collection === name).length,
    ),
  ).toEqual([218, 75, 41]);
  const ids = new Set(current.map((problem) => problem.problemId));
  for (const article of LEARN_ARTICLES) {
    for (const relation of article.relatedProblems) expect(ids.has(relation.id)).toBe(true);
    expect(relatedProblems(article, [])).toEqual([]);
  }
  expect(relatedArticles('lowest_common_ancestor')).toHaveLength(2);
  expect(relatedArticles('not-a-real-problem')).toEqual([]);
});

it('searches local content, composes topic/source filters and returns honest empty results', () => {
  expect(filterArticles('', '', '')).toHaveLength(12);
  expect(filterArticles('foundations', 'other', '')).toHaveLength(4);
  expect(filterArticles('trees-graphs', '', 'IDENTITY')).toHaveLength(2);
  expect(filterArticles('', 'interviewcake', '')).toEqual([]);
  expect(filterArticles('unknown', '', '')).toEqual([]);
  expect(filterArticles('', '', 'nonexistent article term')).toEqual([]);
  expect(headingId('Core idea')).toBe('section-core-idea');
  expect(learnHref('a b')).toBe('/learn/a%20b');
  expect(practiceHref('a b')).toBe('/practice?problem=a%20b');
});

it('shows the actual source inventory and twelve unique cards with hidden empty categories', () => {
  render(<LearnIndex route={appRoute()} />);
  expect(screen.getByRole('heading', { name: 'Learn' })).toBeTruthy();
  expect(document.querySelectorAll('.learn-card')).toHaveLength(12);
  expect(screen.queryByRole('link', { name: /Arrays & Strings/ })).toBeNull();
  expect(screen.queryByRole('option', { name: 'Interview Cake' })).toBeNull();
  expect(
    screen.getByText(/no Interview Cake reading articles are currently available/i),
  ).toBeTruthy();
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'λ & <script>' } });
  expect(new URL(window.location.href).searchParams.get('q')).toBe('λ & <script>');
  fireEvent.change(screen.getByRole('combobox', { name: 'Source' }), {
    target: { value: 'other' },
  });
  expect(appRoute().source).toBe('other');
});

it('renders empty search states and makes clearing filters a real local URL', () => {
  navigateApp('/learn?topic=hashing&q=missing');
  render(<LearnIndex route={appRoute()} />);
  expect(screen.getByRole('heading', { name: 'No matching articles' })).toBeTruthy();
  fireEvent.click(screen.getByRole('link', { name: 'Clear filters' }));
  expect(window.location.pathname + window.location.search).toBe('/learn');
});

it('renders every article, its valid ToC targets, notes, and bounded previous/next links', () => {
  const practice = new PracticeClient();
  practice.ready = true;
  for (const article of LEARN_ARTICLES) {
    const view = render(
      <LearnArticle article={article} practice={practice} problems={[]} catalogError="" />,
    );
    expect(screen.getByRole('heading', { name: article.title })).toBeTruthy();
    for (const heading of articleHeadings(article.lesson.body))
      expect(document.getElementById(heading.id)).toBeTruthy();
    expect(screen.getByRole('textbox', { name: 'Your notes and design response' })).toBeTruthy();
    expect(
      screen.getByText(
        article.relatedProblems.length
          ? 'Loading local practice…'
          : 'No directly related local coding exercise.',
      ),
    ).toBeTruthy();
    for (const link of view.container.querySelectorAll<HTMLAnchorElement>(
      'a[href^="/learn/reading-"]',
    ))
      expect(LEARN_ARTICLES.some((item) => learnHref(item.id) === link.getAttribute('href'))).toBe(
        true,
      );
    view.unmount();
  }
});

it('parses deep links, invalid encodings and unknown routes without crashing', () => {
  navigateApp('/learn/reading-shared-state?topic=foundations&q=locks#section-core-idea');
  expect(appRoute()).toMatchObject({
    section: 'learn',
    articleId: 'reading-shared-state',
    query: 'locks',
    unknownPath: false,
  });
  navigateApp('/learn/%E0%A4%A');
  expect(appRoute().articleId).toBe('__invalid__');
  navigateApp('/missing/path/deeper');
  expect(appRoute().unknownPath).toBe(true);
  navigateApp('/practice?problem=parity', true);
  expect(appRoute()).toMatchObject({ section: 'practice', problemId: 'parity' });
  navigateApp('/reading/reading-parent-pointer-lca');
  expect(appRoute().section).toBe('learn');
});

it('uses normal links for keyboard/new-tab access and respects prevented navigation', () => {
  const view = render(
    <>
      <AppLink href="/learn?topic=foundations">Topic</AppLink>
      <AppLink href="/practice" onClick={(event) => event.preventDefault()}>
        Busy
      </AppLink>
      <AppLink href="/practice" target="_blank">
        New tab
      </AppLink>
      <AppLink>Default</AppLink>
    </>,
  );
  fireEvent.click(screen.getByRole('link', { name: 'Busy' }));
  expect(window.location.pathname).toBe('/learn');
  fireEvent.click(screen.getByRole('link', { name: 'Topic' }));
  expect(appRoute().topic).toBe('foundations');
  expect(screen.getByRole('link', { name: 'New tab' }).getAttribute('target')).toBe('_blank');
  expect(view.container.querySelector('a[href="/"]')).toBeTruthy();
});
