import java.util.*;
class Solution {
  public void Rotate(int[][] matrix) {
    int n = matrix.length;
    for (int r = 0; r < n; ++r) {
      for (int c = r + 1; c < n; ++c) {
        int saved = matrix[r][c];
        matrix[r][c] = matrix[c][r];
        matrix[c][r] = saved;
      }
    }
    for (int r = 0; r < n; ++r) {
      for (int c = 0; c < n / 2; ++c) {
        int saved = matrix[r][c];
        matrix[r][c] = matrix[r][n - 1 - c];
        matrix[r][n - 1 - c] = saved;
      }
    }
  }
}
