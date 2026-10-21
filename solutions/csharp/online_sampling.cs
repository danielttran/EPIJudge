using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> OnlineRandomSample(List<int> stream, int k)
    {
        var sample = stream.Take(k).ToList();
        for (int i = k; i < stream.Count; i++)
        {
            int position = Random.Shared.Next(i + 1);
            if (position < k)
                sample[position] = stream[i];
        }
        return sample;
    }
}
