import { useState } from 'react';
import { guidanceFor } from './problemGuidance';

/** The parent keys this component by problem, so hints never leak across navigation. */
export function ProblemHints({ problemId }: { problemId: string }) {
  const guidance = guidanceFor(problemId);
  const [revealed, setRevealed] = useState(0);
  if (!guidance?.hints.length) return null;
  return (
    <section id={`hints-${problemId}`} className="problem-hints" aria-label="Problem hints">
      <h2>Hints</h2>
      <p>Reveal one at a time. The later hint gives a concrete approach, not code.</p>
      <div aria-live="polite" aria-atomic="false">
        {guidance.hints.slice(0, revealed).map((hint, index) => (
          <details key={index} open className="problem-hint">
            <summary>
              Hint {index + 1} — {index === 0 ? 'What to notice' : 'An approach'}
            </summary>
            <p>{hint}</p>
          </details>
        ))}
      </div>
      <div className="hint-actions">
        {revealed < guidance.hints.length && (
          <button
            type="button"
            className="secondary-button"
            onClick={() => setRevealed((count) => Math.min(count + 1, guidance.hints.length))}
          >
            {revealed === 0 ? 'Reveal first hint' : 'Reveal next hint'}
          </button>
        )}
        {revealed > 0 && (
          <button type="button" className="secondary-button" onClick={() => setRevealed(0)}>
            Hide hints
          </button>
        )}
      </div>
    </section>
  );
}
