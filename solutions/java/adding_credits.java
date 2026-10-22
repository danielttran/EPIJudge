package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.TestFailure;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.TreeSet;

public class AddingCredits {
  public static class ClientsCreditsInfo {
    private long offset = 0;
    private final Map<String, Long> clients = new HashMap<>();
    private final TreeSet<Rank> ranking = new TreeSet<>();

    private static final class Rank implements Comparable<Rank> {
      final long credit;
      final String client;
      Rank(long credit, String client) { this.credit = credit; this.client = client; }
      @Override
      public int compareTo(Rank other) {
        int byCredit = Long.compare(credit, other.credit);
        return byCredit != 0 ? byCredit : client.compareTo(other.client);
      }
    }

    public void insert(String clientID, int credit) {
      remove(clientID);
      long normalized = (long) credit - offset;
      clients.put(clientID, normalized);
      ranking.add(new Rank(normalized, clientID));
    }

    public boolean remove(String clientID) {
      Long normalized = clients.remove(clientID);
      if (normalized == null) return false;
      ranking.remove(new Rank(normalized, clientID));
      return true;
    }

    public int lookup(String clientID) {
      Long normalized = clients.get(clientID);
      return normalized == null ? -1 : Math.toIntExact(normalized + offset);
    }

    public void addAll(int amount) { offset += (long) amount; }

    public String max() { return ranking.isEmpty() ? "" : ranking.last().client; }
  }

  @EpiUserType(ctorParams = {String.class, String.class, int.class})
  public static class Operation {
    public String op;
    public String sArg;
    public int iArg;
    public Operation(String op, String sArg, int iArg) {
      this.op = op;
      this.sArg = sArg;
      this.iArg = iArg;
    }
    @Override
    public boolean equals(Object other) {
      if (!(other instanceof Operation)) return false;
      Operation that = (Operation) other;
      return iArg == that.iArg && Objects.equals(op, that.op)
          && Objects.equals(sArg, that.sArg);
    }
    @Override
    public int hashCode() { return Objects.hash(op, sArg, iArg); }
    @Override
    public String toString() { return op + "(" + sArg + ", " + iArg + ")"; }
  }

  @EpiTest(testDataFile = "adding_credits.tsv")
  public static void ClientsCreditsInfoTester(List<Operation> ops) throws TestFailure {
    ClientsCreditsInfo credits = new ClientsCreditsInfo();
    Map<String, Long> expectedCredits = new HashMap<>();
    for (int index = 0; index < ops.size(); index++) {
      Operation operation = ops.get(index);
      switch (operation.op) {
        case "ClientsCreditsInfo":
          credits = new ClientsCreditsInfo();
          expectedCredits.clear();
          break;
        case "insert":
          credits.insert(operation.sArg, operation.iArg);
          expectedCredits.put(operation.sArg, (long) operation.iArg);
          break;
        case "add_all":
          credits.addAll(operation.iArg);
          expectedCredits.replaceAll((client, credit) -> credit + operation.iArg);
          break;
        case "remove": {
          int actual = credits.remove(operation.sArg) ? 1 : 0;
          expectedCredits.remove(operation.sArg);
          if (actual != operation.iArg) {
            throw new TestFailure("Removal existence differs from its expected result.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.iArg, actual);
          }
          break;
        }
        case "lookup": {
          int actual = credits.lookup(operation.sArg);
          if (actual != operation.iArg) {
            throw new TestFailure("The client credit differs from its expected result.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.iArg, actual);
          }
          break;
        }
        case "max": {
          String actual = credits.max();
          Long selected = expectedCredits.get(actual);
          boolean valid = expectedCredits.isEmpty() ? "".equals(actual) : selected != null;
          if (valid && !expectedCredits.isEmpty()) {
            for (long credit : expectedCredits.values()) {
              if (credit > selected) valid = false;
            }
          }
          if (!valid) {
            throw new TestFailure("Max must return an existing maximal-credit client, or empty when no clients exist.")
                .withProperty(TestFailure.PropertyName.COMMAND, operation)
                .withMismatchInfo(index, operation.sArg, actual);
          }
          break;
        }
        default:
          throw new TestFailure("Unknown credit operation: " + operation.op)
              .withProperty(TestFailure.PropertyName.COMMAND, operation);
      }
    }
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "AddingCredits.java", AddingCredits.class).ordinal());
  }
}
