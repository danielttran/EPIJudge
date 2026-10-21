package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;
import java.util.List;

public class TwoSum {
  @EpiTest(testDataFile = "two_sum.tsv")
  public static boolean hasTwoSum(List<Integer> A, int t) {
    int lower = 0;
    int upper = A.size() - 1;
    while (lower <= upper) {
      long sum = (long) A.get(lower) + (long) A.get(upper);
      if (sum == (long) t) return true;
      if (sum < (long) t) lower++;
      else upper--;
    }
    return false;
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "TwoSum.java", TwoSum.class).ordinal());
  }
}
