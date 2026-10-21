package epi;

import java.util.*;
import epi.test_framework.EpiTest;
import epi.test_framework.EpiUserType;
import epi.test_framework.GenericTest;
import epi.test_framework.RandomSequenceChecker;
import epi.test_framework.TestFailure;

// Original implementation for EPI Practice; preserves the public submission contract.
public class DoListsOverlap {
  private static Set<ListNode<Integer>> nodes(ListNode<Integer> head) {
    Set<ListNode<Integer>> result = Collections.newSetFromMap(new IdentityHashMap<>());
    while (head != null && result.add(head)) head = head.next;
    return result;
  }
  public static ListNode<Integer> overlappingLists(ListNode<Integer> first, ListNode<Integer> second) {
    Set<ListNode<Integer>> seen = nodes(first);
    Set<ListNode<Integer>> traversed = Collections.newSetFromMap(new IdentityHashMap<>());
    while (second != null && traversed.add(second)) { if (seen.contains(second)) return second; second = second.next; }
    return null;
  }
  private static ListNode<Integer> tail(ListNode<Integer> head) {
    if (head == null) return null;
    while (head.next != null) head = head.next;
    return head;
  }
  private static ListNode<Integer> advance(ListNode<Integer> node, int count) {
    while (count-- > 0) node = node.next;
    return node;
  }
  @EpiTest(testDataFile="do_lists_overlap.tsv")
  public static void test(ListNode<Integer> a, ListNode<Integer> b, ListNode<Integer> common, int cycle0, int cycle1) throws TestFailure {
    if (a == null) a = common; else tail(a).next = common;
    if (b == null) b = common; else tail(b).next = common;
    var endA = tail(a); var endB = tail(b);
    if (cycle0 >= 0) endA.next = advance(a,cycle0);
    if (cycle1 >= 0) endB.next = advance(b,cycle1);
    var first = nodes(a); var second = nodes(b);
    boolean exists = false; for (var node : first) if (second.contains(node)) { exists = true; break; }
    var answer = overlappingLists(a,b);
    if (answer == null ? exists : !first.contains(answer) || !second.contains(answer)) throw new TestFailure("Incorrect overlap node identity");
  }
  public static void main(String[] args) {
    System.exit(GenericTest.runFromAnnotations(args, "DoListsOverlap.java", DoListsOverlap.class).ordinal());
  }
}
