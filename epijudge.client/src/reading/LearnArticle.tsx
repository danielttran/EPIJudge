import { AppLink } from '../appNavigation';
import type { PracticeClient } from '../practiceClient';
import type { Problem } from '../workspaceModels';
import { ReadingWorkspace } from './ReadingWorkspace';
import {
  LEARN_ARTICLES,
  LEARN_TOPICS,
  articleHeadings,
  learnHref,
  practiceHref,
  relatedProblems,
  type LearnArticle as Article,
} from './learnCatalog';

export function LearnArticle({
  article,
  practice,
  problems,
  catalogError,
}: {
  article: Article;
  practice: PracticeClient;
  problems: Problem[];
  catalogError: string;
}) {
  const topic = LEARN_TOPICS.find((item) => item.id === article.topicId)!;
  const index = LEARN_ARTICLES.findIndex((item) => item.id === article.id);
  const previous = LEARN_ARTICLES[index - 1],
    next = LEARN_ARTICLES[index + 1];
  const related = relatedProblems(article, problems);
  return (
    <div className="learn-article-page">
      <nav className="learn-breadcrumb" aria-label="Breadcrumb">
        <AppLink href="/learn">Learn</AppLink>
        <span aria-hidden="true">›</span>
        <AppLink href={'/learn?topic=' + article.topicId}>{topic.title}</AppLink>
        <span aria-hidden="true">›</span>
        <span aria-current="page">{article.title}</span>
      </nav>
      <div className="learn-article-grid">
        <ReadingWorkspace
          key={article.id}
          lesson={article.lesson}
          practice={practice}
          catalogError={catalogError}
        />
        <aside className="learn-article-sidebar">
          <p className="learn-card-source">
            {article.sourceLabel}
            <br />
            {article.readingMinutes} min read · {article.wordCount} words
          </p>
          <nav aria-label="On this page">
            <h2>On this page</h2>
            {articleHeadings(article.lesson.body).map((heading) => (
              <a key={heading.id} href={'#' + heading.id}>
                {heading.title}
              </a>
            ))}
          </nav>
          <section>
            <h2>Related practice</h2>
            {!problems.length && article.relatedProblems.length && !catalogError ? (
              <p>Loading local practice…</p>
            ) : related.length ? (
              related.map(({ problem, reason }) => (
                <AppLink className="learn-related" href={practiceHref(problem.id)} key={problem.id}>
                  <strong>{problem.title}</strong>
                  <span>{reason}</span>
                </AppLink>
              ))
            ) : !catalogError ? (
              <p>No directly related local coding exercise.</p>
            ) : null}
            {catalogError && <p>Practice links are unavailable while the catalog is offline.</p>}
          </section>
          <a href="#reading-notes">Your notes & checkpoints</a>
        </aside>
      </div>
      <nav className="learn-pagination" aria-label="Article navigation">
        {previous ? (
          <AppLink href={learnHref(previous.id)}>
            <span>← Previous article</span>
            <strong>{previous.title}</strong>
          </AppLink>
        ) : (
          <span />
        )}
        {next ? (
          <AppLink href={learnHref(next.id)}>
            <span>Next article →</span>
            <strong>{next.title}</strong>
          </AppLink>
        ) : (
          <span />
        )}
      </nav>
    </div>
  );
}
