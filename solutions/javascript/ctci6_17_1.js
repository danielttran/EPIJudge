'use strict';
function AddWithoutArithmetic(first, second) {
  while (second !== 0) {
    const carry = (first & second) << 1;
    first ^= second;
    second = carry;
  }
  return first;
}

module.exports = {AddWithoutArithmetic};
