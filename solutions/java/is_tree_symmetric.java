package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class IsTreeSymmetric {
  private record Pair(BinaryTreeNode<Integer> first, BinaryTreeNode<Integer> second) {}
  @EpiTest(testDataFile="is_tree_symmetric.tsv")
  public static boolean isSymmetric(BinaryTreeNode<Integer> tree) {
    if (tree == null) return true;
    Deque<Pair> pending = new ArrayDeque<>();
    pending.add(new Pair(tree.left, tree.right));
    while (!pending.isEmpty()) {
      Pair pair = pending.remove();
      var a = pair.first(); var b = pair.second();
      if (a == null || b == null) { if (a != b) return false; continue; }
      if (!Objects.equals(a.data, b.data)) return false;
      pending.add(new Pair(a.left, b.right));
      pending.add(new Pair(a.right, b.left));
    }
    return true;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "IsTreeSymmetric.java", IsTreeSymmetric.class).ordinal());
  }
}
