import java.util.*;
class Solution {
  public int[][] PlayOthello(int size, int[][] actions) {
    int[][] board = new int[size][size];
    var trace = new ArrayList<int[]>();
    int middle = size / 2;
    board[middle - 1][middle - 1] = board[middle][middle] = 2;
    board[middle - 1][middle] = board[middle][middle - 1] = 1;
    class Rules {
      ArrayList<int[]> captures(int row, int column, int color) {
        var result = new ArrayList<int[]>();
        if (row < 0 || row >= size || column < 0 || column >= size || board[row][column] != 0)
          return result;
        for (int dr = -1; dr <= 1; ++dr)
          for (int dc = -1; dc <= 1; ++dc) {
            if (dr == 0 && dc == 0)
              continue;
            int r = row + dr, c = column + dc;
            var path = new ArrayList<int[]>();
            while (r >= 0 && r < size && c >= 0 && c < size && board[r][c] == 3 - color) {
              path.add(new int[] {r, c});
              r += dr;
              c += dc;
            }
            if (path.size() > 0 && r >= 0 && r < size && c >= 0 && c < size && board[r][c] == color)
              result.addAll(path);
          }
        return result;
      }
      boolean canMove(int color) {
        for (int r = 0; r < size; ++r)
          for (int c = 0; c < size; ++c)
            if (captures(r, c, color).size() > 0)
              return true;
        return false;
      }
    }
    var rules = new Rules();
    int turn = rules.canMove(1) ? 1 : 0;
    class Snapshotter {
      void snapshot(int accepted, int currentTurn) {
        int black = 0, white = 0;
        for (int[] row : board)
          for (int v : row) {
            if (v == 1)
              black++;
            if (v == 2)
              white++;
          }
        var result = new int[4 + size * size];
        result[0] = currentTurn;
        result[1] = accepted;
        result[2] = black;
        result[3] = white;
        for (int r = 0; r < size; r++)
          for (int c = 0; c < size; c++)
            result[4 + r * size + c] = board[r][c];
        trace.add(result);
      }
    }
    var observer = new Snapshotter();
    observer.snapshot(0, turn);
    for (int[] action : actions) {
      int row = action[0], column = action[1], color = action[2], accepted = 0;
      if (turn != 0 && color == turn) {
        var flipped = rules.captures(row, column, color);
        if (flipped.size() > 0) {
          board[row][column] = color;
          for (int[] p : flipped)
            board[p[0]][p[1]] = color;
          accepted = 1;
          turn = rules.canMove(3 - color) ? 3 - color : rules.canMove(color) ? color : 0;
        }
      }
      observer.snapshot(accepted, turn);
    }
    return trace.toArray(new int[0][]);
  }
}
