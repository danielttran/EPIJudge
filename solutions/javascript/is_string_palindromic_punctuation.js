function isPalindrome(s) {
  let left = 0,
    right = s.length - 1;
  const alphanumeric = (c) => /[\p{L}\p{Nd}]/u.test(c),
    fold = (c) => {
      const lower = c.toLowerCase();
      return lower.length === 1 ? lower : c;
    };
  while (left < right) {
    if (!alphanumeric(s[left])) {
      left++;
      continue;
    }
    if (!alphanumeric(s[right])) {
      right--;
      continue;
    }
    if (fold(s[left]) !== fold(s[right])) return false;
    left++;
    right--;
  }
  return true;
}

module.exports = { isPalindrome };
