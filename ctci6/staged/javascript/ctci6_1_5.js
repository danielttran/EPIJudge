'use strict';
function OneAway(first, second) {
  const n = first.length,
    m = second.length;
  if (Math.abs(n - m) > 1) return false;
  let i = 0,
    j = 0,
    used = false;
  while (i < n && j < m) {
    if (first[i] === second[j]) {
      ++i;
      ++j;
    } else {
      if (used) return false;
      used = true;
      if (n >= m) ++i;
      if (m >= n) ++j;
    }
  }
  return true;
}
