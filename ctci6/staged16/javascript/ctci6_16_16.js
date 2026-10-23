'use strict';
function ShortestSortWindow(values) {
  if (values.length === 0) return [-1, -1];
  let right = -1,
    maximum = values[0];
  for (let i = 0; i < values.length; ++i) {
    if (values[i] < maximum) right = i;
    maximum = Math.max(maximum, values[i]);
  }
  if (right === -1) return [-1, -1];
  let left = -1,
    minimum = values[values.length - 1];
  for (let i = values.length - 1; i >= 0; --i) {
    if (values[i] > minimum) left = i;
    minimum = Math.min(minimum, values[i]);
  }
  return [left, right];
}
