function numCombinationsForFinalScore(final_score, individual_play_scores) {
  const ways = Array(final_score + 1).fill(0);
  ways[0] = 1;
  for (const score of individual_play_scores)
    for (let total = score; total <= final_score; total++)
      ways[total] += ways[total - score];
  return ways[final_score];
}

module.exports = { numCombinationsForFinalScore };
