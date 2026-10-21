function rearrange(values) {
  for (let i = 1; i < values.length; i++) {
    const wrong =
      i % 2 === 1 ? values[i - 1] > values[i] : values[i - 1] < values[i];
    if (wrong) [values[i - 1], values[i]] = [values[i], values[i - 1]];
  }
}

module.exports = { rearrange };
