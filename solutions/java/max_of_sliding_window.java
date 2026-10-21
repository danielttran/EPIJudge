package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class MaxOfSlidingWindow {
  @EpiUserType(ctorParams={int.class,double.class})
  public static class TrafficElement {
    public int time; public double volume;
    public TrafficElement(int time, double volume) { this.time = time; this.volume = volume; }
    @Override public boolean equals(Object object) {
      return object instanceof TrafficElement other && time == other.time && Double.compare(volume,other.volume) == 0;
    }
    @Override public int hashCode() { return Objects.hash(time,volume); }
    @Override public String toString() { return "["+time+", "+volume+"]"; }
  }
  @EpiTest(testDataFile="max_of_sliding_window.tsv")
  public static List<TrafficElement> computeTrafficVolumes(List<TrafficElement> readings, int width) {
    var candidates = new ArrayDeque<Integer>(); var result = new ArrayList<TrafficElement>();
    for (int current = 0; current < readings.size(); current++) {
      while (!candidates.isEmpty() && (long)readings.get(candidates.getFirst()).time < (long)readings.get(current).time-width) candidates.removeFirst();
      while (!candidates.isEmpty() && readings.get(candidates.getLast()).volume <= readings.get(current).volume) candidates.removeLast();
      candidates.addLast(current);
      result.add(new TrafficElement(readings.get(current).time,readings.get(candidates.getFirst()).volume));
    }
    return result;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "MaxOfSlidingWindow.java", MaxOfSlidingWindow.class).ordinal());
  }
}
