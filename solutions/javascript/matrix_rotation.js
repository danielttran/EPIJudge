function rotateMatrix(square_matrix) {
  const n = square_matrix.length;
  for (let r = 0; r < n; r++)
    for (let c = r + 1; c < n; c++)
      [square_matrix[r][c], square_matrix[c][r]] = [
        square_matrix[c][r],
        square_matrix[r][c],
      ];
  for (const row of square_matrix) row.reverse();
  return square_matrix;
}

module.exports = { rotateMatrix };
