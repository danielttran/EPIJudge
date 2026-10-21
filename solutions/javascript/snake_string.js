function snakeString(s) {
  const result = [];
  for (let i = 1; i < s.length; i += 4) result.push(s[i]);
  for (let i = 0; i < s.length; i += 2) result.push(s[i]);
  for (let i = 3; i < s.length; i += 4) result.push(s[i]);
  return result.join("");
}

module.exports = { snakeString };
