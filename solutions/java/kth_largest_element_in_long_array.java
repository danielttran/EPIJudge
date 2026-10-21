package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class KthLargestElementInLongArray {
  public static int findKthLargestUnknownLength(Iterator<Integer> stream, int k) {
    PriorityQueue<Integer> largest = new PriorityQueue<>();
    while (stream.hasNext()) {
      int value = stream.next();
      if (largest.size() < k) largest.add(value);
      else if (value > largest.peek()) { largest.remove(); largest.add(value); }
    }
    if (largest.size() < k) throw new IllegalArgumentException("The stream must contain at least k entries.");
    return largest.element();
  }
  @EpiTest(testDataFile="kth_largest_element_in_long_array.tsv")
  public static int test(List<Integer> values, int k) { return findKthLargestUnknownLength(values.iterator(), k); }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "KthLargestElementInLongArray.java", KthLargestElementInLongArray.class).ordinal());
  }
}
