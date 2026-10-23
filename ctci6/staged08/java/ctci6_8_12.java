import java.util.*;
class Solution {
  public List<List<Integer>> EightQueens() {
    int[] board = new int[8];
    List<List<Integer>> result = new ArrayList<>();
    class Search {
      void Visit(int row, int usedColumns, int usedDown, int usedUp) {
        if (row == 8) {
          var copy = new ArrayList<Integer>();
          for (int column : board)
            copy.add(column);
          result.add(copy);
          return;
        }
        for (int column = 0; column < 8; ++column) {
          int colBit = 1 << column, downBit = 1 << (row - column + 7), upBit = 1 << (row + column);
          if ((usedColumns & colBit) != 0 || (usedDown & downBit) != 0 || (usedUp & upBit) != 0)
            continue;
          board[row] = column;
          Visit(row + 1, usedColumns | colBit, usedDown | downBit, usedUp | upBit);
        }
      }
    }
    new Search().Visit(0, 0, 0, 0);
    return result;
  }
}
