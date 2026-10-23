import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public LinkedListNode AddLists(
      LinkedListNode first, LinkedListNode second, boolean mostSignificantFirst) {
    if (mostSignificantFirst) {
      var left = new ArrayDeque<Integer>();
      var right = new ArrayDeque<Integer>();
      for (LinkedListNode scan = first; scan != null; scan = scan.Next)
        left.push(scan.Value);
      for (LinkedListNode scan = second; scan != null; scan = scan.Next)
        right.push(scan.Value);
      LinkedListNode result = null;
      int forwardCarry = 0;
      while (!left.isEmpty() || !right.isEmpty() || forwardCarry != 0) {
        int total = forwardCarry;
        if (!left.isEmpty())
          total += left.pop();
        if (!right.isEmpty())
          total += right.pop();
        result = new LinkedListNode(total % 10, result);
        forwardCarry = total / 10;
      }
      return result;
    }
    var dummy = new LinkedListNode(0);
    LinkedListNode tail = dummy;
    LinkedListNode p = first;
    LinkedListNode q = second;
    int carry = 0;
    while (p != null || q != null || carry != 0) {
      int total = carry;
      if (p != null) {
        total += p.Value;
        p = p.Next;
      }
      if (q != null) {
        total += q.Value;
        q = q.Next;
      }
      tail.Next = new LinkedListNode(total % 10);
      tail = tail.Next;
      carry = total / 10;
    }
    return dummy.Next;
  }
}
