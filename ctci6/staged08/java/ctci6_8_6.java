import java.util.*;
class Solution {
  public List<List<Integer>> SolveHanoi(int disks) {
    List<Deque<Integer>> towers =
        List.of(new ArrayDeque<>(), new ArrayDeque<>(), new ArrayDeque<>());
    for (int disk = disks; disk >= 1; --disk)
      towers.get(0).push(disk);
    List<List<Integer>> moves = new ArrayList<>();
    class Solver {
      void Transfer(int count, int source, int buffer, int destination) {
        if (count == 0)
          return;
        Transfer(count - 1, source, destination, buffer);
        int disk = towers.get(source).pop();
        towers.get(destination).push(disk);
        moves.add(new ArrayList<>(List.of(disk, source, destination)));
        Transfer(count - 1, buffer, source, destination);
      }
    }
    new Solver().Transfer(disks, 0, 1, 2);
    return moves;
  }
}
