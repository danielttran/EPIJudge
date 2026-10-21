function smallestNonconstructibleValue(A) {
  let covered = 0;
  for (const value of A.slice().sort((a, b) => a - b)) {
    if (value > covered + 1) break;
    covered += value;
  }
  return covered + 1;
}

module.exports = { smallestNonconstructibleValue };
