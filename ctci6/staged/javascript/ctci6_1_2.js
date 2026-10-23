'use strict';
function CheckPermutation(first, second) {
  if (first.length !== second.length) return false;
  const counts = Array(128).fill(0);
  for (let i = 0; i < first.length; ++i) ++counts[first.charCodeAt(i)];
  for (let i = 0; i < second.length; ++i) {
      const code = second.charCodeAt(i);
      if (--counts[code] < 0) return false;
  }
  return true;
}
