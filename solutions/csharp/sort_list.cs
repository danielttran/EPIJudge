using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? StableSortList(ListNode<int>? L)
    {
        if (L?.Next is null)
            return L;
        var slow = L;
        var fast = L.Next;
        while (fast?.Next is not null)
        {
            slow = slow.Next!;
            fast = fast.Next.Next;
        }
        var right = slow.Next;
        slow.Next = null;
        return Merge(StableSortList(L), StableSortList(right));
    }
    private static ListNode<int>? Merge(ListNode<int>? first, ListNode<int>? second)
    {
        var dummy = new ListNode<int>(0);
        var tail = dummy;
        while (first is not null && second is not null)
        {
            if (first.Data <= second.Data)
            {
                tail.Next = first;
                first = first.Next;
            }
            else
            {
                tail.Next = second;
                second = second.Next;
            }
            tail = tail.Next;
        }
        tail.Next = first ?? second;
        return dummy.Next;
    }
}
