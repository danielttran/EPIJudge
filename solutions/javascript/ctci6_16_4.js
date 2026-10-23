'use strict';
function TicTacWinner(board) {
  const n = board.length;
  if (n === 0) return 0;
  for (let i = 0; i < n; ++i) {
    let row = board[i][0],
      column = board[0][i];
    for (let j = 0; j < n; ++j) {
      if (board[i][j] !== row) row = 0;
      if (board[j][i] !== column) column = 0;
    }
    if (row) return row;
    if (column) return column;
  }
  let main = board[0][0],
    other = board[0][n - 1];
  for (let i = 0; i < n; ++i) {
    if (board[i][i] !== main) main = 0;
    if (board[i][n - 1 - i] !== other) other = 0;
  }
  if (main) return main;
  return other;
}

module.exports = {TicTacWinner};
