package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;

public class PathSum {
  @EpiTest(testDataFile = "path_sum.tsv")
  public static boolean hasPathSum(BinaryTreeNode<Integer> tree, int remainingWeight) {
    return reachesLeaf(tree, (long) remainingWeight);
  }

  private static boolean reachesLeaf(BinaryTreeNode<Integer> node, long remaining) {
    if (node == null) return false;
    long afterNode = remaining - (long) node.data;
    if (node.left == null && node.right == null) return afterNode == 0;
    return reachesLeaf(node.left, afterNode) || reachesLeaf(node.right, afterNode);
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "PathSum.java", PathSum.class).ordinal());
  }
}
