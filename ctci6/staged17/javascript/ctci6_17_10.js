'use strict';
function MajorityElement(values) {
  let candidate = 0,
    balance = 0;
  for (const value of values) {
    if (balance === 0) candidate = value;
    balance += value === candidate ? 1 : -1;
  }
  let count = 0;
  for (const value of values) if (value === candidate) ++count;
  return count > Math.floor(values.length / 2) ? [candidate] : [];
}
