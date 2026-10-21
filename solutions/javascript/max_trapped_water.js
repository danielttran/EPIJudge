function getMaxTrappedWater(heights) {
  let left = 0,
    right = heights.length - 1,
    best = 0;
  while (left < right) {
    best = Math.max(
      best,
      (right - left) * Math.min(heights[left], heights[right]),
    );
    if (heights[left] <= heights[right]) left++;
    else right--;
  }
  return best;
}

module.exports = { getMaxTrappedWater };
