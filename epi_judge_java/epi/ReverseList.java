package epi;

import epi.test_framework.EpiTest;
import epi.test_framework.GenericTest;

public class ReverseList {
  @EpiTest(testDataFile = "reverse_list.tsv")
  public static ListNode<Integer> reverseList(ListNode<Integer> head) {
    // TODO - you fill in here.
    return null;
  }

  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "ReverseList.java", ReverseList.class).ordinal());
  }
}
