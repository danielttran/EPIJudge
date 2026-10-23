using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public bool DeleteMiddle(LinkedListNode? target)
    {
        if (target == null || target.Next == null)
            return false;
        LinkedListNode? successor = target.Next;
        target.Value = successor!.Value;
        target.Next = successor!.Next;
        return true;
    }
}
