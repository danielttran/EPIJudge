package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class IsListPalindromic {
  private static ListNode<Integer> reverse(ListNode<Integer> head) {
    ListNode<Integer> previous = null;
    while (head != null) { var next = head.next; head.next = previous; previous = head; head = next; }
    return previous;
  }
  @EpiTest(testDataFile="is_list_palindromic.tsv")
  public static boolean isLinkedListAPalindrome(ListNode<Integer> head) {
    if (head == null || head.next == null) return true;
    var middle = head; var fast = head;
    while (fast.next != null && fast.next.next != null) { middle = middle.next; fast = fast.next.next; }
    var second = reverse(middle.next);
    boolean matches = true;
    var first = head;
    for (var node = second; node != null; node = node.next) { if (!Objects.equals(first.data, node.data)) matches = false; first = first.next; }
    middle.next = reverse(second);
    return matches;
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "IsListPalindromic.java", IsListPalindromic.class).ordinal());
  }
}
