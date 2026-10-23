using System;
using System.Collections.Generic;
using System.Text;
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }
public class Solution
{
    public LinkedListNode? AddLists(LinkedListNode? first, LinkedListNode? second,
                                    bool mostSignificantFirst)
    {
        if (mostSignificantFirst)
        {
            var left = new Stack<int>();
            var right = new Stack<int>();
            for (LinkedListNode? scan = first; scan != null; scan = scan.Next)
                left.Push(scan.Value);
            for (LinkedListNode? scan = second; scan != null; scan = scan.Next)
                right.Push(scan.Value);
            LinkedListNode? result = null;
            int forwardCarry = 0;
            while (left.Count > 0 || right.Count > 0 || forwardCarry != 0)
            {
                int total = forwardCarry;
                if (left.Count > 0)
                    total += left.Pop();
                if (right.Count > 0)
                    total += right.Pop();
                result = new LinkedListNode(total % 10, result);
                forwardCarry = total / 10;
            }
            return result;
        }
        var dummy = new LinkedListNode(0);
        LinkedListNode? tail = dummy;
        LinkedListNode? p = first;
        LinkedListNode? q = second;
        int carry = 0;
        while (p != null || q != null || carry != 0)
        {
            int total = carry;
            if (p != null)
            {
                total += p.Value;
                p = p.Next;
            }
            if (q != null)
            {
                total += q.Value;
                q = q.Next;
            }
            tail!.Next = new LinkedListNode(total % 10);
            tail = tail!.Next;
            carry = total / 10;
        }
        return dummy.Next;
    }
}
