package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.TestFailure;
import java.util.List;
import java.util.NoSuchElementException;

public class CircularQueue {
  public static class Queue {
    private int[] entries;
    private int head = 0;
    private int count = 0;

    public Queue(int capacity) { entries = new int[Math.max(1, capacity)]; }

    public void enqueue(Integer value) {
      if (count == entries.length) {
        int[] expanded = new int[Math.multiplyExact(entries.length, 2)];
        for (int index = 0; index < count; index++) {
          expanded[index] = entries[(int) (((long) head + index) % entries.length)];
        }
        entries = expanded;
        head = 0;
      }
      entries[(int) (((long) head + count) % entries.length)] = value;
      count++;
    }

    public Integer dequeue() {
      if (count == 0) throw new NoSuchElementException("The queue is empty.");
      int result = entries[head];
      head = (head + 1) % entries.length;
      count--;
      return result;
    }

    public int size() { return count; }

    @Override
    public String toString() {
      return "Queue(head=" + head + ", size=" + count + ", capacity=" + entries.length + ")";
    }
  }

  @EpiUserType(ctorParams = {String.class, int.class})
  public static class QueueOp {
    public String op;
    public int arg;
    public QueueOp(String op, int arg) { this.op = op; this.arg = arg; }
    @Override
    public String toString() { return op + "(" + arg + ")"; }
  }

  @EpiTest(testDataFile = "circular_queue.tsv")
  public static void queueTester(List<QueueOp> ops) throws TestFailure {
    Queue queue = new Queue(1);
    for (int index = 0; index < ops.size(); index++) {
      QueueOp operation = ops.get(index);
      switch (operation.op) {
        case "Queue":
          queue = new Queue(operation.arg);
          break;
        case "enqueue":
          queue.enqueue(operation.arg);
          break;
        case "dequeue": {
          int actual;
          try {
            actual = queue.dequeue();
          } catch (NoSuchElementException error) {
            throw new TestFailure("A recorded dequeue unexpectedly found the queue empty.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation);
          }
          if (actual != operation.arg) {
            throw new TestFailure("The dequeued value differs from its expected result.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.arg, actual);
          }
          break;
        }
        case "size": {
          int actual = queue.size();
          if (actual != operation.arg) {
            throw new TestFailure("The queue size differs from its expected result.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.arg, actual);
          }
          break;
        }
        default:
          throw new TestFailure("Unknown circular-queue operation: " + operation.op)
              .withProperty(TestFailure.PropertyName.COMMAND, operation);
      }
    }
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "CircularQueue.java", CircularQueue.class).ordinal());
  }
}
