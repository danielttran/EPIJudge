function generateFirstKABSqrt2(k) {
  if (k <= 0) return [];
  const pairs = [[0, 0]],
    result = [0],
    root = Math.sqrt(2);
  let plusOne = 0,
    plusRoot = 0;
  while (result.length < k) {
    const first = [pairs[plusOne][0] + 1, pairs[plusOne][1]],
      second = [pairs[plusRoot][0], pairs[plusRoot][1] + 1],
      x = first[0] + first[1] * root,
      y = second[0] + second[1] * root,
      next = x <= y ? first : second;
    pairs.push(next);
    result.push(next[0] + next[1] * root);
    if (first[0] === next[0] && first[1] === next[1]) plusOne++;
    if (second[0] === next[0] && second[1] === next[1]) plusRoot++;
  }
  return result;
}

module.exports = { generateFirstKABSqrt2 };
