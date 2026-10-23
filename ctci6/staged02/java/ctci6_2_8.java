import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public LinkedListNode FindLoopEntry(LinkedListNode head) {
    LinkedListNode slow = head;
    LinkedListNode fast = head;
    while (fast != null && fast.Next != null) {
      slow = slow.Next;
      fast = fast.Next.Next;
      if (slow == fast)
        break;
    }
    if (fast == null || fast.Next == null)
      return null;
    slow = head;
    while (slow != fast) {
      slow = slow.Next;
      fast = fast.Next;
    }
    return slow;
  }
}
