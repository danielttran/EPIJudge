'use strict';
function FindRobotPath(grid) {
  const rows = grid.length,
    columns = rows ? grid[0].length : 0;
  if (!rows || !columns) return [];
  const parent = Array.from({ length: rows }, () => Array(columns).fill(0));
  for (let r = 0; r < rows; ++r) {
    for (let c = 0; c < columns; ++c) {
      if (grid[r][c] === 0) continue;
      if (r === 0 && c === 0) parent[r][c] = 3;
      else if (r > 0 && parent[r - 1][c]) parent[r][c] = 1;
      else if (c > 0 && parent[r][c - 1]) parent[r][c] = 2;
    }
  }
  if (!parent[rows - 1][columns - 1]) return [];
  const path = [];
  let r = rows - 1,
    c = columns - 1;
  while (true) {
    path.push([r, c]);
    if (r === 0 && c === 0) break;
    if (parent[r][c] === 1) --r;
    else --c;
  }
  path.reverse();
  return path;
}
