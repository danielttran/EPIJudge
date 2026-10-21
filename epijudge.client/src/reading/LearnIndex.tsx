import { AppLink, navigateApp, type appRoute } from '../appNavigation';
import { availableLearnTopics, filterArticles, learnHref } from './learnCatalog';

export function LearnIndex({ route }: { route: ReturnType<typeof appRoute> }) {
  const articles = filterArticles(route.topic, route.source, route.query);
  const href = (change: Record<string, string>) => {
    const values = { topic: route.topic, source: route.source, q: route.query, ...change };
    const params = new URLSearchParams(Object.entries(values).filter(([, value]) => value));
    return '/learn' + (params.size ? '?' + params : '');
  };
  return (
    <div className="learn-index">
      <header className="learn-intro">
        <p className="learn-eyebrow">READ · REASON · PRACTICE</p>
        <h1>Learn</h1>
        <p>
          Build understanding, then put it into practice. Explore original study companions by
          topic.
        </p>
      </header>
      <div className="learn-index-grid">
        <aside className="learn-topic-sidebar">
          <h2>Topics</h2>
          <nav aria-label="Learn topics">
            <AppLink href={href({ topic: '' })} aria-current={!route.topic ? 'page' : undefined}>
              All topics <span>12</span>
            </AppLink>
            {availableLearnTopics.map((topic) => (
              <AppLink
                key={topic.id}
                href={href({ topic: topic.id })}
                aria-current={route.topic === topic.id ? 'page' : undefined}
              >
                {topic.title}
                <span>{filterArticles(topic.id, '', '').length}</span>
              </AppLink>
            ))}
          </nav>
          <p>Topics appear when local articles are available.</p>
        </aside>
        <section className="learn-results" aria-label="Articles">
          <div className="learn-filters">
            <label>
              Search articles
              <input
                type="search"
                value={route.query}
                placeholder="Search ideas, topics, or titles…"
                onChange={(event) => navigateApp(href({ q: event.target.value }), true)}
              />
            </label>
            <label>
              Source
              <select
                value={route.source}
                onChange={(event) => navigateApp(href({ source: event.target.value }))}
              >
                <option value="">All sources</option>
                <option value="other">Other sources</option>
                {route.source && route.source !== 'other' && (
                  <option value={route.source}>Unavailable source</option>
                )}
              </select>
            </label>
          </div>
          <p className="learn-count" role="status">
            {articles.length} {articles.length === 1 ? 'article' : 'articles'}
          </p>
          {availableLearnTopics.map((topic) => {
            const group = articles.filter((article) => article.topicId === topic.id);
            return group.length ? (
              <section className="learn-topic-group" key={topic.id}>
                <h2>{topic.title}</h2>
                <p>{topic.description}</p>
                <div className="learn-card-grid">
                  {group.map((article) => (
                    <AppLink className="learn-card" key={article.id} href={learnHref(article.id)}>
                      <span className="learn-card-source">
                        {article.sourceLabel} · {article.readingMinutes} min read
                      </span>
                      <h3>{article.title}</h3>
                      <p>{article.description}</p>
                      <span className="learn-card-action">
                        Read article <span aria-hidden="true">→</span>
                      </span>
                    </AppLink>
                  ))}
                </div>
              </section>
            ) : null;
          })}
          {!articles.length && (
            <div className="learn-empty">
              <h2>No matching articles</h2>
              <p>Try another topic, source, or search term.</p>
              <AppLink href="/learn">Clear filters</AppLink>
            </div>
          )}
          <p className="learn-source-note">
            These 12 original EPI study companions are stored locally. Interview Cake’s 41 coding
            questions remain in Practice; no Interview Cake reading articles are currently available
            here. External references remain links to their publishers. These independently authored
            companions are not affiliated with source publishers.
          </p>
        </section>
      </div>
    </div>
  );
}
