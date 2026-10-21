function computeTowerHanoi(numRings) {
  const moves = [];
  function transfer(count, from, to, spare) {
    if (!count) return;
    transfer(count - 1, from, spare, to);
    moves.push([from, to]);
    transfer(count - 1, spare, to, from);
  }
  transfer(numRings, 0, 1, 2);
  return moves;
}

module.exports = { computeTowerHanoi };
