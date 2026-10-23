import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public LinkedListNode KthToLast(LinkedListNode head, int k) {
    if (k <= 0)
      return null;
    LinkedListNode lead = head;
    for (int i = 0; i < k; ++i) {
      if (lead == null)
        return null;
      lead = lead.Next;
    }
    LinkedListNode follow = head;
    while (lead != null) {
      lead = lead.Next;
      follow = follow.Next;
    }
    return follow;
  }
}
