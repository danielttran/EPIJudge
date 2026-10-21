function calculateLargestRectangle(heights) {
  const increasing = [];
  let best = 0;
  for (let right = 0; right <= heights.length; right++) {
    const current = right === heights.length ? 0 : heights[right];
    while (increasing.length && heights[increasing.at(-1)] >= current) {
      const height = heights[increasing.pop()],
        left = increasing.length ? increasing.at(-1) + 1 : 0;
      best = Math.max(best, height * (right - left));
    }
    increasing.push(right);
  }
  return best;
}

module.exports = { calculateLargestRectangle };
