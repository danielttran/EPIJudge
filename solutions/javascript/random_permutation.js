function computeRandomPermutation(n) {
  const result = Array.from({ length: n }, (_, i) => i);
  for (let i = 0; i < n; i++) {
    const j = i + Math.floor(Math.random() * (n - i));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

module.exports = { computeRandomPermutation };
