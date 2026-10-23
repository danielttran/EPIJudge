'use strict';
function LargestBlackBorder(matrix) {
  const n = matrix.length,
    right = Array.from({ length: n }, () => Array(n).fill(0)),
    down = Array.from({ length: n }, () => Array(n).fill(0));
  for (let r = n - 1; r >= 0; --r) {
    for (let c = n - 1; c >= 0; --c) {
      if (matrix[r][c] === 0) {
        right[r][c] = 1 + (c + 1 < n ? right[r][c + 1] : 0);
        down[r][c] = 1 + (r + 1 < n ? down[r + 1][c] : 0);
      }
    }
  }
  for (let size = n; size >= 1; --size) {
    for (let r = 0; r + size <= n; ++r) {
      for (let c = 0; c + size <= n; ++c) {
        if (
          right[r][c] >= size &&
          down[r][c] >= size &&
          right[r + size - 1][c] >= size &&
          down[r][c + size - 1] >= size
        )
          return [r, c, size];
      }
    }
  }
  return [];
}

module.exports = {LargestBlackBorder};
