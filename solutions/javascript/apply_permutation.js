function applyPermutation(perm, A) {
  const result = Array(A.length).fill(0);
  for (let i = 0; i < A.length; i++) result[perm[i]] = A[i];
  return result;
}

module.exports = { applyPermutation };
