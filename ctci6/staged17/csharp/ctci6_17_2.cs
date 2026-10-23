using System;
using System.Collections.Generic;
using System.Text;
public static class RandomSource { internal static Func<int,int,int> Draw=(lower,upper)=>throw new InvalidOperationException("Provided by the judge"); public static int GetRandom(int lower,int upper)=>Draw(lower,upper); }
public class Solution
{
    public void Shuffle(int[] values)
    {
        for (int index = values.Length - 1; index > 0; --index)
        {
            int other = RandomSource.GetRandom(0, index);
            (values[index], values[other]) = (values[other], values[index]);
        }
    }
}
