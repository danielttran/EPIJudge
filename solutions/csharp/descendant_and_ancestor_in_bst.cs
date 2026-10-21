using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool PairIncludesAncestorAndDescendantOfM(BinaryTreeNode<int>? tree,
        int possible_anc_or_desc_0, int possible_anc_or_desc_1, int middle_idx)
    {
        BinaryTreeNode<int>? Find(BinaryTreeNode<int>? node, int value)
        {
            while (node is not null && node.Data != value)
                node = value < node.Data ? node.Left : node.Right;
            return node;
        }
        if (possible_anc_or_desc_0 == middle_idx || possible_anc_or_desc_1 == middle_idx ||
            possible_anc_or_desc_0 == possible_anc_or_desc_1)
            return false;
        var first = Find(tree, possible_anc_or_desc_0);
        var second = Find(tree, possible_anc_or_desc_1);
        var middle = Find(tree, middle_idx);
        if (first is null || second is null || middle is null)
            return false;
        return (Find(first, middle_idx) is not null && Find(middle, possible_anc_or_desc_1) is not null) ||
               (Find(second, middle_idx) is not null && Find(middle, possible_anc_or_desc_0) is not null);
    }
}
