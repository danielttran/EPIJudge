using System;
using System.Collections.Generic;
using System.Text;
public abstract class FairCoinSource {public abstract bool Next();}
public class Solution
{
    public int[] RandomSubset(int[] values, FairCoinSource coins)
    {
        return values.Where(value => coins.Next()).ToArray();
    }
}
