function isMatch(regex, s) {
  const anchored = regex.startsWith("^"),
    first = anchored ? 1 : 0,
    memo = new Map();
  function match(p, t) {
    const key = p + "," + t;
    if (memo.has(key)) return memo.get(key);
    let result;
    if (p === regex.length) result = true;
    else if (p === regex.length - 1 && regex[p] === "$")
      result = t === s.length;
    else {
      const fits = t < s.length && (regex[p] === "." || regex[p] === s[t]);
      result =
        p + 1 < regex.length && regex[p + 1] === "*"
          ? match(p + 2, t) || (fits && match(p, t + 1))
          : fits && match(p + 1, t + 1);
    }
    memo.set(key, result);
    return result;
  }
  if (anchored) return match(first, 0);
  for (let start = 0; start <= s.length; start++)
    if (match(first, start)) return true;
  return false;
}

module.exports = { isMatch };
