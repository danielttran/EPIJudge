'use strict';
function PlayMinesweeper(bombs, actions) {
  const rows = bombs.length,
    columns = bombs[0].length,
    visible = bombs.map((row) => row.map(() => 9)),
    trace = [];
  let safe = bombs.flat().filter((v) => v === 0).length,
    state = 0;
  function snapshot(accepted) {
    trace.push([state, accepted, ...visible.flat()]);
  }
  function expose(row, column, queue) {
    if (visible[row][column] !== 9 || bombs[row][column]) return;
    let number = 0;
    for (let r = Math.max(0, row - 1); r < Math.min(rows, row + 2); ++r)
      for (let c = Math.max(0, column - 1); c < Math.min(columns, column + 2); ++c)
        number += bombs[r][c];
    visible[row][column] = number;
    --safe;
    if (number === 0) queue.push([row, column]);
  }
  snapshot(0);
  for (const [row, column, kind] of actions) {
    let accepted = 0;
    if (state === 0 && row >= 0 && row < rows && column >= 0 && column < columns) {
      if (kind === 1 && (visible[row][column] === 9 || visible[row][column] === 10)) {
        visible[row][column] = 19 - visible[row][column];
        accepted = 1;
      } else if (kind === 0 && visible[row][column] === 9) {
        accepted = 1;
        if (bombs[row][column]) {
          visible[row][column] = 11;
          state = 2;
        } else {
          const queue = [];
          expose(row, column, queue);
          for (let head = 0; head < queue.length; ++head) {
            const [r, c] = queue[head];
            for (let nr = Math.max(0, r - 1); nr < Math.min(rows, r + 2); ++nr)
              for (let nc = Math.max(0, c - 1); nc < Math.min(columns, c + 2); ++nc)
                expose(nr, nc, queue);
          }
          if (safe === 0) state = 1;
        }
      }
    }
    snapshot(accepted);
  }
  return trace;
}

module.exports = {PlayMinesweeper};
