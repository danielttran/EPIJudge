import java.util.*;
class Solution {
  public int[] PondSizes(int[][] land) {
    int rows = land.length, columns = rows == 0 ? 0 : land[0].length;
    boolean[][] seen = new boolean[rows][columns];
    List<Integer> sizes = new ArrayList<>();
    for (int row = 0; row < rows; ++row) {
      for (int column = 0; column < columns; ++column) {
        if (land[row][column] != 0 || seen[row][column])
          continue;
        seen[row][column] = true;
        Deque<int[]> work = new ArrayDeque<>();
        work.push(new int[] {row, column});
        int size = 0;
        while (!work.isEmpty()) {
          var cell = work.pop();
          int r = cell[0], c = cell[1];
          ++size;
          for (int dr = -1; dr <= 1; ++dr) {
            for (int dc = -1; dc <= 1; ++dc) {
              if (dr == 0 && dc == 0)
                continue;
              int nr = r + dr, nc = c + dc;
              if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && land[nr][nc] == 0
                  && !seen[nr][nc]) {
                seen[nr][nc] = true;
                work.push(new int[] {nr, nc});
              }
            }
          }
        }
        sizes.add(size);
      }
    }
    Collections.sort(sizes);
    int[] result = new int[sizes.size()];
    for (int i = 0; i < result.length; ++i)
      result[i] = sizes.get(i);
    return result;
  }
}
