function nextPermutation(perm) {
  let pivot = perm.length - 2;
  while (pivot >= 0 && perm[pivot] >= perm[pivot + 1]) pivot--;
  if (pivot < 0) return [];
  let successor = perm.length - 1;
  while (perm[successor] <= perm[pivot]) successor--;
  [perm[pivot], perm[successor]] = [perm[successor], perm[pivot]];
  for (let l = pivot + 1, r = perm.length - 1; l < r; l++, r--)
    [perm[l], perm[r]] = [perm[r], perm[l]];
  return perm;
}

module.exports = { nextPermutation };
