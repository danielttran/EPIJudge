package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class SortIncreasingDecreasingArray {
  private record Entry(int value, int run, int index) {}
  @EpiTest(testDataFile="sort_increasing_decreasing_array.tsv")
  public static List<Integer> sortKIncreasingDecreasingArray(List<Integer> values) {
    List<List<Integer>> runs = new ArrayList<>();
    for (int start = 0; start < values.size();) {
      int end = start + 1;
      boolean increasing = end == values.size() || values.get(end) >= values.get(start);
      while (end < values.size() && (increasing ? values.get(end) >= values.get(end-1) : values.get(end) <= values.get(end-1))) end++;
      var run = new ArrayList<>(values.subList(start,end));
      if (!increasing) Collections.reverse(run);
      runs.add(run); start = end;
    }
    var smallest = new PriorityQueue<Entry>(Comparator.comparingInt(Entry::value));
    for (int r = 0; r < runs.size(); r++) smallest.add(new Entry(runs.get(r).get(0),r,0));
    var result = new ArrayList<Integer>(values.size());
    while (!smallest.isEmpty()) {
      var next = smallest.remove(); result.add(next.value());
      int position = next.index()+1;
      if (position < runs.get(next.run()).size()) smallest.add(new Entry(runs.get(next.run()).get(position), next.run(), position));
    }
    return result;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "SortIncreasingDecreasingArray.java", SortIncreasingDecreasingArray.class).ordinal());
  }
}
