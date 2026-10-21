function changeMaking(cents) {
  let result = 0;
  for (const coin of [100, 50, 25, 10, 5, 1]) {
    result += Math.floor(cents / coin);
    cents %= coin;
  }
  return result;
}

module.exports = { changeMaking };
