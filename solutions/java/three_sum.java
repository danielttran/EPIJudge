package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class ThreeSum {
  @EpiTest(testDataFile="three_sum.tsv")
  public static boolean hasThreeSum(List<Integer> values, int target) {
    var sorted = new ArrayList<>(values); Collections.sort(sorted);
    for (int value : sorted) {
      int left = 0, right = sorted.size()-1;
      while (left <= right) {
        long sum = (long)value + sorted.get(left) + sorted.get(right);
        if (sum == target) return true;
        if (sum < target) left++; else right--;
      }
    }
    return false;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "ThreeSum.java", ThreeSum.class).ordinal());
  }
}
