import java.util.*;
class Solution {
  public int[][] PaintFill(int[][] screen, int row, int column, int newColor) {
    int rows = screen.length, columns = rows == 0 ? 0 : screen[0].length;
    if (row < 0 || row >= rows || column < 0 || column >= columns)
      return screen;
    int oldColor = screen[row][column];
    if (oldColor == newColor)
      return screen;
    Deque<int[]> work = new ArrayDeque<>();
    work.push(new int[] {row, column});
    screen[row][column] = newColor;
    int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
    while (!work.isEmpty()) {
      var cell = work.pop();
      int r = cell[0], c = cell[1];
      for (int i = 0; i < 4; ++i) {
        int nr = r + dr[i], nc = c + dc[i];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && screen[nr][nc] == oldColor) {
          screen[nr][nc] = newColor;
          work.push(new int[] {nr, nc});
        }
      }
    }
    return screen;
  }
}
