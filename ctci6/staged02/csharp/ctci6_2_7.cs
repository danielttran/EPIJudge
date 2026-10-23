using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public LinkedListNode? FindIntersection(LinkedListNode? first, LinkedListNode? second)
    {
        LinkedListNode? p = first;
        LinkedListNode? q = second;
        while (p != q)
        {
            p = p == null ? second : p.Next;
            q = q == null ? first : q.Next;
        }
        return p;
    }
}
