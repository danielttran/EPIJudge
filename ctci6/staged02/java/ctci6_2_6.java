import java.util.*;
class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }
class Solution {
  public boolean IsPalindrome(LinkedListNode head) {
    var values = new ArrayList<Integer>();
    for (LinkedListNode p = head; p != null; p = p.Next)
      values.add(p.Value);
    int n = values.size();
    for (int i = 0; i < n / 2; ++i)
      if (values.get(i).intValue() != values.get(n - 1 - i).intValue())
        return false;
    return true;
  }
}
