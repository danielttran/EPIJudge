import java.util.*;
class Solution {
  public int[] SearchSortedMatrix(int[][] matrix, int target) {
    int rows = matrix.length, columns = rows == 0 ? 0 : matrix[0].length, row = 0,
        column = columns - 1;
    while (row < rows && column >= 0) {
      int value = matrix[row][column];
      if (value == target)
        return new int[] {row, column};
      if (value > target)
        --column;
      else
        ++row;
    }
    return new int[] {-1, -1};
  }
}
