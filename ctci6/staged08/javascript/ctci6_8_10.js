'use strict';
function PaintFill(screen, row, column, newColor) {
  const rows = screen.length,
    columns = rows ? screen[0].length : 0;
  if (row < 0 || row >= rows || column < 0 || column >= columns) return screen;
  const oldColor = screen[row][column];
  if (oldColor === newColor) return screen;
  const work = [[row, column]];
  screen[row][column] = newColor;
  while (work.length) {
    const [r, c] = work.pop();
    for (const [nr, nc] of [
      [r - 1, c],
      [r + 1, c],
      [r, c - 1],
      [r, c + 1],
    ]) {
      if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && screen[nr][nc] === oldColor) {
        screen[nr][nc] = newColor;
        work.push([nr, nc]);
      }
    }
  }
  return screen;
}
