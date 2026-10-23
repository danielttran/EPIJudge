'use strict';
function RepeatedOccurrences(values) {
  const bits = new Uint8Array(4000);
  let count = 0;
  for (const value of values) {
    const slot = (value - 1) >> 3,
      mask = 1 << ((value - 1) & 7);
    if (bits[slot] & mask) ++count;
    else bits[slot] |= mask;
  }
  const result = new Array(count);
  bits.fill(0);
  let write = 0;
  for (const value of values) {
    const slot = (value - 1) >> 3,
      mask = 1 << ((value - 1) & 7);
    if (bits[slot] & mask) result[write++] = value;
    else bits[slot] |= mask;
  }
  return result;
}

module.exports = {RepeatedOccurrences};
