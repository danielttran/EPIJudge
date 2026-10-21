import { useState } from 'react';
import { ReadOnlyCode } from './Editor';
import type { CodeReference } from './workspaceModels';

export function CodeReferences({
  references,
  language,
}: {
  references: CodeReference[];
  language: string;
}) {
  const [expanded, setExpanded] = useState(false);
  if (!references.length) return null;
  return (
    <details
      className="provided-code-reference"
      onToggle={(event) => setExpanded(event.currentTarget.open)}
    >
      <summary>Provided types and APIs</summary>
      {expanded && (
        <>
          <p>These definitions are available to your code. You do not need to write them.</p>
          {references.map((reference) => (
            <section key={reference.title}>
              <h3>{reference.title}</h3>
              <ReadOnlyCode
                code={reference.code}
                language={language}
                label={reference.title + ' provided reference'}
                className="provided-reference-code"
              />
            </section>
          ))}
        </>
      )}
    </details>
  );
}
