import java.util.*;
class Solution {
  public int[] LargestBlackBorder(int[][] matrix) {
    int n = matrix.length;
    int[][] right = new int[n][n], down = new int[n][n];
    for (int r = n - 1; r >= 0; --r) {
      for (int c = n - 1; c >= 0; --c) {
        if (matrix[r][c] == 0) {
          right[r][c] = 1 + (c + 1 < n ? right[r][c + 1] : 0);
          down[r][c] = 1 + (r + 1 < n ? down[r + 1][c] : 0);
        }
      }
    }
    for (int size = n; size >= 1; --size) {
      for (int r = 0; r + size <= n; ++r) {
        for (int c = 0; c + size <= n; ++c) {
          if (right[r][c] >= size && down[r][c] >= size && right[r + size - 1][c] >= size
              && down[r][c + size - 1] >= size)
            return new int[] {r, c, size};
        }
      }
    }
    return new int[0];
  }
}
