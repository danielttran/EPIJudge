package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class OnlineMedian {
  public static List<Double> onlineMedian(Iterator<Integer> stream) {
    var lower = new PriorityQueue<Integer>(Comparator.reverseOrder());
    var upper = new PriorityQueue<Integer>(); var result = new ArrayList<Double>();
    while (stream.hasNext()) {
      int value = stream.next();
      if (lower.isEmpty() || value <= lower.peek()) lower.add(value); else upper.add(value);
      if (lower.size() > upper.size()+1) upper.add(lower.remove());
      if (upper.size() > lower.size()) lower.add(upper.remove());
      result.add(lower.size() == upper.size() ? ((long)lower.peek()+upper.peek())/2.0 : (double)lower.peek());
    }
    return result;
  }
  @EpiTest(testDataFile="online_median.tsv")
  public static List<Double> test(List<Integer> values) { return onlineMedian(values.iterator()); }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "OnlineMedian.java", OnlineMedian.class).ordinal());
  }
}
