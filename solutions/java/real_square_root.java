package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;

public class RealSquareRoot {
  @EpiTest(testDataFile = "real_square_root.tsv")

  public static double squareRoot(double x) {
    if (x == 0) return 0;
    double low = 0, high = Math.max(1.0, x);
    for (int step = 0; step < 1100; ++step) {
      double middle = low + (high - low) / 2;
      if (middle == low || middle == high) break;
      if (middle <= x / middle) low = middle;
      else high = middle;
    }
    return low + (high - low) / 2;
  }

  private enum Ordering { SMALLER, EQUAL, LARGER }

  private static Ordering compare(double a, double b) {
    final double EPSILON = 0.000001;
    // Uses normalization for precision problem.
    double diff = (a - b) / Math.max(Math.abs(a), Math.abs(b));
    return diff < -EPSILON
        ? Ordering.SMALLER
        : (diff > EPSILON ? Ordering.LARGER : Ordering.EQUAL);
  }

  public static void main(String[] args) {
    System.exit(
        GenericTest
            .runFromAnnotations(args, "RealSquareRoot.java",
                                new Object() {}.getClass().getEnclosingClass())
            .ordinal());
  }
}
