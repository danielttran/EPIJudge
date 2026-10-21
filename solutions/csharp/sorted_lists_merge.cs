using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? MergeTwoSortedLists(ListNode<int>? L1, ListNode<int>? L2)
    {
        var dummy = new ListNode<int>(0);
        var tail = dummy;
        while (L1 is not null && L2 is not null)
        {
            if (L1.Data <= L2.Data)
            {
                tail.Next = L1;
                L1 = L1.Next;
            }
            else
            {
                tail.Next = L2;
                L2 = L2.Next;
            }
            tail = tail.Next;
        }
        tail.Next = L1 ?? L2;
        return dummy.Next;
    }
}
