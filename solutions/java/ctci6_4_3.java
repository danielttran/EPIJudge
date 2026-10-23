import java.util.*;
class TreeNode {public int Data;public TreeNode Left,Right,Parent;public TreeNode(int data){Data=data;}}
class DepthLink {public TreeNode Value;public DepthLink Next;public DepthLink(TreeNode value){Value=value;}}
class Solution {
  public List<DepthLink> LinkedListsByDepth(TreeNode root) {
    List<DepthLink> heads = new ArrayList<>();
    if (root == null)
      return heads;
    List<TreeNode> current = new ArrayList<>();
    current.add(root);
    while (!current.isEmpty()) {
      DepthLink head = null, tail = null;
      List<TreeNode> following = new ArrayList<>();
      for (TreeNode node : current) {
        DepthLink link = new DepthLink(node);
        if (tail == null)
          head = link;
        else
          tail.Next = link;
        tail = link;
        if (node.Left != null)
          following.add(node.Left);
        if (node.Right != null)
          following.add(node.Right);
      }
      heads.add(head);
      current = following;
    }
    return heads;
  }
}
