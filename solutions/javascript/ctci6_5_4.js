'use strict';
function SameWeightNeighbors(number) {
  function successor(value) {
    if (value === 0) return -1;
    const lowest = value & -value,
      raised = value + lowest;
    if (raised > 2147483647) return -1;
    return raised | (Math.floor((raised ^ value) / lowest) >>> 2);
  }
  const larger = successor(number),
    reverse = successor(2147483647 ^ number);
  return [reverse === -1 ? -1 : 2147483647 ^ reverse, larger];
}

module.exports = {SameWeightNeighbors};
