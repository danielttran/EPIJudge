import java.util.*;
class BiNode { public int Data; public BiNode Node1; public BiNode Node2; public BiNode(int data){Data=data;} }
class Solution {
  public BiNode ConvertBiNode(BiNode root) {
    var stack = new ArrayDeque<BiNode>();
    BiNode current = root, previous = null, head = null;
    while (current != null || !stack.isEmpty()) {
      while (current != null) {
        stack.push(current);
        current = current.Node1;
      }
      BiNode node = stack.pop(), right = node.Node2;
      node.Node1 = previous;
      if (previous == null)
        head = node;
      else
        previous.Node2 = node;
      previous = node;
      current = right;
    }
    if (previous != null)
      previous.Node2 = null;
    return head;
  }
}
