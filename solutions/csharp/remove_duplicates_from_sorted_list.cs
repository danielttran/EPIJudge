using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? RemoveDuplicates(ListNode<int>? L)
    {
        for (var node = L; node is not null; node = node.Next)
            while (node.Next is not null && node.Next.Data == node.Data)
                node.Next = node.Next.Next;
        return L;
    }
}
