using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? ReverseList(ListNode<int>? head)
    {
        ListNode<int>? previous = null;
        while (head is not null)
        {
            var next = head.Next;
            head.Next = previous;
            previous = head;
            head = next;
        }
        return previous;
    }
}
