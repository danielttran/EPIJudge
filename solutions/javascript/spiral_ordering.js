function matrixInSpiralOrder(square_matrix) {
  const result = [];
  let top = 0,
    bottom = square_matrix.length - 1,
    left = 0,
    right = bottom;
  while (top <= bottom && left <= right) {
    for (let c = left; c <= right; c++) result.push(square_matrix[top][c]);
    top++;
    for (let r = top; r <= bottom; r++) result.push(square_matrix[r][right]);
    right--;
    if (top <= bottom) {
      for (let c = right; c >= left; c--) result.push(square_matrix[bottom][c]);
      bottom--;
    }
    if (left <= right) {
      for (let r = bottom; r >= top; r--) result.push(square_matrix[r][left]);
      left++;
    }
  }
  return result;
}

module.exports = { matrixInSpiralOrder };
