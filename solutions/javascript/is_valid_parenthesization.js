function isWellFormed(s) {
  const openings = [],
    pairs = { ")": "(", "]": "[", "}": "{" };
  for (const c of s) {
    if (c === "(" || c === "[" || c === "{") {
      openings.push(c);
      continue;
    }
    if (!pairs[c] || !openings.length || openings.pop() !== pairs[c])
      return false;
  }
  return !openings.length;
}

module.exports = { isWellFormed };
