package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class RemoveDuplicatesFromSortedList {
  @EpiTest(testDataFile="remove_duplicates_from_sorted_list.tsv")
  public static ListNode<Integer> removeDuplicates(ListNode<Integer> head) {
    for (ListNode<Integer> node = head; node != null; node = node.next)
      while (node.next != null && Objects.equals(node.data, node.next.data)) node.next = node.next.next;
    return head;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "RemoveDuplicatesFromSortedList.java", RemoveDuplicatesFromSortedList.class).ordinal());
  }
}
