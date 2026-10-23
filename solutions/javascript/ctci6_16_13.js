'use strict';
function BisectSquares(squares) {
  const x = squares[0][0] + squares[0][2] / 2,
    y = squares[0][1] + squares[0][2] / 2;
  let dx = squares[1][0] + squares[1][2] / 2 - x,
    dy = squares[1][1] + squares[1][2] / 2 - y,
    other = 1;
  if (dx === 0 && dy === 0) {
    dy = 1;
    other = 0;
  }
  const scale = Math.max(Math.abs(dx), Math.abs(dy)),
    first = squares[0][2] / (2 * scale),
    second = squares[1][2] / (2 * scale),
    start = Math.min(-first, other - second),
    end = Math.max(first, other + second);
  return [x + start * dx, y + start * dy, x + end * dx, y + end * dy];
}

module.exports = {BisectSquares};
