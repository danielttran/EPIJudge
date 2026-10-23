'use strict';
function ScoreMasterMind(guess, secret) {
  const remaining = Array(4).fill(0);
  let hits = 0,
    pseudoHits = 0;
  for (let i = 0; i < 4; ++i) {
    if (guess[i] === secret[i]) ++hits;
    else ++remaining["RGBY".indexOf(secret[i])];
  }
  for (let i = 0; i < 4; ++i) {
    if (guess[i] === secret[i]) continue;
    const color = "RGBY".indexOf(guess[i]);
    if (remaining[color] > 0) {
      --remaining[color];
      ++pseudoHits;
    }
  }
  return [hits, pseudoHits];
}

module.exports = {ScoreMasterMind};
