'use strict';
function PondSizes(land) {
  const rows = land.length,
    columns = rows ? land[0].length : 0,
    seen = Array.from({ length: rows }, () => Array(columns).fill(false)),
    sizes = [];
  for (let row = 0; row < rows; ++row) {
    for (let column = 0; column < columns; ++column) {
      if (land[row][column] !== 0 || seen[row][column]) continue;
      seen[row][column] = true;
      const work = [[row, column]];
      let size = 0;
      while (work.length) {
        const [r, c] = work.pop();
        ++size;
        for (let dr = -1; dr <= 1; ++dr) {
          for (let dc = -1; dc <= 1; ++dc) {
            if (dr === 0 && dc === 0) continue;
            const nr = r + dr,
              nc = c + dc;
            if (
              nr >= 0 &&
              nr < rows &&
              nc >= 0 &&
              nc < columns &&
              land[nr][nc] === 0 &&
              !seen[nr][nc]
            ) {
              seen[nr][nc] = true;
              work.push([nr, nc]);
            }
          }
        }
      }
      sizes.push(size);
    }
  }
  sizes.sort((a, b) => a - b);
  return sizes;
}
