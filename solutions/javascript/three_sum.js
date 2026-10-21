function hasThreeSum(A, t) {
  const values = A.slice().sort((a, b) => a - b);
  for (const first of values) {
    let left = 0,
      right = values.length - 1;
    while (left <= right) {
      const sum = first + values[left] + values[right];
      if (sum === t) return true;
      if (sum < t) left++;
      else right--;
    }
  }
  return false;
}

module.exports = { hasThreeSum };
