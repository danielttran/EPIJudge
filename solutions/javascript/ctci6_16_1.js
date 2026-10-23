'use strict';
function SwapWithoutTemporary(first, second) {
  first ^= second;
  second ^= first;
  first ^= second;
  return [first, second];
}

module.exports = {SwapWithoutTemporary};
