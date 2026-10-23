'use strict';
function MaximumWithoutComparison(first, second) {
  const negativeFirst = first >>> 31,
    negativeSecond = second >>> 31,
    negativeDifference = (first - second) >>> 31,
    different = negativeFirst ^ negativeSecond,
    chooseFirst = different * (negativeFirst ^ 1) + (different ^ 1) * (negativeDifference ^ 1),
    mask = -chooseFirst;
  return (first & mask) | (second & ~mask);
}
