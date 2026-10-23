'use strict';
function CountBitChanges(first, second) {
  let difference = (first ^ second) >>> 0,
    count = 0;
  while (difference !== 0) {
    difference = (difference & (difference - 1)) >>> 0;
    ++count;
  }
  return count;
}

module.exports = {CountBitChanges};
