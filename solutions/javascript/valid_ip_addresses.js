function getValidIpAddress(s) {
  const output = [];
  if (s.length < 4 || s.length > 12) return output;
  const valid = (part) =>
    part.length > 0 &&
    part.length <= 3 &&
    (part.length === 1 || part[0] !== "0") &&
    Number(part) <= 255;
  for (let a = 1; a <= 3 && a < s.length; a++)
    for (let b = a + 1; b <= a + 3 && b < s.length; b++)
      for (let c = b + 1; c <= b + 3 && c < s.length; c++) {
        const parts = [s.slice(0, a), s.slice(a, b), s.slice(b, c), s.slice(c)];
        if (parts.every(valid)) output.push(parts.join("."));
      }
  return output;
}

module.exports = { getValidIpAddress };
