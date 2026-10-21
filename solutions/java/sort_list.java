package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class SortList {
  private static ListNode<Integer> merge(ListNode<Integer> first, ListNode<Integer> second) {
    var sentinel = new ListNode<Integer>(0,null); var tail = sentinel;
    while (first != null && second != null) {
      if (first.data <= second.data) { tail.next = first; first = first.next; }
      else { tail.next = second; second = second.next; }
      tail = tail.next;
    }
    tail.next = first != null ? first : second;
    return sentinel.next;
  }
  @EpiTest(testDataFile="sort_list.tsv")
  public static ListNode<Integer> stableSortList(ListNode<Integer> head) {
    if (head == null || head.next == null) return head;
    var middle = head; var fast = head.next;
    while (fast != null && fast.next != null) { middle = middle.next; fast = fast.next.next; }
    var right = middle.next; middle.next = null;
    return merge(stableSortList(head), stableSortList(right));
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "SortList.java", SortList.class).ordinal());
  }
}
