// Runs before the stylesheet and React so the first paint uses the chosen theme.
(() => {
  let saved;
  try {
    saved = localStorage.getItem('epi:theme');
  } catch {
    /* Storage may be unavailable. */
  }
  const theme =
    saved === 'light' || saved === 'dark'
      ? saved
      : window.matchMedia?.('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', theme === 'dark' ? '#1a1a1a' : '#f3f5f8');
})();
