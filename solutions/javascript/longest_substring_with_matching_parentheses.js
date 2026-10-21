function longestMatchingParentheses(s) {
  const openings = [-1];
  let best = 0;
  for (let i = 0; i < s.length; i++) {
    if (s[i] === "(") openings.push(i);
    else {
      openings.pop();
      if (!openings.length) openings.push(i);
      else best = Math.max(best, i - openings.at(-1));
    }
  }
  return best;
}

module.exports = { longestMatchingParentheses };
