'use strict';
class Listy { ElementAt(index) { throw new Error("Provided by the judge"); } }
function SearchWithoutSize(values, target) {
  if (target <= 0) return -1;
  let bound = 1;
  while (true) {
    const value = values.ElementAt(bound);
    if (value === -1 || value >= target) break;
    bound *= 2;
  }
  let low = Math.floor(bound / 2),
    high = bound;
  while (low <= high) {
    const middle = low + Math.floor((high - low) / 2),
      value = values.ElementAt(middle);
    if (value === -1 || value > target) high = middle - 1;
    else if (value < target) low = middle + 1;
    else return middle;
  }
  return -1;
}

module.exports = {Listy,SearchWithoutSize};
