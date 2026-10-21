function findMinMax(A) {
  if (!A.length) throw new RangeError("Nonempty array required");
  let minimum, maximum, next;
  if (A.length % 2) {
    minimum = maximum = A[0];
    next = 1;
  } else {
    [minimum, maximum] = A[0] < A[1] ? [A[0], A[1]] : [A[1], A[0]];
    next = 2;
  }
  for (let i = next; i < A.length; i += 2) {
    const [low, high] = A[i] < A[i + 1] ? [A[i], A[i + 1]] : [A[i + 1], A[i]];
    if (low < minimum) minimum = low;
    if (high > maximum) maximum = high;
  }
  return [minimum, maximum];
}

module.exports = { findMinMax };
