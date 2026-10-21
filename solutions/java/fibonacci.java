package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class Fibonacci {
  @EpiTest(testDataFile="fibonacci.tsv")
  public static int fibonacci(int n) {
    int previous = 0, current = 1;
    for (int i = 0; i < n; i++) {
      int next = previous + current;
      previous = current;
      current = next;
    }
    return previous;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "Fibonacci.java", Fibonacci.class).ordinal());
  }
}
