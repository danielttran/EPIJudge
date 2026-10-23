'use strict';
function MultiSearch(text, patterns) {
  const result = [];
  for (const pattern of patterns) {
    const positions = [];
    for (let start = 0; start + pattern.length <= text.length; ++start)
      if (text.startsWith(pattern, start)) positions.push(start);
    result.push(positions);
  }
  return result;
}

module.exports = {MultiSearch};
