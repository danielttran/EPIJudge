import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { setTheme, THEME_KEY, useTheme } from './theme';

let dark = false;
let changes: Set<() => void>;
function Toggle() {
  const theme = useTheme();
  return (
    <button
      aria-pressed={theme === 'dark'}
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      Dark mode
    </button>
  );
}
beforeEach(() => {
  localStorage.clear();
  delete document.documentElement.dataset.theme;
  changes = new Set();
  dark = false;
  vi.stubGlobal(
    'matchMedia',
    vi.fn(() => ({
      get matches() {
        return dark;
      },
      addEventListener: (_: string, cb: () => void) => changes.add(cb),
      removeEventListener: (_: string, cb: () => void) => changes.delete(cb),
    })),
  );
  window.dispatchEvent(new StorageEvent('storage', { key: THEME_KEY }));
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  window.dispatchEvent(new StorageEvent('storage', { key: THEME_KEY }));
  delete document.documentElement.dataset.theme;
  vi.unstubAllGlobals();
});
function system(value: boolean) {
  act(() => {
    dark = value;
    changes.forEach((cb) => cb());
  });
}
it('follows system changes until the user makes a persistent explicit choice', () => {
  render(<Toggle />);
  expect(screen.getByRole('button').getAttribute('aria-pressed')).toBe('false');
  expect(localStorage.getItem(THEME_KEY)).toBeNull();
  system(true);
  expect(document.documentElement.dataset.theme).toBe('dark');
  fireEvent.click(screen.getByRole('button'));
  expect(localStorage.getItem(THEME_KEY)).toBe('light');
  system(false);
  system(true);
  expect(document.documentElement.dataset.theme).toBe('light');
  cleanup();
  delete document.documentElement.dataset.theme;
  render(<Toggle />);
  expect(screen.getByRole('button').getAttribute('aria-pressed')).toBe('false');
});
it('synchronizes another tab and returns to system preference when storage is cleared', () => {
  render(<Toggle />);
  act(() => {
    localStorage.setItem(THEME_KEY, 'dark');
    window.dispatchEvent(new StorageEvent('storage', { key: THEME_KEY }));
  });
  expect(screen.getByRole('button').getAttribute('aria-pressed')).toBe('true');
  act(() => {
    localStorage.clear();
    window.dispatchEvent(new StorageEvent('storage', { key: null }));
  });
  expect(document.documentElement.dataset.theme).toBe('light');
});
it('keeps switching usable and respects the page choice when storage throws', () => {
  vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
    throw new Error('blocked');
  });
  vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
    throw new Error('blocked');
  });
  render(<Toggle />);
  fireEvent.click(screen.getByRole('button'));
  expect(document.documentElement.dataset.theme).toBe('dark');
  system(true);
  system(false);
  expect(document.documentElement.dataset.theme).toBe('dark');
  fireEvent.click(screen.getByRole('button'));
  expect(document.documentElement.dataset.theme).toBe('light');
});
it.each(['light', 'dark', 'invalid', null])(
  'bootstraps %s before React and styles load',
  (saved) => {
    if (saved) localStorage.setItem(THEME_KEY, saved);
    dark = true;
    const html = readFileSync('index.html', 'utf8');
    expect(html.indexOf('src="/theme.js"')).toBeLessThan(html.indexOf('src="/src/main.tsx"'));
    window.eval(readFileSync('public/theme.js', 'utf8'));
    expect(document.documentElement.dataset.theme).toBe(saved === 'light' ? 'light' : 'dark');
  },
);
