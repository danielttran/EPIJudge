using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public void RemoveDups(LinkedListNode? head)
    {
        var seen = new HashSet<int>();
        LinkedListNode? previous = null;
        LinkedListNode? current = head;
        while (current != null)
        {
            if (!(seen.Add(current.Value)))
                previous!.Next = current.Next;
            else
                previous = current;
            current = current.Next;
        }
    }
}
