import java.util.*;
class Solution {
  public int[][] PlayMinesweeper(int[][] bombs, int[][] actions) {
    int rows = bombs.length, columns = bombs[0].length;
    int[][] visible = new int[rows][columns];
    for (int[] row : visible)
      Arrays.fill(row, 9);
    int[] remaining = {0}, state = {0};
    for (int[] row : bombs)
      for (int value : row)
        if (value == 0)
          remaining[0]++;
    var trace = new ArrayList<int[]>();
    class Observer {
      void snapshot(int accepted) {
        int[] result = new int[2 + rows * columns];
        result[0] = state[0];
        result[1] = accepted;
        for (int r = 0; r < rows; r++)
          for (int c = 0; c < columns; c++)
            result[2 + r * columns + c] = visible[r][c];
        trace.add(result);
      }
      void expose(int row, int column, ArrayList<int[]> queue) {
        if (visible[row][column] != 9 || bombs[row][column] != 0)
          return;
        int number = 0;
        for (int r = Math.max(0, row - 1); r < Math.min(rows, row + 2); ++r)
          for (int c = Math.max(0, column - 1); c < Math.min(columns, column + 2); ++c)
            number += bombs[r][c];
        visible[row][column] = number;
        --remaining[0];
        if (number == 0)
          queue.add(new int[] {row, column});
      }
    }
    var observer = new Observer();
    observer.snapshot(0);
    for (int[] action : actions) {
      int row = action[0], column = action[1], kind = action[2], accepted = 0;
      if (state[0] == 0 && row >= 0 && row < rows && column >= 0 && column < columns) {
        if (kind == 1 && (visible[row][column] == 9 || visible[row][column] == 10)) {
          visible[row][column] = 19 - visible[row][column];
          accepted = 1;
        } else if (kind == 0 && visible[row][column] == 9) {
          accepted = 1;
          if (bombs[row][column] != 0) {
            visible[row][column] = 11;
            state[0] = 2;
          } else {
            var queue = new ArrayList<int[]>();
            observer.expose(row, column, queue);
            for (int head = 0; head < queue.size(); ++head) {
              int r = queue.get(head)[0], c = queue.get(head)[1];
              for (int nr = Math.max(0, r - 1); nr < Math.min(rows, r + 2); ++nr)
                for (int nc = Math.max(0, c - 1); nc < Math.min(columns, c + 2); ++nc)
                  observer.expose(nr, nc, queue);
            }
            if (remaining[0] == 0)
              state[0] = 1;
          }
        }
      }
      observer.snapshot(accepted);
    }
    return trace.toArray(new int[0][]);
  }
}
