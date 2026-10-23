'use strict';
function PlayOthello(size, actions) {
  const board = Array.from({ length: size }, () => Array(size).fill(0)),
    middle = Math.floor(size / 2),
    trace = [];
  board[middle - 1][middle - 1] = board[middle][middle] = 2;
  board[middle - 1][middle] = board[middle][middle - 1] = 1;
  function captures(row, column, color) {
    if (row < 0 || row >= size || column < 0 || column >= size || board[row][column] !== 0)
      return [];
    const result = [];
    for (let dr = -1; dr <= 1; ++dr)
      for (let dc = -1; dc <= 1; ++dc) {
        if (dr === 0 && dc === 0) continue;
        let r = row + dr,
          c = column + dc;
        const path = [];
        while (r >= 0 && r < size && c >= 0 && c < size && board[r][c] === 3 - color) {
          path.push([r, c]);
          r += dr;
          c += dc;
        }
        if (path.length && r >= 0 && r < size && c >= 0 && c < size && board[r][c] === color)
          result.push(...path);
      }
    return result;
  }
  function canMove(color) {
    for (let r = 0; r < size; ++r)
      for (let c = 0; c < size; ++c) if (captures(r, c, color).length) return true;
    return false;
  }
  let turn = canMove(1) ? 1 : 0;
  function snapshot(accepted) {
    const flat = board.flat();
    trace.push([
      turn,
      accepted,
      flat.filter((v) => v === 1).length,
      flat.filter((v) => v === 2).length,
      ...flat,
    ]);
  }
  snapshot(0);
  for (const [row, column, color] of actions) {
    let accepted = 0;
    if (turn && color === turn) {
      const flipped = captures(row, column, color);
      if (flipped.length) {
        board[row][column] = color;
        for (const [r, c] of flipped) board[r][c] = color;
        accepted = 1;
        turn = canMove(3 - color) ? 3 - color : canMove(color) ? color : 0;
      }
    }
    snapshot(accepted);
  }
  return trace;
}

module.exports = {PlayOthello};
