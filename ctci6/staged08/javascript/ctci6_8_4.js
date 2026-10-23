'use strict';
function PowerSet(values) {
  const result = [[]];
  for (const value of values) {
    const original = result.length;
    for (let i = 0; i < original; ++i) result.push([...result[i], value]);
  }
  return result;
}
