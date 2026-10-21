function combinations(n, k) {
  const result = [],
    chosen = [];
  function search(next) {
    if (chosen.length === k) {
      result.push(chosen.slice());
      return;
    }
    const needed = k - chosen.length;
    for (let value = next; value <= n - needed + 1; value++) {
      chosen.push(value);
      search(value + 1);
      chosen.pop();
    }
  }
  if (k >= 0 && k <= n) search(1);
  return result;
}

module.exports = { combinations };
