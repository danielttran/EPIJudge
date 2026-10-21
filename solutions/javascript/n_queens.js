function nQueens(n) {
  const answer = [],
    placement = [],
    columns = new Set(),
    rising = new Set(),
    falling = new Set();
  function place(row) {
    if (row === n) {
      answer.push(placement.slice());
      return;
    }
    for (let c = 0; c < n; c++)
      if (!columns.has(c) && !rising.has(row + c) && !falling.has(row - c)) {
        columns.add(c);
        rising.add(row + c);
        falling.add(row - c);
        placement.push(c);
        place(row + 1);
        placement.pop();
        columns.delete(c);
        rising.delete(row + c);
        falling.delete(row - c);
      }
  }
  place(0);
  return answer;
}

module.exports = { nQueens };
