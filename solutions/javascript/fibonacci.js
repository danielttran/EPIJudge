function fibonacci(n) {
  let previous = 0,
    current = 1;
  for (let i = 0; i < n; i++)
    [previous, current] = [current, previous + current];
  return previous;
}

module.exports = { fibonacci };
