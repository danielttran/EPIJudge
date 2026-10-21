import java.util.*;
class ListNode {
  public int val;
  public ListNode next;
  public ListNode(int val, ListNode next) {
    this.val = val;
    this.next = next;
  }
  public ListNode(int val) {
    this(val, null);
  }
}
class TreeNode {
  public int val;
  public TreeNode left, right;
  public TreeNode(int val) {
    this.val = val;
  }
}
class Node {
  public int val;
  public List<Node> neighbors = new ArrayList<>();
  public Node(int val) {
    this.val = val;
  }
}
public class Solution {
  public int lengthOfLongestSubstring(String s) {
    int[] last = new int[128];
    Arrays.fill(last, -1);
    int left = 0, best = 0;
    for (int i = 0; i < s.length(); i++) {
      char c = s.charAt(i);
      left = Math.max(left, last[c] + 1);
      last[c] = i;
      best = Math.max(best, i - left + 1);
    }
    return best;
  }
}

class Probe {
  static List<ListNode> nodes(ListNode n) {
    List<ListNode> a = new ArrayList<>();
    while (n != null) {
      a.add(n);
      n = n.next;
    }
    return a;
  }
  static ListNode link(List<ListNode> a) {
    for (int i = 0; i < a.size(); i++) a.get(i).next = i + 1 < a.size() ? a.get(i + 1) : null;
    return a.isEmpty() ? null : a.get(0);
  }
  static TreeNode invert(TreeNode n) {
    if (n != null) {
      TreeNode l = invert(n.left);
      n.left = invert(n.right);
      n.right = l;
    }
    return n;
  }
  static int depth(TreeNode n) {
    return n == null ? 0 : 1 + Math.max(depth(n.left), depth(n.right));
  }
  static boolean same(TreeNode a, TreeNode b) {
    return a == null || b == null
        ? a == b
        : a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
  }
  static boolean subtree(TreeNode a, TreeNode b) {
    return b == null || a != null && (same(a, b) || subtree(a.left, b) || subtree(a.right, b));
  }
  static int[][] levels(TreeNode root) {
    List<int[]> out = new ArrayList<>();
    List<TreeNode> q = new ArrayList<>();
    if (root != null)
      q.add(root);
    while (!q.isEmpty()) {
      out.add(q.stream().mapToInt(n -> n.val).toArray());
      List<TreeNode> next = new ArrayList<>();
      for (TreeNode n : q) {
        if (n.left != null)
          next.add(n.left);
        if (n.right != null)
          next.add(n.right);
      }
      q = next;
    }
    return out.toArray(int[][] ::new);
  }
  static TreeNode build(int[] pre, int[] ino) {
    if (pre.length == 0)
      return null;
    int i = 0;
    while (ino[i] != pre[0]) i++;
    TreeNode n = new TreeNode(pre[0]);
    n.left = build(Arrays.copyOfRange(pre, 1, i + 1), Arrays.copyOfRange(ino, 0, i));
    n.right = build(
        Arrays.copyOfRange(pre, i + 1, pre.length), Arrays.copyOfRange(ino, i + 1, ino.length));
    return n;
  }
  static List<Integer> inorder(TreeNode n) {
    List<Integer> out = new ArrayList<>();
    if (n != null) {
      out.addAll(inorder(n.left));
      out.add(n.val);
      out.addAll(inorder(n.right));
    }
    return out;
  }
  static int gain(TreeNode n, int[] best) {
    if (n == null)
      return 0;
    int l = Math.max(0, gain(n.left, best)), r = Math.max(0, gain(n.right, best));
    best[0] = Math.max(best[0], n.val + l + r);
    return n.val + Math.max(l, r);
  }
  static int maxPath(TreeNode n) {
    int[] best = {Integer.MIN_VALUE};
    gain(n, best);
    return best[0];
  }
  static String serialize(TreeNode n) {
    return n == null ? "# " : n.val + " " + serialize(n.left) + serialize(n.right);
  }
  static TreeNode read(Deque<String> q) {
    String s = q.remove();
    if (s.equals("#"))
      return null;
    TreeNode n = new TreeNode(Integer.parseInt(s));
    n.left = read(q);
    n.right = read(q);
    return n;
  }
  static TreeNode deserialize(String s) {
    return read(new ArrayDeque<>(Arrays.asList(s.trim().split(" +"))));
  }
  static Node clone(Node root) {
    return clone(root, new IdentityHashMap<>());
  }
  static Node clone(Node n, IdentityHashMap<Node, Node> copies) {
    if (n == null)
      return null;
    if (copies.containsKey(n))
      return copies.get(n);
    Node c = new Node(n.val);
    copies.put(n, c);
    for (Node next : n.neighbors) c.neighbors.add(clone(next, copies));
    return c;
  }
}
