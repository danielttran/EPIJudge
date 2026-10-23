import java.util.*;
class Solution {
  public int[][] SolveJigsaw(int size, int[][] pieces) {
    int count = pieces.length;
    int[][] placed = new int[count][2];
    boolean[] used = new boolean[count];
    class Searcher {
      int edge(int index, int turn, int side) {
        return pieces[index][(side - turn + 4) % 4];
      }
      boolean search(int position) {
        if (position == count)
          return true;
        int row = position / size, column = position % size;
        for (int index = 0; index < count; ++index) {
          if (used[index])
            continue;
          for (int turn = 0; turn < 4; ++turn) {
            int[] values = new int[4];
            boolean[] bounds = {row == 0, column == size - 1, row == size - 1, column == 0};
            boolean fits = true;
            for (int side = 0; side < 4; ++side) {
              values[side] = edge(index, turn, side);
              if ((values[side] == 0) != bounds[side])
                fits = false;
            }
            if (!fits)
              continue;
            if (row > 0
                && values[0] != -edge(placed[position - size][0], placed[position - size][1], 2))
              continue;
            if (column > 0
                && values[3] != -edge(placed[position - 1][0], placed[position - 1][1], 1))
              continue;
            used[index] = true;
            placed[position][0] = index;
            placed[position][1] = turn;
            if (search(position + 1))
              return true;
            used[index] = false;
          }
        }
        return false;
      }
    }
    return new Searcher().search(0) ? placed : new int[0][];
  }
}
