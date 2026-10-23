import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public List<List<Integer>> BstInsertionSequences(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    List<Integer> path = new ArrayList<>();
    class Search {
      void visit(List<TreeNode> available) {
        if (available.isEmpty()) {
          result.add(new ArrayList<>(path));
          return;
        }
        for (int i = 0; i < available.size(); ++i) {
          TreeNode node = available.get(i);
          List<TreeNode> following = new ArrayList<>(available);
          following.remove(i);
          if (node.Left != null)
            following.add(node.Left);
          if (node.Right != null)
            following.add(node.Right);
          path.add(node.Data);
          visit(following);
          path.remove(path.size() - 1);
        }
      }
    }
    List<TreeNode> initial = new ArrayList<>();
    if (root != null)
      initial.add(root);
    new Search().visit(initial);
    return result;
  }
}
