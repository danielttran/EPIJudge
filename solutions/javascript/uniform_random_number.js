function uniformRandom(lower, upper) {
  const range = upper - lower + 1,
    bits = Math.ceil(Math.log2(range));
  let candidate;
  do {
    candidate = 0;
    for (let i = 0; i < bits; i++)
      candidate = candidate * 2 + Math.floor(Math.random() * 2);
  } while (candidate >= range);
  return lower + candidate;
}

module.exports = { uniformRandom };
