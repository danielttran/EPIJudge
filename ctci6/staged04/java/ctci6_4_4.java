import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public boolean IsHeightBalanced(TreeNode root) {
    if (root == null)
      return true;
    record Frame(TreeNode node, boolean exit) {}
    Map<TreeNode, Integer> heights = new HashMap<>();
    Deque<Frame> stack = new ArrayDeque<>();
    stack.push(new Frame(root, false));
    while (!stack.isEmpty()) {
      var frame = stack.pop();
      TreeNode node = frame.node();
      if (!frame.exit()) {
        stack.push(new Frame(node, true));
        if (node.Right != null)
          stack.push(new Frame(node.Right, false));
        if (node.Left != null)
          stack.push(new Frame(node.Left, false));
      } else {
        int left = node.Left == null ? 0 : heights.get(node.Left),
            right = node.Right == null ? 0 : heights.get(node.Right);
        if (Math.abs(left - right) > 1)
          return false;
        heights.put(node, 1 + Math.max(left, right));
      }
    }
    return true;
  }
}
