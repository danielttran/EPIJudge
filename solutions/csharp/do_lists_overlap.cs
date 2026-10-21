using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? OverlappingLists(ListNode<int>? first, ListNode<int>? second)
    {
        var firstNodes = new HashSet<ListNode<int>>();
        while (first is not null && firstNodes.Add(first))
            first = first.Next;
        var visitedSecond = new HashSet<ListNode<int>>();
        while (second is not null && visitedSecond.Add(second))
        {
            if (firstNodes.Contains(second))
                return second;
            second = second.Next;
        }
        return null;
    }
}
