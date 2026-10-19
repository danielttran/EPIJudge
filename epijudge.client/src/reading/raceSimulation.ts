export type RaceState = {
  counter: number;
  stages: number[];
  locals: number[];
  owner: number | null;
  log: string[];
};
export const initialRace = (): RaceState => ({
  counter: 0,
  stages: [0, 0],
  locals: [0, 0],
  owner: null,
  log: [],
});

export function stepRace(state: RaceState, thread: number, locked: boolean): RaceState {
  const stage = state.stages[thread];
  if (stage === undefined || stage === 3) return state;
  const name = thread === 0 ? 'A' : 'B';
  if (locked && state.owner !== null && state.owner !== thread)
    return { ...state, log: [...state.log, `${name} waits for the lock.`] };
  const next = {
    ...state,
    stages: [...state.stages],
    locals: [...state.locals],
    log: [...state.log],
  };
  if (locked && stage === 0) next.owner = thread;
  if (stage === 0) next.locals[thread] = state.counter;
  if (stage === 1) next.locals[thread]++;
  if (stage === 2) {
    next.counter = next.locals[thread];
    next.owner = null;
  }
  next.stages[thread]++;
  next.log.push(
    `${name}: ${['read counter', 'increment local', 'write counter'][stage]} → ${stage === 2 ? next.counter : next.locals[thread]}`,
  );
  return next;
}
