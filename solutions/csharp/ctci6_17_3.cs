using System;
using System.Collections.Generic;
using System.Text;
public static class RandomSource { internal static Func<int,int,int> Draw=(lower,upper)=>throw new InvalidOperationException("Provided by the judge"); public static int GetRandom(int lower,int upper)=>Draw(lower,upper); }
public class Solution
{
    public int[] RandomSubset(int[] values, int count)
    {
        var reservoir = values.Take(count).ToArray();
        if (count == 0)
            return reservoir;
        for (int index = count; index < values.Length; ++index)
        {
            int slot = RandomSource.GetRandom(0, index);
            if (slot < count)
                reservoir[slot] = values[index];
        }
        return reservoir;
    }
}
