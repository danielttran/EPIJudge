import java.util.*;
class RankTracker {
  private static class Node {
    int value, leftCount;
    Node left, right;
    Node(int value) {
      this.value = value;
    }
  }
  private Node root;
  public RankTracker() {
  }
  public void Track(int value) {
    if (root == null) {
      root = new Node(value);
      return;
    }
    Node node = root;
    while (true) {
      if (value <= node.value) {
        ++node.leftCount;
        if (node.left == null) {
          node.left = new Node(value);
          return;
        }
        node = node.left;
      } else {
        if (node.right == null) {
          node.right = new Node(value);
          return;
        }
        node = node.right;
      }
    }
  }
  public int GetRank(int value) {
    Node node = root;
    int skipped = 0;
    while (node != null) {
      if (value == node.value)
        return skipped + node.leftCount;
      if (value < node.value)
        node = node.left;
      else {
        skipped += node.leftCount + 1;
        node = node.right;
      }
    }
    return -1;
  }
}
