function reverse(x) {
  let remaining = Math.abs(x),
    result = 0;
  while (remaining !== 0) {
    result = result * 10 + (remaining % 10);
    remaining = Math.floor(remaining / 10);
  }
  return x < 0 ? -result : result;
}

module.exports = { reverse };
