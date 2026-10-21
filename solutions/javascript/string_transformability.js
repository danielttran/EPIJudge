function transformString(D, s, t) {
  if (s === t) return 0;
  const remaining = new Set(D),
    queue = [[s, 0]];
  remaining.delete(s);
  for (let head = 0; head < queue.length; head++) {
    const [word, distance] = queue[head],
      chars = word.split("");
    for (let i = 0; i < chars.length; i++) {
      const old = chars[i];
      for (let code = 97; code <= 122; code++) {
        const c = String.fromCharCode(code);
        if (c === old) continue;
        chars[i] = c;
        const candidate = chars.join("");
        if (!remaining.delete(candidate)) continue;
        if (candidate === t) return distance + 1;
        queue.push([candidate, distance + 1]);
      }
      chars[i] = old;
    }
  }
  return -1;
}

module.exports = { transformString };
