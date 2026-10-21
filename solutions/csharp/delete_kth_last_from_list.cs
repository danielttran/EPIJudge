using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? RemoveKthLast(ListNode<int>? L, int k)
    {
        var dummy = new ListNode<int>(0) { Next = L };
        var fast = dummy;
        var slow = dummy;
        for (int i = 0; i < k; i++)
            fast = fast.Next!;
        while (fast.Next is not null)
        {
            fast = fast.Next;
            slow = slow.Next!;
        }
        slow.Next = slow.Next!.Next;
        return dummy.Next;
    }
}
