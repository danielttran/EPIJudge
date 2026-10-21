function isPatternContainedInGrid(grid, pattern) {
  if (!pattern.length) return true;
  if (!grid.length || !grid[0].length) return false;
  const rows = grid.length,
    columns = grid[0].length;
  let reachable = grid.map((row) => row.map((value) => value === pattern[0]));
  for (let i = 1; i < pattern.length; i++) {
    const next = Array.from({ length: rows }, () => Array(columns).fill(false));
    for (let r = 0; r < rows; r++)
      for (let c = 0; c < columns; c++)
        next[r][c] =
          grid[r][c] === pattern[i] &&
          ((r > 0 && reachable[r - 1][c]) ||
            (r + 1 < rows && reachable[r + 1][c]) ||
            (c > 0 && reachable[r][c - 1]) ||
            (c + 1 < columns && reachable[r][c + 1]));
    reachable = next;
  }
  return reachable.some((row) => row.some(Boolean));
}

module.exports = { isPatternContainedInGrid };
