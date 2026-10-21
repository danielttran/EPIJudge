function calculateTrappingWater(heights) {
  let left = 0,
    right = heights.length - 1,
    leftMax = 0,
    rightMax = 0,
    water = 0;
  while (left <= right) {
    if (leftMax <= rightMax) {
      leftMax = Math.max(leftMax, heights[left]);
      water += leftMax - heights[left++];
    } else {
      rightMax = Math.max(rightMax, heights[right]);
      water += rightMax - heights[right--];
    }
  }
  return water;
}

module.exports = { calculateTrappingWater };
