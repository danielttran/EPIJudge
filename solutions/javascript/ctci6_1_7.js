'use strict';
function Rotate(matrix) {
  const n = matrix.length;
  for (let r = 0; r < n; ++r) {
    for (let c = r + 1; c < n; ++c) {
      const saved = matrix[r][c];
      matrix[r][c] = matrix[c][r];
      matrix[c][r] = saved;
    }
  }
  for (let r = 0; r < n; ++r) {
    for (let c = 0; c < Math.floor(n / 2); ++c) {
      const saved = matrix[r][c];
      matrix[r][c] = matrix[r][n - 1 - c];
      matrix[r][n - 1 - c] = saved;
    }
  }
}

module.exports = {Rotate};
