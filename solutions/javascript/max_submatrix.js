function maxRectangleSubmatrix(A) {
  if (!A.length) return 0;
  const heights = Array(A[0].length).fill(0);
  let best = 0;
  for (const row of A) {
    for (let c = 0; c < heights.length; c++)
      heights[c] = row[c] ? heights[c] + 1 : 0;
    const stack = [];
    for (let c = 0; c <= heights.length; c++) {
      const current = c === heights.length ? 0 : heights[c];
      while (stack.length && heights[stack.at(-1)] >= current) {
        const height = heights[stack.pop()],
          left = stack.length ? stack.at(-1) + 1 : 0;
        best = Math.max(best, height * (c - left));
      }
      stack.push(c);
    }
  }
  return best;
}

module.exports = { maxRectangleSubmatrix };
