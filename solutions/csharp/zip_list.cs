using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? ZippingLinkedList(ListNode<int>? L)
    {
        if (L?.Next is null)
            return L;
        var slow = L;
        var fast = L;
        while (fast.Next?.Next is not null)
        {
            slow = slow.Next!;
            fast = fast.Next.Next;
        }
        var second = slow.Next;
        slow.Next = null;
        ListNode<int>? reversed = null;
        while (second is not null)
        {
            var next = second.Next;
            second.Next = reversed;
            reversed = second;
            second = next;
        }
        var first = L;
        while (reversed is not null)
        {
            var nextFirst = first!.Next;
            var nextSecond = reversed.Next;
            first.Next = reversed;
            reversed.Next = nextFirst;
            first = nextFirst;
            reversed = nextSecond;
        }
        return L;
    }
}
