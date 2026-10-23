'use strict';
function InsertBits(word, insert, low, high) {
  const width = high - low + 1,
    mask = (2 ** width - 1) >>> 0;
  return (word & ~(mask << low)) | ((insert & mask) << low);
}
