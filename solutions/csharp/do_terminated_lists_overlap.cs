using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? OverlappingLists(ListNode<int>? first, ListNode<int>? second)
    {
        int Length(ListNode<int>? node)
        {
            int length = 0;
            while (node is not null)
            {
                length++;
                node = node.Next;
            }
            return length;
        }
        int difference = Length(first) - Length(second);
        while (difference > 0)
        {
            first = first!.Next;
            difference--;
        }
        while (difference < 0)
        {
            second = second!.Next;
            difference++;
        }
        while (!ReferenceEquals(first, second))
        {
            first = first!.Next;
            second = second!.Next;
        }
        return first;
    }
}
