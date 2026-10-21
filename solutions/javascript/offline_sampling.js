function randomSampling(k, values) {
  for (let i = 0; i < k; i++) {
    const j = i + Math.floor(Math.random() * (values.length - i));
    [values[i], values[j]] = [values[j], values[i]];
  }
}

module.exports = { randomSampling };
