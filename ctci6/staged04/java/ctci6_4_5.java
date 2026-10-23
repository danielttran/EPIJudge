import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public boolean IsDuplicateLeftBst(TreeNode root) {
    record Frame(TreeNode node, long lower, long upper) {}
    Deque<Frame> stack = new ArrayDeque<>();
    if (root != null)
      stack.push(new Frame(root, -2147483649L, 2147483647L));
    while (!stack.isEmpty()) {
      var frame = stack.pop();
      TreeNode node = frame.node();
      if (node.Data <= frame.lower() || node.Data > frame.upper())
        return false;
      if (node.Right != null)
        stack.push(new Frame(node.Right, node.Data, frame.upper()));
      if (node.Left != null)
        stack.push(new Frame(node.Left, frame.lower(), node.Data));
    }
    return true;
  }
}
