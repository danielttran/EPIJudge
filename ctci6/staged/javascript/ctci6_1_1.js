'use strict';
function IsUnique(text) {
  const seen = Array(128).fill(false);
  for (let i = 0; i < text.length; ++i) {
    const code = text.charCodeAt(i);
    if (seen[code]) return false;
    seen[code] = true;
  }
  return true;
}
