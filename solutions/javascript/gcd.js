function gcd(x, y) {
  x = BigInt(x);
  y = BigInt(y);
  while (y !== 0n) [x, y] = [y, x % y];
  return x;
}

module.exports = { gcd };
