function calculateTrafficVolumes(A, w) {
  const candidates = [],
    result = [];
  let head = 0;
  for (let i = 0; i < A.length; i++) {
    while (candidates.length > head && A[candidates[head]][0] < A[i][0] - w)
      head++;
    while (candidates.length > head && A[candidates.at(-1)][1] <= A[i][1])
      candidates.pop();
    candidates.push(i);
    result.push([A[i][0], A[candidates[head]][1]]);
  }
  return result;
}

module.exports = { calculateTrafficVolumes };
