function rabinKarp(t, s) {
  if (!s.length) return 0;
  if (s.length > t.length) return -1;
  const radix = 65599n,
    mask = (1n << 64n) - 1n;
  let pattern = 0n,
    window = 0n,
    power = 1n;
  for (let i = 0; i < s.length; i++) {
    pattern = (pattern * radix + BigInt(s.charCodeAt(i))) & mask;
    window = (window * radix + BigInt(t.charCodeAt(i))) & mask;
    if (i) power = (power * radix) & mask;
  }
  for (let start = 0; ; start++) {
    if (window === pattern) {
      let match = true;
      for (let i = 0; i < s.length; i++)
        if (t[start + i] !== s[i]) {
          match = false;
          break;
        }
      if (match) return start;
    }
    if (start + s.length === t.length) return -1;
    window =
      ((window - BigInt(t.charCodeAt(start)) * power) * radix +
        BigInt(t.charCodeAt(start + s.length))) &
      mask;
  }
}

module.exports = { rabinKarp };
