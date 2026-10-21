function canFormPalindrome(s) {
  const odd = new Set();
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (odd.has(c)) odd.delete(c);
    else odd.add(c);
  }
  return odd.size <= 1;
}

module.exports = { canFormPalindrome };
