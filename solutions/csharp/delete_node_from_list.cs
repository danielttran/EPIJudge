using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public ListNode<int>? DeletionFromList(ListNode<int>? head, int node_to_delete_idx)
    {
        var node = head;
        for (int i = 0; i < node_to_delete_idx; i++)
            node = node!.Next;
        node!.Data = node.Next!.Data;
        node.Next = node.Next.Next;
        return head;
    }
}
