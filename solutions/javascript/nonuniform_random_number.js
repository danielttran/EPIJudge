function nonuniformRandomNumberGeneration(values, probabilities) {
  const target = Math.random();
  let cumulative = 0;
  for (let i = 0; i < values.length - 1; i++) {
    cumulative += probabilities[i];
    if (target < cumulative) return values[i];
  }
  return values.at(-1);
}

module.exports = { nonuniformRandomNumberGeneration };
