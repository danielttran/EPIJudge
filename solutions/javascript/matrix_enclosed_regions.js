function fillSurroundedRegions(board) {
  if (!board.length || !board[0].length) return board;
  const rows = board.length,
    columns = board[0].length,
    safe = Array.from({ length: rows }, () => Array(columns).fill(false)),
    queue = [];
  function add(r, c) {
    if (
      r >= 0 &&
      r < rows &&
      c >= 0 &&
      c < columns &&
      !safe[r][c] &&
      board[r][c] === "W"
    ) {
      safe[r][c] = true;
      queue.push([r, c]);
    }
  }
  for (let r = 0; r < rows; r++) {
    add(r, 0);
    add(r, columns - 1);
  }
  for (let c = 0; c < columns; c++) {
    add(0, c);
    add(rows - 1, c);
  }
  for (let head = 0; head < queue.length; head++) {
    const [r, c] = queue[head];
    add(r - 1, c);
    add(r + 1, c);
    add(r, c - 1);
    add(r, c + 1);
  }
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < columns; c++)
      if (board[r][c] === "W" && !safe[r][c]) board[r][c] = "B";
  return board;
}

module.exports = { fillSurroundedRegions };
