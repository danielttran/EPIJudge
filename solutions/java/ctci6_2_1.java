import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public void RemoveDups(LinkedListNode head) {
    var seen = new HashSet<Integer>();
    LinkedListNode previous = null;
    LinkedListNode current = head;
    while (current != null) {
      if (!(seen.add(current.Value)))
        previous.Next = current.Next;
      else
        previous = current;
      current = current.Next;
    }
  }
}
