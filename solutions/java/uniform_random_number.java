package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TimedExecutor;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class UniformRandomNumber {
  private static final Random FAIR_BITS = new Random();
  private static final int SAMPLE_COUNT = 100000;
  private static final double FALSE_NEGATIVE_TOLERANCE = 0.01;

  private static int zeroOneRandom() { return FAIR_BITS.nextInt(2); }

  public static int uniformRandom(int lowerBound, int upperBound) {
    if (lowerBound > upperBound) throw new IllegalArgumentException("Reversed interval.");
    long outcomes = (long) upperBound - (long) lowerBound + 1L;
    int bits = Long.SIZE - Long.numberOfLeadingZeros(outcomes - 1L);
    while (true) {
      long candidate = 0;
      for (int index = 0; index < bits; index++) {
        candidate = (candidate << 1) | zeroOneRandom();
      }
      if (candidate < outcomes) return (int) ((long) lowerBound + candidate);
    }
  }

  private static int normalMultiplier(double tolerance, long bins) {
    final double[] normalTailBounds = {
        1.0 - 0.682689492137086,
        1.0 - 0.954499736103642,
        1.0 - 0.997300203936740,
        1.0 - 0.999936657516334,
        1.0 - 0.999999426696856,
        1.0 - 0.999999998026825,
        1.0 - 0.999999999997440
    };
    double perBinTolerance = tolerance / (double) bins;
    for (int index = 0; index < normalTailBounds.length; index++) {
      if (normalTailBounds[index] <= perBinTolerance) return index + 1;
    }
    return normalTailBounds.length + 1;
  }

  private static boolean normalBins(long[] values, long outcomes, int order) {
    int samples = Math.max(0, values.length - order + 1);
    // Evaluate density in floating point before constructing any encoded tuple.
    double possibleBins = Math.pow((double) outcomes, order);
    double probability = 1.0 / possibleBins;
    if (samples * probability < 50.0 || samples * (1.0 - probability) < 50.0) {
      return true;
    }
    // With 100,000 samples, informative tuple domains have at most 2,000 bins.
    long bins = (long) possibleBins;
    Map<Long, Integer> counts = new HashMap<>();
    for (int end = order - 1; end < values.length; end++) {
      long key = 0;
      for (int index = end - order + 1; index <= end; index++) {
        key = key * outcomes + values[index];
      }
      counts.merge(key, 1, Integer::sum);
    }
    double mean = samples / possibleBins;
    double deviation = normalMultiplier(FALSE_NEGATIVE_TOLERANCE, bins)
        * Math.sqrt(samples * probability * (1.0 - probability));
    for (int count : counts.values()) {
      if (Math.abs(count - mean) > deviation) return false;
    }
    return true;
  }

  private static int countRepeatedWindows(long[] values, int width) {
    int testedWindows = values.length - width;
    if (width <= 0 || testedWindows <= 0) return 0;
    Map<Long, Integer> counts = new HashMap<>();
    int repeatedKeys = 0;
    for (int index = 0; index < width; index++) {
      int old = counts.getOrDefault(values[index], 0);
      if (old == 1) repeatedKeys++;
      counts.put(values[index], old + 1);
    }
    int repeatedWindows = 0;
    // The inherited predicate intentionally excludes the final possible window.
    for (int start = 0; start < testedWindows; start++) {
      if (repeatedKeys != 0) repeatedWindows++;
      if (start + 1 == testedWindows) break;
      long departing = values[start];
      int old = counts.get(departing);
      if (old == 2) repeatedKeys--;
      if (old == 1) counts.remove(departing);
      else counts.put(departing, old - 1);
      long arriving = values[start + width];
      old = counts.getOrDefault(arriving, 0);
      if (old == 1) repeatedKeys++;
      counts.put(arriving, old + 1);
    }
    return repeatedWindows;
  }

  private static boolean birthdaySpacings(long[] values, long outcomes) {
    int width = (int) Math.ceil(Math.sqrt(Math.log(2.0) * 2.0 * (double) outcomes));
    int denominator = values.length - width + 1;
    if (denominator < 1000) return true;
    return countRepeatedWindows(values, width) >= 0.4 * denominator;
  }

  private static boolean samplesAreUniform(long[] values, long outcomes) {
    if (outcomes < 1L || outcomes > (1L << 32)) return false;
    for (long value : values) {
      if (value < 0L || value >= outcomes) return false;
    }
    return normalBins(values, outcomes, 1)
        && normalBins(values, outcomes, 2)
        && normalBins(values, outcomes, 3)
        && birthdaySpacings(values, outcomes);
  }

  private static boolean uniformRandomRunner(TimedExecutor executor,
                                             int lowerBound, int upperBound)
      throws Exception {
    if (lowerBound > upperBound) throw new IllegalArgumentException("Reversed interval.");
    long outcomes = (long) upperBound - (long) lowerBound + 1L;
    long[] offsets = new long[SAMPLE_COUNT];
    executor.run(() -> {
      for (int index = 0; index < offsets.length; index++) {
        offsets[index] = (long) uniformRandom(lowerBound, upperBound) - (long) lowerBound;
      }
    });
    return samplesAreUniform(offsets, outcomes);
  }

  @EpiTest(testDataFile = "uniform_random_number.tsv")
  public static void uniformRandomWrapper(TimedExecutor executor,
                                          int lowerBound, int upperBound)
      throws Exception {
    RandomSequenceChecker.runFuncWithRetries(
        () -> uniformRandomRunner(executor, lowerBound, upperBound));
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "UniformRandomNumber.java", UniformRandomNumber.class).ordinal());
  }
}
