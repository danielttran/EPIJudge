using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? EvenOddMerge(ListNode<int>? L)
    {
        if (L?.Next is null)
            return L;
        var even = L;
        var odd = L.Next;
        var oddHead = odd;
        while (odd is not null && odd.Next is not null)
        {
            even.Next = odd.Next;
            even = even.Next;
            odd.Next = even.Next;
            odd = odd.Next;
        }
        even.Next = oddHead;
        return L;
    }
}
