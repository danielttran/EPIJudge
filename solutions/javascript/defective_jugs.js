function checkFeasible(jugs, l, h) {
  const impossible = new Set();
  function search(low, high) {
    if (low <= 0 && high >= 0) return true;
    const key = low + "," + high;
    if (high < 0 || low > high || impossible.has(key)) return false;
    for (const [jugLow, jugHigh] of jugs) {
      if (jugLow <= 0 || jugHigh < jugLow) continue;
      if (search(low - jugLow, high - jugHigh)) return true;
    }
    impossible.add(key);
    return false;
  }
  return search(l, h);
}

module.exports = { checkFeasible };
