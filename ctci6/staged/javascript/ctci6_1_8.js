'use strict';
function ZeroMatrix(matrix) {
  const rows = matrix.length;
  if (rows === 0) return;
  const cols = matrix[0].length;
  const zeroRows = Array(rows).fill(false), zeroCols = Array(cols).fill(false);
  for (let r = 0; r < rows; ++r) {
      for (let c = 0; c < cols; ++c) {
          if (matrix[r][c] === 0) { zeroRows[r] = true; zeroCols[c] = true; }
      }
  }
  for (let r = 0; r < rows; ++r) {
      for (let c = 0; c < cols; ++c) {
          if (zeroRows[r] || zeroCols[c]) matrix[r][c] = 0;
      }
  }
}
