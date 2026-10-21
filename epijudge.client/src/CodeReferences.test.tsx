import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { CodeReferences } from './CodeReferences';

vi.mock('./Editor', () => ({
  ReadOnlyCode: ({ code, label }: { code: string; label: string }) => (
    <pre aria-label={label}>{code}</pre>
  ),
}));
afterEach(cleanup);

it('omits the reference surface when no supplied types or APIs are needed', () => {
  const view = render(<CodeReferences references={[]} language="csharp" />);
  expect(view.container.innerHTML).toBe('');
});
it('keeps relevant reference code collapsed and separate from editable code', async () => {
  const view = render(
    <CodeReferences
      references={[
        { title: 'List node', code: 'class ListNode {\n    int value;\n}', names: ['ListNode'] },
      ]}
      language="csharp"
    />,
  );
  const details = view.container.querySelector('details')!;
  expect(details.open).toBe(false);
  expect(screen.queryByLabelText('List node provided reference')).toBeNull();
  expect(screen.queryByRole('textbox')).toBeNull();
  expect(screen.queryByRole('button', { name: /replace|load|editor/i })).toBeNull();
  fireEvent.click(screen.getByText('Provided types and APIs'));
  expect(details.open).toBe(true);
  expect((await screen.findByLabelText('List node provided reference')).textContent).toContain(
    'ListNode',
  );
});
