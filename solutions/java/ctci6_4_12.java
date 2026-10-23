import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public int CountDownwardSumPaths(TreeNode root, int target) {
    if (root == null)
      return 0;
    record Frame(TreeNode node, int sum, boolean exit) {}
    Map<Integer, Integer> prefix = new HashMap<>();
    prefix.put(0, 1);
    Deque<Frame> stack = new ArrayDeque<>();
    stack.push(new Frame(root, 0, false));
    int answer = 0;
    while (!stack.isEmpty()) {
      var frame = stack.pop();
      if (frame.exit()) {
        int count = prefix.get(frame.sum()) - 1;
        if (count == 0)
          prefix.remove(frame.sum());
        else
          prefix.put(frame.sum(), count);
        continue;
      }
      int running = frame.sum() + frame.node().Data;
      answer += prefix.getOrDefault(running - target, 0);
      prefix.put(running, prefix.getOrDefault(running, 0) + 1);
      stack.push(new Frame(frame.node(), running, true));
      if (frame.node().Right != null)
        stack.push(new Frame(frame.node().Right, running, false));
      if (frame.node().Left != null)
        stack.push(new Frame(frame.node().Left, running, false));
    }
    return answer;
  }
}
