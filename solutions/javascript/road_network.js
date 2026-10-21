function findBestProposals(H, P, n) {
  if (!P.length) return [-1, -1, 0];
  const distance = Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => (i === j ? 0 : Infinity)),
  );
  for (const [a, b, length] of H) {
    distance[a][b] = Math.min(distance[a][b], length);
    distance[b][a] = Math.min(distance[b][a], length);
  }
  for (let via = 0; via < n; via++)
    for (let from = 0; from < n; from++)
      for (let to = 0; to < n; to++)
        distance[from][to] = Math.min(
          distance[from][to],
          distance[from][via] + distance[via][to],
        );
  let best = P[0],
    bestSaving = -1;
  for (const proposal of P) {
    const [a, b, length] = proposal;
    let saving = 0;
    for (let from = 0; from < n; from++)
      for (let to = from + 1; to < n; to++) {
        const via = Math.min(
          distance[from][a] + length + distance[b][to],
          distance[from][b] + length + distance[a][to],
        );
        saving += distance[from][to] - Math.min(distance[from][to], via);
      }
    if (saving > bestSaving) {
      bestSaving = saving;
      best = proposal;
    }
  }
  return best;
}

module.exports = { findBestProposals };
