'use strict';
function SwapAdjacentBits(word) {
  return ((word & 0x55555555) << 1) | ((word & 0xaaaaaaaa) >>> 1);
}

module.exports = {SwapAdjacentBits};
