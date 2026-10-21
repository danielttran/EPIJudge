function numberOfWaysToTop(top, maximum_step) {
  if (maximum_step <= 0) return top === 0 ? 1 : 0;
  const ways = Array(top + 1).fill(0);
  ways[0] = 1;
  let window = 1;
  for (let stair = 1; stair <= top; stair++) {
    ways[stair] = window;
    window += ways[stair];
    if (stair >= maximum_step) window -= ways[stair - maximum_step];
  }
  return ways[top];
}

module.exports = { numberOfWaysToTop };
