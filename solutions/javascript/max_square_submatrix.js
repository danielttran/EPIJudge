function maxSquareSubmatrix(A) {
  if (!A.length) return 0;
  let previous = Array(A[0].length + 1).fill(0),
    side = 0;
  for (const row of A) {
    const current = Array(row.length + 1).fill(0);
    for (let c = 1; c <= row.length; c++)
      if (row[c - 1]) {
        current[c] = 1 + Math.min(previous[c - 1], previous[c], current[c - 1]);
        side = Math.max(side, current[c]);
      }
    previous = current;
  }
  return side * side;
}

module.exports = { maxSquareSubmatrix };
