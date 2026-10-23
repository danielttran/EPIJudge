'use strict';
function SearchSortedMatrix(matrix, target) {
  const rows = matrix.length,
    columns = rows ? matrix[0].length : 0;
  let row = 0,
    column = columns - 1;
  while (row < rows && column >= 0) {
    const value = matrix[row][column];
    if (value === target) return [row, column];
    if (value > target) --column;
    else ++row;
  }
  return [-1, -1];
}

module.exports = {SearchSortedMatrix};
