import java.util.*;
class Solution {
  public int[] MaximumSubmatrix(int[][] matrix) {
    int rows = matrix.length, columns = rows == 0 ? 0 : matrix[0].length;
    if (rows == 0 || columns == 0)
      return new int[0];
    int best = -2147483648;
    int[] answer = new int[5];
    for (int top = 0; top < rows; ++top) {
      int[] totals = new int[columns];
      for (int bottom = top; bottom < rows; ++bottom) {
        int running = 0, start = 0;
        for (int c = 0; c < columns; ++c) {
          totals[c] += matrix[bottom][c];
          if (running < 0) {
            running = totals[c];
            start = c;
          } else
            running += totals[c];
          if (running > best) {
            best = running;
            answer = new int[] {best, top, start, bottom, c};
          }
        }
      }
    }
    return answer;
  }
}
