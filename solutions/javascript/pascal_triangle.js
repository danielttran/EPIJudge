function generatePascalTriangle(n) {
  const rows = [];
  for (let r = 0; r < n; r++) {
    const row = Array(r + 1).fill(1);
    for (let c = 1; c < r; c++) row[c] = rows[r - 1][c - 1] + rows[r - 1][c];
    rows.push(row);
  }
  return rows;
}

module.exports = { generatePascalTriangle };
