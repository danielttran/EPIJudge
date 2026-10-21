package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class ZipList {
  private static ListNode<Integer> reverse(ListNode<Integer> head) {
    ListNode<Integer> previous = null;
    while (head != null) { var next = head.next; head.next = previous; previous = head; head = next; }
    return previous;
  }
  @EpiTest(testDataFile="zip_list.tsv")
  public static ListNode<Integer> zippingLinkedList(ListNode<Integer> head) {
    if (head == null || head.next == null) return head;
    var middle = head; var fast = head.next;
    while (fast != null && fast.next != null) { middle = middle.next; fast = fast.next.next; }
    var back = reverse(middle.next); middle.next = null;
    var front = head;
    while (back != null) {
      var nextFront = front.next; var nextBack = back.next;
      front.next = back; back.next = nextFront;
      front = nextFront; back = nextBack;
    }
    return head;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "ZipList.java", ZipList.class).ordinal());
  }
}
