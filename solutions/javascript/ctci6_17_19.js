'use strict';
function MissingTwo(values) {
  const n = values.length + 2;
  let combined = 0;
  for (let value = 1; value <= n; ++value) combined ^= value;
  for (const value of values) combined ^= value;
  const bit = combined & -combined;
  let first = 0,
    second = 0;
  for (let value = 1; value <= n; ++value) {
    if (value & bit) first ^= value;
    else second ^= value;
  }
  for (const value of values) {
    if (value & bit) first ^= value;
    else second ^= value;
  }
  return [Math.min(first, second), Math.max(first, second)];
}

module.exports = {MissingTwo};
