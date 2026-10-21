function hasTwoSum(values, target) {
  let left = 0,
    right = values.length - 1;
  while (left <= right) {
    const sum = values[left] + values[right];
    if (sum === target) return true;
    if (sum < target) left++;
    else right--;
  }
  return false;
}

module.exports = { hasTwoSum };
