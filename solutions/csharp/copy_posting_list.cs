using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public PostingListNode? CopyPostingsList(PostingListNode? head)
    {
        if (head is null)
            return null;
        var copies = new Dictionary<PostingListNode, PostingListNode>();
        var pending = new Queue<PostingListNode>();
        copies[head] = new PostingListNode(head.Order);
        pending.Enqueue(head);
        PostingListNode? Copy(PostingListNode? node)
        {
            if (node is null)
                return null;
            if (!copies.TryGetValue(node, out var copy))
            {
                copies[node] = copy = new PostingListNode(node.Order);
                pending.Enqueue(node);
            }
            return copy;
        }
        while (pending.TryDequeue(out var node))
        {
            copies[node].Next = Copy(node.Next);
            copies[node].Jump = Copy(node.Jump);
        }
        return copies[head];
    }
}
