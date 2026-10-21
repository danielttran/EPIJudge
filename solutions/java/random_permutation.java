package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class RandomPermutation {
  private static final Random random = new Random();
  public static List<Integer> computeRandomPermutation(int n) {
    List<Integer> result = new ArrayList<>(n);
    for (int i = 0; i < n; i++) result.add(i);
    for (int i = 0; i < n; i++) Collections.swap(result, i, i + random.nextInt(n-i));
    return result;
  }
  private static int rank(List<Integer> permutation) throws TestFailure {
    boolean[] seen = new boolean[permutation.size()]; int value = 0;
    for (int i = 0; i < permutation.size(); i++) {
      int item = permutation.get(i);
      if (item < 0 || item >= seen.length || seen[item]) throw new TestFailure("Invalid permutation");
      seen[item] = true; int smaller = 0;
      for (int j = i + 1; j < permutation.size(); j++) if (permutation.get(j) < item) smaller++;
      value = value * (permutation.size()-i) + smaller;
    }
    return value;
  }
  @EpiTest(testDataFile="random_permutation.tsv")
  public static void test(int n) throws Exception {
    int outcomes = 1; for (int i = 2; i <= n; i++) outcomes *= i;
    final int count = outcomes;
    RandomSequenceChecker.runFuncWithRetries(() -> {
      List<Integer> sequence = new ArrayList<>(1_000_000);
      for (int i = 0; i < 1_000_000; i++) sequence.add(rank(computeRandomPermutation(n)));
      return RandomSequenceChecker.checkSequenceIsUniformlyRandom(sequence, count, 0.01);
    });
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "RandomPermutation.java", RandomPermutation.class).ordinal());
  }
}
