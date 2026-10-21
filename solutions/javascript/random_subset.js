function randomSubset(n, k) {
  const moved = new Map(),
    result = [];
  for (let i = 0; i < k; i++) {
    const j = i + Math.floor(Math.random() * (n - i));
    const chosen = moved.has(j) ? moved.get(j) : j;
    moved.set(j, moved.has(i) ? moved.get(i) : i);
    result.push(chosen);
  }
  return result;
}

module.exports = { randomSubset };
