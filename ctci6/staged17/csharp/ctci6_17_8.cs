using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] CircusTower(int[][] people)
    {
        int n = people.Length;
        if (n == 0)
            return [];
        int[] order = new int[n], length = new int[n], previous = new int[n];
        for (int i = 0; i < n; ++i)
            order[i] = i;
        Array.Sort(order, (a, b) =>
                          {
                              int height = people[a][0].CompareTo(people[b][0]);
                              if (height != 0)
                                  return height;
                              int weight = people[a][1].CompareTo(people[b][1]);
                              return weight != 0 ? weight : a.CompareTo(b);
                          });
        Array.Fill(length, 1);
        Array.Fill(previous, -1);
        int best = 0;
        for (int i = 0; i < n; ++i)
        {
            for (int j = 0; j < i; ++j)
                if (people[order[j]][0] < people[order[i]][0] &&
                    people[order[j]][1] < people[order[i]][1] && length[j] + 1 > length[i])
                {
                    length[i] = length[j] + 1;
                    previous[i] = j;
                }
            if (length[i] > length[best])
                best = i;
        }
        var result = new List<int>();
        for (int at = best; at != -1; at = previous[at])
            result.Add(order[at]);
        result.Reverse();
        return result.ToArray();
    }
}
