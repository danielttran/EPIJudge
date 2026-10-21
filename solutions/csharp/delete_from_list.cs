using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? DeleteFromList(ListNode<int>? head, int node_idx)
    {
        var previous = head;
        for (int i = 1; i < node_idx; i++)
            previous = previous!.Next;
        previous!.Next = previous.Next!.Next;
        return head;
    }
}
