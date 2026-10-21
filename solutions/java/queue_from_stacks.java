package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.TestFailure;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.NoSuchElementException;

public class QueueFromStacks {
  public static class Queue {
    private final Deque<Integer> incoming = new ArrayDeque<>();
    private final Deque<Integer> outgoing = new ArrayDeque<>();

    public void enqueue(Integer value) { incoming.push(value); }

    public Integer dequeue() {
      if (outgoing.isEmpty()) {
        while (!incoming.isEmpty()) outgoing.push(incoming.pop());
      }
      return outgoing.pop();
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

  @EpiTest(testDataFile = "queue_from_stacks.tsv")
  public static void queueTester(List<QueueOp> ops) throws TestFailure {
    Queue queue = new Queue();
    for (int index = 0; index < ops.size(); index++) {
      QueueOp operation = ops.get(index);
      switch (operation.op) {
        case "Queue":
          queue = new Queue();
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
        default:
          throw new TestFailure("Unknown queue operation: " + operation.op)
              .withProperty(TestFailure.PropertyName.COMMAND, operation);
      }
    }
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "QueueFromStacks.java", QueueFromStacks.class).ordinal());
  }
}
