'use strict';
function MaximumContiguousSum(values) {
  let running = 0,
    best = 0;
  for (const value of values) {
    running = Math.max(0, running + value);
    best = Math.max(best, running);
  }
  return best;
}

module.exports = {MaximumContiguousSum};
