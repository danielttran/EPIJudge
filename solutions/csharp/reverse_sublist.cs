using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? ReverseSublist(ListNode<int>? L, int start, int finish)
    {
        if (L is null || finish <= start)
            return L;
        var dummy = new ListNode<int>(0) { Next = L };
        var before = dummy;
        for (int index = 1; index < start; index++)
            before = before.Next!;
        var first = before.Next!;
        for (int index = start; index < finish; index++)
        {
            var moved = first.Next!;
            first.Next = moved.Next;
            moved.Next = before.Next;
            before.Next = moved;
        }
        return dummy.Next;
    }
}
