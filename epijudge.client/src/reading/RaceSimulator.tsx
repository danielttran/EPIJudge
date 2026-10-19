import { useState } from 'react';
import { initialRace, stepRace } from './raceSimulation';

export function RaceSimulator() {
  const [state, setState] = useState(initialRace);
  const [locked, setLocked] = useState(false);
  return (
    <section className="reading-interaction" aria-label="Thread interleaving simulator">
      <h2>Try an interleaving</h2>
      <p>Each thread increments once: read, compute, write. Expected final counter: 2.</p>
      <label>
        <input
          type="checkbox"
          checked={locked}
          onChange={(event) => {
            setLocked(event.target.checked);
            setState(initialRace());
          }}
        />{' '}
        Lock the entire increment
      </label>
      <p role="status">
        Shared counter: <strong>{state.counter}</strong>
      </p>
      <div className="reading-actions">
        {['A', 'B'].map((name, index) => (
          <button
            key={name}
            disabled={state.stages[index] === 3}
            onClick={() => setState((s) => stepRace(s, index, locked))}
          >
            Step {name} ({['read', 'compute', 'write', 'done'][state.stages[index]]})
          </button>
        ))}
        <button onClick={() => setState(initialRace())}>Reset simulation</button>
      </div>
      <ol className="simulation-log">
        {state.log.map((line, index) => (
          <li key={index}>{line}</li>
        ))}
      </ol>
    </section>
  );
}
