import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public LinkedListNode FindIntersection(LinkedListNode first, LinkedListNode second) {
    LinkedListNode p = first;
    LinkedListNode q = second;
    while (p != q) {
      p = p == null ? second : p.Next;
      q = q == null ? first : q.Next;
    }
    return p;
  }
}
