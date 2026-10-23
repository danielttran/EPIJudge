using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public LinkedListNode? Partition(LinkedListNode? head, int pivot)
    {
        LinkedListNode? smallHead = null;
        LinkedListNode? smallTail = null;
        LinkedListNode? largeHead = null;
        LinkedListNode? largeTail = null;
        LinkedListNode? current = head;
        while (current != null)
        {
            LinkedListNode? next = current.Next;
            current.Next = null;
            if (current.Value < pivot)
            {
                if (smallTail == null)
                    smallHead = current;
                else
                    smallTail.Next = current;
                smallTail = current;
            }
            else
            {
                if (largeTail == null)
                    largeHead = current;
                else
                    largeTail.Next = current;
                largeTail = current;
            }
            current = next;
        }
        if (smallHead == null)
            return largeHead;
        smallTail!.Next = largeHead;
        return smallHead;
    }
}
