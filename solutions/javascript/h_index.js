function hIndex(citations) {
  const n = citations.length,
    counts = Array(n + 1).fill(0);
  for (const citation of citations) counts[Math.min(n, citation)]++;
  let papers = 0;
  for (let h = n; h >= 0; h--) {
    papers += counts[h];
    if (papers >= h) return h;
  }
  return 0;
}

module.exports = { hIndex };
