'use strict';
function CountTripleSteps(steps) {
  if (steps < 0) return 0;
  let previous = 1,
    older = 0,
    oldest = 0;
  for (let i = 0; i < steps; ++i) {
    const current = previous + older + oldest;
    oldest = older;
    older = previous;
    previous = current;
  }
  return previous;
}
