function onlineRandomSample(stream, k) {
  const sample = stream.slice(0, k);
  for (let i = k; i < stream.length; i++) {
    const position = Math.floor(Math.random() * (i + 1));
    if (position < k) sample[position] = stream[i];
  }
  return sample;
}

module.exports = { onlineRandomSample };
