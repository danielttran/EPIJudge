import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public TreeNode CreateMinimalBst(int[] sortedValues) {
    class Builder {
      TreeNode build(int lower, int upper, TreeNode parent) {
        if (lower >= upper)
          return null;
        int middle = lower + (upper - lower) / 2;
        TreeNode node = new TreeNode(sortedValues[middle]);
        node.Parent = parent;
        node.Left = build(lower, middle, node);
        node.Right = build(middle + 1, upper, node);
        return node;
      }
    }
    return new Builder().build(0, sortedValues.length, null);
  }
}
