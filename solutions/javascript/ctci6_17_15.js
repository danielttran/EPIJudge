'use strict';
function LongestComposedWord(words) {
  const dictionary = new Set(words);
  let best = "";
  for (const word of words) {
    const dp = new Array(word.length + 1).fill(-1);
    dp[0] = 0;
    for (let end = 1; end <= word.length; ++end)
      for (let start = 0; start < end; ++start)
        if (dp[start] >= 0 && dictionary.has(word.slice(start, end)))
          dp[end] = Math.max(dp[end], dp[start] + 1);
    if (
      dp[word.length] >= 2 &&
      (word.length > best.length || (word.length === best.length && word < best))
    )
      best = word;
  }
  return best;
}

module.exports = {LongestComposedWord};
