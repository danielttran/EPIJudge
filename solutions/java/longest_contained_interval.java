package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class LongestContainedInterval {
  @EpiTest(testDataFile="longest_contained_interval.tsv")
  public static int longestContainedRange(List<Integer> values) {
    var remaining = new HashSet<>(values); int best = 0;
    for (int value : values) {
      if (!remaining.remove(value)) continue;
      int length = 1;
      for (long next = (long)value-1; next >= Integer.MIN_VALUE && remaining.remove((int)next); next--) length++;
      for (long next = (long)value+1; next <= Integer.MAX_VALUE && remaining.remove((int)next); next++) length++;
      best = Math.max(best,length);
    }
    return best;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "LongestContainedInterval.java", LongestContainedInterval.class).ordinal());
  }
}
