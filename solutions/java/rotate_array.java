package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;
import epi.test_framework.TimedExecutor;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class RotateArray {
  public static void rotateArray(int rotateAmount, List<Integer> A) {
    if (A.isEmpty()) return;
    int shift = Math.floorMod(rotateAmount, A.size());
    reverseSegment(A, 0, A.size());
    reverseSegment(A, 0, shift);
    reverseSegment(A, shift, A.size());
  }

  private static void reverseSegment(List<Integer> values, int first, int end) {
    for (int left = first, right = end - 1; left < right; left++, right--) {
      Collections.swap(values, left, right);
    }
  }

  @EpiTest(testDataFile = "rotate_array.tsv")
  public static List<Integer> rotateArrayWrapper(
      TimedExecutor executor, List<Integer> A, int rotateAmount) throws Exception {
    List<Integer> rotated = new ArrayList<>(A);
    executor.run(() -> rotateArray(rotateAmount, rotated));
    return rotated;
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "RotateArray.java", RotateArray.class).ordinal());
  }
}
