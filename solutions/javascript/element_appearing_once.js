function findElementAppearsOnce(A) {
  let once = 0,
    twice = 0;
  for (const value of A) {
    once = (once ^ value) & ~twice;
    twice = (twice ^ value) & ~once;
  }
  return once;
}

module.exports = { findElementAppearsOnce };
