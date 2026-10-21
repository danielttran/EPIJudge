function solveSudoku(board) {
  const n = board.length,
    width = Math.sqrt(n),
    rows = Array.from({ length: n }, () => Array(n + 1).fill(false)),
    columns = Array.from({ length: n }, () => Array(n + 1).fill(false)),
    blocks = Array.from({ length: n }, () => Array(n + 1).fill(false));
  const box = (r, c) => Math.floor(r / width) * width + Math.floor(c / width);
  for (let r = 0; r < n; r++)
    for (let c = 0; c < n; c++)
      if (board[r][c])
        rows[r][board[r][c]] =
          columns[c][board[r][c]] =
          blocks[box(r, c)][board[r][c]] =
            true;
  function fill() {
    let row = -1,
      column = -1,
      choices = null;
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (!board[r][c]) {
          const options = [];
          for (let value = 1; value <= n; value++)
            if (
              !rows[r][value] &&
              !columns[c][value] &&
              !blocks[box(r, c)][value]
            )
              options.push(value);
          if (!options.length) return false;
          if (choices === null || options.length < choices.length) {
            row = r;
            column = c;
            choices = options;
          }
        }
    if (row < 0) return true;
    const b = box(row, column);
    for (const value of choices) {
      board[row][column] = value;
      rows[row][value] = columns[column][value] = blocks[b][value] = true;
      if (fill()) return true;
      rows[row][value] = columns[column][value] = blocks[b][value] = false;
      board[row][column] = 0;
    }
    return false;
  }
  if (!fill()) throw new Error("No Sudoku solution");
}

module.exports = { solveSudoku };
