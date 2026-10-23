using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public LinkedListNode? KthToLast(LinkedListNode? head, int k)
    {
        if (k <= 0)
            return null;
        LinkedListNode? lead = head;
        for (int i = 0; i < k; ++i)
        {
            if (lead == null)
                return null;
            lead = lead.Next;
        }
        LinkedListNode? follow = head;
        while (lead != null)
        {
            lead = lead.Next;
            follow = follow!.Next;
        }
        return follow;
    }
}
