import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class Solution {
  public boolean ContainsExactSubtree(TreeNode large, TreeNode small) {
    if (small == null)
      return true;
    class Encoder {
      List<String> encode(TreeNode root) {
        List<String> tokens = new ArrayList<>();
        List<TreeNode> stack = new ArrayList<>();
        stack.add(root);
        while (!stack.isEmpty()) {
          TreeNode node = stack.remove(stack.size() - 1);
          if (node == null)
            tokens.add("#");
          else {
            tokens.add("V" + Integer.toString(node.Data));
            stack.add(node.Right);
            stack.add(node.Left);
          }
        }
        return tokens;
      }
    }
    Encoder encoder = new Encoder();
    List<String> text = encoder.encode(large), pattern = encoder.encode(small);
    int[] prefix = new int[pattern.size()];
    for (int i = 1; i < pattern.size(); ++i) {
      int matched = prefix[i - 1];
      while (matched > 0 && !pattern.get(i).equals(pattern.get(matched)))
        matched = prefix[matched - 1];
      if (pattern.get(i).equals(pattern.get(matched)))
        ++matched;
      prefix[i] = matched;
    }
    int matched = 0;
    for (String token : text) {
      while (matched > 0 && !token.equals(pattern.get(matched)))
        matched = prefix[matched - 1];
      if (token.equals(pattern.get(matched)))
        ++matched;
      if (matched == pattern.size())
        return true;
    }
    return false;
  }
}
