'use strict';
function PalindromePermutation(text) {
  const counts = Array(128).fill(0);
  for (let i = 0; i < text.length; ++i) {
      let code = text.charCodeAt(i);
      if (code >= 65 && code <= 90) code += 32;
      if (code >= 97 && code <= 122) ++counts[code];
  }
  let odd = 0;
  for (let code = 97; code <= 122; ++code) odd += counts[code] % 2;
  return odd <= 1;
}
