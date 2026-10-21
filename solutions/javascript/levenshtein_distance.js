function levenshteinDistance(A, B) {
  if (B.length > A.length) [A, B] = [B, A];
  let previous = Array.from({ length: B.length + 1 }, (_, i) => i);
  for (let i = 1; i <= A.length; i++) {
    const current = Array(B.length + 1).fill(0);
    current[0] = i;
    for (let j = 1; j <= B.length; j++)
      current[j] =
        A[i - 1] === B[j - 1]
          ? previous[j - 1]
          : 1 + Math.min(previous[j - 1], previous[j], current[j - 1]);
    previous = current;
  }
  return previous[B.length];
}

module.exports = { levenshteinDistance };
