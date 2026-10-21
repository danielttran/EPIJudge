package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class ReverseBits {
  @EpiTest(testDataFile="reverse_bits.tsv")
  public static long reverseBits(long value) {
    long result = 0;
    for (int bit = 0; bit < 64; bit++) { result = (result << 1) | (value & 1L); value >>>= 1; }
    return result;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "ReverseBits.java", ReverseBits.class).ordinal());
  }
}
