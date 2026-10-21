function longestNondecreasingSubsequenceLength(A) {
  const tails = [];
  for (const value of A) {
    let low = 0,
      high = tails.length;
    while (low < high) {
      const mid = low + Math.floor((high - low) / 2);
      if (tails[mid] <= value) low = mid + 1;
      else high = mid;
    }
    if (low === tails.length) tails.push(value);
    else tails[low] = value;
  }
  return tails.length;
}

module.exports = { longestNondecreasingSubsequenceLength };
