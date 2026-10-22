package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;

import java.util.List;

public class AdvanceByOffsets {

  @EpiTest(testDataFile = "advance_by_offsets.tsv")
  public static boolean canReachEnd(List<Integer> maxAdvanceSteps) {

    if (maxAdvanceSteps.isEmpty()) return true;
    final int destination = maxAdvanceSteps.size() - 1;
    int reachable = 0;
    for (int position = 0; position <= destination; ++position) {
      if (position > reachable) return false;
      int jump = maxAdvanceSteps.get(position);
      // Addition below is safe because it cannot exceed the destination.
      if (jump >= destination - position) return true;
      reachable = Math.max(reachable, position + jump);
    }
    return false;
  }

  public static void main(String[] args) {
    System.exit(
        GenericTest
            .runFromAnnotations(args, "AdvanceByOffsets.java",
                                new Object() {}.getClass().getEnclosingClass())
            .ordinal());
  }
}
