function longestContainedRange(A) {
  const unseen = new Set(A);
  let best = 0;
  for (const value of A) {
    if (!unseen.delete(value)) continue;
    let size = 1;
    for (let x = value - 1; x >= -2147483648 && unseen.delete(x); x--) size++;
    for (let x = value + 1; x <= 2147483647 && unseen.delete(x); x++) size++;
    best = Math.max(best, size);
  }
  return best;
}

module.exports = { longestContainedRange };
