'use strict';
function EightQueens() {
  const board = Array(8).fill(0),
    result = [];
  function visit(row, usedColumns, usedDown, usedUp) {
    if (row === 8) {
      result.push(board.slice());
      return;
    }
    for (let column = 0; column < 8; ++column) {
      const colBit = 1 << column,
        downBit = 1 << (row - column + 7),
        upBit = 1 << (row + column);
      if (usedColumns & colBit || usedDown & downBit || usedUp & upBit) continue;
      board[row] = column;
      visit(row + 1, usedColumns | colBit, usedDown | downBit, usedUp | upBit);
    }
  }
  visit(0, 0, 0, 0);
  return result;
}

module.exports = {EightQueens};
