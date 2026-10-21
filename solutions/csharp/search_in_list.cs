using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SearchList(ListNode<int>? L, int key)
    {
        for (var node = L; node is not null; node = node.Next)
            if (node.Data == key)
                return key;
        return -1;
    }
}
