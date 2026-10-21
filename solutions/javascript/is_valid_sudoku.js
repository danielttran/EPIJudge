function isValidSudoku(partial_assignment) {
  const n = partial_assignment.length,
    width = Math.sqrt(n);
  if (!n) return true;
  if (
    !Number.isInteger(width) ||
    partial_assignment.some((row) => row.length !== n)
  )
    return false;
  const rows = Array.from({ length: n }, () => new Set()),
    columns = Array.from({ length: n }, () => new Set()),
    blocks = Array.from({ length: n }, () => new Set());
  for (let r = 0; r < n; r++)
    for (let c = 0; c < n; c++) {
      const value = partial_assignment[r][c];
      if (!value) continue;
      const b = Math.floor(r / width) * width + Math.floor(c / width);
      if (
        value < 1 ||
        value > n ||
        rows[r].has(value) ||
        columns[c].has(value) ||
        blocks[b].has(value)
      )
        return false;
      rows[r].add(value);
      columns[c].add(value);
      blocks[b].add(value);
    }
  return true;
}

module.exports = { isValidSudoku };
