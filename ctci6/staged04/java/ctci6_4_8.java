import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public TreeNode FirstCommonAncestor(TreeNode first, TreeNode second) {
    if (first == null || second == null)
      return null;
    int depthFirst = 0, depthSecond = 0;
    for (TreeNode cursor = first; cursor != null; cursor = cursor.Parent)
      ++depthFirst;
    for (TreeNode cursor = second; cursor != null; cursor = cursor.Parent)
      ++depthSecond;
    while (depthFirst > depthSecond) {
      first = first.Parent;
      --depthFirst;
    }
    while (depthSecond > depthFirst) {
      second = second.Parent;
      --depthSecond;
    }
    while (first != second) {
      first = first.Parent;
      second = second.Parent;
    }
    return first;
  }
}
