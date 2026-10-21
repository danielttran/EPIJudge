package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class QueueWithMax {
  private final ArrayDeque<Integer> values = new ArrayDeque<>();
  private final ArrayDeque<Integer> maxima = new ArrayDeque<>();
  public void enqueue(Integer value) {
    values.addLast(value);
    while (!maxima.isEmpty() && maxima.peekLast() < value) maxima.removeLast();
    maxima.addLast(value);
  }
  public Integer dequeue() {
    int value = values.removeFirst();
    if (maxima.getFirst() == value) maxima.removeFirst();
    return value;
  }
  public Integer max() { return maxima.getFirst(); }
  @EpiUserType(ctorParams={String.class,int.class})
  public static class QueueOp {
    public String op; public int arg;
    public QueueOp(String op, int arg) { this.op = op; this.arg = arg; }
  }
  @EpiTest(testDataFile="queue_with_max.tsv")
  public static void test(List<QueueOp> operations) throws TestFailure {
    var queue = new QueueWithMax();
    for (var operation : operations) {
      switch (operation.op) {
        case "QueueWithMax": queue = new QueueWithMax(); break;
        case "enqueue": queue.enqueue(operation.arg); break;
        case "dequeue": if (queue.dequeue() != operation.arg) throw new TestFailure("FIFO result mismatch"); break;
        case "max": if (queue.max() != operation.arg) throw new TestFailure("Maximum result mismatch"); break;
        default: throw new IllegalArgumentException(operation.op);
      }
    }
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "QueueWithMax.java", QueueWithMax.class).ordinal());
  }
}
