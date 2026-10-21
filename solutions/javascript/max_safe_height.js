function getHeight(cases, drops) {
  cases = Math.min(cases, drops);
  const covered = Array(cases + 1).fill(0);
  for (let test = 0; test < drops; test++)
    for (let eggs = cases; eggs > 0; eggs--)
      covered[eggs] = Math.min(
        2147483647,
        1 + covered[eggs] + covered[eggs - 1],
      );
  return covered[cases];
}

module.exports = { getHeight };
