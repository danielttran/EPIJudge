import java.util.*;
class Solution {
  public List<String> LangtonBoard(int steps) {
    int width = 2 * steps + 1, row = 0, column = 0, direction = 0, minRow = 0, maxRow = 0,
        minColumn = 0, maxColumn = 0;
    Set<Integer> black = new HashSet<>();
    int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
    for (int turn = 0; turn < steps; ++turn) {
      int key = (row + steps) * width + column + steps;
      if (black.contains(key)) {
        direction = (direction + 3) % 4;
        black.remove(key);
      } else {
        direction = (direction + 1) % 4;
        black.add(key);
      }
      row += dr[direction];
      column += dc[direction];
      minRow = Math.min(minRow, row);
      maxRow = Math.max(maxRow, row);
      minColumn = Math.min(minColumn, column);
      maxColumn = Math.max(maxColumn, column);
    }
    List<String> result = new ArrayList<>();
    for (int r = minRow; r <= maxRow; ++r) {
      var line = new StringBuilder();
      for (int c = minColumn; c <= maxColumn; ++c)
        line.append(r == row && c == column                       ? "RDLU".charAt(direction)
                : black.contains((r + steps) * width + c + steps) ? '#'
                                                                  : '.');
      result.add(line.toString());
    }
    return result;
  }
}
