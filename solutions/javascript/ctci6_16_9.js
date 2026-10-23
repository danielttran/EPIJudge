'use strict';
function AdditionOnlyArithmetic(first, second, operation) {
  function opposite(value) {
    const step = value < 0 ? 1 : -1;
    let result = 0;
    while (value !== 0) {
      value += step;
      result += step;
    }
    return result;
  }
  if (operation === "subtract") return first + opposite(second);
  if (operation === "multiply") {
    let count = second < 0 ? opposite(second) : second;
    const addend = second < 0 ? opposite(first) : first;
    let result = 0;
    while (count > 0) {
      result += addend;
      count += -1;
    }
    return result;
  }
  let remaining = first < 0 ? opposite(first) : first;
  const divisor = second < 0 ? opposite(second) : second,
    remove = opposite(divisor),
    step = first < 0 === second < 0 ? 1 : -1;
  let result = 0;
  while (remaining + remove >= 0) {
    remaining += remove;
    result += step;
  }
  return result;
}

module.exports = {AdditionOnlyArithmetic};
