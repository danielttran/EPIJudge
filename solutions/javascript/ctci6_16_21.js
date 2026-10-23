'use strict';
function SumSwap(first, second) {
  let difference = 0;
  for (const value of first) difference += value;
  for (const value of second) difference -= value;
  if (difference % 2 !== 0) return [];
  const half = difference / 2,
    contents = new Set(second);
  for (const value of first) {
    const required = value - half;
    if (contents.has(required)) return [value, required];
  }
  return [];
}

module.exports = {SumSwap};
