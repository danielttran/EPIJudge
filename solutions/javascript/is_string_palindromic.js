function isPalindromic(s) {
  for (let left = 0, right = s.length - 1; left < right; left++, right--)
    if (s[left] !== s[right]) return false;
  return true;
}

module.exports = { isPalindromic };
