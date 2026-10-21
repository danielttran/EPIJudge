function countBits(x) {
  let remaining = x >>> 0,
    count = 0;
  while (remaining !== 0) {
    remaining = (remaining & (remaining - 1)) >>> 0;
    count++;
  }
  return count;
}

module.exports = { countBits };
