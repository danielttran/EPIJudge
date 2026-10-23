'use strict';
function WordDistance(words, first, second) {
  let lastFirst = -1,
    lastSecond = -1,
    best = words.length + 1;
  for (let i = 0; i < words.length; ++i) {
    if (words[i] === first) {
      lastFirst = i;
      if (lastSecond >= 0) best = Math.min(best, i - lastSecond);
    } else if (words[i] === second) {
      lastSecond = i;
      if (lastFirst >= 0) best = Math.min(best, i - lastFirst);
    }
  }
  return best === words.length + 1 ? -1 : best;
}

module.exports = {WordDistance};
