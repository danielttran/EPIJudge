import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public boolean DeleteMiddle(LinkedListNode target) {
    if (target == null || target.Next == null)
      return false;
    LinkedListNode successor = target.Next;
    target.Value = successor.Value;
    target.Next = successor.Next;
    return true;
  }
}
