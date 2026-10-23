'use strict';
function MaximumSubmatrix(matrix) {
  const rows = matrix.length,
    columns = rows ? matrix[0].length : 0;
  if (!rows || !columns) return [];
  let best = -2147483648,
    answer = [];
  for (let top = 0; top < rows; ++top) {
    const totals = Array(columns).fill(0);
    for (let bottom = top; bottom < rows; ++bottom) {
      let running = 0,
        start = 0;
      for (let c = 0; c < columns; ++c) {
        totals[c] += matrix[bottom][c];
        if (running < 0) {
          running = totals[c];
          start = c;
        } else running += totals[c];
        if (running > best) {
          best = running;
          answer = [best, top, start, bottom, c];
        }
      }
    }
  }
  return answer;
}

module.exports = {MaximumSubmatrix};
