function findLongestSubarrayLessEqualK(A, k) {
  const prefix = Array(A.length + 1).fill(0),
    maximum = Array(A.length + 1).fill(0);
  for (let i = 0; i < A.length; i++) {
    prefix[i + 1] = prefix[i] + A[i];
    maximum[i + 1] = Math.max(maximum[i], prefix[i + 1]);
  }
  let best = 0;
  for (let end = 1; end <= A.length; end++) {
    const threshold = prefix[end] - k;
    let low = 0,
      high = end;
    while (low < high) {
      const mid = low + Math.floor((high - low) / 2);
      if (maximum[mid] >= threshold) high = mid;
      else low = mid + 1;
    }
    best = Math.max(best, end - low);
  }
  return best;
}

module.exports = { findLongestSubarrayLessEqualK };
