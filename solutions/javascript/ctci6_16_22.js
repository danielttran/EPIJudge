'use strict';
function LangtonBoard(steps) {
  const width = 2 * steps + 1,
    black = new Set(),
    dr = [0, 1, 0, -1],
    dc = [1, 0, -1, 0];
  let row = 0,
    column = 0,
    direction = 0,
    minRow = 0,
    maxRow = 0,
    minColumn = 0,
    maxColumn = 0;
  for (let turn = 0; turn < steps; ++turn) {
    const key = (row + steps) * width + column + steps;
    if (black.has(key)) {
      direction = (direction + 3) % 4;
      black.delete(key);
    } else {
      direction = (direction + 1) % 4;
      black.add(key);
    }
    row += dr[direction];
    column += dc[direction];
    minRow = Math.min(minRow, row);
    maxRow = Math.max(maxRow, row);
    minColumn = Math.min(minColumn, column);
    maxColumn = Math.max(maxColumn, column);
  }
  const result = [];
  for (let r = minRow; r <= maxRow; ++r) {
    const line = [];
    for (let c = minColumn; c <= maxColumn; ++c)
      line.push(
        r === row && c === column
          ? "RDLU"[direction]
          : black.has((r + steps) * width + c + steps)
            ? "#"
            : ".",
      );
    result.push(line.join(""));
  }
  return result;
}

module.exports = {LangtonBoard};
