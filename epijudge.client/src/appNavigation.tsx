import { useEffect, useState, type AnchorHTMLAttributes } from 'react';

export function appRoute() {
  const url = new URL(window.location.href);
  const parts = url.pathname.split('/').filter(Boolean);
  let articleId = '';
  try {
    articleId = decodeURIComponent(parts[1] ?? '');
  } catch {
    articleId = '__invalid__';
  }
  return {
    section: parts[0] === 'learn' || parts[0] === 'reading' ? 'learn' : 'practice',
    articleId,
    topic: url.searchParams.get('topic') ?? '',
    source: url.searchParams.get('source') ?? '',
    query: url.searchParams.get('q') ?? '',
    problemId: url.searchParams.get('problem') ?? '',
    unknownPath:
      !['', 'practice', 'learn', 'reading'].includes(parts[0] ?? '') ||
      parts.length > 2 ||
      (parts[0] === 'practice' && parts.length > 1),
  };
}
export function navigateApp(href: string, replace = false) {
  if (replace) window.history.replaceState(null, '', href);
  else window.history.pushState(null, '', href);
  window.dispatchEvent(new PopStateEvent('popstate'));
}
export function useAppRoute() {
  const [route, setRoute] = useState(appRoute);
  useEffect(() => {
    const update = () => setRoute(appRoute());
    window.addEventListener('popstate', update);
    window.addEventListener('hashchange', update);
    return () => {
      window.removeEventListener('popstate', update);
      window.removeEventListener('hashchange', update);
    };
  }, []);
  useEffect(() => {
    const main = document.querySelector('main');
    if (!main) return;
    if (window.location.hash) {
      const target = document.getElementById(window.location.hash.slice(1));
      target?.scrollIntoView?.();
      target?.focus({ preventScroll: true });
    } else {
      main.scrollTop = 0;
      const heading = main.querySelector('h1');
      heading?.setAttribute('tabindex', '-1');
      heading?.focus({ preventScroll: true });
    }
  }, [route.section, route.articleId, route.problemId]);
  return route;
}
export function AppLink({
  href = '/',
  onClick,
  ...props
}: AnchorHTMLAttributes<HTMLAnchorElement>) {
  return (
    <a
      {...props}
      href={href}
      onClick={(event) => {
        onClick?.(event);
        if (
          !event.defaultPrevented &&
          !event.ctrlKey &&
          !event.metaKey &&
          !event.shiftKey &&
          !event.altKey &&
          event.button === 0 &&
          props.target !== '_blank'
        ) {
          event.preventDefault();
          navigateApp(href);
        }
      }}
    />
  );
}
