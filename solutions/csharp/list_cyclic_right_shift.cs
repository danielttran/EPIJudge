using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? CyclicallyRightShiftList(ListNode<int>? L, int k)
    {
        if (L is null)
            return null;
        int length = 1;
        var tail = L;
        while (tail.Next is not null)
        {
            tail = tail.Next;
            length++;
        }
        k %= length;
        if (k == 0)
            return L;
        var newTail = L;
        for (int i = 1; i < length - k; i++)
            newTail = newTail.Next!;
        var newHead = newTail.Next;
        tail.Next = L;
        newTail.Next = null;
        return newHead;
    }
}
