import { useSyncExternalStore } from 'react';

export type Theme = 'light' | 'dark';
export const THEME_KEY = 'epi:theme';
const mediaQuery = '(prefers-color-scheme: dark)';
let unsavedChoice: Theme | null = null;

function preference(): Theme | null {
  if (unsavedChoice) return unsavedChoice;
  try {
    const saved = localStorage.getItem(THEME_KEY);
    return saved === 'light' || saved === 'dark' ? saved : null;
  } catch {
    return null;
  }
}
function systemTheme(): Theme {
  return window.matchMedia?.(mediaQuery).matches ? 'dark' : 'light';
}
function apply(theme: Theme) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', theme === 'dark' ? '#1a1a1a' : '#f3f5f8');
  window.dispatchEvent(new Event('epi:theme-change'));
}
function snapshot(): Theme {
  const current = document.documentElement.dataset.theme;
  return current === 'light' || current === 'dark' ? current : (preference() ?? systemTheme());
}
function subscribe(update: () => void) {
  const media = window.matchMedia?.(mediaQuery);
  const systemChanged = () => {
    if (!preference()) apply(systemTheme());
  };
  const storageChanged = (event: StorageEvent) => {
    if (event.key === THEME_KEY || event.key === null) {
      unsavedChoice = null;
      apply(preference() ?? systemTheme());
    }
  };
  window.addEventListener('epi:theme-change', update);
  window.addEventListener('storage', storageChanged);
  media?.addEventListener('change', systemChanged);
  // Also initialize isolated renders that do not load index.html's bootstrap.
  if (!document.documentElement.dataset.theme) apply(preference() ?? systemTheme());
  return () => {
    window.removeEventListener('epi:theme-change', update);
    window.removeEventListener('storage', storageChanged);
    media?.removeEventListener('change', systemChanged);
  };
}
export function useTheme() {
  return useSyncExternalStore(subscribe, snapshot);
}
export function setTheme(theme: Theme) {
  try {
    localStorage.setItem(THEME_KEY, theme);
    unsavedChoice = null;
  } catch {
    unsavedChoice = theme; // Keep an explicit choice even when storage is unavailable.
  }
  apply(theme);
}
