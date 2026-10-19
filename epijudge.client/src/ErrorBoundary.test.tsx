import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { ErrorBoundary } from './ErrorBoundary';

afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.restoreAllMocks();
});

function Broken(): never {
  throw new Error('Test crash');
}

it('keeps unsaved recovery copies intact when the root error screen appears', () => {
  vi.spyOn(console, 'error').mockImplementation(() => {});
  const recoveryKey = 'epi:pending:test:python:count_bits';
  localStorage.setItem(recoveryKey, JSON.stringify({ code: 'unsaved answer', revision: 2 }));
  localStorage.setItem('epi:language', 'python');
  const remove = vi.spyOn(Storage.prototype, 'removeItem');
  render(
    <ErrorBoundary>
      <Broken />
    </ErrorBoundary>,
  );
  expect(
    screen.getByRole('heading', { name: 'Something went wrong loading EPI Practice' }),
  ).toBeTruthy();
  expect(screen.getByRole('button', { name: 'Reload page' })).toBeTruthy();
  expect(screen.queryByRole('button', { name: /clear|reset/i })).toBeNull();
  expect(remove).not.toHaveBeenCalled();
  expect(JSON.parse(localStorage.getItem(recoveryKey)!).code).toBe('unsaved answer');
});

it('lets a failed editor retry through its custom fallback', () => {
  vi.spyOn(console, 'error').mockImplementation(() => {});
  let broken = true;
  function Editor() {
    return broken ? <Broken /> : <p>Editor ready</p>;
  }
  render(
    <ErrorBoundary
      fallback={(_error, reset) => (
        <button
          onClick={() => {
            broken = false;
            reset();
          }}
        >
          Retry editor
        </button>
      )}
    >
      <Editor />
    </ErrorBoundary>,
  );
  fireEvent.click(screen.getByRole('button', { name: 'Retry editor' }));
  expect(screen.getByText('Editor ready')).toBeTruthy();
});
