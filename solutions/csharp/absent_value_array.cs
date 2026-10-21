using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindMissingElement(List<int> stream)
    {
        var present = new HashSet<int>(stream);
        int candidate = 0;
        while (present.Contains(candidate))
            candidate++;
        return candidate;
    }
}
