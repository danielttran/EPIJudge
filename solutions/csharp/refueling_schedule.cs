using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindAmpleCity(List<int> gallons, List<int> distances)
    {
        int start = 0;
        long tankMiles = 0;
        for (int city = 0; city < gallons.Count; city++)
        {
            tankMiles += 20L * gallons[city] - distances[city];
            if (tankMiles < 0)
            {
                start = city + 1;
                tankMiles = 0;
            }
        }
        return start % gallons.Count;
    }
}
